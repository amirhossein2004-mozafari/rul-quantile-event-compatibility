"""Retrospective equal-search comparison. See reports/fair_comparison_step2_design.md.

python scripts/fair_comparison_step2.py --prepare
python scripts/fair_comparison_step2.py --smoke
python scripts/fair_comparison_step2.py --run
python scripts/fair_comparison_step2.py --verify
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import joblib
import numpy as np
import pandas as pd
import torch
from scipy.optimize import minimize_scalar
from scipy.special import expit
from sklearn.metrics import f1_score
from src.data.preprocessing import (RegimeAwarePreprocessor, SELECTED_SENSOR_COLUMNS,
    SETTING_COLUMNS, get_cmapss_column_names, create_sliding_windows)
from src.models.simple_quantile_risk import make_model, PARAMETER_COUNTS
from src.training.pcgrad_ablation import task_losses, permutation_for_epoch, reset_seed
from src.evaluation.conformal_adaptive import (_exact_conformal_quantile, _standard_scores,
    _normalized_scores, build_intervals)

OUT = ROOT/'results/fair_comparison_step2'
SUBSETS = ['FD001', 'FD002', 'FD003', 'FD004']
MODELS = ['lstm', 'hybrid']
LRS = [0.0002, 0.0005, 0.001]
SEEDS = [1101, 1202, 1303, 1404, 1505]
FEATURES = SELECTED_SENSOR_COLUMNS+[c+'_scaled' for c in SETTING_COLUMNS]
SOURCES = ['scripts/fair_comparison_step2.py', 'reports/fair_comparison_step2_design.md',
    'src/data/preprocessing.py', 'src/models/simple_quantile_risk.py',
    'src/models/hybrid_lstm_tcn.py', 'src/training/pcgrad_ablation.py',
    'src/evaluation/conformal_adaptive.py', 'tests/test_fair_comparison_step2.py']

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def now():
    return datetime.now(timezone.utc).isoformat()

def atomic(value, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name+f'.{os.getpid()}.tmp')
    temp.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')
    os.replace(temp, path)

def save(value, path):
    temp = path.with_name(path.name+f'.{os.getpid()}.tmp')
    torch.save(value, temp)
    os.replace(temp, path)

def worker_init():
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)

def engine_partition(ids):
    ids = np.random.default_rng(271828).permutation(np.sort(ids))
    n = len(ids)
    return {'fit': ids[:int(.6*n)].tolist(), 'validation': ids[int(.6*n):int(.8*n)].tolist(),
            'calibration': ids[int(.8*n):].tolist()}

def sample_endpoints(frame, ids, seed):
    rng = np.random.default_rng(seed)
    rows = []
    for engine in sorted(ids):
        g = frame[frame.engine_id == engine].sort_values('cycle')
        lifetime = int(g.cycle.max())
        if lifetime <= 30:
            raise ValueError('Engine lacks an eligible endpoint')
        cycle = int(rng.integers(30, lifetime))
        rows.append({'engine_id': int(engine), 'cycle': cycle, 'raw_y': lifetime-cycle})
    return pd.DataFrame(rows)

def endpoint_tensor(scaled, endpoints):
    result = []
    for row in endpoints.itertuples():
        history = scaled[(scaled.engine_id == row.engine_id)&(scaled.cycle <= row.cycle)].sort_values('cycle')
        assert len(history) >= 30 and history.cycle.iloc[-1] == row.cycle
        result.append(history[FEATURES].to_numpy(np.float32)[-30:])
    return torch.from_numpy(np.stack(result))

def provenance():
    return {p: sha(ROOT/p) for p in SOURCES}

def prepare():
    lock = OUT/'protocol.json'
    if lock.exists():
        validate_lock()
        return
    OUT.mkdir(parents=True, exist_ok=True)
    for subset in SUBSETS:
        folder = OUT/'data'/subset
        folder.mkdir(parents=True, exist_ok=True)
        frame = pd.read_csv(ROOT/f'data/raw/cmapss/train_{subset}.txt', sep=r'\s+', header=None, names=get_cmapss_column_names())
        frame['RUL'] = frame.groupby('engine_id').cycle.transform('max')-frame.cycle
        roles = engine_partition(frame.engine_id.unique())
        pre = RegimeAwarePreprocessor(n_regimes=6 if subset in ['FD002','FD004'] else 1, seed=271828)
        pre.fit(frame[frame.engine_id.isin(roles['fit'])])
        scaled = pre.transform(frame)
        x,y,z = create_sliding_windows(scaled[scaled.engine_id.isin(roles['fit'])], FEATURES, 30, 125, 30)
        assert 0 < z.sum() < len(z)
        payload = {'X': torch.from_numpy(x), 'y': torch.from_numpy(y).reshape(-1,1),
                   'z': torch.from_numpy(z).reshape(-1,1), 'pos_weight': float((len(z)-z.sum())/z.sum())}
        for role,seed in [('validation',271829),('calibration',271830)]:
            endpoints = sample_endpoints(frame, roles[role], seed)
            endpoints.to_csv(folder/f'{role}_endpoints.csv', index=False)
            payload[role+'_X'] = endpoint_tensor(scaled, endpoints)
            payload[role+'_raw_y'] = torch.tensor(endpoints.raw_y.to_numpy(), dtype=torch.float64)
        save(payload, folder/'tensors.pt')
        joblib.dump(pre, folder/'preprocessor.joblib')
        atomic(roles, folder/'roles.json')
    inputs = {str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'data').rglob('*')) if p.is_file()}
    raw = {f'data/raw/cmapss/{prefix}_{s}.txt': sha(ROOT/f'data/raw/cmapss/{prefix}_{s}.txt')
           for s in SUBSETS for prefix in ['train','test','RUL']}
    atomic(dict(created_utc=now(), scope='Retrospective exploratory; previously examined data',
        models=MODELS, subsets=SUBSETS, learning_rates=LRS, maximum_epochs=16,
        tuning_seed=101, final_seeds=SEEDS, split_seed=271828, batch_size=128,
        source_sha256=provenance(), raw_sha256=raw, prepared_sha256=inputs,
        selection='Minimum capped validation RMSE, candidate order then earliest epoch',
        expected_searches=24, expected_final_models=40, external_review='NOT_PERFORMED'), lock)
    print('PREPARED: partitions/endpoints/preprocessing and source/data hashes locked', flush=True)

def validate_lock():
    p = json.loads((OUT/'protocol.json').read_text())
    assert p['source_sha256'] == provenance(), 'Source changed since lock'
    for name,h in (p['prepared_sha256'] | p['raw_sha256']).items():
        assert sha(ROOT/name) == h, name
    assert p['learning_rates'] == LRS and p['final_seeds'] == SEEDS
    return sha(OUT/'protocol.json')

def predict(model, x):
    model.eval()
    with torch.inference_mode():
        outputs = [torch.cat(model(b),dim=1) for b in x.split(512)]
    return torch.cat(outputs).numpy().astype(np.float64)

def capped_rmse(y,pred):
    return float(np.sqrt(np.mean((np.clip(pred,0,125)-np.minimum(y,125))**2)))

def train_one(subset, name, seed, lr, epochs, directory, tuning, smoke=False):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    protocol_hash = sha(OUT/'protocol.json')
    identity = dict(subset=subset, model=name, seed=seed, lr=lr, epochs=epochs,
                    tuning=tuning, smoke=smoke, protocol_sha256=protocol_hash)
    if (directory/'final.pt').exists():
        old = torch.load(directory/'final.pt', weights_only=True)
        assert old['identity'] == identity
        return str(directory)
    data = torch.load(OUT/'data'/subset/'tensors.pt', weights_only=True)
    x,y,z = [data[k] for k in ['X','y','z']]
    if smoke:
        x,y,z = x[:256],y[:256],z[:256]
    reset_seed(seed)
    model = make_model(name)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=.0001)
    weight = torch.tensor([data['pos_weight']], dtype=torch.float32)
    start = 0
    history = []
    seconds_prior = 0.
    if (directory/'progress.pt').exists():
        p = torch.load(directory/'progress.pt', weights_only=True)
        assert p['identity'] == identity
        model.load_state_dict(p['state'])
        optimizer.load_state_dict(p['optimizer'])
        torch.set_rng_state(p['rng'])
        history = p['history']
        start = len(history)
        seconds_prior = p['train_seconds']
    else:
        save(dict(state=model.state_dict(), identity=identity), directory/'initial.pt')
    total_start = time.perf_counter()
    for epoch in range(start,epochs):
        model.train()
        started = time.perf_counter()
        permutation = permutation_for_epoch(len(x),seed,epoch)
        loss_total = 0.
        for indices in permutation.split(128):
            optimizer.zero_grad(set_to_none=True)
            a,b = task_losses(model(x[indices]), y[indices], z[indices], weight)
            loss = a+b
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.)
            optimizer.step()
            loss_total += float(loss.detach())*len(indices)
        epoch_seconds = time.perf_counter()-started
        metric = None
        if tuning:
            output = predict(model,data['validation_X'])
            metric = capped_rmse(data['validation_raw_y'].numpy(),output[:,1])
        history.append(dict(epoch=epoch+1, train_loss=loss_total/len(x), validation_RMSE=metric,
                            seconds=epoch_seconds, samples=len(x)))
        pd.DataFrame(history).to_csv(directory/'history.csv',index=False)
        progress = dict(state=model.state_dict(),optimizer=optimizer.state_dict(), rng=torch.get_rng_state(),
            history=history,identity=identity,train_seconds=seconds_prior+time.perf_counter()-total_start)
        save(progress,directory/'progress.pt')
        print(f'{subset}/{name}/{seed}/lr={lr}: epoch {epoch+1}/{epochs} ({epoch_seconds:.1f}s)',flush=True)
    save(dict(state=model.state_dict(),identity=identity,history=history,parameters=PARAMETER_COUNTS[name],
              train_seconds=seconds_prior+time.perf_counter()-total_start),directory/'final.pt')
    return str(directory)

def search_jobs():
    return [(s,m,101,lr,16,OUT/'search'/s/m/f'lr_{i}',True) for s in SUBSETS for m in MODELS for i,lr in enumerate(LRS)]

def select_configs():
    selected = {}
    all_rows = []
    for subset in SUBSETS:
        for model in MODELS:
            options = []
            for i,lr in enumerate(LRS):
                path = OUT/'search'/subset/model/f'lr_{i}'/'final.pt'
                c = torch.load(path,weights_only=True)
                assert len(c['history']) == 16
                for h in c['history']:
                    options.append((h['validation_RMSE'],i,h['epoch'],lr))
                    all_rows.append(dict(subset=subset,model=model,candidate=i,lr=lr,**h))
            score,i,epoch,lr = min(options)
            selected[f'{subset}/{model}'] = dict(lr=lr,epochs=epoch,validation_RMSE=score,candidate=i)
    pd.DataFrame(all_rows).to_csv(OUT/'search_results.csv',index=False)
    if (OUT/'selection.json').exists():
        assert json.loads((OUT/'selection.json').read_text()) == selected
    else:
        atomic(selected,OUT/'selection.json')
    return selected

def pool_jobs(jobs, workers):
    with ProcessPoolExecutor(max_workers=workers, initializer=worker_init) as pool:
        futures = [pool.submit(train_one,*j) for j in jobs]
        for i,future in enumerate(as_completed(futures),1):
            finished = future.result()
            atomic(dict(completed=i,total=len(jobs),last_completed=finished,updated_utc=now()),OUT/'progress.json')
            print(f'COMPLETED {i}/{len(jobs)} {finished}',flush=True)

def ece(y,p):
    b = np.minimum((p*10).astype(int),9)
    return float(sum(np.mean(b==i)*abs(np.mean(p[b==i])-np.mean(y[b==i])) for i in range(10) if np.any(b==i)))

def point_metrics(y,p):
    err = np.clip(p,0,125)-np.minimum(y,125)
    return dict(RMSE=float(np.sqrt(np.mean(err**2))), MAE=float(np.mean(abs(err))),
                NASA_sum=float(np.expm1(np.where(err<0,-err/13,err/10)).sum()))

def interval_metrics(y,lo,hi):
    y=np.minimum(y,125)
    return dict(Coverage=float(np.mean((lo<=y)&(y<=hi))),Width=float(np.mean(hi-lo)),
        Winkler=float(np.mean(hi-lo+20*np.maximum(lo-y,0)+20*np.maximum(y-hi,0))))

def temperature(logits,y):
    if len(np.unique(y)) < 2:
        return None
    fit = minimize_scalar(lambda log_t: float(np.mean(np.logaddexp(0,logits/np.exp(log_t))-y*logits/np.exp(log_t))),
        bounds=(math.log(.1),math.log(10.)),method='bounded',options={'xatol':1e-12})
    if not fit.success:
        raise ValueError('Temperature fit failed')
    return float(np.exp(fit.x))

def test_data(subset):
    pre = joblib.load(OUT/'data'/subset/'preprocessor.joblib')
    raw = pd.read_csv(ROOT/f'data/raw/cmapss/test_{subset}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names())
    y = pd.read_csv(ROOT/f'data/raw/cmapss/RUL_{subset}.txt',header=None,names=['RUL'])
    x,_,_ = create_sliding_windows(pre.transform(raw),FEATURES,30,125,30,is_test=True,test_rul_df=y)
    return torch.from_numpy(x), y.RUL.to_numpy(dtype=np.float64), raw.engine_id.unique()

def final_jobs(selected):
    return [(s,m,seed,selected[f'{s}/{m}']['lr'],selected[f'{s}/{m}']['epochs'],
        OUT/'final'/s/m/f'seed_{seed}',False) for s in SUBSETS for m in MODELS for seed in SEEDS]

def evaluate(selected):
    final_paths = [j[5]/'final.pt' for j in final_jobs(selected)]
    assert len(final_paths) == 40 and all(p.is_file() for p in final_paths)
    validate_lock()
    atomic(dict(started_utc=now(),all_40_final_checkpoints_present=True,
                selection_sha256=sha(OUT/'selection.json'),checkpoint_sha256={str(p.relative_to(ROOT)):sha(p) for p in final_paths}),OUT/'evaluation_start.json')
    rows=[]
    for subset in SUBSETS:
        x,y,ids = test_data(subset)
        data=torch.load(OUT/'data'/subset/'tensors.pt',weights_only=True)
        cal_y=data['calibration_raw_y'].numpy()
        for name in MODELS:
            for seed in SEEDS:
                folder=OUT/'final'/subset/name/f'seed_{seed}'
                checkpoint=torch.load(folder/'final.pt',weights_only=True)
                model=make_model(name)
                model.load_state_dict(checkpoint['state'])
                cal=predict(model,data['calibration_X'])
                pred=predict(model,x)
                frame=pd.DataFrame(dict(engine_id=ids,raw_y=y,q05=pred[:,0],q50=pred[:,1],q95=pred[:,2],logit=pred[:,3]))
                cal_frame=pd.DataFrame(dict(raw_y=cal_y,q05=cal[:,0],q50=cal[:,1],q95=cal[:,2],logit=cal[:,3]))
                record=dict(subset=subset,model=name,seed=seed,**point_metrics(y,pred[:,1]),parameters=PARAMETER_COUNTS[name],
                            selected_lr=selected[f'{subset}/{name}']['lr'],selected_epochs=selected[f'{subset}/{name}']['epochs'],
                            train_seconds=checkpoint['train_seconds'])
                cutoffs={}
                for method,power in [('Raw',None),('Exact',0.),('Normalized',1.)]:
                    if power is None:
                        lo,hi=np.clip(pred[:,0],0,125),np.clip(pred[:,2],0,125)
                    else:
                        scores=_standard_scores(cal[:,0],cal[:,2],np.minimum(cal_y,125)) if power==0 else _normalized_scores(cal[:,0],cal[:,2],np.minimum(cal_y,125))
                        cutoff=_exact_conformal_quantile(scores,.1)
                        cutoffs[method]=cutoff
                        _,_,lo,hi=build_intervals(pred[:,0],pred[:,2],cutoff,power)
                    for k,v in interval_metrics(y,lo,hi).items(): record[f'{k}_{method}']=v
                    frame['lower_'+method]=lo;frame['upper_'+method]=hi
                offset=math.log(data['pos_weight'])
                temps={'Temp':temperature(cal[:,3],cal_y<=30), 'ShiftTemp':temperature(cal[:,3]-offset,cal_y<=30)}
                for method in ['Raw','Bayes','Temp','ShiftTemp']:
                    if method in temps and temps[method] is None:
                        record['Brier_'+method]=None;record['ECE_'+method]=None
                        continue
                    logits=pred[:,3]-(offset if method in ['Bayes','ShiftTemp'] else 0.)
                    p=expit(logits/(temps[method] if method in temps else 1.))
                    frame['p_'+method]=p
                    record['Brier_'+method]=float(np.mean((p-(y<=30))**2))
                    record['ECE_'+method]=ece(y<=30,p)
                record['F1_Raw']=float(f1_score(y<=30,frame.p_Raw>=.5,zero_division=0))
                for _ in range(50):
                    with torch.inference_mode(): model(x[:1])
                durations=[]
                for i in range(300):
                    with torch.inference_mode():
                        start=time.perf_counter_ns();model(x[i%len(x):i%len(x)+1]);durations.append((time.perf_counter_ns()-start)/1e6)
                record['forward_median_ms']=float(np.median(durations))
                record['forward_p95_ms']=float(np.quantile(durations,.95))
                frame.to_csv(folder/'test_predictions.csv',index=False)
                cal_frame.to_csv(folder/'calibration_predictions.csv',index=False)
                atomic(dict(temperatures=temps,cutoffs=cutoffs,ln_pos_weight=offset),folder/'calibration_fits.json')
                pd.DataFrame({'milliseconds':durations}).to_csv(folder/'latency_calls.csv',index=False)
                rows.append(record)
    pd.DataFrame(rows).to_csv(OUT/'per_run.csv',index=False)
    summarize()

def summarize():
    df=pd.read_csv(OUT/'per_run.csv')
    metrics=['RMSE','MAE','NASA_sum','F1_Raw','Brier_Raw','ECE_Raw','Coverage_Exact','Width_Exact','Winkler_Exact',
             'Coverage_Normalized','Width_Normalized','Winkler_Normalized','Brier_Bayes','Brier_Temp','Brier_ShiftTemp',
             'ECE_Bayes','ECE_Temp','ECE_ShiftTemp','forward_median_ms','train_seconds']
    summary=df.groupby(['subset','model'])[metrics].agg(['mean','std'])
    summary.columns=['_'.join(c) for c in summary.columns]
    summary.to_csv(OUT/'summary.csv')
    rows=[]
    rng=np.random.default_rng(314159)
    for subset in SUBSETS:
        group=df[df.subset==subset].pivot(index='seed',columns='model',values='RMSE')
        errors={}
        for model in MODELS:
            frames=[pd.read_csv(OUT/'final'/subset/model/f'seed_{s}'/'test_predictions.csv',float_precision='round_trip') for s in SEEDS]
            ids=frames[0].engine_id.to_numpy()
            assert all(np.array_equal(ids,f.engine_id) for f in frames)
            errors[model]=np.stack([(np.clip(f.q50,0,125)-np.minimum(f.raw_y,125)).to_numpy()**2 for f in frames])
        draws=[]
        for _ in range(2000):
            indices=rng.integers(0,len(ids),len(ids))
            draws.append(float(np.sqrt(errors['hybrid'][:,indices].mean(axis=1)).mean()-np.sqrt(errors['lstm'][:,indices].mean(axis=1)).mean()))
        delta=group.hybrid-group.lstm
        rows.append(dict(subset=subset,mean_RMSE_hybrid_minus_lstm=float(delta.mean()),paired_seed_SD=float(delta.std(ddof=1)),
            hybrid_lower_seeds=int((delta<0).sum()),bootstrap_engine_conditional_lower=float(np.quantile(draws,.025)),
            bootstrap_engine_conditional_upper=float(np.quantile(draws,.975))))
    pd.DataFrame(rows).to_csv(OUT/'paired_comparison.csv',index=False)

def verify():
    validate_lock()
    selected=select_configs()
    for subset in SUBSETS:
        roles=json.loads((OUT/'data'/subset/'roles.json').read_text())
        sets=[set(roles[k]) for k in ['fit','validation','calibration']]
        assert not (sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])
        raw=pd.read_csv(ROOT/f'data/raw/cmapss/train_{subset}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names())
        assert set.union(*sets)==set(raw.engine_id.unique())
        data=torch.load(OUT/'data'/subset/'tensors.pt',weights_only=True)
        assert len(data['X'])==len(data['y'])==len(data['z'])
        pre=joblib.load(OUT/'data'/subset/'preprocessor.joblib')
        expected=RegimeAwarePreprocessor(n_regimes=pre.n_regimes,seed=271828).fit(raw[raw.engine_id.isin(roles['fit'])])
        np.testing.assert_array_equal(pre.setting_scaler.mean_,expected.setting_scaler.mean_)
        for k in pre.sensor_scalers:
            np.testing.assert_array_equal(pre.sensor_scalers[k].mean_,expected.sensor_scalers[k].mean_)
    df=pd.read_csv(OUT/'per_run.csv')
    assert len(df)==40 and not df.duplicated(['subset','model','seed']).any()
    for job in final_jobs(selected):
        subset,model,seed,lr,epochs,folder,_=job
        checkpoint=torch.load(folder/'final.pt',weights_only=True)
        assert checkpoint['identity']==dict(subset=subset,model=model,seed=seed,lr=lr,epochs=epochs,tuning=False,smoke=False,protocol_sha256=sha(OUT/'protocol.json'))
        assert len(checkpoint['history'])==epochs
        row=df[(df.subset==subset)&(df.model==model)&(df.seed==seed)].iloc[0]
        p=pd.read_csv(folder/'test_predictions.csv',float_precision='round_trip')
        truth=np.loadtxt(ROOT/f'data/raw/cmapss/RUL_{subset}.txt')
        np.testing.assert_array_equal(p.raw_y,truth)
        assert p.engine_id.is_unique
        for k,v in point_metrics(truth,p.q50).items():np.testing.assert_allclose(row[k],v,rtol=1e-12)
        for method in ['Raw','Exact','Normalized']:
            for k,v in interval_metrics(truth,p['lower_'+method],p['upper_'+method]).items():np.testing.assert_allclose(row[k+'_'+method],v,rtol=1e-12)
        for method in ['Raw','Bayes','Temp','ShiftTemp']:
            if 'p_'+method in p:
                np.testing.assert_allclose(row['Brier_'+method],np.mean((p['p_'+method]-(truth<=30))**2),rtol=1e-12)
                np.testing.assert_allclose(row['ECE_'+method],ece(truth<=30,p['p_'+method].to_numpy()),rtol=1e-12)
        calls=pd.read_csv(folder/'latency_calls.csv').milliseconds
        assert len(calls)==300 and (calls>0).all()
        np.testing.assert_allclose(row.forward_median_ms,np.median(calls),rtol=1e-12)
    gate=json.loads((OUT/'evaluation_start.json').read_text())
    assert gate['all_40_final_checkpoints_present'] and gate['selection_sha256']==sha(OUT/'selection.json')
    for p,h in gate['checkpoint_sha256'].items():assert sha(ROOT/p)==h,p
    atomic(dict(status='pass',runs=40,search_candidates=24,selection_validation_only=True,
        data_role_checks='pass',raw_ground_truth_and_metrics='pass',external_review='NOT_PERFORMED',
        scope='Deterministic executor verification; no independent scientific review',completed_utc=now()),OUT/'verification.json')
    print('VERIFIED: 24 candidates, 40 final models, raw truth and retained metrics',flush=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for flag in ['prepare','smoke','run','verify']:parser.add_argument('--'+flag,action='store_true')
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if args.prepare:
        worker_init();prepare();return
    validate_lock()
    if args.smoke:
        worker_init()
        for model in MODELS:
            train_one('FD001',model,101,.0005,1,OUT/'diagnostics'/model,True,True)
        print('SMOKE complete; no official-test evaluation',flush=True)
    elif args.verify:
        worker_init();verify()
    elif args.run:
        active=OUT/'active_process.json'
        if active.exists():
            raise RuntimeError('An active-process marker exists; inspect its PID before resuming')
        atomic(dict(pid=os.getpid(),started_utc=now()),active)
        try:
            atomic(dict(status='search',started_utc=now(),protocol_sha256=sha(OUT/'protocol.json')),OUT/'status.json')
            pool_jobs(search_jobs(),args.workers)
            selected=select_configs()
            atomic(dict(status='refit',updated_utc=now()),OUT/'status.json')
            pool_jobs(final_jobs(selected),args.workers)
            worker_init()
            atomic(dict(status='evaluation',updated_utc=now()),OUT/'status.json')
            evaluate(selected)
            verify()
            atomic(dict(status='complete',completed_utc=now(),protocol_sha256=sha(OUT/'protocol.json'),
                output_sha256={str(p.relative_to(OUT)):sha(p) for p in OUT.rglob('*') if p.is_file() and p.name not in ['active_process.json','status.json','completion.json']}),OUT/'completion.json')
            atomic(dict(status='complete',completed_utc=now()),OUT/'status.json')
        except Exception as exc:
            atomic(dict(status='failed',error=repr(exc),updated_utc=now()),OUT/'status.json')
            raise
        finally:
            active.unlink()
    else:
        parser.error('Choose --prepare, --smoke, --run or --verify')

if __name__=='__main__':main()

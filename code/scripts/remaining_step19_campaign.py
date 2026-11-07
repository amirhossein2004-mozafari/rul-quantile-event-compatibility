"""Required/recommended experiment extension. Never modifies previous result files."""
from pathlib import Path
import sys,json,hashlib,time,math,shutil
from concurrent.futures import ProcessPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import numpy as np,pandas as pd,torch,joblib
from threadpoolctl import threadpool_limits
from src.models.remaining_step19 import factory
from src.data.preprocessing import RegimeAwarePreprocessor,get_cmapss_column_names,create_sliding_windows
from src.training.pcgrad_ablation import task_losses,permutation_for_epoch,reset_seed
import fair_comparison_step2 as b
OUT=ROOT/'results/remaining_step19';SUBS=b.SUBSETS;SEEDS=b.SEEDS;ARMS=['tcn_last','transformer','gaussian'];LRS=b.LRS
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
write=b.atomic
def sources():return {n:sha(ROOT/n) for n in ['scripts/remaining_step19_campaign.py','src/models/remaining_step19.py','reports/remaining_step19_protocol.md','scripts/fair_comparison_step2.py','src/models/simple_quantile_risk.py','src/models/hybrid_lstm_tcn.py','src/data/preprocessing.py','src/training/pcgrad_ablation.py']}
def init():
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True);threadpool_limits(1)
def raw(sub):
    f=pd.read_csv(ROOT/f'data/raw/cmapss/train_{sub}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names());f['RUL']=f.groupby('engine_id').cycle.transform('max')-f.cycle;return f
def prepare():
    assert not (OUT/'lock.json').exists();OUT.mkdir(parents=True,exist_ok=True);archive=ROOT/'archive/remaining_step19_before';archive.mkdir(parents=True,exist_ok=True)
    for n in ['manuscript_v4.md','manuscript_v4.pdf','supplement_matched_endpoints.md','supplement_matched_endpoints.pdf','references.bib','submission_header.tex']:shutil.copy2(ROOT/'paper'/n,archive/n)
    inputs={}
    for sub in SUBS:
        roles=load(ROOT/f'results/fair_comparison_step2/data/{sub}/roles.json');f=raw(sub);ids=np.random.default_rng(191900).permutation(sorted(roles['fit']));parts=np.array_split(ids,3)
        for k,held in enumerate(parts):
            fit=sorted(set(map(int,ids))-set(map(int,held)));held=sorted(map(int,held));assert not set(fit)&set(held);pre=RegimeAwarePreprocessor(n_regimes=6 if sub in ['FD002','FD004'] else 1,seed=191900+k);pre.fit(f[f.engine_id.isin(fit)]);folder=OUT/'cv_data'/sub/f'fold_{k}';folder.mkdir(parents=True,exist_ok=True);joblib.dump(pre,folder/'preprocessor.joblib');b.sample_endpoints(f,held,191901+k).to_csv(folder/'endpoints.csv',index=False);write(dict(fit=fit,held=held,outer_validation=roles['validation'],outer_calibration=roles['calibration']),folder/'roles.json')
        for prefix in ['train','test','RUL']:
            p=ROOT/f'data/raw/cmapss/{prefix}_{sub}.txt';inputs[p.relative_to(ROOT).as_posix()]=sha(p)
        for n in ['roles.json','preprocessor.joblib','tensors.pt','calibration_endpoints.csv']:
            p=ROOT/f'results/fair_comparison_step2/data/{sub}/{n}';inputs[p.relative_to(ROOT).as_posix()]=sha(p)
    for p in (OUT/'cv_data').rglob('*'):
        if p.is_file():inputs[p.relative_to(ROOT).as_posix()]=sha(p)
    write(dict(unix=time.time(),sources=sources(),inputs=inputs,search_fits=108,final_fits=100,scope='Retrospective; no test-based selection; optional13/14 excluded'),OUT/'lock.json')
def payload(sub,fold):
    if fold is None:return torch.load(ROOT/f'results/fair_comparison_step2/data/{sub}/tensors.pt',weights_only=True)
    folder=OUT/'cv_data'/sub/f'fold_{fold}';roles=load(folder/'roles.json');f=joblib.load(folder/'preprocessor.joblib').transform(raw(sub));x,y,z=create_sliding_windows(f[f.engine_id.isin(roles['fit'])],b.FEATURES,30,125,30);end=pd.read_csv(folder/'endpoints.csv');return dict(X=torch.from_numpy(x),y=torch.from_numpy(y).reshape(-1,1),z=torch.from_numpy(z).reshape(-1,1),pos_weight=float((len(z)-z.sum())/z.sum()),validation_X=b.endpoint_tensor(f,end),validation_raw_y=torch.tensor(end.raw_y.to_numpy(),dtype=torch.float64))
def train(job):
    sub,arm,fold,lr,seed,epochs,tuning,relative=job;folder=OUT/relative;folder.mkdir(parents=True,exist_ok=True);identity=dict(subset=sub,arm=arm,fold=fold,lr=lr,seed=seed,epochs=epochs,tuning=tuning,lock_sha256=sha(OUT/'lock.json'))
    if (folder/'final.pt').exists():assert torch.load(folder/'final.pt',weights_only=True)['identity']==identity;return relative
    data=payload(sub,fold);x,y,z=[data[n] for n in ['X','y','z']];reset_seed(seed);model=factory(arm);opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=.0001);weight=torch.tensor([data['pos_weight']],dtype=torch.float32);history=[];prior=0
    if (folder/'progress.pt').exists():
        prev=torch.load(folder/'progress.pt',weights_only=True);assert prev['identity']==identity;model.load_state_dict(prev['state']);opt.load_state_dict(prev['optimizer']);torch.set_rng_state(prev['rng']);history=prev['history'];prior=prev['seconds']
    started=time.perf_counter()
    for epoch in range(len(history),epochs):
        model.train();loss_sum=0.;t=time.perf_counter()
        for ids in permutation_for_epoch(len(x),seed,epoch).split(128):
            opt.zero_grad(set_to_none=True)
            if arm=='gaussian':mu,sd=model.mean_scale(x[ids]);loss=(.5*((y[ids]-mu)/sd).square()+torch.log(sd)+.5*math.log(2*math.pi)).mean()
            else:a,c=task_losses(model(x[ids]),y[ids],z[ids],weight);loss=a+c
            assert torch.isfinite(loss);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.);opt.step();loss_sum+=float(loss.detach())*len(ids)
        metric=None
        if tuning:pred=b.predict(model,data['validation_X']);metric=b.capped_rmse(data['validation_raw_y'].numpy(),pred[:,1])
        history.append(dict(epoch=epoch+1,train_loss=loss_sum/len(x),validation_RMSE=metric,seconds=time.perf_counter()-t,train_windows=len(x),validation_n=len(data['validation_X']) if tuning else 0));pd.DataFrame(history).to_csv(folder/'history.csv',index=False)
        b.save(dict(state=model.state_dict(),optimizer=opt.state_dict(),rng=torch.get_rng_state(),history=history,identity=identity,seconds=prior+time.perf_counter()-started),folder/'progress.pt')
    b.save(dict(state=model.state_dict(),history=history,identity=identity,seconds=prior+time.perf_counter()-started,parameters=sum(p.numel() for p in model.parameters())),folder/'final.pt');print('FIT',relative,round(prior+time.perf_counter()-started,1),flush=True);return relative
def search_jobs():
    result=[]
    for sub in SUBS:
        for arm in ARMS:
            for i,lr in enumerate(LRS):result.append((sub,arm,None,lr,101,16,True,f'search/{sub}/{arm}/lr_{i}'))
        for arm in ['lstm','hybrid']:
            for fold in range(3):
                for i,lr in enumerate(LRS):result.append((sub,arm,fold,lr,101+1900*fold,16,True,f'cv_search/{sub}/{arm}/fold_{fold}/lr_{i}'))
    return result
def select():
    selected={};allrows=[]
    for sub in SUBS:
        for arm in ARMS+['lstm','hybrid']:
            options=[]
            for i,lr in enumerate(LRS):
                paths=[OUT/f'search/{sub}/{arm}/lr_{i}/history.csv'] if arm in ARMS else [OUT/f'cv_search/{sub}/{arm}/fold_{k}/lr_{i}/history.csv' for k in range(3)];frames=[pd.read_csv(p) for p in paths]
                for epoch in range(1,17):
                    hs=[f[f.epoch==epoch].iloc[0] for f in frames];score=math.sqrt(sum(h.validation_RMSE**2*h.validation_n for h in hs)/sum(h.validation_n for h in hs));options.append((score,i,epoch,lr));allrows.append(dict(subset=sub,arm=arm,lr=lr,epoch=epoch,validation_RMSE=score,folds=len(frames)))
            best=min(options);selected[sub+'_'+arm]=dict(score=best[0],candidate=best[1],epochs=best[2],lr=best[3],selection='single outer validation' if arm in ARMS else 'pooled threefold held-out engine MSE')
    write(selected,OUT/'selected.json');pd.DataFrame(allrows).to_csv(OUT/'search_scores.csv',index=False)
def final_jobs():
    selected=load(OUT/'selected.json');return [(sub,arm,None,selected[sub+'_'+arm]['lr'],seed,selected[sub+'_'+arm]['epochs'],False,f'final/{sub}/{arm}/seed_{seed}') for sub in SUBS for arm in ARMS+['lstm','hybrid'] for seed in SEEDS]
def run_pool(jobs):
    with ProcessPoolExecutor(max_workers=6,initializer=init) as pool:
        futures=[pool.submit(train,j) for j in jobs]
        for i,f in enumerate(as_completed(futures),1):p=f.result();write(dict(done=i,total=len(jobs),last=p,unix=time.time()),OUT/'progress.json')
def run():
    lock=load(OUT/'lock.json');assert lock['sources']==sources()
    for n,h in lock['inputs'].items():assert sha(ROOT/n)==h,n
    run_pool(search_jobs());select();run_pool(final_jobs());files={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.rglob('final.pt')};assert len(files)==208;write(dict(status='complete',unix=time.time(),files=files,selected_sha256=sha(OUT/'selected.json'),sources=sources(),scope='All neural fits frozen before new test scoring'),OUT/'training_complete.json')
if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--run' in sys.argv:run()

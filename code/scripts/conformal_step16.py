"""M5: signed CQR, all-prefix cluster calibration and bounded shift sensitivity."""
from pathlib import Path
import sys,json,hashlib,time,math,shutil
from concurrent.futures import ProcessPoolExecutor
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
import torch,joblib
from src.models.hybrid_lstm_tcn import HybridLSTMTCNPrognostic
from src.data.matched_benchmark import restore_preprocessor,FEATURES
from src.data.preprocessing import get_cmapss_column_names
OUT=ROOT/'results/conformal_step16';SUBS=['FD001','FD002','FD003','FD004'];SEEDS=[101,202,303,404,505]
METHODS=['RestrictedNonnegative','RestrictedSignedCQR','UnrestrictedSignedCQR','EngineBalancedSigned','EngineMaxSigned','CycleWeightedSigned']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(v,indent=2),encoding='utf-8')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sources():return {n:sha(ROOT/n) for n in ['scripts/conformal_step16.py','reports/conformal_step16_protocol.md','src/models/hybrid_lstm_tcn.py','src/data/preprocessing.py','src/data/matched_benchmark.py']}
def init():torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
def windows(a,cycles):
    padded=np.concatenate([np.repeat(a[:1],29,axis=0),a]);return np.stack([padded[c-1:c+29] for c in cycles]).astype(np.float32)
def predict(m,x):
    m.eval()
    with torch.inference_mode():return np.concatenate([torch.cat(m(torch.from_numpy(x[i:i+256])),dim=1).numpy() for i in range(0,len(x),256)])
def score(f,target):
    y=np.minimum(f.raw_y.to_numpy(),125) if target=='capped' else f.raw_y.to_numpy();return np.maximum(f.q05.to_numpy()-y,y-f.q95.to_numpy())
def rank(values):
    k=math.ceil((len(values)+1)*.9-1e-12);return np.inf if k>len(values) else float(np.sort(values)[k-1])
def weighted(values,weights,test_weight=0):
    order=np.argsort(values,kind='stable');v=np.asarray(values)[order];w=np.asarray(weights)[order];threshold=.9*(w.sum()+test_weight)
    if threshold>w.sum()+1e-12:return np.inf
    return float(v[min(np.searchsorted(np.cumsum(w),threshold,side='left'),len(v)-1)])
def bounds(qlo,qhi,cut,target):
    lo=np.maximum(qlo-cut,0);hi=qhi+cut
    if target=='capped':hi=np.minimum(hi,125)
    return lo,hi
def prepare():
    assert not (OUT/'lock.json').exists();OUT.mkdir(parents=True,exist_ok=True);old=ROOT/'archive/conformal_step16_before';old.mkdir(parents=True,exist_ok=True)
    for n in ['manuscript_v4.md','manuscript_v4.pdf','supplement_matched_endpoints.md','supplement_matched_endpoints.pdf','references.bib']:shutil.copy2(ROOT/'paper'/n,old/n)
    files={}
    for sub in SUBS:
        for prefix in ['train','test','RUL']:
            p=ROOT/f'data/raw/cmapss/{prefix}_{sub}.txt';files[p.relative_to(ROOT).as_posix()]=sha(p)
        for seed in SEEDS:
            for suffix in ['model.pt','preprocessing.joblib']:
                p=ROOT/f'results/final_evaluation_v3/checkpoints/{sub}_seed_{seed}_{suffix}';files[p.relative_to(ROOT).as_posix()]=sha(p)
    write(OUT/'lock.json',dict(created_unix=time.time(),sources=sources(),files=files,scope='Retrospective; no public preregistration or independent review'))
def infer(job):
    sub,seed=job;folder=OUT/'runs'/sub/f'seed_{seed}';folder.mkdir(parents=True,exist_ok=True);assert not (folder/'calibration_prefixes.csv').exists()
    saved=joblib.load(ROOT/f'results/final_evaluation_v3/checkpoints/{sub}_seed_{seed}_preprocessing.joblib');assert not set(saved['model_engines'])&set(saved['calibration_engines'])
    m=HybridLSTMTCNPrognostic();m.load_state_dict(torch.load(ROOT/f'results/final_evaluation_v3/checkpoints/{sub}_seed_{seed}_model.pt',weights_only=True)['model_state_dict'])
    pre=restore_preprocessor(saved);raw=pd.read_csv(ROOT/f'data/raw/cmapss/train_{sub}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names());cal=pre.transform(raw[raw.engine_id.isin(saved['calibration_engines'])]);frames=[]
    for eid,g in cal.groupby('engine_id',sort=True):
        g=g.sort_values('cycle');L=int(g.cycle.max());cy=np.arange(1,L);x=windows(g[FEATURES].to_numpy(np.float32),cy);p=predict(m,x)
        frames.append(pd.DataFrame(dict(engine_id=int(eid),cycle=cy,lifetime=L,raw_y=L-cy,padded=cy<30,q05=p[:,0],q50=p[:,1],q95=p[:,2],logit=p[:,3])))
    frame=pd.concat(frames,ignore_index=True);frame.to_csv(folder/'calibration_prefixes.csv',index=False)
    old=pd.read_csv(ROOT/f'results/final_evaluation_v3_exact_conformal/calibration/{sub}_seed_{seed}_calibration.csv');idx=frame.set_index(['engine_id','cycle']);restricted=idx.loc[list(zip(old.engine_id,old.cycle))].reset_index();assert np.array_equal(restricted.raw_y,old.true_RUL_raw);restricted.to_csv(folder/'restricted.csv',index=False)
    rng=np.random.default_rng(161600+seed+10000*SUBS.index(sub));chosen=[]
    for eid,g in frame.groupby('engine_id',sort=True):chosen.append(g.iloc[int(rng.integers(0,len(g)))])
    pd.DataFrame(chosen).to_csv(folder/'unrestricted.csv',index=False)
    test=pre.transform(pd.read_csv(ROOT/f'data/raw/cmapss/test_{sub}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names()));truth=np.loadtxt(ROOT/f'data/raw/cmapss/RUL_{sub}.txt');frames=[];xs=[]
    for eid,g in test.groupby('engine_id',sort=True):
        g=g.sort_values('cycle');cy=int(g.cycle.max());x=windows(g[FEATURES].to_numpy(np.float32),[cy]);xs.append(x[0]);frames.append(dict(engine_id=int(eid),cycle=cy,raw_y=truth[int(eid)-1],padded=cy<30))
    x=np.stack(xs);p=predict(m,x);t=pd.DataFrame(frames)
    for i,k in enumerate(['q05','q50','q95','logit']):t[k]=p[:,i]
    t.to_csv(folder/'test_predictions.csv',index=False);np.savez_compressed(folder/'test_inputs.npz',X=x)
    write(folder/'inference.json',dict(calibration_engines=len(saved['calibration_engines']),prefixes=len(frame),completed_unix=time.time(),model_sha256=sha(ROOT/f'results/final_evaluation_v3/checkpoints/{sub}_seed_{seed}_model.pt')))
    print('INFERRED',sub,seed,len(frame),flush=True)
def analyze(root=ROOT,out=OUT):
    rows=[];details=[];cutoffs=[]
    for sub in SUBS:
        for seed in SEEDS:
            folder=root/'results/conformal_step16/runs'/sub/f'seed_{seed}';read=lambda n:pd.read_csv(folder/n,float_precision='round_trip')
            c=read('calibration_prefixes.csv');r=read('restricted.csv');u=read('unrestricted.csv');t=read('test_predictions.csv');n=c.engine_id.nunique();counts=c.groupby('engine_id').cycle.transform('size').to_numpy();bins=np.array([0,30,60,90,120,150,200,300,np.inf]);cb=np.searchsorted(bins,u.cycle,side='right')-1;tb=np.searchsorted(bins,t.cycle,side='right')-1
            ratio=((np.bincount(tb,minlength=8)+1)/(len(t)+8))/((np.bincount(cb,minlength=8)+1)/(len(u)+8))
            for target in ['capped','raw']:
                cs=score(c,target);rs=score(r,target);us=score(u,target);maxima=pd.DataFrame(dict(engine=c.engine_id,s=cs)).groupby('engine').s.max().to_numpy()
                for method in METHODS:
                    if method=='RestrictedNonnegative':cuts=np.repeat(rank(np.maximum(rs,0)),len(t))
                    elif method=='RestrictedSignedCQR':cuts=np.repeat(rank(rs),len(t))
                    elif method=='UnrestrictedSignedCQR':cuts=np.repeat(rank(us),len(t))
                    elif method=='EngineBalancedSigned':cuts=np.repeat(weighted(cs,1/counts,1),len(t))
                    elif method=='EngineMaxSigned':cuts=np.repeat(rank(maxima),len(t))
                    else:cuts=np.array([weighted(us,ratio[cb],ratio[b]) for b in tb])
                    lo,hi=bounds(t.q05.to_numpy(),t.q95.to_numpy(),cuts,target);y=np.minimum(t.raw_y,125).to_numpy() if target=='capped' else t.raw_y.to_numpy();empty=lo>hi;covered=(~empty)&(lo<=y)&(y<=hi);width=np.maximum(hi-lo,0)
                    for group,mask in [('All',np.ones(len(t),bool)),('Above125',(t.raw_y>125).to_numpy()),('Within125',(t.raw_y<=125).to_numpy()),('Padded',t.padded.to_numpy(bool)),('FullHistory',~t.padded.to_numpy(bool))]:
                        if not mask.any():continue
                        rows.append(dict(subset=sub,seed=seed,target=target,method=method,group=group,n=int(mask.sum()),coverage=float(covered[mask].mean()),width=float(width[mask].mean()),empty=int(empty[mask].sum()),infinite=int(np.isinf(hi[mask]).sum())))
                    for i in range(len(t)):details.append(dict(subset=sub,seed=seed,target=target,method=method,engine_id=int(t.engine_id.iloc[i]),raw_y=float(t.raw_y.iloc[i]),target_y=y[i],lower=lo[i],upper=hi[i],covered=bool(covered[i]),empty=bool(empty[i]),padded=bool(t.padded.iloc[i]),cutoff=cuts[i]))
                    cutoffs.append(dict(subset=sub,seed=seed,target=target,method=method,n_cal_engines=n,n_cal_prefixes=len(c),min_cutoff=float(cuts.min()),max_cutoff=float(cuts.max())))
    df=pd.DataFrame(rows);df.to_csv(out/'per_run.csv',index=False);pd.DataFrame(details).to_csv(out/'per_engine.csv',index=False);pd.DataFrame(cutoffs).to_csv(out/'cutoffs.csv',index=False)
    df.groupby(['subset','target','method','group'])[['coverage','width']].agg(['mean','std']).to_csv(out/'summary.csv')
def run():
    lock=load(OUT/'lock.json');assert lock['sources']==sources()
    for n,h in lock['files'].items():assert sha(ROOT/n)==h,n
    with ProcessPoolExecutor(max_workers=4,initializer=init) as pool:list(pool.map(infer,[(s,n) for s in SUBS for n in SEEDS]))
    write(OUT/'inference_complete.json',dict(unix=time.time(),sources=sources(),files={p.relative_to(ROOT).as_posix():sha(p) for p in (OUT/'runs').rglob('*') if p.is_file()}));analyze()
if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--run' in sys.argv:run()

"""Fit12 fixed GBR controls; diagnose conditional feature-moment shift in24 splits."""
from pathlib import Path
import sys,json,hashlib,time
from concurrent.futures import ProcessPoolExecutor
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import numpy as np,pandas as pd,torch,joblib
from sklearn.ensemble import GradientBoostingRegressor
from threadpoolctl import threadpool_limits
from src.data.preprocessing import get_cmapss_column_names
from src.data.matched_benchmark import FEATURES,restore_preprocessor
from remaining_step19_campaign import OUT,write,sha,load,SUBS

def init():torch.set_num_threads(1);threadpool_limits(1)
def fit_gbr(sub):
    d=torch.load(ROOT/f'results/fair_comparison_step2/data/{sub}/tensors.pt',weights_only=True);x=d['X'][:,-1,:].numpy();y=d['y'].numpy().ravel();folder=OUT/'gbr'/sub;folder.mkdir(parents=True,exist_ok=True);models={}
    for name,loss,alpha in [('point','squared_error',.5),('lower','quantile',.05),('upper','quantile',.95)]:
        model=GradientBoostingRegressor(loss=loss,alpha=alpha,n_estimators=200,max_depth=3,learning_rate=.05,random_state=101);model.fit(x,y);joblib.dump(model,folder/(name+'.joblib'));models[name]=dict(parameters=model.get_params(),sha256=sha(folder/(name+'.joblib')))
    write(dict(unix=time.time(),models=models,training_windows=len(y),roles=load(ROOT/f'results/fair_comparison_step2/data/{sub}/roles.json'),scope='Three unique fitting-only regressors; no test access'),folder/'fit.json');print('GBR',sub,flush=True)

def prior_case(key):
    data=ROOT/'results/probability_step17/data'/key;meta=load(data/'metadata.json');parts=key.split('_');study,sub=parts[:2]
    if study=='Original':pre=restore_preprocessor(joblib.load(ROOT/f'results/final_evaluation_v3/checkpoints/{sub}_seed_{parts[2]}_preprocessing.joblib'))
    else:pre=joblib.load(ROOT/f'results/fair_comparison_step2/data/{sub}/preprocessor.joblib')
    raw=pd.read_csv(ROOT/f'data/raw/cmapss/train_{sub}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names());f=pre.transform(raw);source={0:[],1:[]}
    for eid,g in f[f.engine_id.isin(meta['fit_engines'])].groupby('engine_id',sort=True):
        a=g.sort_values('cycle')[FEATURES].to_numpy(np.float64)[29:];yy=(len(g)-np.arange(30,len(g)+1)<=30).astype(int)
        for cls in [0,1]:source[cls].append(np.r_[a[yy==cls].sum(axis=0),int((yy==cls).sum())])
    target={0:[],1:[]};cf=pd.read_csv(data/'calibration_features.csv');xx=np.load(data/'calibration_features.npz')['X'].astype(np.float64)
    for eid,g in cf.groupby('engine_id',sort=True):
        ix=g.index.to_numpy();a=xx[ix];yy=g.y.to_numpy();w=1/len(g)
        for cls in [0,1]:target[cls].append(np.r_[a[yy==cls].sum(axis=0)*w,(yy==cls).sum()*w])
    folder=OUT/'prior_shift'/key;folder.mkdir(parents=True,exist_ok=True);rows=[];stats=[]
    for cls in [0,1]:
        a=np.stack(source[cls]);b=np.stack(target[cls]);assert (a[:,-1]>0).all() and (b[:,-1]>0).all();N=len(a);M=len(b);rng=np.random.default_rng(191900+sum(map(ord,key))+cls*10000);ca=rng.multinomial(N,np.repeat(1/N,N),1999);cb=rng.multinomial(M,np.repeat(1/M,M),1999);aa=ca@a;bb=cb@b;boot=bb[:,:-1]/bb[:,-1,None]-aa[:,:-1]/aa[:,-1,None];observed=b[:,:-1].sum(axis=0)/b[:,-1].sum()-a[:,:-1].sum(axis=0)/a[:,-1].sum();se=boot.std(axis=0,ddof=1);active=se>1e-10;maximum=np.max(np.abs(observed[active]/se[active]));null=np.max(np.abs((boot[:,active]-observed[active])/se[active]),axis=1);pv=(1+int((null>=maximum-1e-12).sum()))/2000;q=np.quantile(null,.95)
        np.savez_compressed(folder/f'class_{cls}.npz',source_contributions=a,target_contributions=b,bootstrap=boot,delta=observed,se=se,null_max=null)
        for j,name in enumerate(FEATURES):rows.append(dict(partition=key,event_class=cls,feature=name,delta_target_minus_source=observed[j],se=se[j],simultaneous_low=observed[j]-q*se[j],simultaneous_high=observed[j]+q*se[j]))
        stats.append(dict(partition=key,event_class=cls,source_engines=N,target_engines=M,max_studentized=maximum,p_bootstrap=pv,bootstrap_draws=1999,active_features=int(active.sum())))
    pd.DataFrame(rows).to_csv(folder/'features.csv',index=False);write(stats,folder/'tests.json');print('PRIOR',key,flush=True);return stats

def run():
    lock=OUT/'auxiliary_lock.json';assert not lock.exists();keys=sorted(p.name for p in (ROOT/'results/probability_step17/data').iterdir() if p.is_dir());assert len(keys)==24
    sources={str(Path(__file__).relative_to(ROOT)):sha(__file__),'reports/remaining_step19_protocol.md':sha(ROOT/'reports/remaining_step19_protocol.md')};inputs={}
    for key in keys:
        for n in ['metadata.json','calibration_features.csv','calibration_features.npz']:
            p=ROOT/'results/probability_step17/data'/key/n;inputs[p.relative_to(ROOT).as_posix()]=sha(p)
    write(dict(unix=time.time(),sources=sources,inputs=inputs,scope='No official test labels used; frozen preprocessing; exploratory cluster-bootstrap conditional moments'),lock)
    with ProcessPoolExecutor(max_workers=2,initializer=init) as pool:list(pool.map(fit_gbr,SUBS))
    write(dict(status='complete',unix=time.time(),files={p.relative_to(ROOT).as_posix():sha(p) for p in (OUT/'gbr').rglob('*.joblib')},unique_fits=12),OUT/'gbr_complete.json')
    with ProcessPoolExecutor(max_workers=2,initializer=init) as pool:tests=[r for group in pool.map(prior_case,keys) for r in group]
    frame=pd.DataFrame(tests);order=np.argsort(frame.p_bootstrap.to_numpy(),kind='stable');adjusted=np.maximum.accumulate((len(frame)-np.arange(len(frame)))*frame.p_bootstrap.to_numpy()[order]);frame['p_Holm']=0.;frame.loc[order,'p_Holm']=np.minimum(1,adjusted);frame.to_csv(OUT/'prior_shift_tests.csv',index=False);pd.concat([pd.read_csv(OUT/'prior_shift'/key/'features.csv') for key in keys]).to_csv(OUT/'prior_shift_features.csv',index=False);write(dict(status='complete',unix=time.time(),tests=48,features=864,method='Approximate centered studentized engine-bootstrap; not an exact label-shift test'),OUT/'prior_shift_complete.json')
if __name__=='__main__':
    with threadpool_limits(limits=1):run()

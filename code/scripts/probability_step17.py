"""Frozen neural outputs, engine-cross-fitted calibration and true linear controls."""
from pathlib import Path
import sys,json,hashlib,time,shutil,warnings
from concurrent.futures import ProcessPoolExecutor
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import numpy as np
import pandas as pd
import torch,joblib
from scipy.special import expit,logit
from scipy.optimize import minimize,minimize_scalar
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import roc_auc_score
from threadpoolctl import threadpool_limits
from src.data.matched_benchmark import restore_preprocessor,FEATURES
from src.data.preprocessing import get_cmapss_column_names
from src.models.simple_quantile_risk import make_model
from baseline_step15 import GRU
OUT=ROOT/'results/probability_step17';SUBS=['FD001','FD002','FD003','FD004'];OLD=[101,202,303,404,505];NEW=[1101,1202,1303,1404,1505]
METHODS=['Raw','TrainWeightOffset','CalibrationPriorOffset','InterceptFit','Platt','Temp','OffsetTemp','Isotonic','Beta','CalConstant','CalConstantJeffreys','EndpointConstant','FeatureLogistic','FeatureLogisticPlatt']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,allow_nan=False),encoding='utf-8')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def read(p):return pd.read_csv(p,float_precision='round_trip')
def init():
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True);threadpool_limits(1)
def cases():
    result=[]
    for sub in SUBS:
        for seed in OLD:result.append(dict(study='Original',subset=sub,model='hybrid',seed=seed,data=f'Original_{sub}_{seed}',checkpoint=f'results/final_evaluation_v3/checkpoints/{sub}_seed_{seed}_model.pt',state='model_state_dict'))
        for arm in ['gru','hybrid','lstm','tcn']:
            parent='baseline_step15' if arm in ['gru','tcn'] else 'fair_comparison_step2'
            for seed in NEW:result.append(dict(study='Matched',subset=sub,model=arm,seed=seed,data=f'Matched_{sub}',checkpoint=f'results/{parent}/final/{sub}/{arm}/seed_{seed}/final.pt',state='state'))
    return result
def source():return {n:sha(ROOT/n) for n in ['scripts/probability_step17.py','reports/probability_step17_protocol.md','scripts/baseline_step15.py','src/models/simple_quantile_risk.py','src/models/hybrid_lstm_tcn.py','src/data/preprocessing.py','src/data/matched_benchmark.py']}
def prepare():
    assert not (OUT/'lock.json').exists();OUT.mkdir(parents=True,exist_ok=True);old=ROOT/'archive/probability_step17_before';old.mkdir(parents=True,exist_ok=True)
    for n in ['manuscript_v4.md','manuscript_v4.pdf','supplement_matched_endpoints.md','supplement_matched_endpoints.pdf','references.bib']:shutil.copy2(ROOT/'paper'/n,old/n)
    files={}
    for c in cases():files[c['checkpoint']]=sha(ROOT/c['checkpoint'])
    for pattern in ['results/conformal_step16/runs/*/seed_*/calibration_prefixes.csv','results/conformal_step16/runs/*/seed_*/test_predictions.csv','data/raw/cmapss/*.txt','results/final_evaluation_v3/checkpoints/*_preprocessing.joblib','results/fair_comparison_step2/data/*/preprocessor.joblib','results/fair_comparison_step2/data/*/roles.json','results/calibration_stage3/per_run.csv']:
        for p in ROOT.glob(pattern):files[p.relative_to(ROOT).as_posix()]=sha(p)
    for pattern in ['results/verification_stage1/*_training.json','results/fair_comparison_step2/data/*/calibration_endpoints.csv','results/fair_comparison_step2/final/*/lstm/seed_1101/calibration_fits.json','results/final_evaluation_v3_exact_conformal/calibration/*_calibration.csv']:
        for p in ROOT.glob(pattern):files[p.relative_to(ROOT).as_posix()]=sha(p)
    write(OUT/'lock.json',dict(unix=time.time(),sources=source(),files=files,cases=cases(),new_neural_training=0,linear_fits=24,scope='Retrospective; previous labels examined'))
def sequence(a):
    a=np.asarray(a,np.float32);p=np.concatenate([np.repeat(a[:1],29,axis=0),a]);return np.stack([p[i:i+30] for i in range(len(a)-1)])
def prepare_data(key):
    parts=key.split('_');study,sub=parts[:2];folder=OUT/'data'/key;folder.mkdir(parents=True,exist_ok=True)
    if study=='Original':
        seed=int(parts[2]);saved=joblib.load(ROOT/f'results/final_evaluation_v3/checkpoints/{sub}_seed_{seed}_preprocessing.joblib');pre=restore_preprocessor(saved);fit=set(saved['model_engines']);cal=set(saved['calibration_engines']);end=read(ROOT/f'results/final_evaluation_v3_exact_conformal/calibration/{sub}_seed_{seed}_calibration.csv');endpoint=float((end.true_RUL_raw<=30).mean())
    else:
        roles=load(ROOT/f'results/fair_comparison_step2/data/{sub}/roles.json');fit=set(roles['fit']);cal=set(roles['calibration']);pre=joblib.load(ROOT/f'results/fair_comparison_step2/data/{sub}/preprocessor.joblib');end=read(ROOT/f'results/fair_comparison_step2/data/{sub}/calibration_endpoints.csv');endpoint=float((end.raw_y<=30).mean())
    assert not fit&cal
    raw=pd.read_csv(ROOT/f'data/raw/cmapss/train_{sub}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names());scaled=pre.transform(raw);tx=[];ty=[];cx=[];cy=[];meta=[];seq=[]
    for eid,g in scaled.groupby('engine_id',sort=True):
        g=g.sort_values('cycle');arr=g[FEATURES].to_numpy(np.float32);L=len(arr)
        if eid in fit:tx.append(arr[29:]);ty.extend((L-np.arange(30,L+1)<=30).astype(int))
        if eid in cal:
            cx.append(arr[:-1]);cy.extend((L-np.arange(1,L)<=30).astype(int));meta.extend([dict(engine_id=int(eid),cycle=int(t),raw_y=L-t) for t in range(1,L)])
            if study=='Matched':seq.append(sequence(arr))
    tx=np.concatenate(tx);ty=np.asarray(ty,int);cx=np.concatenate(cx);cy=np.asarray(cy,int);frame=pd.DataFrame(meta)
    assert len(cx)==len(cy)==len(frame);weights=1/frame.groupby('engine_id').cycle.transform('size').to_numpy()
    with warnings.catch_warnings():
        warnings.simplefilter('error',ConvergenceWarning);linear=LogisticRegression(C=1,max_iter=2000,tol=1e-8).fit(tx,ty)
    joblib.dump(linear,folder/'feature_logistic.joblib');frame['linear_logit']=linear.decision_function(cx);frame['y']=cy;frame['engine_weight']=weights
    frame.to_csv(folder/'calibration_features.csv',index=False);np.savez_compressed(folder/'calibration_features.npz',X=cx)
    test_raw=pd.read_csv(ROOT/f'data/raw/cmapss/test_{sub}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names());test_scaled=pre.transform(test_raw);truth=np.loadtxt(ROOT/f'data/raw/cmapss/RUL_{sub}.txt');xs=[];features=[]
    for eid,g in test_scaled.groupby('engine_id',sort=True):
        arr=g.sort_values('cycle')[FEATURES].to_numpy(np.float32);features.append(arr[-1]);hist=arr[-30:];xs.append(np.concatenate([np.repeat(hist[:1],max(0,30-len(hist)),axis=0),hist]))
    tf=pd.DataFrame(dict(engine_id=np.arange(1,len(truth)+1),raw_y=truth,y=(truth<=30).astype(int),linear_logit=linear.decision_function(np.stack(features))));tf.to_csv(folder/'test_features.csv',index=False)
    np.savez_compressed(folder/'test_inputs.npz',X=np.stack(xs),features=np.stack(features))
    if study=='Matched':np.savez_compressed(folder/'calibration_inputs.npz',X=np.concatenate(seq))
    endpoint_labels={str(int(e)):int(y<=30) for e,y in zip(end.engine_id,end.true_RUL_raw if study=='Original' else end.raw_y)}
    weight=float(np.float32((len(ty)-ty.sum())/ty.sum()))
    if study=='Original':
        frozen=load(ROOT/f'results/verification_stage1/{sub}_seed_{seed}_training.json');assert weight==frozen['w_pos_train_float32']
    else:
        frozen=load(ROOT/f'results/fair_comparison_step2/final/{sub}/lstm/seed_1101/calibration_fits.json');assert abs(mathlog(weight)-frozen['ln_pos_weight'])<1e-6
    write(folder/'metadata.json',dict(fit_engines=sorted(map(int,fit)),calibration_engines=sorted(map(int,cal)),train_windows=len(ty),train_positive=int(ty.sum()),train_prior=float(ty.mean()),train_weight_float32=weight,endpoint_labels=endpoint_labels,endpoint_prior=endpoint,endpoint_positive=int((end.true_RUL_raw<=30).sum()) if study=='Original' else int((end.raw_y<=30).sum()),endpoint_n=len(end),feature_coefficients=linear.coef_.tolist(),feature_intercept=linear.intercept_.tolist()))
    print('DATA',key,len(frame),flush=True)
def infer_case(c):
    folder=OUT/'cases'/c['study']/c['subset']/c['model']/f"seed_{c['seed']}";folder.mkdir(parents=True,exist_ok=True);data=OUT/'data'/c['data'];cal=read(data/'calibration_features.csv');test=read(data/'test_features.csv')
    if c['study']=='Original':
        parent=ROOT/f"results/conformal_step16/runs/{c['subset']}/seed_{c['seed']}";p=read(parent/'calibration_prefixes.csv');q=read(parent/'test_predictions.csv');assert np.array_equal(p.engine_id,cal.engine_id) and np.array_equal(p.cycle,cal.cycle);assert np.array_equal(q.engine_id,test.engine_id) and np.array_equal(q.raw_y,test.raw_y);assert np.array_equal(p.raw_y,cal.raw_y);cal['logit']=p.logit;test['logit']=q.logit
    else:
        model=GRU() if c['model']=='gru' else make_model(c['model']);model.load_state_dict(torch.load(ROOT/c['checkpoint'],weights_only=True)[c['state']]);model.eval()
        def predict(x):
            with torch.inference_mode():return np.concatenate([model(torch.from_numpy(x[i:i+256]))[3].numpy().ravel() for i in range(0,len(x),256)])
        cal['logit']=predict(np.load(data/'calibration_inputs.npz')['X']);test['logit']=predict(np.load(data/'test_inputs.npz')['X'])
    cal.to_csv(folder/'calibration_base.csv',index=False);test.to_csv(folder/'test_base.csv',index=False);write(folder/'identity.json',c)
def engine_folds(ids):
    ids=sorted(set(map(int,ids)),key=lambda x:hashlib.sha256(f'step17|{x}'.encode()).hexdigest());return {eid:i%5 for i,eid in enumerate(ids)}
def fit_cal(method,z,y,w,ids,linear,offset,pi_train,endpoint):
    pi=float(np.average(y,weights=w));clip=lambda x:float(np.clip(x,1e-9,1-1e-9));base=dict(method=method,pi=pi,offset=offset,pi_train=pi_train,endpoint=endpoint)
    if method in ['Raw','TrainWeightOffset','CalibrationPriorOffset','CalConstant','CalConstantJeffreys','EndpointConstant','FeatureLogistic']:
        base['n_engines']=len(set(ids));return base
    pos=len(set(ids[y==1]));neg=len(set(ids[y==0]));flex=method in ['Platt','Isotonic','Beta','FeatureLogisticPlatt']
    if min(pos,neg)<(5 if flex else 1):return dict(**base,status='NOT_IDENTIFIABLE',positive_engines=pos,negative_engines=neg)
    zw=linear if method=='FeatureLogisticPlatt' else z;wn=w/w.sum()
    if method=='Isotonic':
        m=IsotonicRegression(out_of_bounds='clip').fit(expit(z),y,sample_weight=w);return dict(**base,x=m.X_thresholds_.tolist(),p=m.y_thresholds_.tolist(),status='fit')
    if method in ['Temp','OffsetTemp']:
        zz=z-(offset if method=='OffsetTemp' else 0);m=minimize_scalar(lambda t:float(np.average(np.logaddexp(0,zz/np.exp(t))-y*zz/np.exp(t),weights=w)),bounds=(mathlog(.1),mathlog(10)),method='bounded');assert m.success;return dict(**base,T=float(np.exp(m.x)),boundary=bool(min(abs(m.x-mathlog(.1)),abs(m.x-mathlog(10)))<1e-4),status='fit')
    if method=='Beta':
        p=np.clip(expit(z),1e-12,1-1e-12);X=np.column_stack([np.log(p),-np.log1p(-p),np.ones(len(z))]);start=[1,1,0];bounds=[(0,None),(0,None),(None,None)]
    elif method=='InterceptFit':X=np.ones((len(z),1));start=[0];bounds=[(None,None)]
    else:X=np.column_stack([zw,np.ones(len(z))]);start=[1,0];bounds=[(0,None),(None,None)]
    fixed=z if method=='InterceptFit' else 0
    def objective(b):
        eta=fixed+X@b;value=np.sum(wn*(np.logaddexp(0,eta)-y*eta))+1e-4*np.dot(b,b);grad=X.T@(wn*(expit(eta)-y))+2e-4*b;return value,grad
    m=minimize(objective,np.array(start,float),jac=True,bounds=bounds,method='L-BFGS-B',options=dict(maxiter=2000,ftol=1e-12,gtol=1e-8));assert m.success,(method,m.message)
    return dict(**base,coef=m.x.tolist(),status='fit',boundary=bool(any(v<1e-7 for v,b in zip(m.x,bounds) if b[0]==0)))
def mathlog(x):return float(np.log(x))
def calibrated_logit(m,z,linear):
    name=m['method']
    if m.get('status')=='NOT_IDENTIFIABLE':return np.full(len(z),np.nan)
    if name=='Raw':eta=z
    elif name=='TrainWeightOffset':eta=z-m['offset']
    elif name=='CalibrationPriorOffset':eta=z-m['offset']+logit(np.clip(m['pi'],1e-9,1-1e-9))-logit(m['pi_train'])
    elif name=='InterceptFit':eta=z+m['coef'][0]
    elif name in ['Platt','FeatureLogisticPlatt']:eta=m['coef'][0]*(linear if name=='FeatureLogisticPlatt' else z)+m['coef'][1]
    elif name in ['Temp','OffsetTemp']:eta=(z-(m['offset'] if name=='OffsetTemp' else 0))/m['T']
    elif name=='Beta':
        p=np.clip(expit(z),1e-12,1-1e-12);eta=m['coef'][0]*np.log(p)-m['coef'][1]*np.log1p(-p)+m['coef'][2]
    elif name=='Isotonic':return logit(np.clip(np.interp(expit(z),m['x'],m['p']),1e-15,1-1e-15))
    elif name=='FeatureLogistic':eta=linear
    else:
        p=m['endpoint'] if name=='EndpointConstant' else ((m['pi']*m['n_engines']+.5)/(m['n_engines']+1) if name=='CalConstantJeffreys' else m['pi']);return np.repeat(logit(np.clip(p,1e-15,1-1e-15)),len(z))
    return eta

def apply_cal(m,z,linear):
    if m['method']=='Isotonic' and m.get('status')!='NOT_IDENTIFIABLE':return np.interp(expit(z),m['x'],m['p'])
    return expit(calibrated_logit(m,z,linear))
def fit_case(c):
    folder=OUT/'cases'/c['study']/c['subset']/c['model']/f"seed_{c['seed']}";f=read(folder/'calibration_base.csv');meta=load(OUT/'data'/c['data']/'metadata.json');foldmap=engine_folds(f.engine_id);fold=f.engine_id.map(foldmap).to_numpy();z=f.logit.to_numpy();y=f.y.to_numpy();w=f.engine_weight.to_numpy();ids=f.engine_id.to_numpy();linear=f.linear_logit.to_numpy();pi_train=meta['train_prior'];offset=mathlog(meta['train_weight_float32']);models={};folds=[]
    for k in range(5):
        keep=fold!=k;valid=~keep;trainids=sorted(set(map(int,ids[keep])));validids=sorted(set(map(int,ids[valid])));assert not set(trainids)&set(validids);models_k={}
        for method in METHODS:
            endpoint=float(np.mean([meta['endpoint_labels'][str(e)] for e in trainids]))
            m=fit_cal(method,z[keep],y[keep],w[keep],ids[keep],linear[keep],offset,pi_train,endpoint);models_k[method]=m
            if 'p_'+method not in f:f['p_'+method]=np.nan
            if 'eta_'+method not in f:f['eta_'+method]=np.nan
            f.loc[valid,'p_'+method]=apply_cal(m,z[valid],linear[valid])
            f.loc[valid,'eta_'+method]=calibrated_logit(m,z[valid],linear[valid])
        folds.append(dict(fold=k,train_engines=trainids,validation_engines=validids,models=models_k))
    for method in METHODS:models[method]=fit_cal(method,z,y,w,ids,linear,offset,pi_train,meta['endpoint_prior'])
    f['fold']=fold;f.to_csv(folder/'calibration_oof.csv',index=False);write(folder/'calibrators.json',dict(models=models,folds=folds,final_fit_unix=time.time(),calibration_engines=sorted(foldmap),case=c))
    print('FITTED',c['study'],c['subset'],c['model'],c['seed'],flush=True)
def edges(p):return np.unique(np.quantile(p,[.2,.4,.6,.8]))
def metrics(y,p,w=None,eta=None):
    w=np.ones(len(y)) if w is None else np.asarray(w);w=w/w.sum();p=np.asarray(p);y=np.asarray(y);b=np.searchsorted(edges(p),p,side='right');b10=np.minimum((p*10).astype(int),9)
    eta=logit(np.clip(p,1e-15,1-1e-15)) if eta is None else np.asarray(eta)
    return dict(Brier=float(np.sum(w*(p-y)**2)),NLL=float(np.sum(w*(np.logaddexp(0,eta)-y*eta))),ECE5=float(sum(abs(np.sum(w[b==i]*(p[b==i]-y[b==i]))) for i in range(5))),ECE10=float(sum(abs(np.sum(w[b10==i]*(p[b10==i]-y[b10==i]))) for i in range(10))),AUC=float(roc_auc_score(y,p,sample_weight=w)) if len(np.unique(y))==2 else None,exact_zero=int((p==0).sum()),exact_one=int((p==1).sum()))
def evaluate():
    assert len(list((OUT/'cases').rglob('calibrators.json')))==100;write(OUT/'fitting_complete.json',dict(unix=time.time(),sources=source(),models=100,files={p.relative_to(ROOT).as_posix():sha(p) for p in (OUT/'cases').rglob('calibrators.json')}));rows=[];oof=[];supports=[]
    for c in cases():
        folder=OUT/'cases'/c['study']/c['subset']/c['model']/f"seed_{c['seed']}";models=load(folder/'calibrators.json')['models'];t=read(folder/'test_base.csv');f=read(folder/'calibration_oof.csv');meta=load(OUT/'data'/c['data']/'metadata.json');key={k:c[k] for k in ['study','subset','model','seed']};y=t.y.to_numpy();full=models['CalConstant']['pi'];endpoint=meta['endpoint_prior'];ref=np.mean((full-y)**2);ref_end=np.mean((endpoint-y)**2)
        supports.append(dict(**key,cal_engines=f.engine_id.nunique(),cal_rows=len(f),cal_positive_rows=int(f.y.sum()),cal_positive_engines=f[f.y==1].engine_id.nunique(),endpoint_n=meta['endpoint_n'],endpoint_positive=meta['endpoint_positive'],all_prefix_prior=full,endpoint_prior=endpoint,training_window_prior=meta['train_prior'],test_positive=int(y.sum()),test_n=len(y)))
        for method in METHODS:
            p=apply_cal(models[method],t.logit.to_numpy(),t.linear_logit.to_numpy());t['p_'+method]=p;eta=calibrated_logit(models[method],t.logit.to_numpy(),t.linear_logit.to_numpy());t['eta_'+method]=eta
            if np.isfinite(p).all():
                m=metrics(y,p,eta=eta);rows.append(dict(**key,method=method,**m,Brier_skill_prefix=1-m['Brier']/ref,Brier_skill_endpoint=1-m['Brier']/ref_end))
            p=f['p_'+method].to_numpy()
            if np.isfinite(p).all():oof.append(dict(**key,method=method,**metrics(f.y.to_numpy(),p,f.engine_weight.to_numpy(),f['eta_'+method].to_numpy())))
        t.to_csv(folder/'test_probabilities.csv',index=False)
    pd.DataFrame(rows).to_csv(OUT/'per_run.csv',index=False);pd.DataFrame(oof).to_csv(OUT/'oof_per_run.csv',index=False);pd.DataFrame(supports).to_csv(OUT/'support.csv',index=False)
def bootstrap():
    rows=[];per=read(OUT/'per_run.csv');groups=list(per[['study','subset','model']].drop_duplicates().itertuples(index=False,name=None));groups.sort(key=lambda g:(0 if g[0]=='Original' else 1,SUBS.index(g[1]),g[2]))
    for index,(study,sub,arm) in enumerate(groups):
        seeds=OLD if study=='Original' else NEW;frames=[read(OUT/'cases'/study/sub/arm/f'seed_{s}'/'test_probabilities.csv') for s in seeds];N=len(frames[0]);rng=np.random.default_rng(171700+index);ew=rng.multinomial(N,np.repeat(1/N,N),size=1000).T/N;rw=rng.multinomial(5,np.repeat(.2,5),size=1000).T/5;boot={}
        for method in METHODS:
            bs=[];es=[]
            for f in frames:
                p=f['p_'+method].to_numpy();y=f.y.to_numpy();b=np.searchsorted(edges(p),p,side='right');bs.append((p-y)**2@ew);es.append(sum(np.abs(((p-y)*(b==i))@ew) for i in range(5)))
            boot[method]=(np.sum(np.stack(bs)*rw,axis=0),np.sum(np.stack(es)*rw,axis=0))
        for method in METHODS:
            g=per[(per.study==study)&(per.subset==sub)&(per.model==arm)&(per.method==method)];b,e=boot[method];d=b-boot['Raw'][0];dl=b-boot['FeatureLogistic'][0]
            rows.append(dict(study=study,subset=sub,model=arm,method=method,Brier=float(g.Brier.mean()),NLL=float(g.NLL.mean()),ECE5=float(g.ECE5.mean()),Brier_skill_prefix=float(g.Brier_skill_prefix.mean()),Brier_skill_endpoint=float(g.Brier_skill_endpoint.mean()),Brier_low=np.quantile(b,.025),Brier_high=np.quantile(b,.975),ECE5_low=np.quantile(e,.025),ECE5_high=np.quantile(e,.975),delta_Raw=float(g.Brier.mean()-per[(per.study==study)&(per.subset==sub)&(per.model==arm)&(per.method=='Raw')].Brier.mean()),delta_Raw_low=np.quantile(d,.025),delta_Raw_high=np.quantile(d,.975),delta_Feature_low=np.quantile(dl,.025),delta_Feature_high=np.quantile(dl,.975)))
        np.savez_compressed(OUT/f'bootstrap_{study}_{sub}_{arm}.npz',**{m+'_'+metric:arr for m,pair in boot.items() for metric,arr in zip(['Brier','ECE5'],pair)})
    pd.DataFrame(rows).to_csv(OUT/'summary.csv',index=False)
def run():
    lock=load(OUT/'lock.json');assert lock['sources']==source()
    for n,h in lock['files'].items():assert sha(ROOT/n)==h,n
    keys=sorted({c['data'] for c in cases()})
    with ProcessPoolExecutor(max_workers=4,initializer=init) as pool:list(pool.map(prepare_data,keys))
    with ProcessPoolExecutor(max_workers=4,initializer=init) as pool:list(pool.map(infer_case,cases()))
    write(OUT/'inference_complete.json',dict(unix=time.time(),cases=100))
    with ProcessPoolExecutor(max_workers=4,initializer=init) as pool:list(pool.map(fit_case,cases()))
    threadpool_limits(1);evaluate();bootstrap();write(OUT/'analysis_complete.json',dict(unix=time.time(),status='complete',sources=source()))
if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--run' in sys.argv:run()

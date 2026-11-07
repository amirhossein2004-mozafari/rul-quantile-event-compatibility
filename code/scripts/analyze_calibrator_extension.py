import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import json,hashlib,datetime,platform,sys
import numpy as np
import pandas as pd
import scipy,sklearn
from scipy.special import expit,logit
from scipy.optimize import minimize,minimize_scalar
from sklearn.isotonic import IsotonicRegression
R=Path(__file__).resolve().parents[1];O=R/'reports/compatibility_null_validation/calibrator_extension';B=2000
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads((O/'protocol_lock.json').read_text());assert sha(O/'protocol.md')==lock['protocol_sha256']
inputs={}; roster=[];missing=[]
def track(p):
 p=R/p if not isinstance(p,Path) else p
 inputs[str(p.relative_to(R)).replace('\\','/')]=sha(p);return p
def read(p):return pd.read_csv(track(p),float_precision='round_trip')
def meta(p):return json.loads(track(p).read_text())
def save(n,v):pd.DataFrame(v).to_csv(O/n,index=False)
def ci(v):
 v=np.asarray(v);z=v[np.isfinite(v)];return dict(ci_low=float(np.quantile(z,.025)) if len(z) else np.nan,ci_high=float(np.quantile(z,.975)) if len(z) else np.nan,undefined_draws=int(len(v)-len(z)))
def row(info,measure,v):return dict(**info,measure=measure,estimate=float(v[0]),**ci(v[1:]))
SUB=['FD001','FD002','FD003','FD004'];seeds=[1101,1202,1303,1404,1505]
# Load saved arrays only. No project model modules or checkpoint readers.
for si,s in enumerate(SUB):
 truth=np.loadtxt(track(R/f'data/raw/cmapss/RUL_{s}.txt'));n=len(truth)
 for family,arms,ss in [('equal',['lstm','hybrid','tcn','gru'],seeds),('original',['hybrid'],[101,202,303,404,505]),('extra',['lstm_gpu','hybrid_gpu','gru_gpu','tcn_gpu','lstm_cv','hybrid_cv'],seeds)]:
  for arm in arms:
   fits=[]
   for seed in ss:
    if family=='original':
     cp=R/f'results/calibration_stage3/{s}_seed_{seed}_calibration_oof.csv';tp=R/f'results/calibration_stage3/{s}_seed_{seed}_test.csv'
    elif family=='extra':
     folder=R/f'results/remaining_step19/predictions/{s}/{arm}/seed_{seed}';cp=folder/'calibration.csv';tp=folder/'test.csv'
    else:
     parent='fair_comparison_step2' if arm in ['lstm','hybrid'] else 'baseline_step15';folder=R/f'results/{parent}/final/{s}/{arm}/seed_{seed}';cp=folder/'calibration_predictions.csv';tp=folder/'test_predictions.csv'
    if not cp.exists() or not tp.exists():missing.append(dict(subset=s,family=family,arm=arm,seed=seed,reason='saved prediction pair missing'));continue
    c=read(cp);t=read(tp)
    if family=='original':
     cq=read(R/f'results/final_evaluation_v3_exact_conformal/calibration/{s}_seed_{seed}_calibration.csv');tq=read(R/f'results/final_evaluation_v3_exact_conformal/{s}_seed_{seed}_predictions.csv')
     np.testing.assert_array_equal(c.engine_id,cq.engine_id);np.testing.assert_array_equal(t.engine_id,tq.engine_id)
     np.testing.assert_array_equal(c.true_RUL_raw,cq.true_RUL_raw);np.testing.assert_array_equal(t.true_RUL_raw,tq.true_RUL_raw)
     q=tq[['q05_raw','q50_raw','q95_raw']].values;cy=c.true_RUL_raw.values;y=t.true_RUL_raw.values;cr=c.raw_logit.values;tr=t.raw_logit.values;off=meta(R/f'results/calibration_stage3/{s}_seed_{seed}_fits.json')['ln_training_weight'];ids=t.engine_id.values;calids=c.engine_id.values
    else:
     q=t[['q05','q50','q95']].values;cy=c.raw_y.values;y=t.raw_y.values;cr=c.logit.values;tr=t.logit.values;ids=t.engine_id.values
     endpoint=read(R/f'results/fair_comparison_step2/data/{s}/calibration_endpoints.csv');calids=endpoint.engine_id.values;np.testing.assert_array_equal(cy,endpoint.raw_y)
     if 'engine_id' in c:np.testing.assert_array_equal(c.engine_id,calids)
     refarm=arm.split('_')[0];parent='fair_comparison_step2' if refarm in ['lstm','hybrid'] else 'baseline_step15'
     off=meta(R/f'results/{parent}/final/{s}/{refarm}/seed_{seed}/calibration_fits.json')['ln_pos_weight']
    np.testing.assert_array_equal(ids,np.arange(1,n+1));np.testing.assert_array_equal(y,truth);assert len(set(calids))==len(calids);assert np.all(np.diff(q,axis=1)>=0)
    fits.append(dict(seed=seed,q=q,y=y,cr=cr,tr=tr,cy=cy,off=off,calids=calids.tolist()))
   roster.append(dict(subset=s,si=si,family=family,arm=arm,fits=fits,n=n))
(O/'input_hashes_before.json').write_text(json.dumps(inputs,indent=2));save('missing.csv',missing)
(O/'roster.json').write_text(json.dumps([dict(subset=g['subset'],family=g['family'],arm=g['arm'],test_engines=g['n'],fits=[dict(seed=f['seed'],calibration_engines=len(f['cy']),calibration_ids=f['calids']) for f in g['fits']]) for g in roster],indent=2))
W={i:np.vstack([np.ones(n)/n,np.random.default_rng(2026110201+i).multinomial(n,np.ones(n)/n,size=B)/n]) for i,n in enumerate([100,259,100,248])}
A=[];C=[];D=[];E=[];FITS=[];EC=[];CACHE=[]
def calfit(cr,cy,tr,off,method):
 y=(cy<=30).astype(float)
 if method=='TrainOff':return expit(tr-off),dict(offset=off)
 if len(np.unique(y))<2:return np.full(len(tr),(y.sum()+.5)/(len(y)+1)),dict(status='single_class_smoothed')
 if method in ['Temp','TrainOff+Temp']:
  x=cr-(off if method=='TrainOff+Temp' else 0);z=tr-(off if method=='TrainOff+Temp' else 0)
  fun=lambda a:np.mean(np.logaddexp(0,x*a)-y*x*a)
  opt=minimize_scalar(fun,bounds=(.1,10),method='bounded',options={'xatol':1e-10});assert opt.success
  a=min([.1,10,1,opt.x],key=fun);return expit(z*a),dict(inverse_temperature=a)
 if method=='Isotonic':
  fit=IsotonicRegression(out_of_bounds='clip').fit(expit(cr),y);return fit.predict(expit(tr)),dict(x=fit.X_thresholds_.tolist(),y=fit.y_thresholds_.tolist())
 if method=='Platt':x=cr[:,None];z=tr[:,None]
 else:
  pp=np.clip(expit(cr),1e-15,1-1e-15);tt=np.clip(expit(tr),1e-15,1-1e-15);x=np.c_[np.log(pp),-np.log1p(-pp)];z=np.c_[np.log(tt),-np.log1p(-tt)]
 x=np.c_[np.ones(len(x)),x];z=np.c_[np.ones(len(z)),z]
 def objective(a):
  r=x@a;return np.mean(np.logaddexp(0,r)-y*r)+.5e-6*np.sum(a[1:]**2),x.T@(expit(r)-y)/len(y)+1e-6*np.r_[0,a[1:]]
 opt=minimize(objective,np.zeros(x.shape[1]),jac=True,method='L-BFGS-B',options={'maxiter':2000,'ftol':1e-12,'gtol':1e-9})
 if not opt.success:raise RuntimeError(str(opt.message))
 return expit(z@opt.x),dict(coefficients=opt.x.tolist())
def curves(p,y,w,info):
 pc=np.clip(p,1e-15,1-1e-15);out=[w@(p-y)**2,w@(-y*np.log(pc)-(1-y)*np.log1p(-pc))]
 for k in [5,10]:
  cuts=np.unique(np.quantile(p,np.linspace(0,1,6)))[1:-1] if k==5 else np.arange(1,10)/10
  ix=np.searchsorted(cuts,p,side='left');res=np.stack([(p-y)*(ix==j) for j in range(len(cuts)+1)],1);out.append(np.abs(w@res).sum(1));EC.append(dict(**info,metric='ECE'+str(k),cuts=cuts.tolist()))
 return np.array(out).T
for g in roster:
 if not g['fits']:continue
 s=g['subset'];w=W[g['si']];n=g['n'];fs=g['fits'];r=len(fs);info=dict(exploratory=True,subset=s,family=g['family'],architecture=g['arm'],evaluation_engines=n,fixed_fits=r,calibration_engines_per_fit=','.join(str(len(f['cy'])) for f in fs),distinct_calibration_engines=len(set(e for f in fs for e in f['calids'])))
 p=np.array([expit(f['tr']) for f in fs]);q=np.array([f['q'] for f in fs]);truth=fs[0]['y'];y=(truth<=30).astype(float)
 L=np.where(q<=30,[.05,.5,.95],0).max(-1);U=np.where(q>30,[.05,.5,.95],1).min(-1);proj=np.clip(p,L,U);d=abs(proj-p);flag=d>0
 variants={'raw':p,'projection':proj}
 for method in ['TrainOff','Temp','TrainOff+Temp','Platt','Isotonic','Beta']:
  pp=[]
  for f in fs:
   try:v,details=calfit(f['cr'],f['cy'],f['tr'],f['off'],method);status='ok'
   except Exception as exc:v=np.full(n,np.nan);details={'error':str(exc)};status='unavailable'
   pp.append(v);FITS.append(dict(**info,seed=f['seed'],method=method,status=status,details=json.dumps(details)))
  variants[method]=np.array(pp);variants[method+'+projection']=np.clip(pp,L,U)
 scores={name:np.mean([curves(v,y,w,dict(**info,seed=f['seed'],method=name)) for v,f in zip(pp,fs)],axis=0) for name,pp in variants.items()}
 for name,v in scores.items():
  for j,metric in enumerate(['Brier','NLL','ECE5','ECE10']):A.append(dict(**row(info,metric,v[:,j]),method=name,difference_vs_raw=float(v[0,j]-scores['raw'][0,j]),**{'difference_'+k:val for k,val in ci(v[1:,j]-scores['raw'][1:,j]).items()}))
 improvement=(p-y)**2-(proj-y)**2
 for label,mask in [('d=0',d==0),('(0,0.05]',(d>0)&(d<=.05)),('(0.05,0.2]',(d>.05)&(d<=.2)),('>0.2',d>.2)]:
  den=w@mask.mean(0)
  with np.errstate(invalid='ignore',divide='ignore'):v=(w@(improvement*mask).mean(0))/den
  C.append(dict(**row(info,'Brier_improvement',v),distance_bin=label,bin_distinct_engines=int(mask.any(0).sum()),bin_engine_fit_rows=int(mask.sum())))
 base=w@y.astype(float);raw=w@p.mean(0);pr=w@proj.mean(0)
 for name,v in [('above_U',w@(p>U).mean(0)),('below_L',w@(p<L).mean(0)),('signed_probability_change',pr-raw),('base_rate',base),('mean_raw_probability',raw),('mean_projected_probability',pr),('raw_base_rate_absolute_gap',abs(raw-base)),('projected_base_rate_absolute_gap',abs(pr-base)),('gap_change',abs(pr-base)-abs(raw-base))]:D.append(row(info,name,v))
 # Weighted within-fit OLS, resampling entire engine clusters.
 yy=np.stack([(q[:,:,1]-np.minimum(truth,125))**2,(p-y)**2],-1)
 for adjustment in ['RUL','RUL_raw_p_band','RUL_within_20_40']:
  mask=(truth>=20)&(truth<=40) if adjustment=='RUL_within_20_40' else np.ones(n,bool)
  a=np.minimum(truth,125)/125;cov=np.broadcast_to(np.stack([a,a*a,a*a*a],-1),(r,n,3));x=np.concatenate([flag[:,:,None],cov],-1).astype(float)
  if adjustment=='RUL_raw_p_band':x=np.concatenate([x,np.stack([p,p*p,p*p*p],-1),np.broadcast_to(((truth>=20)&(truth<=40))[None,:,None],(r,n,1))],-1)
  z=np.concatenate([x,yy],-1)[:,mask,:];ww=w[:,mask];den=ww.sum(1);valid=den>0;ww=np.divide(ww,den[:,None],out=np.zeros_like(ww),where=den[:,None]>0);nn=mask.sum();k=x.shape[-1]
  sec=np.einsum('rni,rnj->nij',z,z)/r;ss=(ww@sec.reshape(nn,-1)).reshape(B+1,k+2,k+2);means=(ww@z.transpose(1,0,2).reshape(nn,-1)).reshape(B+1,r,k+2);ss-=np.einsum('bri,brj->bij',means,means)/r
  aa=ss[:,:k,:k];bb=ss[:,:k,k:];inv=np.linalg.pinv(aa,rcond=1e-10,hermitian=True);ident=(np.linalg.norm((np.eye(k)-inv@aa)[:,0,:],axis=1)<1e-6)&valid;coef=(inv@bb)[:,0,:];coef[~ident]=np.nan
  for j,outcome in enumerate(['median_squared_error','Brier']):
   v=coef[:,j];mu=float(yy[:,mask,j].mean()) if nn else np.nan;lohi=ci(v[1:]);sd=np.nanstd(v[1:],ddof=1);mde=(1.959964+.841621)*sd
   E.append(dict(**row(info,outcome,v),adjustment=adjustment,regression_engines=int(nn),flagged_distinct_engines=int(flag[:,mask].any(0).sum()),own_mean=mu,coefficient_own_mean_ratio=v[0]/mu if mu else np.nan,ratio_ci_low=lohi['ci_low']/mu if mu else np.nan,ratio_ci_high=lohi['ci_high']/mu if mu else np.nan,approximate_MDE=mde,MDE_own_mean_ratio=mde/mu if mu else np.nan))
 CACHE.append((g,scores));print('COMPLETE',s,g['family'],g['arm'],n,flush=True)
# Each subset: equal weight across groups; across subsets: distinct engine counts.
for method in CACHE[0][1]:
 v=np.zeros((B+1,4));raw=np.zeros_like(v)
 for si,n in enumerate([100,259,100,248]):
  gs=[scores for g,scores in CACHE if g['si']==si];v+=n/707*np.mean([sc[method] for sc in gs],0);raw+=n/707*np.mean([sc['raw'] for sc in gs],0)
 for j,metric in enumerate(['Brier','NLL','ECE5','ECE10']):
  info=dict(exploratory=True,subset='pooled',family='all',architecture='all',evaluation_engines=707,fixed_fits=sum(len(g['fits']) for g,sc in CACHE),calibration_engines_per_fit='see roster',distinct_calibration_engines='see roster; no test/calibration pooling')
  A.append(dict(**row(info,metric,v[:,j]),method=method,difference_vs_raw=float(v[0,j]-raw[0,j]),**{'difference_'+k:val for k,val in ci(v[1:,j]-raw[1:,j]).items()}))
cons=[]
for a in A:
 if a['subset']!='pooled' and a['method']=='projection' and a['measure'] in ['Brier','NLL']:
  cons.append(dict(**a,sign='negative' if a['difference_vs_raw']<0 else 'positive' if a['difference_vs_raw']>0 else 'zero',classification='helps' if a['difference_ci_high']<0 else 'hurts' if a['difference_ci_low']>0 else 'unresolved'))
save('A_all_scores.csv',A);save('B_consistency.csv',cons);save('C_dose_response.csv',C);save('D_mechanism.csv',D);save('E_associations.csv',E);save('calibrator_fits.csv',FITS);(O/'ECE_edges.json').write_text(json.dumps(EC,indent=2))
for name,h in inputs.items():assert sha(R/name)==h,name
prov=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,current_executor='GPT-6 family Codex; exact served model/build unavailable unless session records below',served_checkpoint='UNAVAILABLE',independent_human_review='MISSING',training=False,inference=False)
sid=os.environ.get('CODEX_SESSION_ID','');ident=[]
if sid:
 for path in (Path(os.environ['USERPROFILE'])/'.codex/sessions').rglob('*'+sid+'*.jsonl'):
  for line in path.open(encoding='utf-8'):
   try:a=json.loads(line)
   except:continue
   if a.get('type') in ['session_meta','turn_context']:
    p=a.get('payload',{});ident.append({k:p[k] for k in ['model','effort','cli_version','originator'] if k in p})
prov['session_identifiers']=ident
for name in ['ai_provenance.json','app_build.json']:
 p=R/'reports/compatibility_null_validation/controls_projection_power'/name
 if p.exists():prov['historical_'+name]=json.loads(p.read_text())
(O/'provenance.json').write_text(json.dumps(prov,indent=2));(O/'checks.json').write_text(json.dumps(dict(protocol=lock,groups=len(CACHE),fits=sum(len(g['fits']) for g,sc in CACHE),test_distinct_engines=707,unchanged_input_files=len(inputs),calibrator_failures=sum(f['status']!='ok' for f in FITS),missing=missing,all_exploratory=True,independent_human_review='MISSING'),indent=2))
print('DONE',len(CACHE),len(A),len(E),flush=True)

"""Prospectively locked frozen-prediction association analysis. No training."""
import os
os.environ['OPENBLAS_NUM_THREADS']='4'
os.environ['OMP_NUM_THREADS']='4'
from pathlib import Path
import sys,json,csv,hashlib,datetime
import numpy as np
from scipy.special import expit
import collect_compatibility_synthetic as c
m=c.m
O=m.OUT/'association'; B=2000
LOCK=json.loads((O/'protocol_lock.json').read_text(encoding='utf-8-sig'))
assert hashlib.sha256((O/'protocol.md').read_bytes()).hexdigest()==LOCK['protocol_sha256']
ROWS=[]; PER=[]; BINS=[]; NEAR=[]; DRAWS={}; CHECK=[]
addlock=json.loads((O/'numerical_addendum_lock.json').read_text(encoding='utf-8-sig'))
assert m.sha(O/'numerical_addendum.md')==addlock['sha256']
def save(name,rows):
    if not rows:return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (O/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def weights(sub,policy,n):
    seed=2026110103+1000*m.SUBS.index(sub)+100*(policy=='uniform')+(n==10000)
    return np.random.default_rng(seed).multinomial(n,np.full(n,1/n),size=B).astype(float)/n
def interval(x):
    ok=np.isfinite(x);return (*np.quantile(x[ok],[.025,.975]),int((~ok).sum())) if ok.any() else (np.nan,np.nan,B)
def emit(base,metric,point,draw,**kw):
    lo,hi,bad=interval(draw);r=dict(**base,metric=metric,effect=float(point),ci_low=float(lo),ci_high=float(hi),undefined_draws=bad,**kw);ROWS.append(r);return r
def poly(x):return np.stack([x,x*x,x*x*x],axis=-1)
def counts(flag):
    return dict(incompatible_engines=int(flag.any(0).sum()),compatible_engines=int((~flag).any(0).sum()),incompatible_engine_runs=int(flag.sum()),compatible_engine_runs=int((~flag).sum()))
def solve(cov,ix,yix):
    a=cov[...,ix,:][...,ix];b=cov[...,ix,:][...,yix]
    pinv=np.linalg.pinv(a,rcond=1e-10,hermitian=True)
    null=np.eye(len(ix))-pinv@a
    valid=np.linalg.norm(null[:,0,:],axis=1)<1e-6
    rank=np.linalg.matrix_rank(a,rtol=1e-10)
    CHECK.append(dict(columns=len(ix),point_rank=int(rank[0]),target_identifiable=bool(valid[0]),undefined_bootstrap_draws=int((~valid[1:]).sum()),point_target_null_row_norm=float(np.linalg.norm(null[0,0,:]))))
    ans=np.full((len(cov),len(ix),len(yix)),np.nan)
    if valid.any():ans[valid]=pinv[valid]@b[valid]
    return ans
def analyze(base,q,p,truth,oracleq=None,oraclep=None,extra=False):
    # Arrays: fixed states x shared engine IDs. State intercepts are eliminated
    # anew within each bootstrap, so state predictions are never independent units.
    r,n=p.shape;d=np.stack([m.diagnostic(a,b) for a,b in zip(q,p)]);flag=d>0
    assert np.isfinite(q).all() and np.isfinite(p).all()
    if oraclep is None:
        y=np.minimum(truth,125.);label=y<=30
        out=np.stack([(q[:,:,1]-y)**2,(p-label)**2],axis=-1);names=['median_squared_error','Brier']
        cov=poly(y/125.)
    else:
        out=np.stack([(p-oraclep)**2,abs(q-oracleq).mean(-1),abs(p-oraclep),((q-oracleq)**2).mean(-1)],axis=-1)
        names=['oracle_probability_squared_deviation','oracle_quantile_MAE','oracle_probability_absolute_deviation','oracle_quantile_MSE']
        cov=np.concatenate([poly(oracleq[:,1]/125.),poly(oraclep)],axis=-1)
    w=weights(base['subset'],base['policy'],n);wa=np.vstack([np.full(n,1/n),w]);cc=counts(flag);base=dict(**base,fits=r,**cc)
    # Raw group means and differences, engine-cluster bootstrapped.
    den=np.stack([flag.mean(0),(~flag).mean(0)],axis=-1);denb=wa@den
    for j,name in enumerate(names):
        num=np.stack([(out[:,:,j]*flag).mean(0),(out[:,:,j]*(~flag)).mean(0)],axis=-1)
        with np.errstate(divide='ignore',invalid='ignore'):means=(wa@num)/denb
        for k,group in enumerate(['incompatible','compatible']):emit(base,name+'_mean_'+group,means[0,k],means[1:,k])
        emit(base,name+'_unadjusted_difference',means[0,0]-means[0,1],means[1:,0]-means[1:,1])
        for rep in range(r):
            a=flag[rep];PER.append(dict(**{k:v for k,v in base.items() if k not in cc},replication=rep,metric=name,incompatible_engines=int(a.sum()),compatible_engines=int((~a).sum()),incompatible_mean=float(out[rep,a,j].mean()) if a.any() else np.nan,compatible_mean=float(out[rep,~a,j].mean()) if (~a).any() else np.nan))
    z=np.concatenate([flag[:,:,None].astype(float),d[:,:,None]/.1,np.broadcast_to(cov,(r,n,cov.shape[-1])),out],axis=-1);k=z.shape[-1];nc=cov.shape[-1];ys=list(range(2+nc,k))
    # Pooled per-engine second moments and each state's first moments suffice
    # for exact weighted within-state least squares in every resample.
    second=np.einsum('rni,rnj->nij',z,z)/r
    sums=(wa@second.reshape(n,-1)).reshape(B+1,k,k)
    variable=[0,1]+ys
    variable_data=z[:,:,variable].transpose(1,0,2).reshape(n,-1)
    common=wa@cov
    for start in range(0,B+1,100):
        ww=wa[start:start+100];means=np.empty((len(ww),r,k))
        means[:,:,variable]=(ww@variable_data).reshape(-1,r,len(variable))
        means[:,:,2:2+nc]=common[start:start+100,None,:]
        sums[start:start+100]-=np.einsum('bri,brj->bij',means,means)/r
    for pred,ix in [('flag',[0]+list(range(2,2+nc))),('distance_per_0.1',[1]+list(range(2,2+nc)))]:
        beta=solve(sums,ix,ys)
        for j,name in enumerate(names):
            rr=emit(base,name+'_adjusted_'+pred,beta[0,0,j],beta[1:,0,j]);DRAWS[tuple(base.get(k) for k in ['family','subset','architecture','variant','policy','evaluation_engines'])+(name,pred)]=beta[1:,0,j]
        # Direct least squares check on a single point calculation.
        xx=z[:,:,ix];yy=z[:,:,ys];xx=xx-xx.mean(1,keepdims=True);yy=yy-yy.mean(1,keepdims=True)
        direct=np.linalg.lstsq(xx.reshape(-1,len(ix)),yy.reshape(-1,len(ys)),rcond=1e-5)[0]
        if np.isfinite(beta[0]).all():np.testing.assert_allclose(beta[0,0],direct[0],rtol=1e-4,atol=1e-5)
    if extra:real_extra(base,q,p,y,out,flag,d,wa)
    return d

def real_extra(base,q,p,y,out,flag,d,wa):
    r,n=p.shape;bins=np.select([y<20,y<=40,y<=60,y<=80,y<=100],[0,1,2,3,4],default=5);labels=['[0,20)','[20,40]','(40,60]','(60,80]','(80,100]','(100,125]']
    diffs=[];mass=[];validbins=[]
    for b in range(6):
        mask=bins==b;f=flag[:,mask];cnt=counts(f);row=dict(**{k:v for k,v in base.items() if k not in cnt},RUL_bin=labels[b],bin_engines=int(mask.sum()),**cnt)
        den=np.stack([(flag*mask).mean(0),((~flag)*mask).mean(0)],axis=-1);db=wa@den
        effect=[]
        for j,name in enumerate(['median_squared_error','Brier']):
            num=np.stack([(out[:,:,j]*flag*mask).mean(0),(out[:,:,j]*(~flag)*mask).mean(0)],axis=-1)
            with np.errstate(divide='ignore',invalid='ignore'):mu=(wa@num)/db
            diff=mu[:,0]-mu[:,1];lo,hi,bad=interval(diff[1:]);row.update({name+'_difference':diff[0],name+'_lo':lo,name+'_hi':hi,name+'_undefined_draws':bad});effect.append(diff)
        BINS.append(row)
        if np.all(db[0]>0):validbins.append(b);mass.append(mask.mean());diffs.append(np.array(effect).T)
    if mass:
        val=np.einsum('b,bkj->kj',np.array(mass)/sum(mass),np.array(diffs))
        for j,name in enumerate(['median_squared_error','Brier']):emit(base,name+'_RUL_bin_standardized_difference',val[0,j],val[1:,j],retained_engines=int(np.isin(bins,validbins).sum()),excluded_bins=';'.join(labels[b] for b in range(6) if b not in validbins))
    near=(y>=20)&(y<=40);vals=[]
    for mask,label in [(near,'20_to_40'),(~near,'elsewhere')]:
        den=wa@mask.astype(float)
        for field,arr in [('rate',flag),('distance',d)]:
            with np.errstate(divide='ignore',invalid='ignore'):v=(wa@(arr.mean(0)*mask))/den
            emit(base,'near_threshold_'+field+'_'+label,v[0],v[1:],band_engines=int(mask.sum()));
            if field=='rate':vals.append(v)
    emit(base,'near_threshold_rate_difference',vals[0][0]-vals[1][0],vals[0][1:]-vals[1][1:])
    # Incremental probability-adjusted regression, state-centered moments.
    z=np.concatenate([d[:,:,None]/.1,poly(p),np.broadcast_to(poly(y/125.),(r,n,3)),out[:,:,1,None]],axis=-1);k=8
    sec=np.einsum('rni,rnj->nij',z,z)/r;s=(wa@sec.reshape(n,-1)).reshape(B+1,k,k)
    means=(wa@z.transpose(1,0,2).reshape(n,-1)).reshape(B+1,r,k);s-=np.einsum('bri,brj->bij',means,means)/r
    a=solve(s,list(range(7)),[7]);b=solve(s,list(range(1,7)),[7]);emit(base,'Brier_distance_beyond_raw_p_per_0.1',a[0,0,0],a[1:,0,0])
    # Use total outcome variance (including state offsets) as R2 denominator.
    total=wa@(out[:,:,1]**2).mean(0)-(wa@out[:,:,1].mean(0))**2
    full=np.einsum('bi,bi->b',a[:,:,0],s[:,:7,7]);reduced=np.einsum('bi,bi->b',b[:,:,0],s[:,1:7,7]);delta=(full-reduced)/total
    emit(base,'Brier_incremental_in_sample_R_squared',delta[0],delta[1:])

def real():
    engine_rows=[];gate=json.loads((m.OUT/'reproduction_gate.json').read_text())
    for sub in m.SUBS:
      for arch in ['lstm','hybrid']:
        qs=[];ps=[];ys=[];ids=None
        for seed in [1101,1202,1303,1404,1505]:
            path=m.ROOT/f'results/fair_comparison_step2/final/{sub}/{arch}/seed_{seed}/test_predictions.csv'
            with path.open() as f:rows=list(csv.DictReader(f))
            ii=np.array([int(a['engine_id']) for a in rows]);y=np.minimum([float(a['raw_y']) for a in rows],125.);q=np.array([[float(a[k]) for k in ['q05','q50','q95']] for a in rows]);p=expit([float(a['logit']) for a in rows])
            np.testing.assert_allclose(p,[float(a['p_Raw']) for a in rows],atol=1e-12,rtol=1e-12)
            if ids is not None:np.testing.assert_array_equal(ii,ids);np.testing.assert_array_equal(y,ys[0])
            ids=ii;qs.append(q);ps.append(p);ys.append(y);d=m.diagnostic(q,p)
            for i in range(len(y)):engine_rows.append(dict(subset=sub,architecture=arch,seed=seed,engine_id=int(ii[i]),evaluation_engines=len(y),fitting_engines=m.CFG['fit_counts'][sub],true_capped_RUL=y[i],event_label=int(y[i]<=30),p_raw=p[i],q05=q[i,0],q50=q[i,1],q95=q[i,2],incompatible=int(d[i]>0),distance=d[i],median_squared_error=(q[i,1]-y[i])**2,Brier=(p[i]-(y[i]<=30))**2))
        base=dict(family='real',subset=sub,architecture=arch,variant='weighted_raw',policy='final',evaluation_engines=len(ids),fitting_engines=m.CFG['fit_counts'][sub]);d=analyze(base,np.array(qs),np.array(ps),ys[0],extra=True)
        old=next(g for g in gate['summary'] if g['subset']==sub and g['model']==('LSTM' if arch=='lstm' else 'Hybrid'))
        np.testing.assert_allclose((d>0).mean()*100,old['recomputed_mean'],atol=1e-9);print('REAL',sub,arch,flush=True)
    save('real_engine_run.csv',engine_rows);save('real_associations.csv',ROWS);save('real_RUL_bins.csv',BINS);save('real_per_seed.csv',PER)

def synthetic():
    for sub in m.SUBS:
      for family,arch in [('temporal','lstm'),('temporal','hybrid'),('covariate','covariate')]:
       for policy in ['final','uniform']:
        groups=c.load_group(family,sub,arch,policy)
        with np.load(m.RUN/f'evaluation_{sub}_{policy}.npz') as ev:qt=ev['q_true'];pt=ev['p_true'];ids=ev['engine_id'];np.testing.assert_array_equal(ids,np.arange(10000))
        for variant,outputs in groups.items():
         q=np.array([a for a,b in outputs]);p=np.array([b for a,b in outputs])
         path=O/'engine_arrays'/f'{family}_{sub}_{arch}_{policy}_{variant}.npz';path.parent.mkdir(exist_ok=True)
         if not path.exists():np.savez_compressed(path,q=q,p=p,q_oracle=qt,p_oracle=pt,engine_id=ids,source='original frozen synthetic predictions and known-law evaluation arrays')
         for n in [m.CFG['small_eval_counts'][sub],10000]:
            base=dict(family=family,subset=sub,architecture=arch,variant=variant,policy=policy,evaluation_engines=n,fitting_engines=m.CFG['fit_counts'][sub],shared_FD001_control_states=sub=='FD003' and family=='covariate')
            analyze(base,q[:,:n],p[:,:n],None,qt[:n],pt[:n])
         print('SYNTHETIC',family,sub,arch,policy,variant,flush=True)
        save('synthetic_associations.csv',[a for a in ROWS if a['family']!='real']);save('synthetic_per_fit.csv',[a for a in PER if a['family']!='real'])

def report():
    familyrows=[];syntheticpass=True
    for family in ['temporal','covariate']:
      for outcome in ['oracle_probability_squared_deviation','oracle_quantile_MAE']:
       for pred in ['flag','distance_per_0.1']:
        keys=[k for k in DRAWS if k[0]==family and k[3:6]==('weighted_raw','final',10000) and k[6:]==(outcome,pred)]
        draws=np.mean([DRAWS[k] for k in keys],axis=0)
        pts=[r['effect'] for r in ROWS if r['family']==family and r['variant']=='weighted_raw' and r['policy']=='final' and r['evaluation_engines']==10000 and r['metric']==outcome+'_adjusted_'+pred]
        lo,hi,bad=interval(draws);passed=bool(lo>0 and np.isfinite(pts).all());syntheticpass &= passed
        familyrows.append(dict(family=family,outcome=outcome,predictor=pred,effect=float(np.mean(pts)),ci_low=lo,ci_high=hi,undefined_draws=bad,settings=len(keys),evaluation_engines_per_subset=10000,unique_evaluation_engines=40000,fitting_engines='60/156/60/149',passes=passed))
    save('synthetic_family_confirmation.csv',familyrows)
    groups=[]
    for sub in m.SUBS:
     for arch in ['lstm','hybrid']:
      rr=[r for r in ROWS if r['family']=='real' and r['subset']==sub and r['architecture']==arch and r['metric'] in ['median_squared_error_adjusted_flag','Brier_adjusted_flag']]
      groups.append(dict(subset=sub,architecture=arch,evaluation_engines=m.CFG['small_eval_counts'][sub],fitting_engines=m.CFG['fit_counts'][sub],both_outcomes_pass=len(rr)==2 and all(r['ci_low']>0 for r in rr)))
    save('real_decision_components.csv',groups);count=sum(r['both_outcomes_pass'] for r in groups);decision='diagnostic is informative' if count>=6 and syntheticpass else 'not informative'
    (O/'decision.json').write_text(json.dumps(dict(decision=decision,real_groups_both_positive=count,required=6,synthetic_confirmation=syntheticpass,protocol=LOCK),indent=2))
    text=f'# Frozen-model incompatibility association analysis\n\nVerdict under the locked joint rule: **{decision}**. {count}/8 real groups pass both RUL-adjusted outcomes; synthetic joint confirmation={syntheticpass}.\n\nProtocol SHA256 `{LOCK["protocol_sha256"]}`. All results use 2,000 engine-cluster bootstrap draws, preserving fixed states/seeds. Real evaluation: 707 unique engines across subsets; each architecture uses the same engines. Synthetic: 10,000 unique engines per subset/policy, reused across states; small fleets are prefixes. Engine-group counts overlap when a fixed engine changes flag across states.\n\nThe temporal experiment includes approximation and optimization effects. Conditional bootstrap intervals exclude fitting uncertainty. Brier is determined by probability and event label; probability-adjusted residual associations depend on the fixed cubic regression specification and are not held-out predictive gains. No models were trained or selected.\n\nTables: real_associations.csv (all effects, means, intervals and counts), real_engine_run.csv, real_RUL_bins.csv (all bins including empty), real_per_seed.csv, synthetic_associations.csv, synthetic_per_fit.csv, synthetic_family_confirmation.csv, real_decision_components.csv. Undefined/singular results are NA/NaN with undefined-draw counts, never silently removed from decision components.\n'
    (O/'report.md').write_text(text,encoding='utf-8')
    print('DECISION',decision,count,syntheticpass,flush=True)
if __name__=='__main__':
    real();synthetic();report();save('all_associations.csv',ROWS)
    save('regression_rank_diagnostics.csv',[dict(regression_call=i,**row) for i,row in enumerate(CHECK)])
    np.savez_compressed(O/'bootstrap_effects.npz',**{'key_'+str(i):v for i,v in enumerate(DRAWS.values())})
    (O/'bootstrap_keys.json').write_text(json.dumps([list(k) for k in DRAWS],indent=2))
    (O/'complete.json').write_text(json.dumps(dict(status='COMPLETE',protocol=LOCK,rows=len(ROWS),per_fit_rows=len(PER),source_sha256=m.sha(__file__),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))

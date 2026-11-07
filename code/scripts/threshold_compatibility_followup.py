"""Read-only frozen-prediction follow-up, writes exclusively to new output folder."""
import os
os.environ['OPENBLAS_NUM_THREADS']='4'
from pathlib import Path
import csv,json,hashlib,datetime
import numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'reports/compatibility_null_validation';A=BASE/'association';O=BASE/'threshold_followup';SUBS=['FD001','FD002','FD003','FD004'];NS=[100,259,100,248];FIT=[60,156,60,149]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def save(name,rows):
    with (O/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
lock=json.loads((O/'protocol_lock.json').read_text(encoding='utf-8-sig'));assert sha(O/'protocol.md')==lock['protocol_sha256']
old=[p for p in BASE.rglob('*') if p.is_file() and O not in p.parents]
hashes={p.relative_to(ROOT).as_posix():sha(p) for p in old};(O/'earlier_files_before.json').write_text(json.dumps(hashes,indent=2))
protocol=(A/'protocol.md').read_text(encoding='utf-8');rule=protocol.split('## Locked decision rule\n\n')[1].split('\n## Real cohort')[0]
add=(A/'numerical_addendum.md').read_text(encoding='utf-8');para=add.split('\n\n')[2]
step0='# Step 0 consistency check (existing files only)\n\nLocked rule, verbatim:\n\n> '+rule+'\n\nNumerical addendum, verbatim:\n\n> '+para+'\n\n| Component | Existing result | Engines |\n|---|---|---|\n| Real median error positive, CI excludes zero | 0/8 | 100/259/100/248 per subset |\n| Real Brier positive, CI excludes zero | 6/8 | Same engines |\n| Real both outcomes in same groups | 0/8, requires >=6/8 | 707 unique |\n| Temporal synthetic required coefficients | 4/4 pass | 10,000/subset |\n| Covariate synthetic required coefficients | 1/4 pass | 10,000/subset |\n\nLevel reached: **not informative**. No partially informative level is defined. Earlier verdict agrees; no verdict discrepancy. Both original locks verified.\n'
for file,key,locked in [('protocol.md','protocol_sha256','protocol_lock.json'),('numerical_addendum.md','sha256','numerical_addendum_lock.json')]:assert sha(A/file)==json.loads((A/locked).read_text(encoding='utf-8-sig'))[key]
(O/'step0_consistency.md').write_text(step0,encoding='utf-8')
def weights(si,policy,n):
    seed=2026110103+1000*si+100*(policy=='uniform')+(n==10000)
    return np.vstack([np.full(n,1/n),np.random.default_rng(seed).multinomial(n,np.full(n,1/n),size=2000)/n])
def ci(v):
    ok=np.isfinite(v);return (*np.quantile(v[ok],[.025,.975]),int((~ok).sum())) if ok.any() else (np.nan,np.nan,2000)
def poly(x):return np.stack([x,x*x,x*x*x],axis=-1)
def diagnostic(q,p):
    levels=np.array([.05,.5,.95]);l=np.where(q<=30,levels,0).max(-1);u=np.where(q>30,levels,1).min(-1)
    return np.maximum.reduce([l-p,p-u,np.zeros_like(p)])
rows=read(A/'real_engine_run.csv');original=read(A/'real_associations.csv');results=[]
for si,sub in enumerate(SUBS):
 for arch in ['lstm','hybrid']:
    group=[r for r in rows if r['subset']==sub and r['architecture']==arch];seeds=sorted({int(r['seed']) for r in group});states=[];ids=None
    for seed in seeds:
        rr=[r for r in group if int(r['seed'])==seed];ii=np.array([int(r['engine_id']) for r in rr]);y=np.array([float(r['true_capped_RUL']) for r in rr]);p=np.array([float(r['p_raw']) for r in rr]);flag=np.array([int(r['incompatible']) for r in rr]);brier=np.array([float(r['Brier']) for r in rr]);q=np.array([[float(r[k]) for k in ['q05','q50','q95']] for r in rr])
        np.testing.assert_array_equal(diagnostic(q,p)>0,flag);np.testing.assert_allclose(brier,(p-(y<=30))**2)
        if ids is not None:np.testing.assert_array_equal(ids,ii);np.testing.assert_array_equal(y,oldy)
        ids=ii;oldy=y;band=((y>=20)&(y<=40));states.append(np.concatenate([flag[:,None],poly(p),poly(y/125),band[:,None],brier[:,None]],axis=1))
    z=np.array(states);r,n,k=z.shape;w=weights(si,'final',n);f=z[:,:,0].astype(bool);cov=(w@np.einsum('rni,rnj->nij',z,z).reshape(n,-1)/r).reshape(2001,k,k);mu=(w@z.transpose(1,0,2).reshape(n,-1)).reshape(2001,r,k);cov-=np.einsum('bri,brj->bij',mu,mu)/r
    a=cov[:,:8,:8];b=cov[:,:8,8];pinv=np.linalg.pinv(a,rcond=1e-10,hermitian=True);null=np.eye(8)-pinv@a;valid=np.linalg.norm(null[:,0,:],axis=1)<1e-6;beta=np.einsum('bij,bj->bi',pinv,b);effect=beta[:,0];effect[~valid]=np.nan
    centered=z-z.mean(1,keepdims=True);direct=np.linalg.lstsq(centered[:,:,:8].reshape(-1,8),centered[:,:,8].ravel(),rcond=1e-5)[0][0]
    if valid[0]:np.testing.assert_allclose(effect[0],direct,rtol=1e-4,atol=1e-6)
    lo,hi,bad=ci(effect[1:]);oldrate=next(x for x in original if x['subset']==sub and x['architecture']==arch and x['metric']=='near_threshold_rate_20_to_40');np.testing.assert_allclose(f[:,band].mean(),float(oldrate['effect']))
    results.append(dict(subset=sub,architecture=arch,fitting_engines=FIT[si],evaluation_engines=n,fits=r,band_engines=int(band.sum()),elsewhere_engines=int((~band).sum()),incompatible_engines=int(f.any(0).sum()),compatible_engines=int((~f).any(0).sum()),incompatible_engine_runs=int(f.sum()),compatible_engine_runs=int((~f).sum()),Brier_flag_coefficient=effect[0],ci_low=lo,ci_high=hi,undefined_bootstrap_draws=bad,point_design_rank=int(np.linalg.matrix_rank(a[0],rtol=1e-10)),point_target_identifiable=bool(valid[0]),passes=bool(effect[0]>0 and lo>0)))
save('real_Brier_adjusted.csv',results);print('REAL COMPLETE',flush=True)
syn=[];prior=read(A/'synthetic_associations.csv')
for si,sub in enumerate(SUBS):
 for family,arch in [('temporal','lstm'),('temporal','hybrid'),('covariate','covariate')]:
  for policy in ['final','uniform']:
    with np.load(BASE/f'synthetic/evaluation_{sub}_{policy}.npz') as ev:y=np.minimum(ev['y'],125);ids=ev['engine_id']
    for variant in ['weighted_raw','weighted_corrected','unweighted']:
      with np.load(A/f'engine_arrays/{family}_{sub}_{arch}_{policy}_{variant}.npz') as pred:q=pred['q'];p=pred['p'];np.testing.assert_array_equal(ids,pred['engine_id'])
      assert np.isfinite(q).all() and np.isfinite(p).all();flag=diagnostic(q,p)>0;r=flag.shape[0]
      for n in [NS[si],10000]:
        band=(y[:n]>=20)&(y[:n]<=40);f=flag[:,:n];w=weights(si,policy,n);base=dict(family=family,subset=sub,architecture=arch,policy=policy,variant=variant,fitting_engines=FIT[si],evaluation_engines=n,fits=r,shared_FD001_fitted_states=family=='covariate' and sub=='FD003',band_engines=int(band.sum()),elsewhere_engines=int((~band).sum()),band_incompatible_engine_runs=int(f[:,band].sum()),band_compatible_engine_runs=int((~f[:,band]).sum()),elsewhere_incompatible_engine_runs=int(f[:,~band].sum()),elsewhere_compatible_engine_runs=int((~f[:,~band]).sum()))
        reference=next(x for x in prior if x['family']==family and x['subset']==sub and x['architecture']==arch and x['policy']==policy and x['variant']==variant and int(x['evaluation_engines'])==n)
        assert f.sum()==int(reference['incompatible_engine_runs'])
        vs=[]
        for mask in [band,~band]:
            den=w@mask.astype(float)
            with np.errstate(divide='ignore',invalid='ignore'):v=(w@(f.mean(0)*mask))/den
            vs.append(v)
        for metric,v in [('band_rate',vs[0]),('elsewhere_rate',vs[1]),('band_minus_elsewhere',vs[0]-vs[1])]:
            lo,hi,bad=ci(v[1:]);syn.append(dict(**base,metric=metric,effect=v[0],ci_low=lo,ci_high=hi,undefined_bootstrap_draws=bad))
    print('SYNTHETIC',sub,family,arch,policy,flush=True)
save('synthetic_band_rates.csv',syn);assert len(syn)==432 and len(results)==8
passing=sum(r['passes'] for r in results);verdict='not explained by threshold proximity' if passing>=6 else 'explained by or confounded with threshold proximity'
report='# Threshold-proximity follow-up\n\n'+step0+'\n## New analysis\n\nProtocol SHA256 `'+lock['protocol_sha256']+'`. All predictions were already saved. No training or changes to earlier files.\n\nQuestion A operational verdict: **'+verdict+'** ('+str(passing)+'/8 groups positive with 95% CI excluding zero; requires >=6/8). Adjustment includes cubic raw probability, inclusive RUL 20–40 band, original cubic capped RUL, and seed intercepts. This label does not establish a causal explanation.\n\n| Subset | Model | Fit/test engines | Band/elsewhere engines | Flag effect [95% CI] |\n|---|---|---|---|---|\n'
for r in results:report+=f'| {r["subset"]} | {r["architecture"]} | {r["fitting_engines"]}/{r["evaluation_engines"]} | {r["band_engines"]}/{r["elsewhere_engines"]} | {r["Brier_flag_coefficient"]:.6f} [{r["ci_low"]:.6f}, {r["ci_high"]:.6f}] |\n'
report+='\nQuestion B: synthetic_band_rates.csv reports all 144 settings, each with both rates and their difference (432 rows). Rates are fractions. Band membership uses realized capped RUL, never oracle median. Evaluation counts and engine/run counts accompany every row; state counts do not add independent engines. Empty-band/draw estimates remain NA. Bootstrap intervals condition on saved fits; 2,000 engine draws preserve all states per engine. FD003 covariate states shared with FD001 are identified. All unfavorable results are retained.\n\nIndependent human review is still missing. AI identifiers and command/source provenance are archived alongside this report. No new overall diagnostic-informativeness verdict replaces Step 0.\n'
(O/'report.md').write_text(report,encoding='utf-8')
after={p.relative_to(ROOT).as_posix():sha(p) for p in old};assert after==hashes,'Earlier file changed'
(O/'checks.json').write_text(json.dumps(dict(status='PASS',earlier_files_checked=len(old),earlier_files_unchanged=True,real_groups=8,synthetic_settings=144,synthetic_rows=432,all_raw_flags_and_rates_crosschecked=True,direct_lstsq_checks_passed=True,protocol_hash_verified=True,passing_real_groups=passing,verdict=verdict),indent=2))
# Archive available local AI identity records and exact execution/edit inputs.
calls=[];ident=[]
for path in (Path(os.environ['USERPROFILE'])/'.codex/sessions').rglob('*'+os.environ['CODEX_SESSION_ID']+'*.jsonl'):
 for line in path.open(encoding='utf-8'):
    try:entry=json.loads(line)
    except json.JSONDecodeError:continue
    item=entry.get('payload',{})
    if entry.get('type')=='turn_context':ident.append(dict(timestamp=entry.get('timestamp'),model=item.get('model'),effort=item.get('effort')))
    if entry.get('type')=='session_meta':ident.append(dict(timestamp=entry.get('timestamp'),runtime_version=item.get('cli_version'),originator=item.get('originator')))
    if entry.get('type')=='response_item' and item.get('type') in ['function_call','custom_tool_call'] and item.get('name','').split('.')[-1] in ['exec','apply_patch','exec_command']:calls.append(dict(timestamp=entry.get('timestamp'),name=item.get('name'),call_id=item.get('call_id'),arguments=item.get('arguments'),input=item.get('input')))
with (O/'exact_tool_calls.jsonl').open('w',encoding='utf-8') as f:
 for row in calls:f.write(json.dumps(row,ensure_ascii=False)+'\n')
(O/'ai_provenance.json').write_text(json.dumps(dict(tool='Codex desktop',available_session_identifiers=ident,exact_served_model_checkpoint='UNAVAILABLE',independent_human_review='MISSING'),indent=2))
files=[p for p in O.rglob('*') if p.is_file() and p.name not in ['manifest.json','run.log']]+[Path(__file__)]
(O/'manifest.json').write_text(json.dumps(dict(protocol=lock,files={str(p.relative_to(ROOT).as_posix()):sha(p) for p in files}),indent=2))
print(json.dumps(dict(status='PASS',passing=passing,verdict=verdict,earlier_files_unchanged=len(old))),flush=True)

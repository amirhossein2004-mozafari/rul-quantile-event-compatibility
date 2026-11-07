"""Locked read-only summaries from saved rates and prediction arrays."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import csv,json,hashlib,datetime,shutil
import numpy as np
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parents[1];V=ROOT/'reports/compatibility_null_validation';O=V/'difficulty_check';SUBS=['FD001','FD002','FD003','FD004'];SEEDS=[1101,1202,1303,1404,1505]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
inputs={}
def track(p):inputs[str(p.relative_to(ROOT).as_posix())]=sha(p);return p
def read(p):
    with track(p).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def save(name,rows):
    with (O/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
lock=json.loads((O/'protocol_lock.json').read_text(encoding='utf-8-sig'));assert sha(O/'protocol.md')==lock['protocol_sha256']
per=read(V/'followup/null_per_replication.csv');prior=read(V/'followup/null_stratified_summary.csv');labels=read(V/'followup/null_collapse_labels.csv');realprior=read(V/'followup/real_variant_summary.csv')
distribution=[];difficulty=[];summary=[]
def diag(q,p):
    levels=np.array([.05,.5,.95]);lo=np.where(q<=30,levels,0).max(-1);hi=np.where(q>30,levels,1).min(-1)
    return np.maximum.reduce([lo-p,p-hi,np.zeros_like(p)])
def metric(q,p,y,base,identifier):
    truth=np.minimum(y,125);event=truth<=30
    return dict(**base,fit_identifier=identifier,RMSE_capped=float(np.sqrt(np.mean((np.clip(q[:,1],0,125)-truth)**2))),event_AUC=float(roc_auc_score(event,p)) if np.unique(event).size==2 else np.nan,event_base_rate=float(event.mean()),median_q95_minus_q05_width=float(np.median(q[:,2]-q[:,0])))
for si,sub in enumerate(SUBS):
    evpath=track(V/f'synthetic/evaluation_{sub}_final.npz')
    with np.load(evpath) as ev:y=ev['y'];ids=ev['engine_id'];np.testing.assert_array_equal(ids,np.arange(10000))
    for arch in ['lstm','hybrid']:
        chosen=[r for r in per if r['family']=='temporal' and r['subset']==sub and r['architecture']==arch and r['policy']=='final' and r['variant']=='weighted_raw' and r['evaluation_engines']=='10000' and r['collapsed']=='False']
        repids=[int(r['replication']) for r in chosen];rates=np.array([float(r['incompatibility_rate']) for r in chosen]);assert len(rates)>0
        quant=np.quantile(rates,[0,.025,.25,.5,.75,.975,1],method='linear')
        old=next(r for r in prior if r['family']=='temporal' and r['subset']==sub and r['architecture']==arch and r['policy']=='final' and r['variant']=='weighted_raw' and r['evaluation_engines']=='10000' and r['stratum']=='noncollapsed')
        np.testing.assert_allclose(quant[[0,1,5,6]],[float(old[k]) for k in ['training_rate_min','training_rate_p025','training_rate_p975','training_rate_max']],atol=1e-14,rtol=1e-14)
        rr=next(r for r in realprior if r['subset']==sub and r['architecture']==arch and r['variant']=='weighted_raw');realrate=float(rr['rate']);location='below' if realrate<quant[1] else ('above' if realrate>quant[5] else 'inside')
        common=dict(subset=sub,architecture=arch,fitting_engines=int(rr['fitting_engines']),synthetic_evaluation_engines=10000,real_evaluation_engines=int(rr['evaluation_engines']),noncollapsed_synthetic_fits=len(rates),real_fits=5)
        distribution.append(dict(**common,real_raw_rate=realrate,**dict(zip(['null_min','null_p025','null_p25','null_median','null_p75','null_p975','null_max'],map(float,quant))),real_location=location))
        path=track(V/f'association/engine_arrays/temporal_{sub}_{arch}_final_weighted_raw.npz')
        with np.load(path) as data:q=data['q'];p=data['p'];np.testing.assert_array_equal(data['engine_id'],ids)
        for r,rep in zip(chosen,repids):
            membership=next(t for t in labels if t['family']=='temporal' and t['subset']==sub and t['architecture']==arch and t['variant']=='weighted_raw' and t['replication']==str(rep));assert membership['collapsed']=='False'
            np.testing.assert_allclose((diag(q[rep],p[rep])>0).mean(),float(r['incompatibility_rate']),atol=1e-14,rtol=1e-14)
            difficulty.append(metric(q[rep],p[rep],y,dict(subset=sub,architecture=arch,cohort='synthetic_noncollapsed',fitting_engines=common['fitting_engines'],evaluation_engines=10000),rep))
        realrates=[];realids=None
        for seed in SEEDS:
            frame=read(ROOT/f'results/fair_comparison_step2/final/{sub}/{arch}/seed_{seed}/test_predictions.csv');ii=np.array([int(r['engine_id']) for r in frame]);ry=np.array([float(r['raw_y']) for r in frame]);rq=np.array([[float(r[k]) for k in ['q05','q50','q95']] for r in frame]);rp=np.array([float(r['p_Raw']) for r in frame])
            if realids is not None:np.testing.assert_array_equal(realids,ii);np.testing.assert_array_equal(realtruth,ry)
            realids=ii;realtruth=ry;assert len(ii)==common['real_evaluation_engines'];realrates.append((diag(rq,rp)>0).mean())
            difficulty.append(metric(rq,rp,ry,dict(subset=sub,architecture=arch,cohort='real',fitting_engines=common['fitting_engines'],evaluation_engines=len(ii)),seed))
        np.testing.assert_allclose(np.mean(realrates),realrate,atol=1e-14,rtol=1e-14)
        for cohort in ['synthetic_noncollapsed','real']:
            selected=[r for r in difficulty if r['subset']==sub and r['architecture']==arch and r['cohort']==cohort]
            summary.append(dict(subset=sub,architecture=arch,cohort=cohort,fitting_engines=common['fitting_engines'],evaluation_engines=selected[0]['evaluation_engines'],fixed_fits=len(selected),mean_RMSE_capped=float(np.mean([r['RMSE_capped'] for r in selected])),mean_event_AUC=float(np.mean([r['event_AUC'] for r in selected])),event_base_rate=selected[0]['event_base_rate'],mean_fit_median_width=float(np.mean([r['median_q95_minus_q05_width'] for r in selected]))))
    print('COMPLETE',sub,flush=True)
save('null_distribution.csv',distribution);save('difficulty_per_fit.csv',difficulty);save('difficulty_summary.csv',summary)
def markdown(rows,columns):
    def val(x):return f'{x:.6f}' if isinstance(x,(float,np.floating)) else str(x)
    return '| '+' | '.join(columns)+' |\n|'+ '|'.join(['---']*len(columns))+'|\n'+''.join('| '+' | '.join(val(r[c]) for c in columns)+' |\n' for r in rows)
report='# Read-only null distribution and difficulty tables\n\nProtocol SHA256: `'+lock['protocol_sha256']+'`. Rates are fractions. Display: six decimals; CSVs retain unrounded values.\n\n'+markdown(distribution,['subset','architecture','fitting_engines','synthetic_evaluation_engines','real_evaluation_engines','noncollapsed_synthetic_fits','real_raw_rate','null_min','null_p025','null_p25','null_median','null_p75','null_p975','null_max','real_location'])
for sub in SUBS:
    table=[r for r in summary if r['subset']==sub];save(f'difficulty_{sub}.csv',table);save(f'difficulty_per_fit_{sub}.csv',[r for r in difficulty if r['subset']==sub])
    report+='\n## '+sub+'\n\n'+markdown(table,['architecture','cohort','fitting_engines','evaluation_engines','fixed_fits','mean_RMSE_capped','mean_event_AUC','event_base_rate','mean_fit_median_width'])
# Facts transcribed from the generator, without executing its code.
source=track(ROOT/'scripts/validate_compatibility_synthetic.py');content=source.read_text(encoding='utf-8')
assert 'lifetimes=30+rng.exponential(60*np.exp(.5*xs))' in content
assert 'scale=60*np.exp(.5*x)' in content and "if policy=='final':" in content
design='''
## Synthetic law (generator record)

- Weibull shape: 1 (exponential excess lifetime).
- Covariate: x in {-1, +1}; scale(x) = 60 exp(0.5 x).
- Training and uniform-endpoint lifetime: T = 30 + Exponential(scale(x)).
- Final-window generator: age sampled from saved empirical truncation ages; RUL = Exponential(scale(x)); lifetime = age + RUL.
- Final-window conditional RUL law: depends on x/features; independent of age given x. For 0 <= u < 125, F(u | x,age) = 1 - exp(-u/scale(x)). Capping places the remaining probability mass at 125.
- Uniform-endpoint conditional RUL law: depends on age and x/features. For 0 <= u < 125, F(u | x,age) = 1 - E1((age-30+u)/scale(x)) / E1((age-30)/scale(x)). Capping places the remaining probability mass at 125.
- Features: the first channel is x, the second is observed time/125; remaining channels combine x, time/scale(x), and independent Gaussian noise. They are not generated directly from realized RUL.
- Source: scripts/validate_compatibility_synthetic.py, oracle, endpoints, features, training_data; reports/compatibility_null_validation/report.md (Weibull shape 1 record).

Difficulty rows are arithmetic means over fixed-fit metrics. Width column is a mean of each fit's median raw width. Per-fit values: difficulty_per_fit.csv and difficulty_per_fit_FD001–FD004.csv. No bootstrap, training or forward inference was run. Independent human review remains missing.
'''
track(V/'report.md');report+=design;(O/'report.md').write_text(report,encoding='utf-8');(O/'synthetic_design.md').write_text(design,encoding='utf-8')
for name,h in inputs.items():assert sha(ROOT/name)==h,name
shutil.copy2(V/'followup/ai_provenance.json',O/'ai_provenance.json');shutil.copy2(V/'followup/app_build.json',O/'app_build.json')
checks=dict(status='PASS',groups=len(distribution),difficulty_rows=len(difficulty),difficulty_summary_rows=len(summary),inputs_unchanged=len(inputs),protocol=lock,source_sha256=sha(Path(__file__)),training=False,inference=False)
(O/'checks.json').write_text(json.dumps(checks,indent=2))
(O/'manifest.json').write_text(json.dumps(dict(inputs=inputs,outputs={p.name:sha(p) for p in O.iterdir() if p.is_file() and p.name not in ['manifest.json','run.log']},checks=checks),indent=2))
calls=[]
for path in (Path(os.environ['USERPROFILE'])/'.codex/sessions').rglob('*'+os.environ['CODEX_SESSION_ID']+'*.jsonl'):
 for line in path.open(encoding='utf-8'):
    try:r=json.loads(line)
    except json.JSONDecodeError:continue
    p=r.get('payload',{})
    if r.get('type')=='response_item' and p.get('type') in ['function_call','custom_tool_call'] and p.get('name','').split('.')[-1] in ['exec','apply_patch','exec_command']:calls.append(dict(timestamp=r.get('timestamp'),name=p.get('name'),call_id=p.get('call_id'),arguments=p.get('arguments'),input=p.get('input')))
with (O/'exact_tool_calls.jsonl').open('w',encoding='utf-8') as f:
 for row in calls:f.write(json.dumps(row,ensure_ascii=False)+'\n')
print(json.dumps(checks),flush=True)

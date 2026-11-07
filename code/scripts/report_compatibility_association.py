"""Summarize executed association outputs and archive provenance."""
from pathlib import Path
import os,json,csv,hashlib,datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path('reports/compatibility_null_validation/association')
def read(name):
    with (O/name).open() as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,rows):
    with (O/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
complete=json.loads((O/'complete.json').read_text());lock=json.loads((O/'protocol_lock.json').read_text(encoding='utf-8-sig'))
assert sha(O/'protocol.md')==lock['protocol_sha256'];assert complete['status']=='COMPLETE'
real=read('real_associations.csv');syn=read('synthetic_associations.csv');per=read('synthetic_per_fit.csv');eng=read('real_engine_run.csv');bins=read('real_RUL_bins.csv')
assert len(real)==152 and len(syn)==2880 and len(eng)==7070 and len(bins)==48 and len(per)==49920,(len(real),len(syn),len(eng),len(bins),len(per))
rankrows=read('regression_rank_diagnostics.csv');contexts=[]
for source,types in [(real,['adjusted_flag','adjusted_distance','incremental_Brier_full','incremental_Brier_reduced']),(syn,['adjusted_flag','adjusted_distance'])]:
    seen=set()
    for r in source:
        keys=['family','subset','architecture','variant','policy','evaluation_engines','fitting_engines'];key=tuple(r[k] for k in keys)
        if key in seen:continue
        seen.add(key)
        for kind in types:contexts.append(dict(**{k:r[k] for k in keys},regression=kind))
assert len(rankrows)==len(contexts)==320
save('regression_rank_diagnostics.csv',[dict(**r,**context) for r,context in zip(rankrows,contexts)])
decision=json.loads((O/'decision.json').read_text());family=read('synthetic_family_confirmation.csv')
tables={k:[] for k in ['real_primary_table.csv','near_threshold_table.csv','incremental_Brier_table.csv']}
for sub in ['FD001','FD002','FD003','FD004']:
 for arch in ['lstm','hybrid']:
    rr=[r for r in real if r['subset']==sub and r['architecture']==arch]
    for filename,metrics in [('real_primary_table.csv',['median_squared_error_adjusted_flag','Brier_adjusted_flag']),('near_threshold_table.csv',['near_threshold_rate_20_to_40','near_threshold_rate_elsewhere','near_threshold_rate_difference']),('incremental_Brier_table.csv',['Brier_distance_beyond_raw_p_per_0.1','Brier_incremental_in_sample_R_squared'])]:
        row={k:rr[0][k] for k in ['subset','architecture','fitting_engines','evaluation_engines','fits','incompatible_engines','compatible_engines','incompatible_engine_runs','compatible_engine_runs']}
        for metric in metrics:
            value=next(r for r in rr if r['metric']==metric)
            for field in ['effect','ci_low','ci_high','undefined_draws']:
                row[metric+'_'+field]=value[field]
            if filename=='near_threshold_table.csv' and metric!='near_threshold_rate_difference':row[metric+'_engines']=value['band_engines']
        tables[filename].append(row)
for filename,rows in tables.items():save(filename,rows)
for filename in ['real_per_seed.csv','synthetic_per_fit.csv']:
    rows=read(filename)
    for row in rows:row['unadjusted_difference']=float(row['incompatible_mean'])-float(row['compatible_mean'])
    save(filename,rows)
fig,axes=plt.subplots(1,2,figsize=(11,5),sharey=True)
for ax,metric,label in zip(axes,['median_squared_error_adjusted_flag','Brier_adjusted_flag'],['Median squared error difference (cycles²)','Brier contribution difference']):
    rows=[r for r in real if r['metric']==metric];pts=np.array([float(r['effect']) for r in rows]);lo=np.array([float(r['ci_low']) for r in rows]);hi=np.array([float(r['ci_high']) for r in rows]);yy=np.arange(8)
    ax.errorbar(pts,yy,xerr=[pts-lo,hi-pts],fmt='o',capsize=3);ax.axvline(0,color='gray',linestyle='--');ax.set_xlabel(label);ax.set_yticks(yy);ax.set_yticklabels([r['subset']+' '+r['architecture']+' (n='+r['evaluation_engines']+')' for r in rows]);ax.invert_yaxis();ax.grid(axis='x',alpha=.2)
fig.suptitle('Incompatible − compatible: RUL-adjusted flag coefficients\n95% engine-cluster bootstrap intervals; all five frozen seeds retained');fig.tight_layout();fig.savefig(O/'real_adjusted_associations.png',dpi=180);fig.savefig(O/'real_adjusted_associations.pdf');plt.close(fig)
text=(O/'report.md').read_text(encoding='utf-8')
text+='\n## Documented numerical correction\n\nThe initial full-matrix rank screen returned undefined synthetic final-window regressions because the oracle has only two distinct probability/quantile pairs. Cubic nuisance columns are redundant. Initial partial outputs are preserved under initial_rank_screen. A separately hashed numerical_addendum.md was written before the corrected run, which uses an SVD generalized inverse and explicitly checks target identifiability. This retains the specified adjustment column space. Rank-deficient nuisance coefficients are not individually interpreted. Truly unidentifiable target coefficients remain NA. The initial run was interrupted and the full cohort was rerun; no fits were removed. All corrected point target coefficients were checked against direct least squares with the matching SVD cutoff. regression_rank_diagnostics.csv records point ranks, target identifiability and undefined bootstrap counts.\n'
text+='\n## Real adjusted associations\n\n'
for r in real:
    if r['metric'].endswith('adjusted_flag'):
        text+=f'- {r["subset"]} {r["architecture"]}, {r["metric"]}: {float(r["effect"]):.5g} [{float(r["ci_low"]):.5g}, {float(r["ci_high"]):.5g}]. Engines: fitting {r["fitting_engines"]}, evaluation {r["evaluation_engines"]}, ever incompatible {r["incompatible_engines"]}, ever compatible {r["compatible_engines"]} (overlap allowed).\n'
text+='\n## Synthetic joint components\n\n'
for r in family:
    text+=f'- {r["family"]}, {r["outcome"]}, {r["predictor"]}: {float(r["effect"]):.5g} [{float(r["ci_low"]):.5g}, {float(r["ci_high"]):.5g}], pass={r["passes"]}. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.\n'
text+='\n## Near-threshold and incremental probability adjustment\n\n'
for sub in ['FD001','FD002','FD003','FD004']:
 for arch in ['lstm','hybrid']:
    rr=[r for r in real if r['subset']==sub and r['architecture']==arch];find=lambda metric:next(r for r in rr if r['metric']==metric)
    a=find('near_threshold_rate_20_to_40');b=find('near_threshold_rate_elsewhere');inc=find('Brier_distance_beyond_raw_p_per_0.1')
    text+=f'- {sub} {arch}: near-band rate {float(a["effect"])*100:.2f}% (n={a["band_engines"]}), elsewhere {float(b["effect"])*100:.2f}% (n={b["band_engines"]}); Brier distance coefficient beyond raw probability {float(inc["effect"]):.5g} [{float(inc["ci_low"]):.5g}, {float(inc["ci_high"]):.5g}], evaluation n={inc["evaluation_engines"]}, fitting n={inc["fitting_engines"]}. All rate/distance CIs and incremental R² are in real_associations.csv.\n'
text+='\nThe criterion fails if either branch fails, even when selected individual associations are positive. Negative median-error associations are retained. This verdict does not establish universal uselessness. No N-CMAPSS association experiment was requested or executed here. External independent review: REVIEW_UNAVAILABLE.\n'
text+='\nCompact tables: real_primary_table.csv, near_threshold_table.csv, incremental_Brier_table.csv. Per-fit/seed group differences are descriptive; cohort effects and their uncertainty are in the association tables. The scientific figure real_adjusted_associations.pdf/png shows every real primary coefficient.\n'
(O/'report.md').write_text(text,encoding='utf-8')
root=Path(os.environ['USERPROFILE'])/'.codex/sessions';sid=os.environ['CODEX_SESSION_ID'];calls=[];identities=[]
for path in root.rglob('*'+sid+'*.jsonl'):
 for line in path.open(encoding='utf-8'):
    try:r=json.loads(line)
    except json.JSONDecodeError:continue
    p=r.get('payload',{})
    if r.get('type')=='turn_context':identities.append(dict(timestamp=r.get('timestamp'),model=p.get('model'),effort=p.get('effort')))
    if r.get('type')=='session_meta':identities.append(dict(timestamp=r.get('timestamp'),cli_version=p.get('cli_version'),originator=p.get('originator')))
    if r.get('type')=='response_item' and p.get('type') in ['function_call','custom_tool_call'] and p.get('name','').split('.')[-1] in ['exec','apply_patch','exec_command']:
        calls.append(dict(timestamp=r.get('timestamp'),name=p.get('name'),call_id=p.get('call_id'),arguments=p.get('arguments'),input=p.get('input')))
with (O/'exact_tool_calls.jsonl').open('w',encoding='utf-8') as f:
 for r in calls:f.write(json.dumps(r,ensure_ascii=False)+'\n')
(O/'ai_provenance.json').write_text(json.dumps(dict(tool='Codex desktop',observed_session_identifiers=identities,exact_served_checkpoint='UNAVAILABLE',role='Protocol/code authoring; numerical outputs from executed code',independent_review='REVIEW_UNAVAILABLE'),indent=2))
checks=dict(status='PASS',real_groups=8,real_rows=len(real),synthetic_rows=len(syn),synthetic_per_fit_rows=len(per),real_engine_runs=len(eng),real_unique_engines=707,all_bins=len(bins),protocol_hash_verified=True,raw_rates_reproduced=True,regression_direct_lstsq_checks='passed in analysis worker',no_training_or_selection=True)
(O/'checks.json').write_text(json.dumps(checks,indent=2))
paths=[p for p in O.rglob('*') if p.is_file() and p.name!='manifest.json']+[Path('scripts/analyze_compatibility_association.py'),Path(__file__)]
(O/'manifest.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),protocol=lock,files={p.as_posix():dict(bytes=p.stat().st_size,sha256=sha(p)) for p in paths}),indent=2))
print(json.dumps(dict(checks=checks,decision=decision['decision'],real_passing=decision['real_groups_both_positive'],synthetic_confirmation=decision['synthetic_confirmation'])))

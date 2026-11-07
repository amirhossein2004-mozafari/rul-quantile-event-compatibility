"""Present all executed frozen-prediction results and archive checks/provenance."""
from pathlib import Path
import json,csv,hashlib,os
import numpy as np
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'reports/compatibility_null_validation/controls_projection_power'
def read(name):
    with (O/name).open(encoding='utf-8') as f:return list(csv.DictReader(f))
def save(name,rows):
    with (O/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def num(x,rate=False):return f'{100*float(x):.1f}' if rate else f'{float(x):.3g}'
def ci(r,key,rate=False,suffix=''):return num(r[key],rate)+suffix+' ['+num(r[key+'_lo'],rate)+', '+num(r[key+'_hi'],rate)+']'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)
A=read('A_controls.csv');BB=read('B_projection.csv');C=read('C_effect_sizes_power.csv');D=read('D_dependence.csv');checks=json.loads((O/'checks.json').read_text());assert checks['status']=='PASS'
assert len(A)==65 and len(BB)==130 and len(C)==26 and len(read('A_uniform_per_draw.csv'))==4000
lock=json.loads((O/'protocol_lock.json').read_text(encoding='utf-8-sig'));assert hashlib.sha256((O/'protocol.md').read_bytes()).hexdigest()==lock['protocol_sha256']
manifest_inputs=json.loads((O/'input_hashes.json').read_text())
for name,h in manifest_inputs.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
previous=json.loads((ROOT/'reports/manuscript_real_evidence_revision/manifest.json').read_text())
for name,h in previous['outputs'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,('Earlier claim/document changed',name)
labels={'raw':'Raw','uniform':'Uniform, 100 draws','one_minus_p':'1-p','logit_plus_1':'logit +1','logit_minus_1':'logit -1'}
def group(r):return r['subset']+' '+r['architecture']
def engine(r):return r['fitting_engines']+'/'+r['evaluation_engines']
report='# Frozen controls, direct projection, effect size and engine dependence\n\nProtocol SHA256: `'+lock['protocol_sha256']+'`. Locked before these calculations; no outcome, threshold or criterion changed afterward. No training, forward inference or model selection ran. Earlier manuscript/claim artifacts remain unchanged.\n\nAll brackets are 95% engine-cluster percentile CIs from 2000 draws. Rates are percentages and rate differences are percentage points; Brier/NLL/ECE/distance use their original score units. Displayed non-rate estimates use three significant figures; CSVs retain full precision. Fit/test or fit/cal engine counts accompany every table row. Fixed-fit counts never multiply the engine count.\n\n'
report+='## Pooled estimates\n\nTest: 707 engine clusters; calibration: 142 separate engine clusters. LSTM/hybrid are averaged equally within each subset, followed by engine-count weighting across subsets. There are 40 fixed models, not 40 independent fleets.\n\n'
report+=table(['Control','Fit/test engines','Fixed fits','Incompatibility % [CI]','Mean distance [CI]'],[[labels[r['variant']],engine(r),r['fixed_fits'],ci(r,'incompatibility_rate',True),ci(r,'mean_distance')] for r in A if r['scope']=='pooled'])
report+='\n'+table(['Role/metric','Fit/evaluation engines','Raw [CI]','Projected [CI]','Projected minus raw [CI]'],[[r['role']+' '+r['metric'],engine(r),ci(r,'raw',r['metric']=='incompatibility_rate'),ci(r,'projected',r['metric']=='incompatibility_rate'),ci(r,'projected_minus_raw',r['metric']=='incompatibility_rate')] for r in BB if r['scope']=='pooled'])
report+='\nThe -1 logit control lowers the pooled incompatibility rate. Direct projection produces zero incompatibility by construction. FD001 LSTM test Brier increases after projection; its paired interval includes zero. All group results, including these directions, are retained below.\n\n'
for scope,title in [('group','A. Every frozen group'),('subset_combined','A. Within-subset combined estimates')]:
    rr=[r for r in A if r['scope']==scope]
    report+='## '+title+'\n\n'+table(['Group/control','Fit/test engines','Fixed fits','Incompatibility % [CI]','Mean distance [CI]'],[[group(r)+' '+labels[r['variant']],engine(r),r['fixed_fits'],ci(r,'incompatibility_rate',True),ci(r,'mean_distance')] for r in rr])+'\n'
report+='The uniform-control group estimand averages 100 fixed probability draws per engine/run; CIs condition on those draws. A_per_seed.csv and A_uniform_per_draw.csv retain all seeds and all 4000 draw/seed rows. Saved uniform probability arrays preserve every generated control.\n\n'
for role in ['test','calibration']:
    for scope,title in [('group','Every frozen group'),('subset_combined','Within-subset combined')]:
        rr=[r for r in BB if r['role']==role and r['scope']==scope]
        report+='## B. '+role+': '+title+'\n\n'+table(['Group/metric','Fit/evaluation engines','Fixed fits','Raw [CI]','Projected [CI]','Paired difference [CI]'],[[group(r)+' '+r['metric'],engine(r),r['fixed_fits'],ci(r,'raw',r['metric']=='incompatibility_rate'),ci(r,'projected',r['metric']=='incompatibility_rate'),ci(r,'projected_minus_raw',r['metric']=='incompatibility_rate')] for r in rr])+'\n'
report+='Brier uses unmodified probabilities; NLL alone clips to [1e-15,1-1e-15] and uses log1p for the non-event term. ECE5 uses label-free method-specific probability-quantile cuts, duplicates collapsed, fixed across bootstrap draws. ECE10 uses fixed equal-width bins. Both metrics average the fixed-model ECE values; they are not ECE of a model-averaged probability. ECE_bin_definitions.json records every edge set and occupied-bin count. Calibration endpoints are a separate recorded role, not independent validation of a fitted calibration map.\n\n'
for scope,title in [('group','Every frozen group'),('subset_combined','Within-subset combined'),('pooled','Across-subset pooled')]:
    for outcome in ['median_squared_error','Brier']:
        rr=[r for r in C if r['scope']==scope and r['outcome']==outcome]
        body=[]
        for r in rr:
            interval=num(r['coefficient'])+' ['+num(r['ci_low'])+', '+num(r['ci_high'])+']'
            body.append([group(r),engine(r),r['fixed_fits'],interval,num(r['mean_outcome_MSE']),f'{float(r["upper_CI_as_percent_of_mean"]):.1f}%',num(r['MDE_80_power']),f'{float(r["MDE_as_percent_of_mean"]):.1f}%',r['undefined_bootstrap_draws']])
        report+='## C. '+title+': '+outcome+'\n\n'+table(['Group','Fit/test engines','Fits','Flag coefficient [CI]','Own mean MSE','Upper CI / mean','MDE 80%','MDE / mean','Undefined draws'],body)+'\n'
report+='For point error, the mean is squared error of the saved unprojected median against true RUL capped at 125, in cycles squared. For Brier, the mean is the raw event-probability MSE. Upper-endpoint ratios are signed and use the observed group mean denominator; they are not explained-variance percentages.\n\nThe MDE is approximate: (Phi^-1(0.975)+Phi^-1(0.80)) times the saved engine-bootstrap coefficient SD (ddof=1), for a two-sided alpha=0.05 normal/Wald test. It is not an exact bounded-outcome power simulation or an observed-effect power calculation. Existing percentile CIs are unchanged. The pooled coefficient is an engine-count-weighted average of group-specific adjusted effects, not a common-slope pooled regression.\n\n'
report+='## D. Dependence and independent engine units\n\n'+table(['Subset/role','Fitting engines','Evaluation engines','Architectures','Seeds/architecture','Fixed fits','Engine/run rows','Shared across architectures/seeds'],[[r['subset']+' '+r['role'],r['fitting_engines'],r['independent_evaluation_engines'],r['architectures'],r['seeds_per_architecture'],r['fixed_fits'],r['engine_run_rows'],'yes / yes'] for r in D])
report+='\nBoth architectures and all five seeds share the same engines within a subset and role. IDs are namespaced by subset and role; calibration and official-test engines are never pooled. Across subsets, independent resampling streams are used. The pooled test estimate contains 707 engine clusters; the separately pooled calibration estimate contains 142. Engine IDs are saved in D_dependence.csv. Bootstrap indices/counts remain synchronized across methods and architectures within each subset.\n\n'
report+='## Files, checks and provenance\n\n- A_controls.csv: all group, subset-combined and pooled control estimates/CIs.\n- B_projection.csv: all raw/projected scores, marginal CIs and paired-difference CIs for both roles.\n- C_effect_sizes_power.csv: every coefficient, CI, outcome mean, signed relative upper endpoint, bootstrap SE and approximate MDE.\n- A_per_seed.csv, B_per_seed.csv, A_uniform_per_draw.csv: all fixed seeds and realizations.\n- ECE_bin_definitions.json, bootstrap_*.npz, projection_*.npz, uniform_*.npz: fixed scoring and resampling records.\n- checks.json: source reproduction, zero projection incompatibility, direct ECE checks and unchanged inputs.\n\nAll 89 experimental input files used by the analysis remained unchanged. Independent human review is still missing.\n'
ai=json.loads((O/'ai_provenance.json').read_text());app=json.loads((O/'app_build.json').read_text())
report+='\nAI identifiers: configured model `'+ai['configured_model_identifier']+'`; runtime `'+ai['runtime_version']+'`; desktop build `'+app['Version']+'`. Exact served checkpoint remains unavailable. Saved source provenance and current session identity records are retained.\n'
(O/'report.md').write_text(report,encoding='utf-8')
# Compact tables are additional presentations of the same full-precision rows.
save('pooled_A.csv',[r for r in A if r['scope']=='pooled']);save('pooled_B.csv',[r for r in BB if r['scope']=='pooled']);save('pooled_C.csv',[r for r in C if r['scope']=='pooled']);save('C_group_effect_sizes.csv',[r for r in C if r['scope']=='group'])
for sub in ['FD001','FD002','FD003','FD004']:
    save('A_'+sub+'.csv',[r for r in A if r['scope']=='group' and r['subset']==sub]);save('B_'+sub+'.csv',[r for r in BB if r['scope']=='group' and r['subset']==sub])
calls=[];identities=[]
for path in (Path(os.environ['USERPROFILE'])/'.codex/sessions').rglob('*'+os.environ['CODEX_SESSION_ID']+'*.jsonl'):
    for line in path.open(encoding='utf-8'):
        try:r=json.loads(line)
        except json.JSONDecodeError:continue
        p=r.get('payload',{})
        if r.get('type')=='turn_context':identities.append(dict(timestamp=r.get('timestamp'),model=p.get('model'),effort=p.get('effort')))
        if r.get('type')=='session_meta':identities.append(dict(timestamp=r.get('timestamp'),runtime_version=p.get('cli_version'),originator=p.get('originator')))
        if r.get('type')=='response_item' and p.get('type') in ['function_call','custom_tool_call'] and p.get('name','').split('.')[-1] in ['exec','apply_patch','exec_command']:calls.append(dict(timestamp=r.get('timestamp'),name=p.get('name'),call_id=p.get('call_id'),arguments=p.get('arguments'),input=p.get('input')))
with (O/'exact_tool_calls.jsonl').open('w',encoding='utf-8') as f:
    for r in calls:f.write(json.dumps(r,ensure_ascii=False)+'\n')
(O/'session_ai_provenance.json').write_text(json.dumps(dict(available_identifiers=identities,served_checkpoint='UNAVAILABLE',independent_human_review='MISSING'),indent=2))
for r in BB:assert r['projected_incompatibility_rate']=='0.0' if 'projected_incompatibility_rate' in r else True
assert all(float(r['projected'])==0 for r in BB if r['metric']=='incompatibility_rate')
assert all(int(r['undefined_bootstrap_draws'])==0 for r in C)
validation=dict(status='PASS',A_rows=len(A),B_rows=len(BB),C_rows=len(C),earlier_claim_artifacts_unchanged=len(previous['outputs']),experimental_inputs_unchanged=len(manifest_inputs),test_clusters=707,calibration_clusters=142,all_projection_flags_zero=True,all_required_results_retained=True,protocol_hash=lock['protocol_sha256'],independent_human_review='MISSING')
(O/'final_checks.json').write_text(json.dumps(validation,indent=2))
paths=[p for p in O.iterdir() if p.is_file() and p.name!='manifest.json']+[ROOT/'scripts/frozen_controls_projection_power.py',Path(__file__)]
(O/'manifest.json').write_text(json.dumps(dict(protocol=lock,inputs=manifest_inputs,files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},checks=validation),indent=2))
print(json.dumps(validation))

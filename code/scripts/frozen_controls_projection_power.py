"""Locked analysis of saved frozen predictions; no model imports or training."""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from pathlib import Path
import csv,json,hashlib,datetime,shutil
import numpy as np
from scipy.special import expit
from scipy.stats import norm
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'reports/compatibility_null_validation';OUT=BASE/'controls_projection_power'
SUBS=['FD001','FD002','FD003','FD004'];ARCHS=['lstm','hybrid'];SEEDS=[1101,1202,1303,1404,1505];FIT=[60,156,60,149];TEST=[100,259,100,248];CAL=[20,52,20,50];B=2000;LEVELS=np.array([.05,.5,.95]);METRICS=['Brier','NLL','ECE5','ECE10','incompatibility_rate']
inputs={};A=[];BROWS=[];C=[];APER=[];BPER=[];UDRAWS=[];BINS=[];DEPEND=[];a_cache={};b_cache={};c_cache={};outcome_cache={};weight_cache={};id_records={}
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
def track(path):inputs[path.relative_to(ROOT).as_posix()]=sha(path);return path
def read(path):
    with track(path).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def save(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')
lock=json.loads((OUT/'protocol_lock.json').read_text(encoding='utf-8-sig'));assert sha(OUT/'protocol.md')==lock['protocol_sha256']
def weights(si,role):
    key=(si,role)
    if key not in weight_cache:
        n=(TEST if role=='test' else CAL)[si];seed=(2026110103 if role=='test' else 2026110105)+1000*si
        counts=np.random.default_rng(seed).multinomial(n,np.full(n,1/n),size=B)
        weight_cache[key]=np.vstack([np.full(n,1/n),counts/n]);np.savez_compressed(OUT/f'bootstrap_{SUBS[si]}_{role}.npz',counts=counts,seed=seed)
    return weight_cache[key]
def interval(v):
    good=np.isfinite(v)
    return (*np.quantile(v[good],[.025,.975]),int((~good).sum())) if good.any() else (np.nan,np.nan,len(v))
def base(si,arch,role,scope='group'):
    return dict(scope=scope,subset=SUBS[si],architecture=arch,role=role,fitting_engines=FIT[si],evaluation_engines=(TEST if role=='test' else CAL)[si],fixed_fits=5 if scope=='group' else 10)
def bounds(q):
    assert np.all(np.diff(q,axis=-1)>=0)
    lo=np.where(q<=30,LEVELS,0).max(-1);hi=np.where(q>30,LEVELS,1).min(-1);assert np.all(lo<=hi)
    return lo,hi
def distance(lo,hi,p):return np.maximum.reduce([lo-p,p-hi,np.zeros_like(p)])
def load(si,arch,role):
    sub=SUBS[si];qs=[];ps=[];rs=[];ids=None;truth=None
    endpoints=read(ROOT/f'results/fair_comparison_step2/data/{sub}/calibration_endpoints.csv') if role=='calibration' else None
    for seed in SEEDS:
        frame=read(ROOT/f'results/fair_comparison_step2/final/{sub}/{arch}/seed_{seed}/{role if role=="test" else "calibration"}_predictions.csv')
        ii=np.array([int(float(r['engine_id'])) for r in (frame if role=='test' else endpoints)])
        yy=np.array([float(r['raw_y']) for r in frame]);q=np.array([[float(r[k]) for k in ['q05','q50','q95']] for r in frame]);r=np.array([float(v['logit']) for v in frame]);p=expit(r)
        if role=='test':np.testing.assert_allclose(p,[float(v['p_Raw']) for v in frame],atol=1e-12,rtol=1e-12)
        else:np.testing.assert_array_equal(yy,[float(v['raw_y']) for v in endpoints])
        if ids is not None:np.testing.assert_array_equal(ii,ids);np.testing.assert_array_equal(yy,truth)
        ids=ii;truth=yy;qs.append(q);ps.append(p);rs.append(r)
    expected=(TEST if role=='test' else CAL)[si];assert len(ids)==expected and len(set(ids))==expected
    key=(sub,role)
    if key in id_records:np.testing.assert_array_equal(ids,id_records[key]['ids']);np.testing.assert_array_equal(truth,id_records[key]['truth'])
    else:id_records[key]=dict(ids=ids,truth=truth)
    return np.array(qs),np.array(ps),np.array(rs),truth,ids
def a_row(info,variant,curves):
    row=dict(**info,variant=variant,uniform_realizations=100 if variant=='uniform' else 0)
    for j,name in enumerate(['incompatibility_rate','mean_distance']):
        lo,hi,bad=interval(curves[1:,j]);row[name]=float(curves[0,j]);row[name+'_lo']=float(lo);row[name+'_hi']=float(hi);row[name+'_undefined_draws']=bad
    A.append(row)
def controls(si,arch,q,p,r,ids):
    lo,hi=bounds(q);w=weights(si,'test');ai=ARCHS.index(arch);seed=2026110104+1000*si+100*ai
    uniform=np.random.default_rng(seed).random((100,len(SEEDS),len(ids)))
    np.savez_compressed(OUT/f'uniform_{SUBS[si]}_{arch}.npz',probability=uniform,engine_id=ids,seed=seed)
    for variant,pp in [('raw',p),('uniform',uniform),('one_minus_p',1-p),('logit_plus_1',expit(r+1)),('logit_minus_1',expit(r-1))]:
        d=distance(lo,hi,pp);vals=np.stack([d>0,d],axis=-1)
        if variant=='uniform':
            for draw in range(100):
                for j,s in enumerate(SEEDS):UDRAWS.append(dict(subset=SUBS[si],architecture=arch,role='test',fitting_engines=FIT[si],evaluation_engines=len(ids),seed=s,uniform_realization=draw,incompatibility_rate=float(vals[draw,j,:,0].mean()),mean_distance=float(vals[draw,j,:,1].mean())))
            per=vals.mean(0)
        else:per=vals
        engine=per.mean(0);curves=w@engine;a_cache[si,arch,variant]=curves;a_row(base(si,arch,'test'),variant,curves)
        for j,s in enumerate(SEEDS):
            cc=w@per[j];row=dict(**base(si,arch,'test'),seed=s,variant=variant);row['fixed_fits']=1;row['cohort_fixed_fits']=5
            for k,name in enumerate(['incompatibility_rate','mean_distance']):row[name]=float(cc[0,k]);row[name+'_lo'],row[name+'_hi'],row[name+'_undefined_draws']=interval(cc[1:,k])
            APER.append(row)
def ece_curves(p,y,w,kind,info,variant,seed):
    cuts=np.unique(np.quantile(p,np.linspace(0,1,6)))[1:-1] if kind=='ECE5' else np.linspace(.1,.9,9)
    labels=np.searchsorted(cuts,p,side='left');occupied=np.unique(labels)
    residual=np.stack([(p-y)*(labels==b) for b in range(len(cuts)+1)],axis=1)
    values=np.abs(w@residual).sum(1)
    direct=sum(abs(float(p[labels==b].mean()-y[labels==b].mean()))*float((labels==b).mean()) for b in occupied)
    np.testing.assert_allclose(values[0],direct,atol=1e-14,rtol=1e-12)
    BINS.append(dict(**info,variant=variant,seed=seed,metric=kind,interior_cuts=cuts.tolist(),occupied_bins=int(len(occupied))))
    return values
def scores(si,arch,role,p,y,lo,hi,variant):
    w=weights(si,role);clipped=np.clip(p,1e-15,1-1e-15)
    additive=np.stack([(p-y)**2,-y*np.log(clipped)-(1-y)*np.log1p(-clipped),distance(lo,hi,p)>0],axis=-1)
    per=[]
    for j,s in enumerate(SEEDS):
        basic=w@additive[j];e5=ece_curves(p[j],y,w,'ECE5',base(si,arch,role),variant,s);e10=ece_curves(p[j],y,w,'ECE10',base(si,arch,role),variant,s)
        per.append(np.stack([basic[:,0],basic[:,1],e5,e10,basic[:,2]],axis=-1))
    per=np.array(per);assert np.isfinite(per).all();return per.mean(0),per
def b_rows(info,raw,proj,collection):
    for k,metric in enumerate(METRICS):
        row=dict(**info,metric=metric)
        for name,v in [('raw',raw[:,k]),('projected',proj[:,k]),('projected_minus_raw',proj[:,k]-raw[:,k])]:
            low,high,bad=interval(v[1:]);row[name]=float(v[0]);row[name+'_lo']=float(low);row[name+'_hi']=float(high);row[name+'_undefined_draws']=bad
        collection.append(row)
def project(si,arch,role,q,p,y):
    lo,hi=bounds(q);proj=np.clip(p,lo,hi);assert np.all(distance(lo,hi,proj)==0)
    label=(y<=30).astype(float);rawcur,rawper=scores(si,arch,role,p,label,lo,hi,'raw');projcur,projper=scores(si,arch,role,proj,label,lo,hi,'projected')
    assert np.all(projcur[:,4]==0)
    b_cache[si,arch,role]=(rawcur,projcur);b_rows(base(si,arch,role),rawcur,projcur,BROWS)
    for j,s in enumerate(SEEDS):
        info=dict(**base(si,arch,role),seed=s);info['fixed_fits']=1;info['cohort_fixed_fits']=5
        b_rows(info,rawper[j],projper[j],BPER)
    np.savez_compressed(OUT/f'projection_{SUBS[si]}_{arch}_{role}.npz',p_raw=p,p_projected=proj,L=lo,U=hi,engine_id=id_records[SUBS[si],role]['ids'],event_label=label)
    return rawcur
# Existing coefficient draws are saved with the exact earlier engine resampling alignment.
primary=read(BASE/'association/real_primary_table.csv');prior_rates=read(BASE/'followup/real_variant_summary.csv')
with track(BASE/'association/bootstrap_keys.json').open(encoding='utf-8') as f:keys=json.load(f)
drawfile=np.load(track(BASE/'association/bootstrap_effects.npz'))
old_engine=read(BASE/'association/real_engine_run.csv')
def coefficient_row(info,outcome,coefficient,draws,mean):
    low,high,bad=interval(draws);valid=draws[np.isfinite(draws)];se=float(np.std(valid,ddof=1)) if len(valid)>1 else np.nan;mde=float((norm.ppf(.975)+norm.ppf(.80))*se)
    C.append(dict(**info,outcome=outcome,coefficient=float(coefficient),ci_low=float(low),ci_high=float(high),mean_outcome_MSE=float(mean),upper_CI_as_percent_of_mean=float(100*high/mean) if mean>0 else np.nan,bootstrap_SE=se,MDE_80_power=mde,MDE_as_percent_of_mean=float(100*mde/mean) if mean>0 else np.nan,undefined_bootstrap_draws=bad,bootstrap_draws=B,power_method='normal/Wald, two-sided alpha=.05, bootstrap SE; approximate'))
for si,sub in enumerate(SUBS):
    for arch in ARCHS:
        q,p,r,y,ids=load(si,arch,'test');controls(si,arch,q,p,r,ids);rawtest=project(si,arch,'test',q,p,y)
        rr=next(v for v in prior_rates if v['subset']==sub and v['architecture']==arch and v['variant']=='weighted_raw')
        np.testing.assert_allclose(a_cache[si,arch,'raw'][0],[float(rr['rate']),float(rr['mean_distance'])],atol=1e-13,rtol=1e-12)
        saved=[v for v in old_engine if v['subset']==sub and v['architecture']==arch];np.testing.assert_allclose(rawtest[0,0],np.mean([float(v['Brier']) for v in saved]),atol=1e-13)
        outcomes={'median_squared_error':(q[:,:,1]-np.minimum(y,125))**2,'Brier':(p-(y<=30))**2}
        previous=next(v for v in primary if v['subset']==sub and v['architecture']==arch)
        for outcome,values in outcomes.items():
            key=['real',sub,arch,'weighted_raw','final',len(ids),outcome,'flag'];index=keys.index(key);draws=drawfile[f'key_{index}'];assert draws.shape==(B,)
            col=outcome+'_adjusted_flag';coef=float(previous[col+'_effect']);lo,hi,bad=interval(draws)
            np.testing.assert_allclose([lo,hi],[float(previous[col+'_ci_low']),float(previous[col+'_ci_high'])],atol=1e-12,rtol=1e-12)
            mean=float(values.mean());source_values=[float(v['median_squared_error'] if outcome=='median_squared_error' else v['Brier']) for v in saved];np.testing.assert_allclose(mean,np.mean(source_values),atol=1e-10,rtol=1e-12)
            c_cache[si,arch,outcome]=(coef,draws,mean);coefficient_row(base(si,arch,'test'),outcome,coef,draws,mean)
        q,p,r,y,ids=load(si,arch,'calibration');project(si,arch,'calibration',q,p,y)
        print('GROUP COMPLETE',sub,arch,flush=True)
# Pool all fixed outputs, using the same synchronized engine draws within a subset.
for si,sub in enumerate(SUBS):
    for variant in ['raw','uniform','one_minus_p','logit_plus_1','logit_minus_1']:
        curve=(a_cache[si,'lstm',variant]+a_cache[si,'hybrid',variant])/2;a_cache[si,'combined',variant]=curve;a_row(base(si,'combined','test','subset_combined'),variant,curve)
    for role in ['test','calibration']:
        raw=(b_cache[si,'lstm',role][0]+b_cache[si,'hybrid',role][0])/2;proj=(b_cache[si,'lstm',role][1]+b_cache[si,'hybrid',role][1])/2;b_cache[si,'combined',role]=(raw,proj);b_rows(base(si,'combined',role,'subset_combined'),raw,proj,BROWS)
    for outcome in ['median_squared_error','Brier']:
        left=c_cache[si,'lstm',outcome];right=c_cache[si,'hybrid',outcome];entry=tuple((a+b)/2 for a,b in zip(left,right));c_cache[si,'combined',outcome]=entry;coefficient_row(base(si,'combined','test','subset_combined'),outcome,*entry)
for role in ['test','calibration']:
    ns=np.array(TEST if role=='test' else CAL);ww=ns/ns.sum();pooled=dict(scope='pooled',subset='FD001-FD004',architecture='combined',role=role,fitting_engines=sum(FIT),evaluation_engines=int(ns.sum()),fixed_fits=40)
    raw=sum(ww[i]*b_cache[i,'combined',role][0] for i in range(4));proj=sum(ww[i]*b_cache[i,'combined',role][1] for i in range(4));b_rows(pooled,raw,proj,BROWS)
    if role=='test':
        for variant in ['raw','uniform','one_minus_p','logit_plus_1','logit_minus_1']:a_row(pooled,variant,sum(ww[i]*a_cache[i,'combined',variant] for i in range(4)))
        for outcome in ['median_squared_error','Brier']:
            entry=tuple(sum(ww[i]*c_cache[i,'combined',outcome][j] for i in range(4)) for j in range(3));coefficient_row(pooled,outcome,*entry)
    for i,sub in enumerate(SUBS):
        ids=id_records[sub,role]['ids'].tolist();DEPEND.append(dict(subset=sub,role=role,fitting_engines=FIT[i],independent_evaluation_engines=len(ids),architectures=2,seeds_per_architecture=5,fixed_fits=10,engine_run_rows=len(ids)*10,shared_between_architectures=True,shared_between_seeds=True,ID_namespace=role+'/'+sub,engine_IDs=json.dumps(ids)))
save('A_controls.csv',A);save('A_per_seed.csv',APER);save('A_uniform_per_draw.csv',UDRAWS);save('B_projection.csv',BROWS);save('B_per_seed.csv',BPER);save('C_effect_sizes_power.csv',C);save('D_dependence.csv',DEPEND);write('ECE_bin_definitions.json',BINS)
assert len(A)==65 and len(BROWS)==130 and len(C)==26 and len(UDRAWS)==4000
for name,h in inputs.items():assert sha(ROOT/name)==h,name
shutil.copy2(BASE/'followup/ai_provenance.json',OUT/'ai_provenance.json');shutil.copy2(BASE/'followup/app_build.json',OUT/'app_build.json')
checks=dict(status='PASS',A_rows=len(A),B_rows=len(BROWS),C_rows=len(C),uniform_draw_seed_rows=len(UDRAWS),test_engines=707,calibration_engines=142,source_files_unchanged=len(inputs),projection_incompatibility_exactly_zero=True,raw_flags_distances_Brier_reproduced=True,prior_coefficients_CIs_reproduced=True,ECE_direct_checks_passed=True,training=False,inference=False,protocol=lock,source_sha256=sha(Path(__file__)))
write('checks.json',checks);write('input_hashes.json',inputs)
print(json.dumps(checks),flush=True)

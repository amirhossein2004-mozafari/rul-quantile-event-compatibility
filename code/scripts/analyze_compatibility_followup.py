from pathlib import Path
import os,sys,csv,json,itertools
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import compatibility_followup_train as f
import collect_compatibility_synthetic as c
import numpy as np
from scipy.special import expit
F=f.F;m=f.m

def read(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def save(name,rows):
    assert rows,name
    with (F/name).open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def classify(q):return float(np.median(q[:,1]-q[:,0]))<1.25

def summarize_group(family,sub,arch,policy,variant,outputs,labels,rep_ids,planned,failed,summary,perrep):
    with np.load(m.RUN/f'evaluation_{sub}_{policy}.npz') as ev:qt=ev['q_true'];pt=ev['p_true']
    names=['incompatibility_rate','mean_distance','tolerance_rate','oracle_quantile_mae','oracle_probability_MSE','negative_lower_gap_rate']
    vals=[]
    for q,p in outputs:
        assert np.isfinite(q).all() and np.isfinite(p).all() and np.all((p>=0)&(p<=1))
        d=m.diagnostic(q,p);vals.append(np.stack([d>0,d,d>1e-6,abs(q-qt).mean(1),(p-pt)**2,q[:,1]<q[:,0]],axis=1))
    values=np.array(vals);r=len(vals);labels=np.asarray(labels,dtype=bool)
    for n in [m.CFG['small_eval_counts'][sub],10000]:
        base=dict(family=family,subset=sub,architecture=arch,policy=policy,variant=variant,fitting_engines=m.CFG['fit_counts'][sub],classification_engines=10000,evaluation_engines=n,planned_fits=planned,successful_fits=r,failed_fits=failed,collapsed_fits=int(labels.sum()),noncollapsed_fits=int(r-labels.sum()))
        if r:
            weights=c.bootstrap(sub,policy,n);v=values[:,:n];means=v.mean(1)
            draws=(weights@v.transpose(1,0,2).reshape(n,r*len(names))).reshape(2000,r,len(names))
            ci=np.quantile(draws,[.025,.975],axis=0)
            for i,rep in enumerate(rep_ids):
                row=dict(**base,replication=rep,collapsed=bool(labels[i]))
                for k,name in enumerate(names):row[name]=float(means[i,k]);row[name+'_lo']=float(ci[0,i,k]);row[name+'_hi']=float(ci[1,i,k])
                perrep.append(row)
        for label,mask in [('all',np.ones(r,dtype=bool)),('noncollapsed',~labels),('collapsed',labels)]:
            count=int(mask.sum());row=dict(**base,stratum=label,selected_fits=count,status='EMPTY_STRATUM' if count==0 else ('SINGLE_FIT' if count==1 else ('SPARSE_STRATUM' if count<20 else 'OK')))
            for name in names:row[name]=row[name+'_lo']=row[name+'_hi']=''
            for name in ['training_rate_p025','training_rate_p975','training_rate_min','training_rate_max']:row[name]=''
            if count:
                point=means[mask].mean(0);boot=draws[:,mask].mean(1)
                for k,name in enumerate(names):row[name]=float(point[k]);row[name+'_lo'],row[name+'_hi']=np.quantile(boot[:,k],[.025,.975]).tolist()
                row['training_rate_p025'],row['training_rate_p975']=np.quantile(means[mask,0],[.025,.975]).tolist();row['training_rate_min']=float(means[mask,0].min());row['training_rate_max']=float(means[mask,0].max())
            summary.append(row)

def comparisons(summary):
    gate=json.loads((m.OUT/'reproduction_gate.json').read_text());rows=[]
    for r in summary:
        if r['policy']!='final':continue
        architectures=[('LSTM' if r['architecture']=='lstm' else 'Hybrid')] if r['family'] in ['temporal','fixed_init'] else ['LSTM','Hybrid']
        for arch in architectures:
            real=next(v for v in gate['summary'] if v['subset']==r['subset'] and v['model']==arch)
            threshold=r['training_rate_p975'];point=real['recomputed_mean']/100
            rows.append(dict(family=r['family'],subset=r['subset'],architecture=r['architecture'],real_architecture=arch,variant=r['variant'],same_probability_convention=r['variant']=='weighted_raw',stratum=r['stratum'],status=r['status'],fitting_engines=r['fitting_engines'],classification_engines=r['classification_engines'],null_evaluation_engines=r['evaluation_engines'],real_evaluation_engines=real['engines'],selected_fits=r['selected_fits'],collapsed_fits=r['collapsed_fits'],noncollapsed_fits=r['noncollapsed_fits'],real_seed_mean_rate=point,null_mean_rate=r['incompatibility_rate'],null_rate_ci_low=r['incompatibility_rate_lo'],null_rate_ci_high=r['incompatibility_rate_hi'],null_p975=threshold,exceeds='' if threshold=='' else point>float(threshold),real_initializations=5,null_initializations_per_fitting_fleet=1,scope='Descriptive conditional benchmark; not a matched five-seed null test'))
    return rows

def baseline():
    f.check();summary=[];perrep=[];labelrows=[]
    original={(r['family'],r['subset'],r['architecture'],r['policy'],r['variant'],int(r['evaluation_engines'])):r for r in read(m.OUT/'synthetic_summary.csv')}
    for sub in m.SUBS:
     for family,arch in [('temporal','lstm'),('temporal','hybrid'),('covariate','covariate'),('parametric','independent_exact_family')]:
        groups={policy:c.load_group(family,sub,arch,policy) for policy in ['final','uniform']}
        for variant in ['weighted_raw','weighted_corrected','unweighted']:
            audit=groups['uniform'][variant];labels=[classify(q) for q,p in audit];reps=list(range(len(audit)))
            for rep,(q,p) in enumerate(audit):labelrows.append(dict(family=family,subset=sub,architecture=arch,variant=variant,replication=rep,shared_state_variant='weighted' if variant!='unweighted' else 'unweighted',fitting_engines=m.CFG['fit_counts'][sub],classification_engines=10000,classification_policy='uniform',median_lower_gap=float(np.median(q[:,1]-q[:,0])),negative_gap_fraction=float((q[:,1]<q[:,0]).mean()),collapsed=labels[rep]))
            for policy in ['final','uniform']:summarize_group(family,sub,arch,policy,variant,groups[policy][variant],labels,reps,len(reps),0,summary,perrep)
        print('STRATIFIED',family,sub,arch,flush=True)
    for r in summary:
        if r['stratum']=='all':
            old=original[r['family'],r['subset'],r['architecture'],r['policy'],r['variant'],r['evaluation_engines']]
            np.testing.assert_allclose([r['incompatibility_rate'],r['mean_distance']],[float(old['incompatibility_rate']),float(old['mean_distance'])],atol=1e-12,rtol=1e-12)
    save('null_collapse_labels.csv',labelrows);save('null_stratified_summary.csv',summary);save('null_per_replication.csv',perrep);save('real_vs_null_strata.csv',comparisons(summary))
    m.write(F/'baseline_analysis_complete.json',dict(rows=len(summary),per_replication_rows=len(perrep),original_all_fit_rates_match=True,source_sha256=m.sha(__file__)))

def real_collapse():
    f.check();rows=[];groups=[];globaldraw=[]
    for si,sub in enumerate(m.SUBS):
        endpoints=read(ROOT/f'results/fair_comparison_step2/data/{sub}/calibration_endpoints.csv');ids=np.array([int(r['engine_id']) for r in endpoints]);n=len(ids)
        rng=np.random.default_rng(2026110101+1000*si);indices=rng.integers(0,n,size=(2000,n));np.savez_compressed(F/f'calibration_bootstrap_{sub}.npz',indices=indices,engine_ids=ids)
        gaps=[];entries=[]
        for arch in ['lstm','hybrid']:
         for seed in f.CFG['real_retrain_seeds']:
            path=ROOT/f'results/fair_comparison_step2/final/{sub}/{arch}/seed_{seed}/calibration_predictions.csv';frame=read(path);assert len(frame)==n
            gap=np.array([float(r['q50'])-float(r['q05']) for r in frame]);gaps.append(gap);entries.append((arch,seed))
        gaps=np.array(gaps);med=np.median(gaps,axis=1);draw_median=np.median(gaps[:,indices],axis=2);labels=med<1.25;drawlabels=draw_median<1.25;globaldraw.append(drawlabels)
        for j,(arch,seed) in enumerate(entries):
            lo,hi=np.quantile(draw_median[j],[.025,.975]);rows.append(dict(subset=sub,architecture=arch,seed=seed,fitting_engines=m.CFG['fit_counts'][sub],calibration_engines=n,test_engines=m.CFG['small_eval_counts'][sub],median_lower_gap=float(med[j]),median_gap_ci_low=float(lo),median_gap_ci_high=float(hi),collapsed=bool(labels[j])))
        for arch in ['lstm','hybrid']:
            mask=np.array([a==arch for a,s in entries]);boot=drawlabels[mask].mean(0);lo,hi=np.quantile(boot,[.025,.975])
            groups.append(dict(subset=sub,architecture=arch,fitting_engines=m.CFG['fit_counts'][sub],calibration_engines=n,test_engines=m.CFG['small_eval_counts'][sub],fits=5,collapsed_fits=int(labels[mask].sum()),collapsed_fraction=float(labels[mask].mean()),fraction_ci_low=float(lo),fraction_ci_high=float(hi),ci_scope='Calibration-engine bootstrap conditional on frozen fits; no model resampling'))
    boot=np.concatenate(globaldraw,axis=0).mean(0);lo,hi=np.quantile(boot,[.025,.975])
    save('real_collapse_labels.csv',rows);save('real_collapse_fractions.csv',groups)
    m.write(F/'real_collapse_overall.json',dict(fits=40,collapsed_fits=sum(r['collapsed'] for r in rows),fraction=sum(r['collapsed'] for r in rows)/40,calibration_engines=sum(r['calibration_engines'] for r in groups[::2]),test_engines=707,fraction_ci_low=float(lo),fraction_ci_high=float(hi),classification_role='fixed calibration endpoints only',scope='Descriptive fitted-state fraction; CI resamples calibration engines, preserving all model dependencies'))

def real_arrays(sub,arch,unweighted=False):
    q=[];praw=[];pc=[];ids=None
    for seed in f.CFG['real_retrain_seeds']:
        if unweighted:
            folder=F/f'real_unweighted/FD001/{arch}/seed_{seed}';assert (folder/'complete.json').exists()
            with np.load(folder/'test_predictions.npz') as d:qq=d['q'];eta=d['logit'];ii=d['engine_id'];offset=0.
        else:
            folder=ROOT/f'results/fair_comparison_step2/final/{sub}/{arch}/seed_{seed}';frame=read(folder/'test_predictions.csv');ii=np.array([int(float(r['engine_id'])) for r in frame]);qq=np.array([[float(r[k]) for k in ['q05','q50','q95']] for r in frame]);eta=np.array([float(r['logit']) for r in frame]);offset=json.loads((folder/'calibration_fits.json').read_text())['ln_pos_weight']
            np.testing.assert_allclose(expit(eta),[float(r['p_Raw']) for r in frame],atol=1e-12,rtol=1e-12);np.testing.assert_allclose(expit(eta-offset),[float(r['p_Bayes']) for r in frame],atol=1e-12,rtol=1e-12)
        if ids is None:ids=ii
        np.testing.assert_array_equal(ids,ii);q.append(qq);praw.append(expit(eta));pc.append(expit(eta-offset))
    return np.array(q),np.array(praw),np.array(pc),ids

def paired_row(sub,arch,a,b,indices,description,fitn,engineids):
    # a,b: models x engines x [indicator,distance]. Average models inside engine.
    av=a.mean(0);bv=b.mean(0);resolved=((a[:,:,0]>0)&(b[:,:,0]==0)).mean(0);introduced=((a[:,:,0]==0)&(b[:,:,0]>0)).mean(0)
    vals=np.stack([av[:,0],bv[:,0],av[:,1],bv[:,1],av[:,0]-bv[:,0],av[:,1]-bv[:,1],resolved,introduced],axis=1)
    draws=vals[indices].mean(1);point=vals.mean(0);row=dict(subset=sub,architecture=arch,comparison=description,fitting_engines=fitn,evaluation_engines=len(engineids),paired_seeds=len(a))
    for k,name in enumerate(['before_rate','after_rate','before_distance','after_distance','net_rate_reduction','net_distance_reduction','resolved_fraction','introduced_fraction']):row[name]=float(point[k]);row[name+'_lo'],row[name+'_hi']=np.quantile(draws[:,k],[.025,.975]).tolist()
    frac=point[4]/point[0] if point[0] else None;den=draws[:,0];valid=den>0
    row['net_proportional_reduction']='' if frac is None else float(frac)
    row['ratio_bootstrap_undefined_draws']=int((~valid).sum())
    if valid.any():row['net_proportional_reduction_lo'],row['net_proportional_reduction_hi']=np.quantile(draws[valid,4]/den[valid],[.025,.975]).tolist()
    else:row['net_proportional_reduction_lo']=row['net_proportional_reduction_hi']=''
    np.testing.assert_allclose(point[4],point[6]-point[7],atol=1e-14)
    return row

def real_attribution():
    f.check();assert (F/'real_training_complete.json').exists();rows=[];rates=[]
    for si,sub in enumerate(m.SUBS):
        n=m.CFG['small_eval_counts'][sub];rng=np.random.default_rng(2026110102+1000*si);indices=rng.integers(0,n,size=(2000,n));np.savez_compressed(F/f'test_bootstrap_{sub}.npz',indices=indices)
        for arch in ['lstm','hybrid']:
            q,raw,corrected,ids=real_arrays(sub,arch);a=np.stack([m.diagnostic(qq,p) for qq,p in zip(q,raw)]);b=np.stack([m.diagnostic(qq,p) for qq,p in zip(q,corrected)])
            before=np.stack([a>0,a],axis=2);after=np.stack([b>0,b],axis=2)
            rows.append(paired_row(sub,arch,before,after,indices,'weighted_raw_minus_fixed_weight_correction',m.CFG['fit_counts'][sub],ids))
            for variant,metrics in [('weighted_raw',before),('weighted_corrected',after)]:
                for j,seed in enumerate(f.CFG['real_retrain_seeds']):rates.append(dict(subset=sub,architecture=arch,seed=seed,variant=variant,fitting_engines=m.CFG['fit_counts'][sub],evaluation_engines=n,rate=float(metrics[j,:,0].mean()),distance=float(metrics[j,:,1].mean())))
            if sub=='FD001':
                uq,up,unused,uids=real_arrays(sub,arch,True);np.testing.assert_array_equal(ids,uids);d=np.stack([m.diagnostic(qq,p) for qq,p in zip(uq,up)]);unw=np.stack([d>0,d],axis=2)
                rows.append(paired_row(sub,arch,before,unw,indices,'weighted_raw_minus_unweighted_retrain',60,ids));rows.append(paired_row(sub,arch,after,unw,indices,'corrected_weighted_minus_unweighted_retrain',60,ids))
                for j,seed in enumerate(f.CFG['real_retrain_seeds']):rates.append(dict(subset=sub,architecture=arch,seed=seed,variant='unweighted_retrain',fitting_engines=60,evaluation_engines=n,rate=float(unw[j,:,0].mean()),distance=float(unw[j,:,1].mean())))
    save('real_weighting_attribution.csv',rows);save('real_probability_variant_per_seed.csv',rates)
    # Classify all ten new refits from their calibration endpoints, never test outputs.
    labels=[]
    for arch in ['lstm','hybrid']:
     for seed in f.CFG['real_retrain_seeds']:
        with np.load(F/f'real_unweighted/FD001/{arch}/seed_{seed}/calibration_predictions.npz') as d:q=d['q'];n=len(q)
        labels.append(dict(subset='FD001',architecture=arch,seed=seed,fitting_engines=60,calibration_engines=n,test_engines=100,median_lower_gap=float(np.median(q[:,1]-q[:,0])),collapsed=classify(q)))
    save('real_unweighted_collapse_labels.csv',labels);m.write(F/'real_attribution_complete.json',dict(comparisons=len(rows),source_sha256=m.sha(__file__)))

def read_pred(folder,policy):
    if (folder/'failure.json').exists() or not (folder/'complete.json').exists():return None
    with np.load(folder/f'{policy}_predictions.npz') as d:return d['q'],d['logit'],float(d['weight'])

def interventions():
    f.check();assert (F/'synthetic_training_complete.json').exists();summary=[];perrep=[];fix_rows=[];factor_rows=[];factor_draws={};quality_rows=[]
    factorial_weights=c.bootstrap('FD001','final',10000)
    for arch in ['lstm','hybrid']:
        groups={v:{p:[] for p in ['final','uniform']} for v in ['weighted_raw','weighted_corrected','unweighted']};labels={v:[] for v in groups};repids={v:[] for v in groups}
        for weighted in [True,False]:
         for rep in range(30):
            folder=f.fix_folder(arch,rep,weighted);audit=read_pred(folder,'uniform')
            if audit is None:continue
            qq,eta,w=audit;label=classify(qq)
            variants=['weighted_raw','weighted_corrected'] if weighted else ['unweighted']
            for v in variants:
                labels[v].append(label);repids[v].append(rep)
                for policy in ['final','uniform']:
                    q,e,w=read_pred(folder,policy);p=expit(e-np.log(w)) if v=='weighted_corrected' else expit(e);groups[v][policy].append((q,p))
        for v in groups:
            for policy in ['final','uniform']:summarize_group('fixed_init','FD001',arch,policy,v,groups[v][policy],labels[v],repids[v],30,30-len(repids[v]),summary,perrep)
            if v=='weighted_corrected':continue
            weighted=v=='weighted_raw';paired=[];perq=[];beforeq=[];afterq=[]
            with np.load(m.RUN/'evaluation_FD001_final.npz') as ev:qt=ev['q_true']
            for rep,(q,p) in zip(repids[v],groups[v]['final']):
                orig=m.RUN/f"temporal/FD001/{arch}/rep_{rep:03d}/{'weighted' if weighted else 'unweighted'}"
                with np.load(orig/'final_predictions.npz') as old:oq=old['q']
                paired.append(abs(q-qt).mean(1)-abs(oq-qt).mean(1))
                perq.append(abs(q-qt)-abs(oq-qt));beforeq.append(abs(oq-qt));afterq.append(abs(q-qt))
            if paired:
                delta=np.mean(paired,axis=0);boot=c.bootstrap('FD001','final',10000)@delta;lo,hi=np.quantile(boot,[.025,.975]);change=float(delta.mean())
            else:change=lo=hi=''
            removed=len(repids[v])==30 and not any(labels[v]);good=removed and change!='' and change<=0
            fix_rows.append(dict(subset='FD001',architecture=arch,objective='weighted' if weighted else 'unweighted',fitting_engines=60,classification_engines=10000,evaluation_engines=10000,planned_fits=30,completed_fits=len(repids[v]),failed_fits=30-len(repids[v]),collapsed_fits=sum(labels[v]),literal_collapse_removed=removed,oracle_q_MAE_change=change,oracle_q_MAE_change_lo=lo,oracle_q_MAE_change_hi=hi,passes_gap_and_quality_safeguard=good))
            if perq:
                difference=np.mean(perq,axis=0);boots=factorial_weights@difference
                oldmean=np.mean(beforeq,axis=(0,1));newmean=np.mean(afterq,axis=(0,1))
                for k,tau in enumerate([.05,.5,.95]):
                    lo,hi=np.quantile(boots[:,k],[.025,.975]);quality_rows.append(dict(architecture=arch,objective='weighted' if weighted else 'unweighted',tau=tau,fitting_engines=60,evaluation_engines=10000,paired_fits=len(repids[v]),before_oracle_MAE=float(oldmean[k]),after_oracle_MAE=float(newmean[k]),oracle_MAE_change=float(difference[:,k].mean()),change_lo=float(lo),change_hi=float(hi)))
        # Every factorial state, including failures, is retained as a row.
        for rep in [0,1,2]:
         for bits in itertools.product([0,1],repeat=4):
            folder=f.factor_folder(arch,rep,bits);a=read_pred(folder,'uniform');b=read_pred(folder,'final')
            row=dict(subset='FD001',architecture=arch,replication=rep,initialization=bits[0],pinball_normalized=bits[1],lr_tripled=bits[2],clipping_disabled=bits[3],fitting_engines=60,classification_engines=10000,evaluation_engines=10000,status='FAILED' if a is None or b is None else 'OK',collapsed='',median_gap='',evaluation_median_gap='',rate='',rate_lo='',rate_hi='',distance='',distance_lo='',distance_hi='',raw_pinball_final='',risk_loss_final='',preclip_norm_final='',clipping_fraction_final='',initial_reg_gradient='',initial_risk_gradient='')
            if row['status']=='OK':
                q,e,w=b;d=m.diagnostic(q,expit(e));hist=json.loads((folder/'history.json').read_text());first=json.loads((folder/'first_step.json').read_text());row.update(collapsed=classify(a[0]),median_gap=float(np.median(a[0][:,1]-a[0][:,0])),evaluation_median_gap=float(np.median(q[:,1]-q[:,0])),rate=float((d>0).mean()),distance=float(d.mean()),raw_pinball_final=hist[-1]['raw_pinball'],risk_loss_final=hist[-1]['risk_loss'],preclip_norm_final=hist[-1]['preclip_norm_mean'],clipping_fraction_final=hist[-1]['clipping_fraction'],initial_reg_gradient=first['scaled_pinball_shared_gradient_norm'],initial_risk_gradient=first['weighted_BCE_shared_gradient_norm'])
                boot=factorial_weights@np.stack([d>0,d],axis=1);factor_draws[arch,rep,bits]=boot
                row['rate_lo'],row['rate_hi']=np.quantile(boot[:,0],[.025,.975]).tolist();row['distance_lo'],row['distance_hi']=np.quantile(boot[:,1],[.025,.975]).tolist()
            factor_rows.append(row)
    save('fixed_init_summary.csv',summary);save('fixed_init_per_replication.csv',perrep);save('fixed_init_vs_real.csv',comparisons(summary));save('fix_success_checks.csv',fix_rows);save('fix_per_quantile_quality.csv',quality_rows);save('factorial_all_runs.csv',factor_rows)
    cells=[];keys=['initialization','pinball_normalized','lr_tripled','clipping_disabled']
    for arch in ['lstm','hybrid']:
     for bits in itertools.product([0,1],repeat=4):
        rr=[r for r in factor_rows if r['architecture']==arch and tuple(r[k] for k in keys)==bits];valid=[r for r in rr if r['status']=='OK']
        row=dict(architecture=arch,initialization=bits[0],pinball_normalized=bits[1],lr_tripled=bits[2],clipping_disabled=bits[3],fitting_engines=60,classification_engines=10000,evaluation_engines=10000,planned_fits=3,successful_fits=len(valid),failed_fits=3-len(valid),collapsed_fits=sum(bool(r['collapsed']) for r in valid),rate='',rate_lo='',rate_hi='',distance='',distance_lo='',distance_hi='')
        if valid:
            boot=np.mean([factor_draws[arch,r['replication'],bits] for r in valid],axis=0)
            row['rate']=float(np.mean([r['rate'] for r in valid]));row['distance']=float(np.mean([r['distance'] for r in valid]));row['rate_lo'],row['rate_hi']=np.quantile(boot[:,0],[.025,.975]).tolist();row['distance_lo'],row['distance_hi']=np.quantile(boot[:,1],[.025,.975]).tolist()
        cells.append(row)
    save('factorial_cell_summary.csv',cells)
    effects=[]
    for arch in ['lstm','hybrid']:
     for rep in [0,1,2]:
        rr=[r for r in factor_rows if r['architecture']==arch and r['replication']==rep];complete=len(rr)==16 and all(r['status']=='OK' for r in rr)
        for k in range(1,5):
         for subset in itertools.combinations(keys,k):
          for metric in ['collapsed','rate','distance']:
            val=(2**k)*np.mean([float(r[metric])*np.prod([2*r[key]-1 for key in subset]) for r in rr]) if complete else ''
            effects.append(dict(architecture=arch,replication=rep,factors='*'.join(subset),order=k,metric=metric,fitting_engines=60,evaluation_engines=10000,paired_factorial_complete=complete,contrast=val,scope='Paired k-order difference of means; no model-level significance inference'))
    save('factorial_all_interactions.csv',effects);m.write(F/'intervention_analysis_complete.json',dict(fix_rows=len(summary),factorial_runs=len(factor_rows),interactions=len(effects),source_sha256=m.sha(__file__)))

if __name__=='__main__':
    f.check();action=sys.argv[1]
    if action=='baseline':baseline();real_collapse()
    elif action=='real':real_attribution()
    elif action=='interventions':interventions()
    else:raise ValueError(action)

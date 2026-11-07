from pathlib import Path
import os,sys,json,csv,hashlib
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from scipy.special import expit
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import validate_compatibility_synthetic as m
OUT=m.OUT;RUN=m.RUN

def csvsave(p,rows):
    with Path(p).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def bootstrap(sub,policy,n):
    path=RUN/f'bootstrap_{sub}_{policy}_{n}.npz'
    if not path.exists():
        seed=16180339+m.SUBS.index(sub)*1000+(['final','uniform'].index(policy))*100+(n==10000)
        rng=np.random.default_rng(seed)
        counts=rng.multinomial(n,np.full(n,1/n),size=2000).astype(np.uint16)
        np.savez_compressed(path,counts=counts,seed=seed)
    return np.load(path)['counts'].astype(np.float64)/n

def stats(values,weights):
    # values: replications, engines, metrics. Every bootstrap draw resamples engines.
    r,n,k=values.shape
    draws=(weights@values.transpose(1,0,2).reshape(n,r*k)).reshape(2000,r,k)
    means=values.mean(1);lohi=np.quantile(draws,[.025,.975],axis=0)
    cohort=draws.mean(1)
    return means,lohi,cohort

def oracle_noise():
    m.check_lock();rng=np.random.default_rng(14142135);rows=[]
    for sub in m.SUBS:
      for policy in ['final','uniform']:
        with np.load(RUN/f'evaluation_{sub}_{policy}.npz') as ev:q=ev['q_true'];p=ev['p_true']
        z=rng.standard_normal((100,10000,2));width=q[:,2]-q[:,0]
        np.savez_compressed(RUN/f'oracle_noise_{sub}_{policy}.npz',z=z)
        for fraction in [0,.05,.10,.20]:
            noisy=np.broadcast_to(q,(100,10000,3)).copy()
            noisy[:,:,0]+=fraction*width*z[:,:,0];noisy[:,:,2]+=fraction*width*z[:,:,1]
            d=m.diagnostic(noisy,np.broadcast_to(p,noisy.shape[:-1]))
            empty=np.max(np.where(noisy<=30,m.LEVELS,0),axis=2)>np.min(np.where(noisy>30,m.LEVELS,1),axis=2)
            engine=np.stack([(d>0).mean(0),d.mean(0),(d>1e-6).mean(0),np.any(np.diff(noisy,axis=2)<0,axis=2).mean(0),empty.mean(0)],axis=1)
            for n in [m.CFG['small_eval_counts'][sub],10000]:
                w=bootstrap(sub,policy,n);draws=w@engine[:n];v=engine[:n].mean(0)
                rec=dict(setting='oracle_quantiles_plus_noise_true_probability',subset=sub,policy=policy,fitting_engines=0,evaluation_engines=n,noise_sd_fraction=fraction,noise_replications=100)
                for k,name in enumerate(['incompatibility_rate','mean_distance','tolerance_rate','crossing_rate','empty_probability_bounds_rate']):
                    rec[name]=float(v[k]);rec[name+'_lo'],rec[name+'_hi']=np.quantile(draws[:,k],[.025,.975]).tolist()
                if fraction==0:assert rec['incompatibility_rate']==0 and rec['mean_distance']==0
                rows.append(rec)
        print('ORACLE_NOISE',sub,policy,'n=10000',flush=True)
    csvsave(OUT/'synthetic_oracle_noise.csv',rows)
    m.write(RUN/'oracle_noise_complete.json',dict(groups=8,noise_replications=100,source_sha256=m.sha(__file__)))

def load_group(family,sub,arch,policy):
    source_sub='FD001' if sub=='FD003' and family!='temporal' else sub
    reps=30 if family=='temporal' else 200;result={k:[] for k in ['weighted_raw','weighted_corrected','unweighted']}
    for rep in range(reps):
        if family=='parametric':
            folder=RUN/f'parametric/{source_sub}/rep_{rep:03d}/{policy}'
            assert (folder/'complete.json').exists(),str(folder)
            fn=folder/('FD003_predictions.npz' if sub=='FD003' else 'predictions.npz')
            with np.load(fn) as f:
                np.testing.assert_array_equal(f['engine_id'],np.arange(10000))
                q=f['q'];p=f['p'];w=float(f['weight'])
                result['unweighted'].append((q,p[:,0]));result['weighted_raw'].append((q,p[:,1]));result['weighted_corrected'].append((q,p[:,1]/(w-(w-1)*p[:,1])))
        else:
            for weighted in [True,False]:
                cohort_root=RUN/'secondary_cpu' if family=='covariate' else RUN
                folder=cohort_root/f"{family}/{source_sub}/{arch}/rep_{rep:03d}/{'weighted' if weighted else 'unweighted'}"
                assert (folder/'complete.json').exists(),str(folder)
                fn=folder/(f'FD003_{policy}_predictions.npz' if sub=='FD003' and family=='covariate' else f'{policy}_predictions.npz')
                with np.load(fn) as f:
                    np.testing.assert_array_equal(f['engine_id'],np.arange(10000))
                    q=f['q'];logit=f['logit'];w=float(f['weight'])
                    result['weighted_raw' if weighted else 'unweighted'].append((q,expit(logit)))
                    if weighted:result['weighted_corrected'].append((q,expit(logit-np.log(w))))
    return result

def collect(controls_only=False):
    m.check_lock();summary=[];perrep=[];contrasts=[]
    gate=json.loads((OUT/'reproduction_gate.json').read_text())
    for sub in m.SUBS:
     for family,arch in [('temporal','lstm'),('temporal','hybrid'),('covariate','covariate'),('parametric','independent_exact_family')]:
      if controls_only and family=='temporal':continue
      for policy in ['final','uniform']:
        group=load_group(family,sub,arch,policy)
        with np.load(RUN/f'evaluation_{sub}_{policy}.npz') as ev:truth=ev['p_true'];qt=ev['q_true']
        for variant,outputs in group.items():
            nrep=len(outputs);base=dict(family=family,subset=sub,architecture=arch,policy=policy,variant=variant,fitting_engines=m.CFG['fit_counts'][sub],fitting_replications=nrep)
            values=[]
            for q,p in outputs:
                assert np.isfinite(q).all() and np.isfinite(p).all() and np.all((p>=0)&(p<=1))
                d=m.diagnostic(q,p)
                empty=np.max(np.where(q<=30,m.LEVELS,0),axis=1)>np.min(np.where(q>30,m.LEVELS,1),axis=1)
                values.append(np.stack([d>0,d,d>1e-6,np.any(np.diff(q,axis=1)<0,axis=1),np.abs(q-qt).mean(1),(p-truth)**2,empty,(d>0)&(d<=1e-6)],axis=1))
            values=np.array(values)
            for n in [m.CFG['small_eval_counts'][sub],10000]:
                weights=bootstrap(sub,policy,n);means,ci,draws=stats(values[:,:n],weights);avg=means.mean(0)
                rec=dict(**base,evaluation_engines=n)
                names=['incompatibility_rate','mean_distance','tolerance_rate','crossing_rate','oracle_quantile_mae','probability_error_squared','empty_probability_bounds_rate','tiny_positive_distance_rate']
                for k,name in enumerate(names):
                    rec[name]=float(avg[k]);rec[name+'_lo'],rec[name+'_hi']=np.quantile(draws[:,k],[.025,.975]).tolist()
                rec['training_rate_min']=float(means[:,0].min());rec['training_rate_max']=float(means[:,0].max())
                rec['training_rate_p025'],rec['training_rate_p975']=np.quantile(means[:,0],[.025,.975]).tolist()
                summary.append(rec)
                for i in range(nrep):
                    rr=dict(**base,evaluation_engines=n,replication=i)
                    for k,name in enumerate(names):rr[name]=float(means[i,k]);rr[name+'_lo']=float(ci[0,i,k]);rr[name+'_hi']=float(ci[1,i,k])
                    perrep.append(rr)
                if n==10000 and policy=='final':
                    for real_arch in (['LSTM' if arch=='lstm' else 'Hybrid'] if family=='temporal' else ['LSTM','Hybrid']):
                        real=next(r for r in gate['summary'] if r['subset']==sub and r['model']==real_arch)
                        contrasts.append(dict(**base,real_architecture=real_arch,real_event_variant='weighted_raw',real_initialization_seeds=5,null_initializations_per_fitting_fleet=1,same_event_output_convention=variant=='weighted_raw',real_evaluation_engines=real['engines'],null_evaluation_engines=n,real_rate=real['recomputed_mean']/100,null_mean=rec['incompatibility_rate'],null_training_p975=rec['training_rate_p975'],null_training_max=rec['training_rate_max'],exceeds_prespecified_benchmark=(real['recomputed_mean']/100)>rec['training_rate_p975'],scope='descriptive benchmark, not a matched five-initialization null test; cross-variant contrasts are descriptive; not a universal null rejection'))
        print('COLLECTED',family,sub,arch,policy,flush=True)
    prefix='controls' if controls_only else 'synthetic'
    csvsave(OUT/f'{prefix}_summary.csv',summary);csvsave(OUT/f'{prefix}_per_replication.csv',perrep);csvsave(OUT/('controls_real_vs_synthetic.csv' if controls_only else 'real_vs_synthetic.csv'),contrasts)
    m.write(RUN/('controls_collection_complete.json' if controls_only else 'collection_complete.json'),dict(scope='complete control cohorts' if controls_only else 'all complete cohorts',summary_rows=len(summary),per_replication_rows=len(perrep),contrast_rows=len(contrasts),source_sha256=m.sha(__file__),protocol=m.check_lock()))
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='oracle-noise':oracle_noise()
    elif len(sys.argv)>1 and sys.argv[1]=='controls':collect(controls_only=True)
    else:collect()

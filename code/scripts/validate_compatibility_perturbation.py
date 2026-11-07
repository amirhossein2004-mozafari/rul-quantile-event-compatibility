from pathlib import Path
import sys, json, csv, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/compatibility_null_validation'
def diagnostic(q,p):
    levels=np.array([.05,.5,.95])
    lower=np.max(np.where(q<=30,levels,0),axis=-1)
    upper=np.min(np.where(q>30,levels,1),axis=-1)
    return np.maximum(np.maximum(lower-p,p-upper),0),lower>upper

def main():
    assert json.loads((OUT/'reproduction_gate.json').read_text())['status']=='PASS'
    # Boundary/equality, upper/lower violation, and crossing fixtures.
    q=np.array([[30,40,50],[10,20,30],[40,50,60],[10,20,40],[40,20,50.]])
    p=np.array([.05,.95,.1,.49,.3])
    d,empty=diagnostic(q,p)
    np.testing.assert_allclose(d,[0,0,.05,.01,.25],atol=1e-15)
    assert empty.tolist()==[False,False,False,False,True]
    rng=np.random.default_rng(2026103101);brng=np.random.default_rng(2026103102)
    fractions=[0,.05,.10,.20];summary=[];perrun=[];hashes={}
    gate=json.loads((OUT/'reproduction_gate.json').read_text())
    for sub in ['FD001','FD002','FD003','FD004']:
      for model in ['lstm','hybrid']:
        paths=sorted((ROOT/f'results/fair_comparison_step2/final/{sub}/{model}').glob('seed_*/test_predictions.csv'))
        assert len(paths)==5
        engine_metrics=[];stored={};allids=None
        for index,path in enumerate(paths):
            with path.open(encoding='utf-8-sig',newline='') as f:rows=sorted(csv.DictReader(f),key=lambda r:int(r['engine_id']))
            ids=np.array([int(r['engine_id']) for r in rows]);n=len(ids)
            if allids is None:allids=ids
            np.testing.assert_array_equal(ids,allids)
            q=np.array([[float(r[k]) for k in ['q05','q50','q95']] for r in rows]);p=np.array([float(r['p_Raw']) for r in rows])
            assert np.isfinite(q).all() and np.isfinite(p).all() and np.all(np.diff(q,axis=1)>=0)
            z=rng.standard_normal((100,n,2));width=q[:,2]-q[:,0];metrics=[]
            stored[f'q_{index}']=q;stored[f'p_{index}']=p;stored[f'z_{index}']=z
            hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
            seed=int(path.parent.name.split('_')[1])
            for frac in fractions:
                noisy=np.broadcast_to(q,(100,n,3)).copy()
                noisy[:,:,0]+=frac*width*z[:,:,0];noisy[:,:,2]+=frac*width*z[:,:,1]
                gap,empty=diagnostic(noisy,p)
                crossing=np.any(np.diff(noisy,axis=2)<0,axis=2)
                values=np.stack([(gap>0).mean(0),gap.mean(0),(gap>1e-6).mean(0),crossing.mean(0),empty.mean(0)],axis=1)
                metrics.append(values)
                perrun.append(dict(subset=sub,model=model,seed=seed,engines=n,noise_replications=100,noise_sd_fraction=frac,rate=float(values[:,0].mean()),distance=float(values[:,1].mean()),tolerance_rate=float(values[:,2].mean()),crossing_rate=float(values[:,3].mean()),empty_rate=float(values[:,4].mean())))
            engine_metrics.append(metrics)
        # Models and perturbation replicates are averaged inside each engine.
        em=np.mean(engine_metrics,axis=0) # levels, engines, metrics
        indices=brng.integers(0,n,size=(2000,n))
        draws=np.stack([em[:,ix,:].mean(1) for ix in indices])
        delta=draws-draws[:,0:1,:]
        stored.update(engine_ids=allids,engine_metrics=em,bootstrap_indices=indices,bootstrap_metrics=draws)
        np.savez_compressed(OUT/f'perturbation_{sub}_{model}.npz',**stored)
        for j,frac in enumerate(fractions):
            rec=dict(subset=sub,model=model,engines=n,models=5,noise_replications=100,noise_sd_fraction=frac)
            for k,name in enumerate(['rate','distance','tolerance_rate','crossing_rate','empty_rate']):
                rec[name]=float(em[j,:,k].mean());rec[name+'_lo'],rec[name+'_hi']=np.quantile(draws[:,j,k],[.025,.975]).tolist()
            rec['rate_delta']=float(em[j,:,0].mean()-em[0,:,0].mean())
            rec['rate_delta_lo'],rec['rate_delta_hi']=np.quantile(delta[:,j,0],[.025,.975]).tolist()
            summary.append(rec)
        ref=next(r for r in gate['summary'] if r['subset']==sub and r['model']==('LSTM' if model=='lstm' else 'Hybrid'))
        np.testing.assert_allclose(em[0,:,2].mean()*100,ref['recomputed_mean'],atol=1e-12)
        print(sub,model,'n=',n,'rates=',[round(r['rate']*100,4) for r in summary[-4:]],flush=True)
    for name,rows in [('perturbation_summary.csv',summary),('perturbation_per_run.csv',perrun)]:
        with (OUT/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'perturbation_complete.json').write_text(json.dumps(dict(status='complete',models=40,groups=8,noise_replications=100,engine_counts=[100,259,100,248],bootstrap_draws=2000,input_sha256=hashes,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),protocol_sha256=hashlib.sha256((OUT/'protocol.md').read_bytes()).hexdigest()),indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,4,figsize=(14,7),sharex=True)
    for ax,(sub,model) in zip(axes.flat,[(s,m) for m in ['lstm','hybrid'] for s in ['FD001','FD002','FD003','FD004']]):
        g=[r for r in summary if r['subset']==sub and r['model']==model]
        ax.plot([100*r['noise_sd_fraction'] for r in g],[100*r['rate'] for r in g],marker='o')
        ax.fill_between([100*r['noise_sd_fraction'] for r in g],[100*r['rate_lo'] for r in g],[100*r['rate_hi'] for r in g],alpha=.2)
        ax.set_title(f"{sub} {model} (n={g[0]['engines']} engines)");ax.set_ylabel('Incompatible (%)');ax.set_xlabel('Noise SD (% interval width)')
    fig.suptitle('Frozen equal-search models; 95% engine-bootstrap CIs conditional on fits/noise')
    fig.tight_layout();fig.savefig(OUT/'perturbation_curve.png',dpi=180);fig.savefig(OUT/'perturbation_curve.pdf');plt.close(fig)
if __name__=='__main__':main()

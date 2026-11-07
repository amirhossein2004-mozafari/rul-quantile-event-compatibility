"""Independent arithmetic reconstruction of the nominal cross-head diagnostic."""
from pathlib import Path
import argparse,csv,hashlib,json,math,statistics,collections
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def close(a,b):assert math.isclose(float(a),float(b),abs_tol=2e-12,rel_tol=2e-12),(a,b)
def constraints(q,p):
    # Evaluate each implication separately, rather than the analysis L/U algorithm.
    excess=[0.]
    for value,level in zip(q,[.05,.5,.95]):
        excess.append(max(level-p,0.) if value<=30 else max(p-level,0.))
    return max(excess)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--output-dir',type=Path,default=Path('cross_head_review_outputs'));ap.add_argument('--workspace',action='store_true')
    args=ap.parse_args();root=args.root.resolve();out=args.output_dir.resolve();assert not out.exists(),'Choose a fresh output directory'
    if not args.workspace:
        manifest=json.loads((root/'FILE_MANIFEST.json').read_text(encoding='utf-8'))
        for n,h in manifest['files'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==h,n
    # Boundary cases include equality at 30 and conservative upper equality.
    for q,p,expected in [([10,20,25],.90,.05),([35,40,50],.10,.05),([10,30,50],.49,.01),([30,40,50],.01,.04),([10,20,30],.94,.01),([10,20,30],.95,0),([10,40,50],.5,0),([10,40,50],.51,.01),([10,20,25],1,0),([35,40,50],0,0)]:close(constraints(q,p),expected)
    base=root/'results/contribution_step12';per=read(base/'per_engine.csv')
    actual={(r['subset'],r['model'],int(r['seed']),r['method'],int(r['engine_id'])):r for r in per};assert len(actual)==len(per)==28280
    by_run=collections.defaultdict(list);seen=set();models=0
    for path in sorted((root/'results/fair_comparison_step2/final').glob('*/*/seed_*/test_predictions.csv')):
        sub=path.parents[2].name;model='LSTM' if path.parents[1].name=='lstm' else 'Hybrid';seed=int(path.parent.name.removeprefix('seed_'));rows=read(path);models+=1
        truth=[float(s) for s in (root/f'data/raw/cmapss/RUL_{sub}.txt').read_text().split()]
        assert len(rows)==len(truth) and len({r['engine_id'] for r in rows})==len(rows)
        for r in rows:
            eid=int(r['engine_id']);y=float(r['raw_y']);assert y==truth[eid-1]
            q=[float(r[k]) for k in ['q05','q50','q95']];assert q[0]<=q[1]<=q[2]
            # Equivalent piecewise bound construction covers all threshold bins.
            if 30<q[0]:bounds=(0.,.05)
            elif 30<q[1]:bounds=(.05,.5)
            elif 30<q[2]:bounds=(.5,.95)
            else:bounds=(.95,1.)
            for method in ['Raw','Bayes','Temp','ShiftTemp']:
                key=(sub,model,seed,method,eid);target=actual[key];seen.add(key);p=float(r['p_'+method]);d=constraints(q,p)
                for name,value in zip(['q05','q50','q95','probability','lower_probability','upper_probability','distance'],q+[p,*bounds,d]):close(target[name],value)
                expected={'incompatible':int(d>1e-6),'q95_below_event':int(q[2]<30),'q95_tail_conflict':int(q[2]<30 and p<.95-1e-6),'q05_above_event':int(q[0]>30),'q05_tail_conflict':int(q[0]>30 and p>.05+1e-6)}
                for n,value in expected.items():assert int(target[n])==value,(key,n)
                by_run[key[:4]].append(dict(**expected,distance=d,loss=(p-int(y<=30))**2))
    assert seen==set(actual) and models==40 and len(by_run)==160
    runs=read(base/'per_run.csv');assert len(runs)==160
    recomputed={}
    for r in runs:
        key=(r['subset'],r['model'],int(r['seed']),r['method']);g=by_run[key]
        values=dict(n=len(g),incompatible=sum(x['incompatible'] for x in g),fraction=statistics.fmean(x['incompatible'] for x in g),mean_distance=statistics.fmean(x['distance'] for x in g),max_distance=max(x['distance'] for x in g),Brier=statistics.fmean(x['loss'] for x in g))
        for n in ['q95_below_event','q95_tail_conflict','q05_above_event','q05_tail_conflict']:values[n]=sum(x[n] for x in g)
        for tol in [1e-8,1e-4,.01]:values['fraction_tol_'+str(tol)]=statistics.fmean(x['distance']>tol for x in g)
        for name,value in values.items():close(r[name],value)
        recomputed[key]=values
    summaries=read(base/'summary.csv');assert len(summaries)==32
    for r in summaries:
        g=[v for k,v in recomputed.items() if (k[0],k[1],k[3])==(r['subset'],r['model'],r['method'])];assert len(g)==5
        close(r['runs'],5);close(r['n_per_run'],g[0]['n'])
        for name in ['fraction','mean_distance','Brier','q95_below_event','q95_tail_conflict','q05_above_event','q05_tail_conflict']:
            close(r[name+'_mean'],statistics.fmean(x[name] for x in g));close(r[name+'_sd'],statistics.stdev(x[name] for x in g))
        close(r['incompatible_count_min'],min(x['incompatible'] for x in g));close(r['incompatible_count_max'],max(x['incompatible'] for x in g))
    for r in read(base/'extremal_examples.csv'):
        best=sorted([x for x in per if x['method']==r['method']],key=lambda x:(-float(x['distance']),x['subset'],x['model'],int(x['seed']),int(x['engine_id'])))[0]
        assert best==r
    raw=[r for r in summaries if r['method']=='Raw'];temp=[r for r in summaries if r['method']=='Temp']
    assert all(float(t['fraction_mean'])>float(r['fraction_mean']) for r,t in zip(raw,temp))
    for r in runs:
        assert float(r['fraction_tol_1e-08'])>=float(r['fraction'])>=float(r['fraction_tol_0.0001'])>=float(r['fraction_tol_0.01'])
    result=dict(status='pass',models=models,method_runs=len(runs),engine_method_records=len(per),summary_groups=len(summaries),boundary_cases=10,raw_mean_fraction_range=[min(float(r['fraction_mean']) for r in raw),max(float(r['fraction_mean']) for r in raw)],Temp_increases_group_mean=8,
        max_fraction_change_at_1e_4=max(abs(float(r['fraction_tol_0.0001'])-float(r['fraction'])) for r in runs),
        scope='Arithmetic and nominal implications only; no fitting, selection, full distribution validation, scientific novelty assessment or independent review')
    out.mkdir(parents=True);(out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

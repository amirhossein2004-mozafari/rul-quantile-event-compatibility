from pathlib import Path
import csv, json, statistics, hashlib, math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/compatibility_null_validation'
table=ROOT/'paper/tables/compact_table2.md'
expected={}
for line in table.read_text(encoding='utf-8').splitlines():
    c=[v.strip() for v in line.split('|')]
    if len(c)>5 and c[1].startswith('FD'):
        expected[c[1],c[2]]=(int(c[3]),c[4].split(' ± ')[0],c[4].split(' ± ')[1])
paths=sorted((ROOT/'results/fair_comparison_step2/final').glob('*/*/seed_*/test_predictions.csv'))
runs=[]; hashes={str(table.relative_to(ROOT)):hashlib.sha256(table.read_bytes()).hexdigest()}
for path in paths:
    sub=path.parents[2].name; model={'lstm':'LSTM','hybrid':'Hybrid'}[path.parents[1].name]
    seed=int(path.parent.name.split('_')[1])
    with path.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    ids=[int(r['engine_id']) for r in rows]
    assert len(ids)==len(set(ids)) and set(ids)==set(range(1,len(ids)+1))
    distances=[]
    for r in rows:
        q=[float(r[k]) for k in ['q05','q50','q95']];p=float(r['p_Raw'])
        assert all(math.isfinite(v) for v in q+[p]) and q==sorted(q) and 0<=p<=1
        lower=max([0]+[t for t,v in zip([.05,.5,.95],q) if v<=30])
        upper=min([1]+[t for t,v in zip([.05,.5,.95],q) if v>30])
        distances.append(max(lower-p,p-upper,0))
    runs.append(dict(subset=sub,model=model,seed=seed,engines=len(ids),rate=statistics.fmean(d>1e-6 for d in distances),strict_rate=statistics.fmean(d>0 for d in distances),distance=statistics.fmean(distances)))
    hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
summary=[]
for (sub,model),(n,mean,sd) in expected.items():
    g=[r for r in runs if (r['subset'],r['model'])==(sub,model)]
    complete=len(g)==5 and {r['seed'] for r in g}=={1101,1202,1303,1404,1505} and all(r['engines']==n for r in g)
    m=100*statistics.fmean(r['rate'] for r in g);s=100*statistics.stdev(r['rate'] for r in g)
    summary.append(dict(subset=sub,model=model,engines=n,published_mean=mean,recomputed_mean=m,published_sd=sd,recomputed_sd=s,strict_mean=100*statistics.fmean(r['strict_rate'] for r in g),mean_distance=statistics.fmean(r['distance'] for r in g),match=complete and f'{m:.2f}'==mean and f'{s:.2f}'==sd))
passed=len(paths)==40 and len(summary)==8 and all(r['match'] for r in summary)
result=dict(status='PASS' if passed else 'FAIL_STOP',definition='Table: d>1e-6; strict: d>0',models=len(paths),unique_engines=707,summary=summary,runs=runs,input_sha256=hashes)
(OUT/'reproduction_gate.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
lines=['Table 2 reproduction gate: '+result['status'],'','Every row uses five models on the same engines; engines are not multiplied by five.','']
for r in summary:
    lines.append(f"{r['subset']} {r['model']}: n={r['engines']}; published {r['published_mean']}%; reproduced {r['recomputed_mean']:.8f}%; SD {r['recomputed_sd']:.8f}; strict {r['strict_mean']:.8f}%; match={r['match']}")
(OUT/'reproduction_gate.txt').write_text('\n'.join(lines),encoding='utf-8')
print('\n'.join(lines))
if not passed: raise SystemExit(2)

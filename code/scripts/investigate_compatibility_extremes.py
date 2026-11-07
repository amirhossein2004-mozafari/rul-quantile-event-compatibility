from pathlib import Path
import csv,json,numpy as np
from scipy.special import expit
out=Path('reports/compatibility_null_validation');run=out/'synthetic';rows=[]
for p in sorted((run/'temporal').rglob('complete.json')):
 r=json.loads(p.read_text());i=r['identity'];folder=p.parent
 with np.load(folder/'final_predictions.npz') as f:q=f['q'];eta=f['logit'];w=float(f['weight'])
 with np.load(run/f"evaluation_{i['subset']}_final.npz") as e:qt=e['q_true']
 d=json.loads((folder/'data.json').read_text())
 rec=dict(subset=i['subset'],architecture=i['architecture'],replication=i['replication'],weighted=i['weighted'],fitting_engines=i['fitting_engines'],evaluation_engines=10000,fitting_windows=d['windows'],epochs=len(r['history']),first_loss=r['history'][0]['loss'],last_loss=r['history'][-1]['loss'],q95_at_or_below30_rate=float((q[:,2]<=30).mean()),q05_above30_rate=float((q[:,0]>30).mean()),p_raw_mean=float(expit(eta).mean()))
 for j,name in enumerate(['q05','q50','q95']):
    rec[name+'_mean']=float(q[:,j].mean());rec[name+'_min']=float(q[:,j].min());rec[name+'_max']=float(q[:,j].max());rec[name+'_oracle_MAE']=float(abs(q[:,j]-qt[:,j]).mean())
 rows.append(rec)
with (out/'temporal_extreme_rate_investigation.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for r in rows:
 if r['subset']=='FD001' and r['replication']==0:print(json.dumps(r))

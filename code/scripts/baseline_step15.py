"""Retrospective matched-budget TCN/GRU extension; never overwrites prior studies."""
from pathlib import Path
import sys,hashlib,json,time,os,shutil
from concurrent.futures import ProcessPoolExecutor
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import numpy as np
import pandas as pd
import torch
from torch import nn
import fair_comparison_step2 as b
from src.models.simple_quantile_risk import QuantileRiskBase,TCNQuantileRisk
OUT=ROOT/'results/baseline_step15';BASE=ROOT/'results/fair_comparison_step2'
class GRU(QuantileRiskBase):
    def __init__(self):
        super().__init__();self.gru=nn.GRU(18,64,batch_first=True)
    def encode(self,x):return self.gru(x)[0][:,-1,:]
def factory(name):return {'tcn':TCNQuantileRisk,'gru':GRU}[name]()
COUNTS={n:sum(p.numel() for p in factory(n).parameters()) for n in ['tcn','gru']}
b.OUT=OUT;b.MODELS=['tcn','gru'];b.make_model=factory;b.PARAMETER_COUNTS=COUNTS
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):b.atomic(v,p)
def source():return {n:sha(ROOT/n) for n in ['scripts/baseline_step15.py','scripts/fair_comparison_step2.py','reports/baseline_step15_protocol.md','src/models/simple_quantile_risk.py','src/models/hybrid_lstm_tcn.py','src/training/pcgrad_ablation.py']}
def validate():
    lock=load(OUT/'protocol.json');assert lock['sources']==source()
    for n,h in lock['inherited_inputs'].items():assert sha(ROOT/n)==h,n
    return sha(OUT/'protocol.json')
b.validate_lock=validate
def init():
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
def job(args):return b.train_one(*args)
def pool(jobs):
    with ProcessPoolExecutor(max_workers=6,initializer=init) as executor:
        for i,p in enumerate(executor.map(job,jobs),1):write(OUT/'progress.json',dict(done=i,total=len(jobs),last=p,unix=time.time()))
def prepare():
    assert not (OUT/'protocol.json').exists();OUT.mkdir(parents=True,exist_ok=True)
    archive=ROOT/'archive/baseline_step15_before';archive.mkdir(parents=True,exist_ok=True)
    for name in ['manuscript_v4.md','manuscript_v4.pdf','supplement_matched_endpoints.md','supplement_matched_endpoints.pdf','references.bib','submission_header.tex']:shutil.copy2(ROOT/'paper'/name,archive/name)
    inherited={}
    for p in (BASE/'data').rglob('*'):
        if not p.is_file():continue
        q=OUT/'data'/p.relative_to(BASE/'data');q.parent.mkdir(parents=True,exist_ok=True);os.link(p,q);inherited[p.relative_to(ROOT).as_posix()]=sha(p)
    inherited[(BASE/'protocol.json').relative_to(ROOT).as_posix()]=sha(BASE/'protocol.json')
    for p in (BASE/'final').rglob('*'):
        if p.is_file() and p.name in ['final.pt','test_predictions.csv','calibration_predictions.csv']:inherited[p.relative_to(ROOT).as_posix()]=sha(p)
    write(OUT/'protocol.json',dict(created_unix=time.time(),sources=source(),inherited_inputs=inherited,models=COUNTS,grid=b.LRS,seeds=b.SEEDS,scope='Retrospective fixed split; equal candidate/epoch budget, not equal wall time or nested CV; forty old LSTM/hybrid fits reused, forty new TCN/GRU fits'))
def summary():
    new=pd.read_csv(OUT/'per_run.csv');old=pd.read_csv(BASE/'per_run.csv');df=pd.concat([old,new],ignore_index=True);assert len(df)==80
    df.to_csv(OUT/'combined_per_run.csv',index=False)
    keys=['RMSE','MAE','Brier_Raw','Winkler_Exact','Coverage_Exact','Width_Exact','parameters']
    df.groupby(['subset','model'])[keys].agg(['mean','std']).to_csv(OUT/'combined_summary.csv')
    from uncertainty_step14_statistics import crossed_bootstrap
    rows=[]
    for si,sub in enumerate(b.SUBSETS):
        arrays={}
        for arm in ['lstm','hybrid','tcn','gru']:
            parent=BASE if arm in ['lstm','hybrid'] else OUT
            frames=[pd.read_csv(parent/'final'/sub/arm/f'seed_{s}'/'test_predictions.csv',float_precision='round_trip') for s in b.SEEDS]
            truth=np.loadtxt(ROOT/f'data/raw/cmapss/RUL_{sub}.txt')
            for f in frames:np.testing.assert_array_equal(f.raw_y,truth)
            arrays[arm]=np.stack([(np.clip(f.q50,0,125)-np.minimum(f.raw_y,125)).to_numpy()**2 for f in frames])
        for ai,arm in enumerate(['lstm','tcn','gru']):
            stat,draws=crossed_bootstrap(arrays['hybrid'],arrays[arm],seed=171500+si*3+ai)
            rows.append(dict(subset=sub,contrast='hybrid-'+arm,**stat));np.savez_compressed(OUT/f'bootstrap_{sub}_{arm}.npz',**draws)
    pd.DataFrame(rows).to_csv(OUT/'paired_statistics.csv',index=False)
def run():
    validate();pool(b.search_jobs());selected=b.select_configs();pool(b.final_jobs(selected))
    paths=[v[5]/'final.pt' for v in b.final_jobs(selected)];assert len(paths)==40
    write(OUT/'fit_complete.json',dict(frozen_unix=time.time(),files={p.relative_to(ROOT).as_posix():sha(p) for p in paths},sources=source()))
    init();b.summarize=lambda:None;b.evaluate(selected);summary();verify()
def verify():
    validate();fit=load(OUT/'fit_complete.json');gate=load(OUT/'evaluation_start.json');assert fit['frozen_unix']<=__import__('datetime').datetime.fromisoformat(gate['started_utc']).timestamp()
    for n,h in fit['files'].items():assert sha(ROOT/n)==h
    df=pd.read_csv(OUT/'per_run.csv');assert len(df)==40
    for r in df.itertuples():
        folder=OUT/'final'/r.subset/r.model/f'seed_{r.seed}';p=pd.read_csv(folder/'test_predictions.csv',float_precision='round_trip');truth=np.loadtxt(ROOT/f'data/raw/cmapss/RUL_{r.subset}.txt');np.testing.assert_array_equal(p.raw_y,truth)
        for k,v in b.point_metrics(truth,p.q50).items():np.testing.assert_allclose(getattr(r,k),v,rtol=1e-10)
        model=factory(r.model);c=torch.load(folder/'final.pt',weights_only=True);model.load_state_dict(c['state']);x,_,_=b.test_data(r.subset);actual=b.predict(model,x);np.testing.assert_allclose(actual,p[['q05','q50','q95','logit']].to_numpy(),atol=1e-4,rtol=1e-5)
        np.testing.assert_allclose(r.Brier_Raw,np.mean((p.p_Raw-(truth<=30))**2),rtol=1e-10)
    write(OUT/'verification.json',dict(status='pass',new_models=40,reused_models=40,tuning_candidates=24,all_new_forward_replayed=True,selection_validation_only=True,independent_review='UNAVAILABLE'))
if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--run' in sys.argv:run()
    else:raise SystemExit('Use --prepare or --run')

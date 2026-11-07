"""15 additional paired split/seed runs; preserve and combine five archived controls."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import argparse,hashlib,json,random,sys,time,csv
import numpy as np
import pandas as pd
import torch
import joblib
from sklearn.model_selection import train_test_split
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.data.preprocessing import RegimeAwarePreprocessor,get_cmapss_column_names,create_sliding_windows,SELECTED_SENSOR_COLUMNS,SETTING_COLUMNS
from src.models.simple_quantile_risk import make_model
from src.training.pcgrad import PCGradOptimizer
from src.training.pcgrad_ablation import reset_seed,task_losses,permutation_for_epoch,state_hash,tensor_hash
OUT=ROOT/'results/uncertainty_step14';PROTOCOL=ROOT/'reports/uncertainty_step14_protocol.md'
SUBSETS=['FD001','FD002','FD003','FD004'];NEW=list(range(1001,1016));OLD=[101,202,303,404,505]
FEATURES=SELECTED_SENSOR_COLUMNS+[c+'_scaled' for c in SETTING_COLUMNS]
sha=lambda p:hashlib.file_digest(Path(p).open('rb'),'sha256').hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,r):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(r,indent=2),encoding='utf-8');tmp.replace(p)
def sources():return {n:sha(ROOT/n) for n in ['scripts/uncertainty_step14_campaign.py','reports/uncertainty_step14_protocol.md','src/data/preprocessing.py','src/models/simple_quantile_risk.py','src/models/hybrid_lstm_tcn.py','src/training/pcgrad.py','src/training/pcgrad_ablation.py']}
def configure():
    torch.set_num_threads(1)
    if torch.get_num_interop_threads()!=1:torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
def prepare_one(job):
    sub,seed=job;folder=OUT/'data'/sub/f'seed_{seed}';folder.mkdir(parents=True,exist_ok=True)
    if (folder/'metadata.json').exists():
        m=load(folder/'metadata.json');assert sha(folder/'training.npz')==m['training_sha256'];return m
    frame=pd.read_csv(ROOT/f'data/raw/cmapss/train_{sub}.txt',sep=r'\s+',header=None,names=get_cmapss_column_names())
    frame['RUL']=frame.groupby('engine_id').cycle.transform('max')-frame.cycle
    ids=np.sort(frame.engine_id.unique());fit,held=train_test_split(ids,test_size=.2,random_state=seed);assert not set(fit)&set(held)
    training=frame[frame.engine_id.isin(fit)].copy()
    with threadpool_limits(limits=1):
        prep=RegimeAwarePreprocessor(n_regimes=6 if sub in ['FD002','FD004'] else 1,seed=seed);prep.fit(training)
        scaled=prep.transform(training)
    x,y,z=create_sliding_windows(scaled,FEATURES,30,125,30);assert 0<z.sum()<len(z)
    np.savez_compressed(folder/'training.npz',X=x,y=y,z=z);joblib.dump(prep,folder/'preprocessor.joblib')
    m=dict(subset=sub,seed=seed,fit_engines=[int(v) for v in fit],heldout_engines=[int(v) for v in held],samples=len(y),positive=int(z.sum()),negative=int(len(z)-z.sum()),pos_weight=float(np.float32((len(z)-z.sum())/z.sum())),training_sha256=sha(folder/'training.npz'),preprocessor_sha256=sha(folder/'preprocessor.joblib'),raw_training_sha256=sha(ROOT/f'data/raw/cmapss/train_{sub}.txt'),prepared_unix=time.time())
    write(folder/'metadata.json',m);print('PREPARED',sub,seed,len(y),flush=True);return m
def prepare():
    OUT.mkdir(parents=True,exist_ok=True);lock=OUT/'protocol_lock.json'
    if lock.exists():assert load(lock)['source_sha256']==sources()
    else:write(lock,dict(created_unix=time.time(),scope='Retrospective, previously examined C-MAPSS; 15 new plus five verified archived split/seed pairs',source_sha256=sources(),new_models=135))
    with ProcessPoolExecutor(max_workers=6,initializer=configure) as pool:list(pool.map(prepare_one,[(s,n) for s in SUBSETS for n in NEW]))
    write(OUT/'prepared.json',dict(status='complete',partitions=60,files={p.relative_to(ROOT).as_posix():sha(p) for p in (OUT/'data').rglob('*') if p.is_file()}))
def train_one(job):
    sub,seed,arm=job;folder=OUT/'models'/sub/f'seed_{seed}'/arm;folder.mkdir(parents=True,exist_ok=True)
    final=folder/'final.pt'
    if final.exists():
        r=load(folder/'training.json');assert sha(final)==r['checkpoint_sha256'];return r
    datafolder=OUT/'data'/sub/f'seed_{seed}';meta=load(datafolder/'metadata.json');assert sha(datafolder/'training.npz')==meta['training_sha256']
    data=np.load(datafolder/'training.npz');x=torch.from_numpy(data['X']);y=torch.from_numpy(data['y']).reshape(-1,1);z=torch.from_numpy(data['z']).reshape(-1,1)
    reset_seed(seed);model=make_model('hybrid' if arm=='pcgrad' else arm);init=state_hash(model.state_dict())
    optimizer=torch.optim.AdamW(model.parameters(),lr=.0005,weight_decay=.0001)
    shared=[p for n,p in model.named_parameters() if not n.startswith(('median_head.','lower_delta_head.','upper_delta_head.','risk_head.'))]
    wrapper=PCGradOptimizer(optimizer,shared_params=shared,reduction='sum',seed=seed);weight=torch.tensor([meta['pos_weight']],dtype=torch.float32)
    history=[];started=time.time();progress=folder/'progress.pt'
    if progress.exists():
        state=torch.load(progress,weights_only=True);assert state['protocol_sha256']==sha(PROTOCOL)
        model.load_state_dict(state['state']);optimizer.load_state_dict(state['optimizer']);torch.set_rng_state(state['rng']);history=state['history'];started=state['started_unix']
    for epoch in range(len(history),16):
        model.train();order=permutation_for_epoch(len(x),seed,epoch);rng=hashlib.sha256();total=0.;conflicts=0
        for batch in order.split(128):
            rng.update(torch.get_rng_state().numpy().tobytes());optimizer.zero_grad(set_to_none=True)
            a,b=task_losses(model(x[batch]),y[batch],z[batch],weight);wrapper.pc_backward([a,b],project=arm=='pcgrad')
            torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);optimizer.step();total+=float((a+b).detach())*len(batch);conflicts+=wrapper.last_stats['conflict']
        history.append(dict(epoch=epoch+1,samples=len(x),training_loss=total/len(x),permutation_sha256=tensor_hash(order),rng_stream_sha256=rng.hexdigest(),conflict_steps=conflicts))
        with (folder/'history.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(history[0]));w.writeheader();w.writerows(history)
        if (epoch+1)%4==0:
            torch.save(dict(state=model.state_dict(),optimizer=optimizer.state_dict(),rng=torch.get_rng_state(),history=history,started_unix=started,protocol_sha256=sha(PROTOCOL)),progress)
            print('TRAIN',sub,seed,arm,epoch+1,'/16',flush=True)
    checkpoint=dict(model_state_dict=model.state_dict(),subset=sub,seed=seed,arm=arm,epochs=16,initial_state_sha256=init,final_state_sha256=state_hash(model.state_dict()),protocol_sha256=sha(PROTOCOL),training_input_sha256=meta['training_sha256'])
    torch.save(checkpoint,final)
    r={k:v for k,v in checkpoint.items() if k!='model_state_dict'};r.update(checkpoint_sha256=sha(final),history_sha256=sha(folder/'history.csv'),started_unix=started,completed_unix=time.time(),parameters=sum(p.numel() for p in model.parameters()))
    write(folder/'training.json',r);return r
def train():
    assert load(OUT/'protocol_lock.json')['source_sha256']==sources();assert not (OUT/'fit_complete.json').exists()
    assert load(OUT/'prepared.json')['status']=='complete'
    jobs=[(s,n,m) for s in SUBSETS for n in NEW for m in ['lstm','hybrid']]+[('FD001',n,'pcgrad') for n in NEW]
    with ProcessPoolExecutor(max_workers=6,initializer=configure) as pool:records=list(pool.map(train_one,jobs))
    assert len(records)==135
    for n in NEW:
        a=load(OUT/'models/FD001'/f'seed_{n}'/'hybrid/training.json');b=load(OUT/'models/FD001'/f'seed_{n}'/'pcgrad/training.json');assert a['initial_state_sha256']==b['initial_state_sha256']
        with (OUT/'models/FD001'/f'seed_{n}'/'hybrid/history.csv').open() as f:aa=list(csv.DictReader(f))
        with (OUT/'models/FD001'/f'seed_{n}'/'pcgrad/history.csv').open() as f:bb=list(csv.DictReader(f))
        assert [(r['permutation_sha256'],r['rng_stream_sha256']) for r in aa]==[(r['permutation_sha256'],r['rng_stream_sha256']) for r in bb]
    write(OUT/'fit_complete.json',dict(status='complete',models=records,source_sha256=sources(),frozen_unix=time.time(),files={p.relative_to(ROOT).as_posix():sha(p) for p in (OUT/'models').rglob('*') if p.is_file() and p.name!='progress.pt'},new_models=135))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','train']);a=p.parse_args();{'prepare':prepare,'train':train}[a.stage]()

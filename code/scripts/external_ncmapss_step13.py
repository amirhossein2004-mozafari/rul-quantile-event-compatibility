"""Prospective DS01 protocol: dev-only preparation/training, then one frozen evaluation."""
from pathlib import Path
import argparse,collections,csv,hashlib,json,math,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/external_step13';DATA=ROOT/'data/raw/ncmapss/N-CMAPSS_DS01-005.h5'
SEEDS=[2101,2202,2303,2404,2505];EPOCHS=128
sha=lambda p:hashlib.file_digest(Path(p).open('rb'),'sha256').hexdigest()
def write(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,allow_nan=False),encoding='utf-8')
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def csvwrite(name,rows):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def check_protocol():
    lock=read('protocol_lock.json');assert sha(ROOT/'reports/external_step13_protocol.md')==lock['protocol_sha256'];return lock
def sources():return {n:sha(ROOT/n) for n in ['scripts/external_ncmapss_step13.py','src/models/simple_quantile_risk.py','src/models/hybrid_lstm_tcn.py','reports/external_step13_protocol.md','tests/test_external_ncmapss_step13.py','requirements-external-step13.txt']}
def decode(a):return [v.decode() if isinstance(v,bytes) else str(v) for v in a.reshape(-1)]

def windows(split):
    import h5py
    assert split in ['dev','test']
    with h5py.File(DATA,'r') as h:
        names=decode(h['W_var'][:])+decode(h['X_s_var'][:]);anames=decode(h['A_var'][:])
        assert anames[:2]==['unit','cycle'],anames
        a=h['A_'+split][:,:2];y=h['Y_'+split][:].reshape(-1)
        assert len(a)==len(y)==h['W_'+split].shape[0]==h['X_s_'+split].shape[0]
        assert np.isfinite(a).all() and np.isfinite(y).all() and (y>=0).all()
        starts=np.r_[0,1+np.flatnonzero(np.any(a[1:]!=a[:-1],axis=1))];ends=np.r_[starts[1:],len(a)]
        x=[];truth=[];ids=[];flights=[];excluded=[];seen=set();last={}
        for begin,end in zip(starts,ends):
            unit,cycle=map(int,a[begin]);assert (unit,cycle) not in seen;seen.add((unit,cycle))
            assert unit not in last or cycle>last[unit];last[unit]=cycle
            assert np.all(y[begin:end]==y[begin]),(split,unit,cycle,'variable within-flight label')
            if end-begin<291:
                excluded.append(dict(unit=unit,cycle=cycle,raw_rows=int(end-begin)));continue
            indices=np.arange(begin,begin+291,10)
            value=np.concatenate([h['W_'+split][indices],h['X_s_'+split][indices]],axis=1).astype(np.float32)
            assert value.shape==(30,len(names)) and np.isfinite(value).all()
            x.append(value);truth.append(y[begin+290]);ids.append(unit);flights.append(cycle)
    assert x and len(names)==18,'Unexpected channel schema; requires a documented pre-test implementation amendment'
    return dict(X=np.stack(x),raw_y=np.asarray(truth,dtype=np.float32),unit=np.array(ids),cycle=np.array(flights)),dict(features=names,engines=sorted(set(ids)),windows=len(x),excluded_flights=excluded,raw_rows=int(len(a)),source_split=split)

def prepare():
    check_protocol();assert not (OUT/'development.npz').exists()
    acq=read('acquisition.json');assert sha(DATA)==acq['sha256']
    opened=time.time();d,meta=windows('dev');meta['first_development_array_open_unix']=opened
    mean=d['X'].mean(axis=(0,1),dtype=np.float64);std=d['X'].std(axis=(0,1),dtype=np.float64);std[std==0]=1
    d['X']=((d['X']-mean)/std).astype(np.float32)
    positive=int((d['raw_y']<=30).sum());negative=len(d['raw_y'])-positive;assert positive>0 and negative>0
    np.savez_compressed(OUT/'development.npz',**d)
    np.savez_compressed(OUT/'preprocessor.npz',mean=mean,std=std)
    meta.update(positive=positive,negative=negative,pos_weight=negative/positive,development_sha256=sha(OUT/'development.npz'),preprocessor_sha256=sha(OUT/'preprocessor.npz'),hdf5_sha256=acq['sha256'],test_arrays_opened=False)
    write('development.json',meta);write('source_lock.json',dict(files=sources(),created_unix=time.time(),protocol=read('protocol_lock.json')))
    print(json.dumps(meta,indent=2),flush=True)

def train_one(job):
    name,seed=job
    import torch,random
    sys.path.insert(0,str(ROOT));from src.models.simple_quantile_risk import make_model
    torch.set_num_threads(1)
    if torch.get_num_interop_threads()!=1:torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
    directory=OUT/'models'/name/f'seed_{seed}'
    if directory.exists():
        record=json.loads((directory/'training.json').read_text());assert record['model']==name and record['seed']==seed and record['epochs']==EPOCHS
        assert record['checkpoint_sha256']==sha(directory/'final.pt') and record['history_sha256']==sha(directory/'history.csv')
        assert record['protocol_sha256']==read('protocol_lock.json')['protocol_sha256']
        return record
    directory.mkdir(parents=True)
    data=np.load(OUT/'development.npz');x=torch.from_numpy(data['X']);raw=torch.from_numpy(data['raw_y']).reshape(-1,1);y=raw.clamp(0,125);z=(raw<=30).float()
    meta=read('development.json');assert sha(OUT/'development.npz')==meta['development_sha256'];model=make_model(name)
    optimizer=torch.optim.AdamW(model.parameters(),lr=.0005,weight_decay=.0001);pos=torch.tensor([meta['pos_weight']],dtype=torch.float32)
    history=[];started=time.time()
    for epoch in range(EPOCHS):
        model.train();order=torch.randperm(len(x),generator=torch.Generator().manual_seed(seed*1000+epoch));loss_sum=0.
        for indices in order.split(64):
            optimizer.zero_grad(set_to_none=True);q05,q50,q95,logit=model(x[indices])
            pinball=sum(torch.maximum(t*(y[indices]-q),(t-1)*(y[indices]-q)).mean() for t,q in zip([.05,.5,.95],[q05,q50,q95]))/3
            loss=pinball+.5*torch.nn.functional.binary_cross_entropy_with_logits(logit,z[indices],pos_weight=pos)
            assert torch.isfinite(loss);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.);optimizer.step();loss_sum+=float(loss.detach())*len(indices)
        history.append(dict(epoch=epoch+1,training_loss=loss_sum/len(x),samples=len(x)))
    checkpoint=dict(state=model.state_dict(),model=name,seed=seed,epochs=EPOCHS,parameters=sum(p.numel() for p in model.parameters()),protocol_sha256=read('protocol_lock.json')['protocol_sha256'],started_unix=started,completed_unix=time.time())
    torch.save(checkpoint,directory/'final.pt')
    with (directory/'history.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(history[0]));w.writeheader();w.writerows(history)
    record={k:v for k,v in checkpoint.items() if k!='state'};record.update(checkpoint_sha256=sha(directory/'final.pt'),history_sha256=sha(directory/'history.csv'),training_only=True,execution_source_sha256=sha(Path(__file__)))
    (directory/'training.json').write_text(json.dumps(record,indent=2));print(name,seed,'complete',round(time.time()-started,1),'s',flush=True);return record

def train():
    check_protocol();assert not (OUT/'fit_complete.json').exists() and not (OUT/'evaluation_started.json').exists()
    assert sources()==read('source_lock.json')['files'];assert read('development.json')['test_arrays_opened'] is False
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=3) as executor:records=list(executor.map(train_one,[(m,s) for m in ['lstm','hybrid'] for s in SEEDS]))
    assert len(records)==10 and all(r['epochs']==EPOCHS for r in records)
    files={p.relative_to(ROOT).as_posix():sha(p) for p in (OUT/'models').rglob('*') if p.is_file()}
    for n in ['development.npz','preprocessor.npz','development.json','source_lock.json']:files[(OUT/n).relative_to(ROOT).as_posix()]=sha(OUT/n)
    write('fit_complete.json',dict(status='complete',models=records,files=files,sources=sources(),frozen_unix=time.time(),test_evaluation_started=False))

def score_vectors(y,q,logit,offset=0):
    p=np.exp(-np.logaddexp(0,-(logit-offset)));target=np.clip(y,0,125);point=np.clip(q[:,1],0,125);lo=np.clip(q[:,0],0,125);hi=np.clip(q[:,2],0,125)
    levels=np.array([.05,.5,.95]);L=np.max(np.where(q<=30,levels,0),axis=1);U=np.min(np.where(q>30,levels,1),axis=1);distance=np.maximum.reduce([L-p,p-U,np.zeros(len(y))])
    return dict(squared_error=(point-target)**2,absolute_error=np.abs(point-target),Brier=(p-(y<=30))**2,coverage=((lo<=target)&(target<=hi)).astype(float),width=hi-lo,Winkler=hi-lo+20*np.maximum(lo-target,0)+20*np.maximum(target-hi,0),incompatible=(distance>1e-6).astype(float),distance=distance,NLL=np.logaddexp(0,(1-2*(y<=30).astype(int))*(logit-offset))),p

def evaluate():
    check_protocol();lock=read('fit_complete.json');assert len(lock['models'])==10 and sources()==lock['sources']
    for n,h in lock['files'].items():assert sha(ROOT/n)==h,n
    assert not (OUT/'evaluation_started.json').exists();write('evaluation_started.json',dict(unix=time.time(),fit_complete_sha256=sha(OUT/'fit_complete.json'),all_ten_models_frozen=True))
    assert sha(DATA)==read('acquisition.json')['sha256'];data,meta=windows('test');assert not set(meta['engines'])&set(read('development.json')['engines'])
    prep=np.load(OUT/'preprocessor.npz');x=((data['X']-prep['mean'])/prep['std']).astype(np.float32);np.savez_compressed(OUT/'test_windows.npz',**data);write('test_population.json',meta)
    import torch
    sys.path.insert(0,str(ROOT));from src.models.simple_quantile_risk import make_model
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    raw_rows=[];records=[];per_engine=[];offset=math.log(read('development.json')['pos_weight'])
    for m in lock['models']:
        name,seed=m['model'],m['seed'];path=OUT/'models'/name/f'seed_{seed}'/'final.pt';saved=torch.load(path,weights_only=True);model=make_model(name);model.load_state_dict(saved['state']);model.eval()
        with torch.no_grad():
            batches=[np.concatenate([t.numpy() for t in model(torch.from_numpy(batch))],axis=1) for batch in np.array_split(x,max(1,math.ceil(len(x)/128)))]
        predictions=np.concatenate(batches);assert predictions.shape==(len(x),4) and np.isfinite(predictions).all()
        q=predictions[:,:3].astype(float);logit=predictions[:,3].astype(float)
        for method,delta in [('Raw',0.),('Bayes',offset)]:
            vectors,p=score_vectors(data['raw_y'].astype(float),q,logit,delta)
            for i in range(len(p)):
                raw_rows.append(dict(model=name,seed=seed,method=method,unit=int(data['unit'][i]),cycle=int(data['cycle'][i]),raw_y=float(data['raw_y'][i]),q05=float(q[i,0]),q50=float(q[i,1]),q95=float(q[i,2]),logit=float(logit[i]),probability=float(p[i]),**{k:float(v[i]) for k,v in vectors.items()}))
            engines=[]
            for unit in meta['engines']:
                mask=data['unit']==unit;row=dict(model=name,seed=seed,method=method,unit=unit,n=int(mask.sum()),**{k:float(v[mask].mean()) for k,v in vectors.items()});engines.append(row);per_engine.append(row)
            rec=dict(model=name,seed=seed,method=method,test_engines=len(engines),test_windows=len(p),RMSE=math.sqrt(np.mean([r['squared_error'] for r in engines])),MAE=np.mean([r['absolute_error'] for r in engines]))
            for k in ['Brier','coverage','width','Winkler','incompatible','distance','NLL']:rec[k]=float(np.mean([r[k] for r in engines]))
            rec['window_RMSE']=float(np.sqrt(vectors['squared_error'].mean()));rec['window_Brier']=float(vectors['Brier'].mean());rec['window_incompatible']=float(vectors['incompatible'].mean());records.append(rec)
    csvwrite('predictions.csv',raw_rows);csvwrite('per_engine.csv',per_engine);csvwrite('per_run.csv',records)
    summary=[]
    for model in ['lstm','hybrid']:
        for method in ['Raw','Bayes']:
            group=[r for r in records if (r['model'],r['method'])==(model,method)];assert len(group)==5
            item=dict(model=model,method=method,seeds=5,test_engines=len(meta['engines']),test_windows=meta['windows'])
            for k in ['RMSE','MAE','Brier','coverage','width','Winkler','incompatible','distance','NLL']:
                values=np.array([r[k] for r in group]);item[k+'_mean']=float(values.mean());item[k+'_sd']=float(values.std(ddof=1))
            summary.append(item)
    csvwrite('summary.csv',summary)
    pairs=[]
    for seed in SEEDS:
        l=next(r for r in records if (r['model'],r['seed'],r['method'])==('lstm',seed,'Raw'));h=next(r for r in records if (r['model'],r['seed'],r['method'])==('hybrid',seed,'Raw'))
        pairs.append(dict(seed=seed,**{k:h[k]-l[k] for k in ['RMSE','Brier','Winkler','incompatible']}))
    csvwrite('paired_differences.csv',pairs)
    write('evaluation.json',dict(status='complete',finished_unix=time.time(),source_lock_sha256=sha(OUT/'source_lock.json'),fit_complete_sha256=sha(OUT/'fit_complete.json'),test_population=meta,rows=len(raw_rows),scope='Prospectively specified retraining on DS01, no new external-fleet or population guarantee',no_post_test_changes=True))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['prepare','train','evaluate']);args=ap.parse_args()
    {'prepare':prepare,'train':train,'evaluate':evaluate}[args.stage]()

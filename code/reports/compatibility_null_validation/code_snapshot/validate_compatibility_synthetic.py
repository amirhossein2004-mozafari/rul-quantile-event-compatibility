"""Locked known-law nulls; no test-label access. See the locked protocol."""
from pathlib import Path
import os,sys,json,hashlib,time,platform,traceback,argparse
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('MKL_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
if '--cuda' in sys.argv:sys.path.insert(0,str(ROOT/'tmp/compatibility_cuda'))
import numpy as np
from scipy.special import exp1, expit
from scipy.optimize import minimize_scalar
import torch
from torch import nn
from src.models.simple_quantile_risk import make_model,QuantileRiskBase
from src.training.pcgrad_ablation import task_losses
OUT=ROOT/'reports/compatibility_null_validation';RUN=OUT/'synthetic';RUN.mkdir(exist_ok=True)
CFG=json.loads((OUT/'config.json').read_text(encoding='utf-8-sig'))
LEVELS=np.array([.05,.5,.95]);SUBS=['FD001','FD002','FD003','FD004']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(v,indent=2,allow_nan=False),encoding='utf-8');os.replace(tmp,p)
def check_lock():
    lock=json.loads((OUT/'protocol_lock.json').read_text(encoding='utf-8-sig'))
    assert sha(OUT/'protocol.md')==lock['protocol_sha256']
    assert sha(OUT/'config.json')==lock['config_sha256']
    return lock

def oracle(age,scale,policy):
    age=np.asarray(age);scale=np.broadcast_to(scale,age.shape)
    if policy=='final':
        q=-scale[:,None]*np.log1p(-LEVELS);p=-np.expm1(-30/scale)
    else:
        b=(age-30)/scale;den=exp1(b)
        assert np.all(b>0) and np.isfinite(den).all()
        p=-np.expm1(np.log(exp1(b+30/scale))-np.log(den))
        lo=np.zeros((len(age),3));hi=np.full_like(lo,125.)
        for _ in range(42):
            mid=(lo+hi)/2
            cdf=1-exp1(b[:,None]+mid/scale[:,None])/den[:,None]
            below=cdf<LEVELS
            lo=np.where(below,mid,lo);hi=np.where(below,hi,mid)
        q=hi
    return np.minimum(q,125),p

def diagnostic(q,p):
    lo=np.max(np.where(q<=30,LEVELS,0),axis=-1)
    hi=np.min(np.where(q>30,LEVELS,1),axis=-1)
    return np.maximum.reduce([lo-p,p-hi,np.zeros_like(p)])

def single_quantile(age,scale,tau):
    b=(age-30)/scale;den=exp1(b)
    lo=np.zeros(len(age));hi=np.full(len(age),125.)
    for _ in range(42):
        mid=(lo+hi)/2;below=(1-exp1(b+mid/scale)/den)<tau
        lo=np.where(below,mid,lo);hi=np.where(below,hi,mid)
    return hi

def censor_ages(sub):
    p=ROOT/f'data/raw/cmapss/test_{sub}.txt';a=np.loadtxt(p,usecols=(0,1))
    ids=np.unique(a[:,0]);return np.array([a[a[:,0]==i,1].max() for i in ids]),sha(p)

def endpoints(n,policy,seed,ages):
    rng=np.random.default_rng(seed);x=rng.choice([-1.,1.],n);scale=60*np.exp(.5*x)
    if policy=='final':
        age=rng.choice(ages,n);y=rng.exponential(scale);lifetime=age+y
    else:
        lifetime=30+rng.exponential(scale);age=30+rng.random(n)*(lifetime-30);y=lifetime-age
    return x,age,y,lifetime

def features(x,times,rng):
    times=np.asarray(times);f=np.empty(times.shape+(18,),dtype=np.float32)
    f[...,0]=x;f[...,1]=times/125
    f[...,2:]=np.arange(1,17)/16*x+.25*times[...,None]/(60*np.exp(.5*x))+rng.normal(0,.25,times.shape+(16,))
    return f

def prepare():
    check_lock();manifest={}
    for k,sub in enumerate(SUBS):
      ages,h=censor_ages(sub);manifest[sub]=dict(input_sha256=h,ages=ages.tolist())
      for j,policy in enumerate(['final','uniform']):
        dest=RUN/f'evaluation_{sub}_{policy}.npz'
        if dest.exists():continue
        seed=27182818+100*k+j;x,a,y,t=endpoints(10000,policy,seed,ages)
        rng=np.random.default_rng(seed+100000);xx=np.stack([features(v,np.arange(-29,1)+u,rng) for v,u in zip(x,a)])
        q,p=oracle(a,60*np.exp(.5*x),policy);d=diagnostic(q,p)
        assert np.all(d==0),'Oracle incompatibility'
        np.savez_compressed(dest,x=x,age=a,y=y,lifetime=t,X=xx,q_true=q,p_true=p,engine_id=np.arange(10000),seed=seed)
        print('ORACLE',sub,policy,'engines=10000 rate=',float((d>0).mean()),flush=True)
    write(RUN/'evaluation_manifest.json',dict(policy='empirical ages only, no labels',inputs=manifest,files={p.name:sha(p) for p in RUN.glob('evaluation_*.npz')},protocol=check_lock()))

def training_data(n,seed):
    rng=np.random.default_rng(seed);xs=rng.choice([-1.,1.],n);lifetimes=30+rng.exponential(60*np.exp(.5*xs))
    arrays=[];ys=[];cov=[];engine=[]
    for eid,(x,t) in enumerate(zip(xs,lifetimes)):
        f=features(x,np.arange(1,int(np.floor(t))+1),rng)
        windows=np.lib.stride_tricks.sliding_window_view(f,30,axis=0).transpose(0,2,1).copy()
        ages=np.arange(30,int(np.floor(t))+1);y=t-ages
        arrays.append(windows);ys.extend(y);cov.append(np.stack([np.full(len(ages),x),ages/125],axis=1));engine.extend([eid]*len(ages))
    y=np.array(ys,dtype=np.float32).reshape(-1,1);z=(y<=30).astype(np.float32)
    if not 0<z.sum()<len(z):raise ValueError('Missing event class; retain failed fleet')
    return np.concatenate(arrays),np.concatenate(cov).astype(np.float32),np.minimum(y,125),z,dict(seed=seed,engines=n,windows=len(y),positive=int(z.sum()),weight=float((len(z)-z.sum())/z.sum()),lifetimes=lifetimes.tolist(),x=xs.tolist(),engine_id=engine)

class CovariateNet(QuantileRiskBase):
    def __init__(self):
        super().__init__();self.encoder=nn.Sequential(nn.Linear(2,64),nn.ReLU())
    def encode(self,x):return self.encoder(x)

def train(family,sub,arch,rep,weighted,device):
    n=CFG['fit_counts'][sub];identity=dict(family=family,subset=sub,architecture=arch,replication=rep,weighted=weighted,fitting_engines=n)
    folder=RUN/f"{family}/{sub}/{arch}/rep_{rep:03d}/{'weighted' if weighted else 'unweighted'}"
    folder.mkdir(parents=True,exist_ok=True)
    if (folder/'complete.json').exists():return
    group=SUBS.index(sub) if family=='temporal' else [60,156,149].index(n)
    ds=31415926+group*100000+rep*10+(0 if family=='temporal' else 1000000)
    init=ds+2000000+(0 if arch=='lstm' else 1)
    xx,cc,yy,zz,meta=training_data(n,ds)
    torch.manual_seed(init)
    if device=='cuda':torch.cuda.manual_seed_all(init)
    model=(make_model(arch) if family=='temporal' else CovariateNet()).to(device)
    selection=json.loads((ROOT/'results/fair_comparison_step2/selection.json').read_text())
    choice=selection[f'{sub}/{arch}'] if family=='temporal' else dict(lr=.0005,epochs=16)
    identity.update(data_seed=ds,initial_seed=init,choice=choice,device=device,protocol_sha256=check_lock()['protocol_sha256'],script_sha256=sha(__file__))
    write(folder/'identity.json',identity);meta.pop('engine_id');write(folder/'data.json',meta)
    data=torch.from_numpy(xx if family=='temporal' else cc).to(device);y=torch.from_numpy(yy).to(device);z=torch.from_numpy(zz).to(device)
    del xx,cc
    opt=torch.optim.AdamW(model.parameters(),lr=choice['lr'],weight_decay=.0001)
    weight=torch.tensor([meta['weight'] if weighted else 1.],device=device);history=[];start=time.time()
    progress=folder/'progress.pt'
    if progress.exists():
        state=torch.load(progress,map_location=device,weights_only=False)
        assert state['identity']==identity
        model.load_state_dict(state['model']);opt.load_state_dict(state['optimizer']);history=state['history'];torch.set_rng_state(state['rng'].cpu())
        if device=='cuda':torch.cuda.set_rng_state(state['cuda_rng'].cpu())
    for epoch in range(len(history),choice['epochs']):
        model.train();total=0.
        perm=torch.randperm(len(data),generator=torch.Generator().manual_seed(init*1000+epoch))
        for ids in perm.split(128):
            ids=ids.to(device);opt.zero_grad(set_to_none=True)
            a,b=task_losses(model(data[ids]),y[ids],z[ids],weight);loss=a+b
            if not torch.isfinite(loss):raise ValueError('Nonfinite training loss')
            loss.backward();nn.utils.clip_grad_norm_(model.parameters(),1.);opt.step();total+=float(loss.detach())*len(ids)
        history.append(dict(epoch=epoch+1,loss=total/len(data),elapsed_seconds=time.time()-start))
        torch.save(dict(identity=identity,model=model.state_dict(),optimizer=opt.state_dict(),history=history,rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state() if device=='cuda' else None),progress)
        write(folder/'history.json',history)
    model.eval();torch.save(dict(identity=identity,state={k:v.cpu() for k,v in model.state_dict().items()}),folder/'final.pt')
    for policy in ['final','uniform']:
        with np.load(RUN/f'evaluation_{sub}_{policy}.npz') as ev:
            arr=ev['X'] if family=='temporal' else np.stack([ev['x'],ev['age']/125],axis=1).astype(np.float32)
            outputs=[]
            with torch.inference_mode():
                for i in range(0,len(arr),512):outputs.append(torch.cat(model(torch.from_numpy(arr[i:i+512]).to(device)),dim=1).cpu().numpy())
            pred=np.concatenate(outputs).astype(np.float64);assert np.isfinite(pred).all()
            assert np.all(np.diff(pred[:,:3],axis=1)>=0)
            np.savez_compressed(folder/f'{policy}_predictions.npz',q=pred[:,:3],logit=pred[:,3],weight=meta['weight'] if weighted else 1,engine_id=ev['engine_id'])
    write(folder/'complete.json',dict(identity=identity,seconds=time.time()-start,parameters=sum(p.numel() for p in model.parameters()),history=history))
    print('FIT',family,sub,arch,rep,'weighted' if weighted else 'unweighted',round(time.time()-start,1),'seconds',flush=True)

def run_neural(family,device):
    if family=='temporal':groups=[(s,a) for s in SUBS for a in ['lstm','hybrid']];reps=30
    else:groups=[('FD001','covariate'),('FD002','covariate'),('FD004','covariate')];reps=200
    for rep in range(reps):
      for sub,arch in groups:
       for weighted in [True,False]:
        try:train(family,sub,arch,rep,weighted,device)
        except Exception:
            write(RUN/f'failure_{family}_{sub}_{arch}_{rep}_{weighted}.json',dict(traceback=traceback.format_exc(),time=time.time()));raise
    write(RUN/f'{family}_complete.json',dict(replicates=reps,groups=groups,device=device))

def param_fit(x,age,y,policy):
    qparameters=np.empty((2,3));risks=np.empty((2,2));notes=[]
    z=y<=30;w=(len(z)-z.sum())/z.sum() if z.sum() else np.inf
    if not 0<z.sum()<len(z):raise ValueError('Missing event class in parametric fleet')
    for k,val in enumerate([-1,1]):
        ids=x==val;a=age[ids];target=np.minimum(y[ids],125);event=z[ids]
        if not len(a):raise ValueError('Missing covariate stratum')
        if policy=='final':
            qparameters[k]=np.quantile(target,LEVELS,method='inverted_cdf')
            frequency=event.mean();risks[k]=[frequency,w*frequency/(1-frequency+w*frequency)]
            notes.append(dict(stratum=val,n=len(a),event_count=int(event.sum()),exact_saturated_solution=True))
        else:
            grid=np.linspace(np.log(5),np.log(500),25)
            def optimize(fn):
                losses=np.array([fn(v) for v in grid]);j=int(np.argmin(losses))
                fit=minimize_scalar(fn,bounds=(grid[max(0,j-1)],grid[min(24,j+1)]),method='bounded',options={'xatol':1e-5})
                best=min([(losses[j],grid[j]),(float(fit.fun),float(fit.x))])
                notes.append(dict(stratum=val,success=bool(fit.success),boundary_grid_minimum=j in [0,24],objective=best[0],log_scale=best[1]))
                return np.exp(best[1])
            for j,tau in enumerate(LEVELS):
                def pin(logscale):
                    qs=single_quantile(a,np.full(len(a),np.exp(logscale)),tau);err=target-qs
                    return np.maximum(tau*err,(tau-1)*err).mean()
                qparameters[k,j]=optimize(pin)
            for j,weight in enumerate([1,w]):
                def bce(logscale):
                    _,p=oracle_probability(a,np.full(len(a),np.exp(logscale)),policy)
                    p=np.clip(p,1e-15,1-1e-15);eta=np.log(p)-np.log1p(-p)+np.log(weight)
                    return np.mean((1-event)*np.logaddexp(0,eta)+weight*event*np.logaddexp(0,-eta))
                risks[k,j]=optimize(bce)
    return qparameters,risks,float(w),notes

def oracle_probability(age,scale,policy):
    if policy=='final':return None,-np.expm1(-30/scale)
    b=(age-30)/scale
    return None,1-exp1(b+30/scale)/exp1(b)

def run_parametric(subset=None):
    for sub in ([subset] if subset else ['FD001','FD002','FD004']):
      ages,_=censor_ages(sub);n=CFG['fit_counts'][sub]
      for rep in range(200):
       for j,policy in enumerate(['final','uniform']):
        folder=RUN/f'parametric/{sub}/rep_{rep:03d}/{policy}';folder.mkdir(parents=True,exist_ok=True)
        if (folder/'complete.json').exists():continue
        seed=31415926+3000000+SUBS.index(sub)*100000+rep*10+j
        x,a,y,t=endpoints(n,policy,seed,ages);qp,rp,w,notes=param_fit(x,a,y,policy)
        with np.load(RUN/f'evaluation_{sub}_{policy}.npz') as ev:
            ix=(ev['x']>0).astype(int);aa=ev['age'];q=np.empty((len(aa),3));p=np.empty((len(aa),2))
            if policy=='final':q=qp[ix];p=rp[ix]
            else:
                for k in range(3):qs,_=oracle(aa,qp[ix,k],policy);q[:,k]=qs[:,k]
                for k in range(2):_,pp=oracle_probability(aa,rp[ix,k],policy);p[:,k]=pp if k==0 else w*pp/(1-pp+w*pp)
            np.savez_compressed(folder/'predictions.npz',q=q,p=p,weight=w,engine_id=ev['engine_id'],fit_x=x,fit_age=a,fit_y=y)
        write(folder/'complete.json',dict(seed=seed,fitting_engines=n,policy=policy,qparameters=qp.tolist(),risk_parameters=rp.tolist(),weight=w,optimizer_notes=notes))
       print('PARAMETRIC',sub,rep,flush=True)
    write(RUN/f"parametric_complete_{subset or 'all'}.json",dict(replicates=200))

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','temporal','covariate','parametric']);p.add_argument('--cuda',action='store_true');p.add_argument('--subset',choices=['FD001','FD002','FD004']);args=p.parse_args()
    lock=check_lock();torch.set_num_threads(1);torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True);torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
    torch.backends.cudnn.allow_tf32=False;torch.backends.cuda.matmul.allow_tf32=False
    device='cuda' if args.cuda else 'cpu'
    if args.cuda:assert torch.cuda.is_available()
    write(RUN/f"execution_{args.action}_{args.subset or 'all'}.json",dict(action=args.action,subset=args.subset,device=device,python=platform.python_version(),torch=str(torch.__version__),numpy=np.__version__,scipy=__import__('scipy').__version__,hardware=torch.cuda.get_device_name(0) if args.cuda else platform.processor(),script_sha256=sha(__file__),lock=lock))
    if args.action=='prepare':prepare()
    elif args.action=='parametric':run_parametric(args.subset)
    else:run_neural(args.action,device)
if __name__=='__main__':main()

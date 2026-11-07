from pathlib import Path
import os,sys,json,time,hashlib,traceback,itertools,platform
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('MKL_NUM_THREADS','1');os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import validate_compatibility_synthetic as m
import numpy as np
import torch
from scipy.special import expit
from src.training.pcgrad_ablation import reset_seed,permutation_for_epoch,task_losses
BASE=m.OUT;F=BASE/'followup';CFG=json.loads((F/'config.json').read_text(encoding='utf-8-sig'));SOURCE=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
HEADS={'median_head','lower_delta_head','upper_delta_head','risk_head'}

def check():
    lock=json.loads((F/'protocol_lock.json').read_text(encoding='utf-8-sig'))
    assert m.sha(BASE/'protocol.md')==lock['protocol_sha256']
    assert m.sha(F/'config.json')==lock['config_sha256']
    assert m.sha(BASE/'protocol_v1_locked.md')==lock['parent_protocol_sha256']
    return lock

def setup(action,cuda=False):
    check();torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False;torch.backends.cudnn.allow_tf32=False;torch.backends.cuda.matmul.allow_tf32=False
    if cuda:assert torch.cuda.is_available()
    (F/'code').mkdir(exist_ok=True)
    snapshot=F/'code'/f'{SOURCE}.py'
    if not snapshot.exists():snapshot.write_bytes(Path(__file__).read_bytes())
    assert m.sha(snapshot)==SOURCE
    sources={str(p.relative_to(ROOT)):m.sha(p) for p in [ROOT/'src/models/simple_quantile_risk.py',ROOT/'src/models/hybrid_lstm_tcn.py',ROOT/'src/training/pcgrad_ablation.py']}
    old=json.loads((F/'model_sources.json').read_text()) if (F/'model_sources.json').exists() else sources
    assert old==sources,'Paper model source changed'
    if not (F/'model_sources.json').exists():m.write(F/'model_sources.json',sources)
    m.write(F/f'execution_{action}.json',dict(source_sha256=SOURCE,device='cuda' if cuda else 'cpu',torch=str(torch.__version__),torch_git=torch.version.git_version,python=platform.python_version(),numpy=np.__version__,lock=check(),sources=sources))

def atomic_torch(value,path):
    temp=path.with_suffix(path.suffix+'.tmp');torch.save(value,temp);os.replace(temp,path)

def initialize(arch,seed,fix,device,real_folder=None):
    if real_folder is None:
        torch.manual_seed(seed)
        if device=='cuda':torch.cuda.manual_seed_all(seed)
    else:reset_seed(seed)
    model=m.make_model(arch)
    initial_match=None
    if real_folder:
        frozen=torch.load(real_folder/'initial.pt',weights_only=True,map_location='cpu')['state']
        initial_match=all(torch.equal(v,frozen[k]) for k,v in model.state_dict().items())
        assert initial_match,'Seeded initial state differs from frozen cohort'
        model.load_state_dict(frozen)
    if fix:
        with torch.no_grad():
            for name,gap in [('lower_delta_head',20.),('upper_delta_head',80.)]:
                last=getattr(model,name)[-1];last.weight.zero_();last.bias.fill_(gap+np.log(-np.expm1(-gap)))
    return model.to(device),initial_match

def gap_probe(model,x):
    was=model.training;model.eval()
    with torch.no_grad():
        q=torch.cat(model(x[:min(len(x),512)])[:3],dim=1);gap=q[:,1]-q[:,0]
    model.train(was)
    return dict(median_gap=float(gap.median().cpu()),mean_gap=float(gap.mean().cpu()),probe_windows=len(gap))

def train(folder,identity,x,y,z,weight,choice,seed,device,fix=False,scale=1.,lr_multiplier=1.,clip=1.,real_folder=None,engine_tags=None):
    folder.mkdir(parents=True,exist_ok=True)
    if (folder/'fit_complete.json').exists():return
    identity=dict(**identity,protocol_sha256=check()['protocol_sha256'],source_sha256=SOURCE,pinball_scale=scale,lr_multiplier=lr_multiplier,gradient_clip=clip,fix_initialization=fix,device=device,epochs=choice['epochs'],lr=choice['lr']*lr_multiplier)
    model,match=initialize(identity['architecture'],seed,fix,device,real_folder)
    optimizer=torch.optim.AdamW(model.parameters(),lr=identity['lr'],weight_decay=.0001)
    x=x.to(device);y=y.to(device);z=z.to(device);w=torch.tensor([weight],dtype=torch.float32,device=device)
    history=[];start=time.time();initial_probe=gap_probe(model,x)
    m.write(folder/'identity.json',dict(**identity,initial_state_exact_match=match));m.write(folder/'initial_probe.json',initial_probe)
    progress=folder/'progress.pt'
    if progress.exists():
        old=torch.load(progress,map_location=device,weights_only=False);assert old['identity']==identity
        model.load_state_dict(old['state']);optimizer.load_state_dict(old['optimizer']);history=old['history'];torch.set_rng_state(old['rng'].cpu())
        if device=='cuda':torch.cuda.set_rng_state(old['cuda_rng'].cpu())
    for epoch in range(len(history),choice['epochs']):
        model.train();rul_sum=risk_sum=total=norm_sum=0.;clipped=0;steps=0
        permutation=permutation_for_epoch(len(x),seed,epoch)
        for step,ids in enumerate(permutation.split(128)):
            optimizer.zero_grad(set_to_none=True);idx=ids.to(device)
            rul,risk=task_losses(model(x[idx]),y[idx],z[idx],w);reg=rul if scale==1 else rul*scale;loss=reg+risk
            assert torch.isfinite(loss),'Nonfinite training loss'
            if epoch==0 and step==0 and not (folder/'first_step.json').exists():
                shared=[p for name,p in model.named_parameters() if name.split('.')[0] not in HEADS]
                a=torch.autograd.grad(reg,shared,retain_graph=True,allow_unused=True);b=torch.autograd.grad(risk,shared,retain_graph=True,allow_unused=True)
                av=torch.cat([v.reshape(-1) if v is not None else torch.zeros_like(p).reshape(-1) for v,p in zip(a,shared)]);bv=torch.cat([v.reshape(-1) if v is not None else torch.zeros_like(p).reshape(-1) for v,p in zip(b,shared)])
                an=float(av.norm().detach().cpu());bn=float(bv.norm().detach().cpu())
                m.write(folder/'first_step.json',dict(fitting_engines=identity['fitting_engines'],batch_windows=len(ids),batch_engines=int(len(np.unique(engine_tags[ids.numpy()]))) if engine_tags is not None else None,scaled_pinball_shared_gradient_norm=an,weighted_BCE_shared_gradient_norm=bn,gradient_cosine=float((av@bv).detach().cpu())/(an*bn) if an*bn else None))
            loss.backward()
            if clip is not None:norm=torch.nn.utils.clip_grad_norm_(model.parameters(),clip)
            else:norm=torch.linalg.vector_norm(torch.stack([p.grad.detach().norm() for p in model.parameters() if p.grad is not None]))
            assert torch.isfinite(norm),'Nonfinite gradient norm'
            optimizer.step();n=len(ids);rul_sum+=float(rul.detach())*n;risk_sum+=float(risk.detach())*n;total+=float(loss.detach())*n;norm_sum+=float(norm.detach());clipped+=int(clip is not None and float(norm.detach())>clip);steps+=1
        history.append(dict(epoch=epoch+1,raw_pinball=rul_sum/len(x),risk_loss=risk_sum/len(x),total_loss=total/len(x),preclip_norm_mean=norm_sum/steps,clipping_fraction=clipped/steps,steps=steps,windows=len(x),seconds=time.time()-start))
        m.write(folder/'history.json',history)
        atomic_torch(dict(identity=identity,state=model.state_dict(),optimizer=optimizer.state_dict(),history=history,rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state() if device=='cuda' else None),progress)
    model.eval();atomic_torch(dict(state={k:v.cpu() for k,v in model.state_dict().items()},identity=identity),folder/'final.pt')
    m.write(folder/'fit_complete.json',dict(identity=identity,history=history,initial_probe=initial_probe,final_probe=gap_probe(model,x),parameters=sum(p.numel() for p in model.parameters()),seconds=time.time()-start))

def forward(model,arr,device):
    model.eval();result=[]
    with torch.inference_mode():
        for i in range(0,len(arr),512):result.append(torch.cat(model(torch.from_numpy(arr[i:i+512]).to(device)),dim=1).cpu().numpy())
    return np.concatenate(result).astype(np.float64)

def predict_synthetic(folder,device,weight):
    if (folder/'complete.json').exists():return
    state=torch.load(folder/'final.pt',weights_only=False,map_location='cpu');model=m.make_model(state['identity']['architecture']).to(device);model.load_state_dict(state['state']);model.eval()
    for policy in ['final','uniform']:
        with np.load(m.RUN/f'evaluation_FD001_{policy}.npz') as ev:
            pred=forward(model,ev['X'],device);assert np.isfinite(pred).all();np.testing.assert_array_less(-1e-12,np.diff(pred[:,:3],axis=1))
            np.savez_compressed(folder/f'{policy}_predictions.npz',q=pred[:,:3],logit=pred[:,3],weight=weight,engine_id=ev['engine_id'])
    m.write(folder/'complete.json',json.loads((folder/'fit_complete.json').read_text()))

def synthetic_one(arch,rep,weighted,factors,folder,device):
    if (folder/'complete.json').exists():return
    if (folder/'failure.json').exists():return
    init,loss,rate,clipping=factors;ds=31415926+rep*10;seed=ds+2000000+(0 if arch=='lstm' else 1)
    xx,cc,yy,zz,meta=m.training_data(60,ds);tags=np.array(meta.pop('engine_id'));weight=meta['weight'] if weighted else 1.
    choice=json.loads((ROOT/'results/fair_comparison_step2/selection.json').read_text())[f'FD001/{arch}']
    ident=dict(kind='synthetic_followup',subset='FD001',architecture=arch,replication=rep,weighted=weighted,fitting_engines=60,data_seed=ds,initial_seed=seed,factors=list(factors))
    folder.mkdir(parents=True,exist_ok=True);m.write(folder/'data.json',meta)
    train(folder,ident,torch.from_numpy(xx),torch.from_numpy(yy),torch.from_numpy(zz),weight,choice,seed,device,bool(init),1/125 if loss else 1.,3. if rate else 1.,None if clipping else 1.,engine_tags=tags)
    predict_synthetic(folder,device,weight)
    if factors==(0,0,0,0):
        original=m.RUN/f"temporal/FD001/{arch}/rep_{rep:03d}/weighted"
        with np.load(original/'final_predictions.npz') as a,np.load(folder/'final_predictions.npz') as b:
            aa=np.column_stack([a['q'],a['logit']]);bb=np.column_stack([b['q'],b['logit']]);np.testing.assert_allclose(aa,bb,atol=.001,rtol=1e-5)
            m.write(folder/'baseline_replay_check.json',dict(max_abs_difference=float(abs(aa-bb).max()),fitting_engines=60,evaluation_engines=10000))
    print('SYNTHETIC',arch,rep,weighted,list(factors),flush=True)

def fix_folder(arch,rep,weighted):return F/f"fixed_init/{arch}/rep_{rep:03d}/{'weighted' if weighted else 'unweighted'}"
def factor_folder(arch,rep,factors):
    if factors==(1,0,0,0):return fix_folder(arch,rep,True)
    return F/f"factorial/{arch}/rep_{rep:03d}/cell_{''.join(map(str,factors))}"

def run_synthetic():
    setup('synthetic',True)
    for rep in range(30):
      for arch in ['lstm','hybrid']:
       for weighted in [True,False]:
        folder=fix_folder(arch,rep,weighted)
        try:synthetic_one(arch,rep,weighted,(1,0,0,0),folder,'cuda')
        except Exception:m.write(folder/'failure.json',dict(traceback=traceback.format_exc()));print('FAILED',str(folder),flush=True)
    for rep in [0,1,2]:
      for arch in ['lstm','hybrid']:
       for factors in itertools.product([0,1],repeat=4):
        folder=factor_folder(arch,rep,factors)
        try:synthetic_one(arch,rep,True,factors,folder,'cuda')
        except Exception:
            folder.mkdir(parents=True,exist_ok=True);m.write(folder/'failure.json',dict(traceback=traceback.format_exc()));print('FAILED',str(folder),flush=True)
    m.write(F/'synthetic_training_complete.json',dict(fixed_init_planned=120,factorial_configurations=96,distinct_training_executions=210,failures=[str(p.relative_to(F)) for p in F.rglob('failure.json')]))

def run_real():
    setup('real',False)
    import fair_comparison_step2 as paper
    data=torch.load(paper.OUT/'data/FD001/tensors.pt',weights_only=True);choice=json.loads((paper.OUT/'selection.json').read_text());roles=json.loads((paper.OUT/'data/FD001/roles.json').read_text())
    raw=np.loadtxt(ROOT/'data/raw/cmapss/train_FD001.txt',usecols=(0,1));tags=[]
    for eid in sorted(roles['fit']):tags.extend([eid]*max(1,int(raw[raw[:,0]==eid,1].max())-29))
    tags=np.array(tags);assert len(tags)==len(data['X'])
    for arch in ['lstm','hybrid']:
     for seed in CFG['real_retrain_seeds']:
        folder=F/f'real_unweighted/FD001/{arch}/seed_{seed}';original=paper.OUT/f'final/FD001/{arch}/seed_{seed}'
        ident=dict(kind='real_unweighted',subset='FD001',architecture=arch,seed=seed,fitting_engines=len(roles['fit']),weighted=False)
        train(folder,ident,data['X'],data['y'],data['z'],1.,choice[f'FD001/{arch}'],seed,'cpu',real_folder=original,engine_tags=tags)
        print('REAL FIT',arch,seed,flush=True)
    m.write(F/'real_weights_frozen.json',dict(fits=10,files={str(p.relative_to(F)):m.sha(p) for p in (F/'real_unweighted').rglob('final.pt')}))
    x,unused_y,ids=paper.test_data('FD001');xx=x.numpy();cal=data['calibration_X'].numpy();calids=np.loadtxt(paper.OUT/'data/FD001/calibration_endpoints.csv',delimiter=',',skiprows=1,usecols=0).astype(int)
    checks=[]
    for arch in ['lstm','hybrid']:
     for seed in CFG['real_retrain_seeds']:
        original=paper.OUT/f'final/FD001/{arch}/seed_{seed}';folder=F/f'real_unweighted/FD001/{arch}/seed_{seed}'
        frozen=torch.load(original/'final.pt',weights_only=True,map_location='cpu');model=m.make_model(arch);model.load_state_dict(frozen['state'])
        import pandas as pd
        for role,arr in [('test',xx),('calibration',cal)]:
            pred=forward(model,arr,'cpu');saved=pd.read_csv(original/f'{role}_predictions.csv',float_precision='round_trip')[['q05','q50','q95','logit']].to_numpy();np.testing.assert_allclose(pred,saved,atol=.001,rtol=1e-5)
            checks.append(dict(architecture=arch,seed=seed,role=role,engines=len(arr),max_abs_difference=float(abs(pred-saved).max())))
        state=torch.load(folder/'final.pt',map_location='cpu',weights_only=False);model.load_state_dict(state['state'])
        for role,arr,eids in [('test',xx,ids),('calibration',cal,calids)]:
            pred=forward(model,arr,'cpu');np.savez_compressed(folder/f'{role}_predictions.npz',q=pred[:,:3],logit=pred[:,3],weight=1.,engine_id=eids)
        m.write(folder/'complete.json',json.loads((folder/'fit_complete.json').read_text()))
    m.write(F/'real_training_complete.json',dict(fits=10,reconstruction_checks=checks,prepared_tensor_sha256=m.sha(paper.OUT/'data/FD001/tensors.pt')))

if __name__=='__main__':
    action=sys.argv[1]
    if action=='synthetic':run_synthetic()
    elif action=='real':run_real()
    else:raise ValueError(action)

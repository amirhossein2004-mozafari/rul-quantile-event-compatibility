"""Portable numerical review: Python standard library only; no fitting/inference."""
from pathlib import Path
import argparse,csv,hashlib,json,math,platform,statistics
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def avg(v):return math.fsum(v)/len(v)
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=2e-11,abs_tol=2e-12),(a,b)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--output-dir',type=Path,default=Path('csv_review_outputs'));args=ap.parse_args()
    root=args.root.resolve();out=args.output_dir.resolve();assert not out.exists(),'Choose a new output directory'
    manifest=json.loads((root/'FILE_MANIFEST.json').read_text())
    for n,h in manifest['files'].items():assert hashlib.sha256((root/n).read_bytes()).hexdigest()==h,n
    history=read(root/'results/fair_comparison_step2/search_results.csv');selection=json.loads((root/'results/fair_comparison_step2/selection.json').read_text());candidate=read(root/'results/remaining_step10/validation_candidates.csv')
    assert len(history)==384 and len(candidate)==24
    for key,chosen in selection.items():
        subset,model=key.split('/');g=[r for r in history if r['subset']==subset and r['model']==model]
        best=min(g,key=lambda r:(float(r['validation_RMSE']),int(r['candidate']),int(r['epoch'])))
        assert (int(best['candidate']),int(best['epoch']),float(best['lr']))==(chosen['candidate'],chosen['epochs'],chosen['lr']);close(best['validation_RMSE'],chosen['validation_RMSE'])
        for c in range(3):
            rg=[r for r in g if int(r['candidate'])==c];assert sorted(int(r['epoch']) for r in rg)==list(range(1,17))
            cb=min(rg,key=lambda r:(float(r['validation_RMSE']),int(r['epoch'])))
            target=next(r for r in candidate if r['subset']==subset and r['model']==model and int(r['candidate'])==c)
            assert int(target['best_epoch'])==int(cb['epoch']);close(target['best_validation_RMSE'],cb['validation_RMSE']);close(target['delta_from_selected_validation_RMSE'],float(cb['validation_RMSE'])-float(best['validation_RMSE']))
    original=read(root/'results/calibration_stage3/per_run.csv')
    expected={(r['study'],r['subset'],r['model'],int(r['seed']),r['method']):r for r in read(root/'results/risk_context_step8/per_run.csv')}
    runs=[]
    for r in original:
        subset=r['Subset'];seed=int(r['Seed']);stem=f'{subset}_seed_{seed}';base=root/'results/calibration_stage3'
        runs.append(('Original',subset,'Hybrid',seed,read(base/f'{stem}_test.csv'),read(base/f'{stem}_calibration_oof.csv'),'true_RUL_raw','raw_logit',float(r['ln_w_pos']),{'Temp':float(r['T_raw']),'ShiftTemp':float(r['T_shift'])}))
    point_expected={(r['subset'],r['model'],int(r['seed'])):r for r in read(root/'results/fair_comparison_step2/per_run.csv')};point_checks=0
    for path in sorted((root/'results/fair_comparison_step2/final').glob('*/*/seed_*/test_predictions.csv')):
        subset,model,seed=path.parents[2].name,path.parents[1].name,int(path.parent.name.removeprefix('seed_'));meta=json.loads((path.parent/'calibration_fits.json').read_text());test=read(path)
        errors=[max(0,min(125,float(r['q50'])))-min(125,float(r['raw_y'])) for r in test]
        close(math.sqrt(avg([e*e for e in errors])),point_expected[(subset,model,seed)]['RMSE']);close(avg([abs(e) for e in errors]),point_expected[(subset,model,seed)]['MAE']);point_checks+=1
        runs.append(('EqualSearch',subset,'LSTM' if model=='lstm' else 'Hybrid',seed,test,read(path.with_name('calibration_predictions.csv')),'raw_y','logit',meta['ln_pos_weight'],meta['temperatures']))
    assert len(runs)==60 and point_checks==40;prob_checks=0;positive=0
    for study,subset,model,seed,test,cal,yk,lk,offset,temps in runs:
        labels=[int(float(r[yk])<=30) for r in test];p0=sum(float(r[yk])<=30 for r in cal)/len(cal);bs0=avg([(p0-y)**2 for y in labels]);assert bs0>0
        # Supplied official RUL labels are small; sensor trajectories are unnecessary here.
        truth=[float(x) for x in (root/f'data/raw/cmapss/RUL_{subset}.txt').read_text().split()]
        assert len({r['engine_id'] for r in test})==len(test)==len(truth)
        assert all(float(r[yk])==truth[int(r['engine_id'])-1] for r in test)
        for method in ['Raw','Bayes','Temp','ShiftTemp']:
            probabilities=[float(r['p_'+method]) for r in test];bs=avg([(p-y)**2 for p,y in zip(probabilities,labels)])
            logits=[(float(r[lk])-(offset if method in ['Bayes','ShiftTemp'] else 0))/(temps[method] if method in temps else 1) for r in test]
            signed=[(1-2*y)*ell for y,ell in zip(labels,logits)]
            nll=avg([max(x,0)+math.log1p(math.exp(-abs(x))) for x in signed]);skill=1-bs/bs0;target=expected[(study,subset,model,seed,method)]
            for metric,value in [('Brier',bs),('constant_Brier',bs0),('Brier_skill',skill),('NLL',nll)]:close(target[metric],value)
            prob_checks+=1;positive+=skill>0
    counts={(r['subset'],r['model'],int(r['seed']),r['method']):r for r in read(root/'results/path_precision_step9/per_run_counts.csv')};path_checks=0
    for path in sorted((root/'results/monitoring_step4/runs').glob('*/*/seed_*/predictions.csv')):
        subset,model,seed=path.parents[2].name,path.parents[1].name,int(path.parent.name.removeprefix('seed_'));data=[r for r in read(path) if r['role']=='evaluation']
        for method in ['Raw','FirstVisitExact','BlockExact','BlockNormalized']:
            by_engine={}
            for r in data:by_engine.setdefault(int(r['engine_id']),[]).append(float(r['lower_'+method])<=min(float(r['raw_y']),125)<=float(r['upper_'+method]))
            n=len(by_engine);k=sum(all(v) for v in by_engine.values());target=counts[(subset,model,seed,method)]
            assert (int(target['covered_engines']),int(target['evaluation_engines']))==(k,n);close(target['PathCoverage'],k/n);path_checks+=1
    assert (prob_checks,path_checks)==(240,160)
    out.mkdir(parents=True)
    record=dict(status='pass',python=platform.python_version(),manifest_entries_checked=len(manifest['files']),validation_history_rows=384,validation_candidate_minima=24,frozen_selections=8,equal_search_point_runs=point_checks,probability_method_results=prob_checks,positive_Brier_skill=positive,monitoring_method_run_counts=path_checks,scope='CSV/JSON arithmetic and input checks only; no training, forward replay, full table-by-table verification, scientific validation or independent review')
    (out/'summary.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record,indent=2))
if __name__=='__main__':main()

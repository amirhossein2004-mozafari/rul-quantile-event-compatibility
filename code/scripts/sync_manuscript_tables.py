"""Generate manuscript tables directly from saved evidence; never fit models."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/manuscript_sync_stage12'
TABLES=ROOT/'paper/tables'
SUBSETS=['FD001','FD002','FD003','FD004']
SEEDS=[101,202,303,404,505]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def table(headers,rows,caption):
    return '\n'.join(['| '+' | '.join(headers)+' |',
                      '| '+' | '.join(['---']+['---:']*(len(headers)-1))+' |']+
                     ['| '+' | '.join(map(str,r))+' |' for r in rows])+f'\n\n: {caption}\n'


def pair(a,digits=3):
    a=np.asarray(a,dtype=float)
    return f'{a.mean():.{digits}f} ± {a.std(ddof=1):.{digits}f}'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    TABLES.mkdir(parents=True,exist_ok=True)
    sources={}
    def read(path):
        p=ROOT/path
        sources[path]=sha(p)
        return pd.read_csv(p,float_precision='round_trip')
    verification_paths=['results/calibration_stage3/verification.json',
                        'results/conformal_stage56/verification.json',
                        'results/pcgrad_stage78/verification.json',
                        'results/baselines_stage9/verification.json',
                        'results/metrics_latency_stage1011/verification.json']
    for path in verification_paths:
        v=json.loads((ROOT/path).read_text())
        assert v.get('status')=='pass',path
        sources[path]=sha(ROOT/path)
    frames=[]
    point_rows=[]
    raw_rows=[]
    risk_rows=[]
    for subset in SUBSETS:
        group=[]
        for seed in SEEDS:
            df=read(f'results/final_evaluation_v3_exact_conformal/{subset}_seed_{seed}_predictions.csv')
            y=df.true_RUL_clipped.to_numpy()
            p=df.predicted_RUL.to_numpy()
            e=p-y
            group.append(dict(Subset=subset,Seed=seed,RMSE=np.sqrt(np.mean(e**2)),MAE=np.mean(abs(e)),
                              R2=1-np.sum(e**2)/np.sum((y-y.mean())**2),
                              NASA=np.expm1(np.where(e<0,-e/13,e/10)).sum()))
            l=np.clip(df.q05_raw.to_numpy(),0,125)
            u=np.clip(df.q95_raw.to_numpy(),0,125)
            raw_rows.append(dict(Subset=subset,Seed=seed,Coverage=np.mean((y>=l)&(y<=u)),
                                 Width=np.mean(u-l),Winkler=np.mean(u-l+20*np.maximum(l-y,0)+20*np.maximum(y-u,0))))
            z=(df.true_RUL_raw.to_numpy()<=30)
            from sklearn.metrics import roc_auc_score,average_precision_score,f1_score
            risk_rows.append(dict(Subset=subset,Seed=seed,AUC=roc_auc_score(z,df.risk_probability),
                                  AP=average_precision_score(z,df.risk_probability),
                                  F1=f1_score(z,df.risk_probability>=.5)))
        frame=pd.DataFrame(group)
        frames.extend(group)
        point_rows.append([subset]+[pair(frame[m]) for m in ['RMSE','MAE','R2','NASA']])
    point=pd.DataFrame(frames)
    point.to_csv(OUT/'original_point_per_run.csv',index=False)
    raw=pd.DataFrame(raw_rows)
    raw.to_csv(OUT/'raw_intervals_per_run.csv',index=False)
    risk=pd.DataFrame(risk_rows)
    risk.to_csv(OUT/'original_discrimination_per_run.csv',index=False)
    tables={}
    tables['table3_point.md']=table(['Subset','RMSE','MAE','$R^2$','NASA sum'],point_rows,
        'Original 20-checkpoint official-test benchmark. Mean ± sample SD over five seeds; capped target and clipped median, both in [0,125]. NASA is a sum over test engines within each run.')
    uq=read('results/conformal_stage56/per_run.csv')
    rows=[]
    for subset in SUBSETS:
        g=raw[raw.Subset==subset]
        rows.append([subset,'Raw',pair(g.Coverage,4),pair(g.Width),pair(g.Winkler),f'{int((g.Coverage>=.9).sum())}/5'])
        g=uq[uq.Subset==subset]
        for name,key in [('Exact','exact'),('Normalized','adaptive')]:
            rows.append([subset,name,pair(g['Coverage_'+key],4),pair(g['Width_'+key]),
                         pair(g['Winkler_'+key]),f'{int((g["Coverage_"+key]>=.9).sum())}/5'])
    tables['table4_intervals.md']=table(['Subset','Method','Coverage','Width','Winkler','Runs ≥0.90'],rows,
        'Interval performance on the capped target. Mean ± sample SD over five seeds; widths and Winkler scores in cycles after endpoint projection to [0,125]. Lower Winkler is better. Empirical coverage is not a guarantee under the current sampling protocol.')
    rows=[]
    for subset,g in risk.groupby('Subset',sort=True):
        rows.append([subset]+[pair(g[k]) for k in ['AUC','AP','F1']])
    tables['table5_risk_discrimination.md']=table(['Subset','ROC-AUC','AP','Raw F1'],rows,
        'Original naive-MT benchmark: discrimination from raw sigmoid risk outputs. Mean ± sample SD over five seeds; F1 uses probability threshold 0.5 and event raw RUL ≤30.')
    cal=read('results/calibration_stage3/per_run.csv')
    rows=[]
    for subset in SUBSETS:
        g=cal[cal.Subset==subset]
        for method in ['Raw','Bayes','Temp','ShiftTemp']:
            rows.append([subset,method,pair(g['Brier_'+method],4),pair(g['ECE_'+method],4)])
    tables['table6_risk_calibration.md']=table(['Subset','Method','Brier','ECE'],rows,
        'All four probability methods on official-test engines. Mean ± sample SD over five seeds. Fitted methods use final full-calibration refits, not pooled OOF predictions. ECE uses ten equal-width bins.')
    pc=read('results/pcgrad_stage78/per_run.csv')
    rows=[]
    for arm,label in [('single_task','RUL-only'),('naive_mt','Naive MT'),('pcgrad','PCGrad MT')]:
        g=pc[pc.Arm==arm]
        rows.append([label,pair(g.RMSE),pair(g.MAE),pair(g.R2),
                     'not trained' if arm=='single_task' else pair(g.Risk_F1,4)])
    tables['table7_controlled_pcgrad.md']=table(['Arm','RMSE','MAE','$R^2$','Raw F1'],rows,
        'Controlled FD001 official-test optimization ablation: five paired seeds, final epoch 16, canonical model. Mean ± sample SD. RUL-only has no trained risk head.')
    base=read('results/baselines_stage9/per_run.csv')
    rows=[]
    for subset in SUBSETS:
        for model,label in [('lstm','LSTM'),('tcn','TCN'),('hybrid','Hybrid')]:
            g=base[(base.Subset==subset)&(base.Model==model)]
            assert len(g)==5
            rows.append([subset,label,pair(g.RMSE),pair(g.MAE),pair(g.Risk_F1,4)])
    tables['table8_matched_architectures.md']=table(['Subset','Model','RMSE','MAE','Raw F1'],rows,
        'Separate matched architecture experiment: five seeds per model/subset, common fixed 16-epoch naive-MT schedule. Mean ± sample SD. Parameters: LSTM 34,116; TCN 69,668; Hybrid 115,095. These hybrid results are not the original Table 3 checkpoint results.')
    for filename,key,path,label in [
        ('table9_noise_exploratory.md','Sigma','results/metrics/FD001_noise_robustness.csv','Noise SD'),
        ('table10_dropout_exploratory.md','N_Failed','results/metrics/FD001_sensor_dropout_robustness.csv','Failed sensors')]:
        df=read(path)
        rows=[[r[key],f"{r['RMSE_mean']:.3f} ± {r['RMSE_std']:.3f}",
               f"{r['Coverage_mean']:.3f}",f"{r['RiskRecall_mean']:.3f}"] for _,r in df.iterrows()]
        tables[filename]=table([label,'RMSE','Coverage','Risk recall'],rows,
            'Historical exploratory FD001 15-sensor development experiment, not the canonical 18-feature benchmark. Values transcribed from retained summary CSVs; trial-level predictions were not replayed in the present verification.')
    for name,content in tables.items():
        (TABLES/name).write_text(content,encoding='utf-8')
    manifest=dict(status='generated',source_sha256=sources,
                  table_sha256={name:sha(TABLES/name) for name in tables},
                  script_sha256=sha(Path(__file__)),
                  scope='source-derived tables; separate deterministic verification follows')
    (OUT/'table_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'Generated {len(tables)} evidence-derived tables')


if __name__=='__main__':
    main()

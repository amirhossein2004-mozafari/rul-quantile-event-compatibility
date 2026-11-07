from pathlib import Path
import pandas as pd,numpy as np,json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path.cwd();O=R/'reports/manuscript_compact_package_20261102';source=R/'reports/compatibility_null_validation/calibrator_extension/A_all_scores.csv';a=pd.read_csv(source);x=a[(a.method=='projection')&(a.measure=='Brier')&(a.subset!='pooled')].copy();assert len(x)==44
# Rendering only: copy saved values; no aggregation, resampling or fitting.
labels=[f"{r.subset}  {r.family}/{r.architecture}  (n={r.evaluation_engines})" for r in x.itertuples()];v=x.difference_vs_raw.to_numpy();lo=x.difference_ci_low.to_numpy();hi=x.difference_ci_high.to_numpy();y=np.arange(len(x))
fig,ax=plt.subplots(figsize=(8.0,10.8));ax.errorbar(v,y,xerr=np.vstack([v-lo,hi-v]),fmt='o',markersize=3,color='#234f6b',ecolor='#71818d',elinewidth=1,capsize=2);ax.axvline(0,color='black',lw=.8);ax.set_yticks(y,labels,fontsize=7.1);ax.invert_yaxis();ax.set_xlabel('Projection minus raw Brier (score units; negative favors projection)',fontsize=9);ax.set_title('Exploratory projection comparison: all 44 fixed groups',fontsize=11,pad=12);ax.grid(axis='x',alpha=.2);ax.spines[['top','right']].set_visible(False);fig.subplots_adjust(left=.46,right=.98,top=.95,bottom=.08)
fig.text(.46,.025,'Saved 95% engine-cluster bootstrap CIs.\n707 distinct test engines shared across groups.',fontsize=8)
fig.savefig(R/'paper/figures/projection_brier_44_groups.png',dpi=220);fig.savefig(R/'paper/figures/projection_brier_44_groups.pdf');plt.close(fig)
(O/'forest_plot_values.csv').write_text(x.to_csv(index=False),encoding='utf-8');(O/'figure_provenance.json').write_text(json.dumps(dict(source=str(source.relative_to(R)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),rows=44,transformation='Select projection/Brier/nonpooled rows and render saved estimates/CIs only',new_estimates_or_CIs=False,pooled_bin_figure='NOT CREATED: no pooled true-RUL-bin rate/bootstrap-CI CSV saved'),indent=2),encoding='utf-8')
print('Forest rendered directly from 44 saved rows')

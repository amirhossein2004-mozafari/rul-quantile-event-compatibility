---
header-includes:
  - \usepackage{longtable}
  - \usepackage{pdflscape}
  - \usepackage{booktabs}
  - \usepackage{etoolbox}
  - \AtBeginEnvironment{longtable}{\scriptsize\setlength{\tabcolsep}{2pt}}
---

# Validation supplement: quantile and event-probability compatibility

Rates and rate CIs are percentages to one decimal; rate differences are percentage points. Regression coefficients and their CIs use three significant figures. Brier means use the five-decimal source-table precision; other continuous error/width/distance summaries use three significant figures. Counts and protocol identifiers are unchanged. Full-precision source CSVs accompany this document. NA denotes an empty or unidentifiable estimate and is not zero. Engine counts are explicit; repeated fixed fits are not additional independent engines. In incompatible/compatible group counts, the same engine can occur in both groups across fixed fits, so these counts can overlap. S-table labels below are fixed identifiers.

## S0. Locked rule and numerical addendum

Association protocol SHA256: `da781da5c725624ab53503d65cff89037e5ce15f0769a23b27e6d6a04eeb4540`.

> Protocol text (verbatim): require both real outcomes and both synthetic deviations in both families. The same at least six of eight real groups must have positive flag coefficients with 95% engine-bootstrap CIs excluding zero for BOTH median squared error and Brier after the specified RUL adjustment. Synthetic confirmation requires positive adjusted flag AND distance coefficients, with 95% CIs excluding zero, for BOTH squared oracle probability deviation and mean absolute oracle quantile deviation in BOTH families. Family-level effects are the equally weighted mean of the eight temporal subset/architecture coefficients or four covariate subset coefficients, using weighted-raw, final-window, 10,000-engine settings only. Bootstrap draws share engine resamples within each subset across architectures/variants, independently across subsets. Every individual setting is also reported; no choice of favorable settings. Rank-deficient required components fail the rule. If either real or synthetic condition fails, report "not informative" under this rule. No subgroup search or post-result revision.

# Numerical implementation correction, 2026-11-01

The initial run screened the entire covariance matrix for full rank. Inspection showed only two distinct oracle pairs in the FD001 final-window fleet. Cubic nuisance columns are therefore redundant; this alone does not make the requested flag/distance coefficient unidentifiable. The initial partial outputs and run log are retained under initial_rank_screen. That run was interrupted after discovering this issue; no fit was removed.

Before rerunning: preserve the identical regression column space, use the Moore-Penrose solution for redundant nuisance columns, and check target identifiability using the target row of I-A^+A. Return NA only when the target is unidentifiable. SVD relative tolerance 1e-10; target null-space row norm tolerance 1e-6. Report full matrix rank, target identifiability, and condition diagnostics in a separate ledger. Use the same correction for all settings. This changes numerical handling, not outcome definitions, covariates, resampling, cohorts, decision thresholds or hypothesis. The original requirement to report rank-deficient point regressions as NA is retained for genuinely unidentifiable target effects; redundant nuisance parameterizations are disclosed. Both initial nominal-rank-screen outputs and corrected estimable-target results remain available.

Previously observed real branch remains 0/8 jointly passing groups. The corrected run is not a new prospectively unseen experiment; it is a documented implementation correction after a rank-screening issue, with all original outputs retained.



## S0a. Known-law pipeline check: design and limits

The underlying Weibull shape is 1: the exponential excess lifetime is memoryless. The covariate is binary, x in {-1,+1}, with scale(x)=60 exp(0.5x). For final-window evaluation, true conditional RUL depends on x but is independent of age given x; the first feature directly supplies x, while other channels include age and noise. This simplified conditional law and feature construction are not a C-MAPSS-matched pipeline. Matching empirical truncation-age marginals does not match the real conditional RUL/history structure.

Per-fit incompatibility rates occur near 0.0% or 100.0% in the recorded pipeline-check distribution. Among non-collapsed fits, FD001 LSTM has median 99.7% and 97.5th percentile 100.0% (22 fits, 60 fitting engines, 10000 evaluation engines). FD003 LSTM also has 97.5th percentile 100.0% (28 fits, 60 fitting engines, 10000 evaluation engines). FD001 hybrid's real rate of 13.6% on 100 test engines is below the pipeline-check 2.5th percentile of 14.3% from 5 non-collapsed fits evaluated on 10000 engines after fitting on 60 engines. The full min/2.5/25/50/75/97.5/max table is Table S11.

An upper percentile of 100.0% cannot be exceeded by an incompatibility rate. Such a comparison supplies no validation of the real rates. This degenerate known-law pipeline check neither confirms nor refutes the real-data incompatibility rates. The oracle-association results in Table S8 come from this same design and are descriptive only.

### Archived pipeline construction and numerical checks

The synthetic law uses Weibull lifetimes with a simplified covariate relationship and a known conditional RUL distribution. Final-window sampling matches observed C-MAPSS truncation-length marginals; uniform-endpoint evaluation supplies a separate sampling policy. Oracle quantities are evaluated analytically or by deterministic inversion. Temporal models retain independently estimated quantile and event heads and the recorded training objective and budget. This is a known-law pipeline check, including approximation and optimization effects. Covariate-only networks and separately estimated parametric controls provide additional fitted controls within this design. Weighted raw outputs, TrainOff-corrected outputs and unweighted objectives remain separate arms.

Fitting fleets contain 60/156/60/149 engines for FD001–FD004. Evaluation uses both 100/259/100/248-engine fleets and 10,000-engine fleets per subset. The temporal cohorts retain 30 fits per architecture/subset/objective; covariate and parametric controls retain 200 per setting. Tables S1a–S1d report all-fit, non-collapsed and collapsed final-window weighted-raw references; the full policy/objective/size summary accompanies them.

For the FD001 final-window oracle check (Table S2), true quantiles with the true probability give incompatibility rate 0.0% and mean distance 0.0 on 10000 engines. The independently trained temporal LSTM weighted-raw rate is 67.5% on 10000 evaluation engines after fitting on 60 engines. These values describe this fitted pipeline only.

### Archived oracle associations and original decision components

The following material is retained solely as a descriptive record of the same degenerate known-law design and the original locked rule. It is not support for the real-model claim.

Oracle deviations are squared probability error against the known conditional event probability and mean absolute quantile error against the known conditional quantiles. These oracle associations come from the same degenerate shape-1, binary-covariate design described in Supplement S0a. They are reported descriptively and are not support for the real-model central claim. Within this pipeline check, both temporal oracle deviations have positive adjusted flag and distance associations, whereas the covariate family gives mixed directions (10000 evaluation engines per subset; fitting engines 60/156/60/149). For oracle quantile MAE, the temporal family flag coefficient is 1.21 cycles, CI [1.19, 1.24]; the covariate coefficient is -1.89 cycles, CI [-1.91, -1.86]. These are equally weighted family summaries, not independent-model samples. The remaining coefficients are listed below.

- Temporal, squared-probability flag: coefficient 0.00501;  
  CI [0.00492, 0.00511].

- Temporal, squared-probability distance: coefficient 0.00141;  
  CI [0.00138, 0.00145].

- Temporal, quantile-MAE distance: coefficient 0.428;  
  CI [0.420, 0.437].

- Covariate, squared-probability flag: coefficient -0.00124;  
  CI [-0.00151, -0.000952].

- Covariate, squared-probability distance: coefficient 0.000923;  
  CI [0.000811, 0.00104].

- Covariate, quantile-MAE distance: coefficient -0.655;  
  CI [-0.670, -0.640].

Distance effects are per 0.1 probability-distance unit; all brackets are 95% engine-bootstrap CIs, with 10000 evaluation engines per subset and fitting counts 60/156/60/149. Tables S7a–S7b give the complete real associations and RUL-bin contrasts; Table S8 gives all primary oracle coefficients and links the full setting-specific association CSV.

### Table S0a-1. Original main-text decision-component table

| Component | Saved result | Evaluation engines |
|---|---|---|
| Real positive median-error associations | 0/8 groups | 100/259/100/248 per subset |
| Real positive Brier associations | 6/8 groups | 100/259/100/248 per subset |
| Real groups passing both outcomes | 0/8 groups | 100/259/100/248 per subset |
| Temporal required synthetic coefficients | 4/4 pass | 10000 per subset |
| Covariate required synthetic coefficients | 1/4 pass | 10000 per subset |

Saved components of the original locked decision rule. Positive means that the corresponding 95% CI excludes zero in the positive direction; the joint verdict remains not informative. Synthetic components are protocol records, not evidence validating the real-data rates.

## S0b. Synthetic gap and optimization checks

Gap collapse is defined by a median lower softplus gap below 1.25 cycles. Synthetic strata use a separate uniform-endpoint audit fleet of 10000 engines; real classification uses calibration engines. The retained real fits show no collapse under this definition on 20/52/20/50 calibration engines for FD001–FD004. The initialization-only intervention removes collapse in its tested synthetic cohort, yet incompatibility remains (60 fitting engines and 10000 evaluation engines). Tables S4a–S4c and S5 give the initialization/loss-scale/learning-rate/clipping outcomes; the frozen paper models are unchanged.

## S0c. AI-use model and build details

OpenAI Codex assisted with code implementation and correction, analysis scripting, figure preparation, language editing and manuscript revision. The recorded configured model is `gpt-6.1-sol`, runtime `0.166.0-alpha.5.1`, and desktop build `26.1027.3384.0`. The runtime executable SHA256 is `3097c909fb6d5cd63510d44aceb1d42df9f6e85722a3e447e477def1ecf60e16`. The exact served checkpoint is unavailable. These identifiers are copied from the saved AI provenance records; they are not inferred from the product name. The author remains responsible for checking the text, evidence and submitted version.

Revision date: 2026-11-01. The exact served checkpoint remains unavailable.

## S0d. Full chronological analysis history

The table records every identifiable stage from the skeptical-review findings. “After results” means that the stage was chosen after earlier results were examined. Initial choice history is unresolved; local locks do not establish independent registration or an untouched scientific design.

| Analysis stage, in chronological order | Chosen after seeing earlier results? |
|---|---|
| Initial benchmark, architecture/loss, event horizon, RUL cap and compatibility choices; equal-search fitting and selection | Initial choice history unknown; equal-search design followed earlier benchmark development, although fitting selection used validation error. |
| Real-table reproduction gate and synthetic/quantile-perturbation validation, including final temporal synthetic design | Yes; real-model incompatibility rates had already been examined. |
| Extreme-null investigation of near-coincident quantiles | Yes; followed extreme synthetic incompatibility and small gaps. |
| Collapse cutoff and collapse-conditioned null analysis | Yes; followed the extreme-null investigation. |
| Factorial collapse-cause experiment | Yes; followed inspected collapse results. |
| Fixed initialization intervention | Yes; followed inspected collapse results. |
| Real-model weighting attribution and unweighted retraining comparisons | Yes; chosen in the collapse/weighting follow-up. |
| RUL-adjusted median-error/Brier associations, RUL bins, incremental probability adjustment and threshold-band rates | Yes; followed incompatibility/collapse results; the band was fixed before the first association calculation. |
| Additional probability-plus-band flag adjustment and operational decision rule | Yes; followed the association results. |
| Synthetic percentile/difficulty comparisons in the retained non-collapsed stratum | Yes; followed earlier synthetic results. |
| Event-head replacements and logit shifts; direct probability projection | Yes; followed compatibility/association results. |
| Own-mean effect ratios, MDEs and pooled effects | Yes; part of the later controls/projection/power analysis. |
| Expanded-model standard-calibrator comparison and calibrator-then-projection paths | Yes; followed the earlier controls/projection/association results. |
| Expanded-roster projection consistency counts and fixed distance-bin analysis | Yes; chosen for the expanded-model follow-up. |
| Projection mechanism/base-rate checks and replicated adjusted associations, including the restricted threshold band | Yes; chosen for the expanded-model follow-up. |

## Table S1a. Known-law pipeline-check strata: final-window, weighted raw, 10000 engines

Source: `null_stratified_summary.csv`. Rows: 48. The full source is in `validation_data`.

| Family / group | Fit / test engines | Stratum | Fits | Rate [95% CI] | Mean distance |
|---|---|---|---|---|---|
| temporal FD001 lstm | 60/10000 | all | 30 | 67.5% [67.5%, 67.6%] | 0.150 |
| temporal FD001 lstm | 60/10000 | noncollapsed | 22 | 60.3% [60.2%, 60.3%] | 0.0782 |
| temporal FD001 lstm | 60/10000 | collapsed | 8 | 87.5% [87.5%, 87.5%] | 0.348 |
| temporal FD001 hybrid | 60/10000 | all | 30 | 65.7% [65.3%, 66.0%] | 0.149 |
| temporal FD001 hybrid | 60/10000 | noncollapsed | 5 | 42.6% [42.5%, 42.8%] | 0.0310 |
| temporal FD001 hybrid | 60/10000 | collapsed | 25 | 70.3% [69.9%, 70.7%] | 0.172 |
| covariate FD001 covariate | 60/10000 | all | 200 | 34.1% [33.5%, 34.8%] | 0.0519 |
| covariate FD001 covariate | 60/10000 | noncollapsed | 200 | 34.1% [33.5%, 34.8%] | 0.0519 |
| covariate FD001 covariate | 60/10000 | collapsed | 0 | NA [NA, NA] | NA |
| parametric FD001 independent exact family | 60/10000 | all | 200 | 13.7% [13.4%, 14.0%] | 0.0146 |
| parametric FD001 independent exact family | 60/10000 | noncollapsed | 200 | 13.7% [13.4%, 14.0%] | 0.0146 |
| parametric FD001 independent exact family | 60/10000 | collapsed | 0 | NA [NA, NA] | NA |
| temporal FD002 lstm | 156/10000 | all | 30 | 26.8% [26.3%, 27.2%] | 0.0407 |
| temporal FD002 lstm | 156/10000 | noncollapsed | 30 | 26.8% [26.3%, 27.2%] | 0.0407 |
| temporal FD002 lstm | 156/10000 | collapsed | 0 | NA [NA, NA] | NA |
| temporal FD002 hybrid | 156/10000 | all | 30 | 45.0% [44.8%, 45.2%] | 0.0873 |
| temporal FD002 hybrid | 156/10000 | noncollapsed | 10 | 25.7% [25.4%, 26.0%] | 0.0139 |
| temporal FD002 hybrid | 156/10000 | collapsed | 20 | 54.6% [54.2%, 55.1%] | 0.124 |
| covariate FD002 covariate | 156/10000 | all | 200 | 12.2% [12.0%, 12.4%] | 0.0188 |
| covariate FD002 covariate | 156/10000 | noncollapsed | 200 | 12.2% [12.0%, 12.4%] | 0.0188 |
| covariate FD002 covariate | 156/10000 | collapsed | 0 | NA [NA, NA] | NA |
| parametric FD002 independent exact family | 156/10000 | all | 200 | 7.3% [7.1%, 7.4%] | 0.00783 |
| parametric FD002 independent exact family | 156/10000 | noncollapsed | 200 | 7.3% [7.1%, 7.4%] | 0.00783 |
| parametric FD002 independent exact family | 156/10000 | collapsed | 0 | NA [NA, NA] | NA |
| temporal FD003 lstm | 60/10000 | all | 30 | 42.9% [42.6%, 43.2%] | 0.0337 |
| temporal FD003 lstm | 60/10000 | noncollapsed | 28 | 40.6% [40.2%, 41.0%] | 0.0348 |
| temporal FD003 lstm | 60/10000 | collapsed | 2 | 75.1% [74.5%, 75.6%] | 0.0186 |
| temporal FD003 hybrid | 60/10000 | all | 30 | 47.1% [46.9%, 47.3%] | 0.0843 |
| temporal FD003 hybrid | 60/10000 | noncollapsed | 17 | 34.3% [33.8%, 34.7%] | 0.0721 |
| temporal FD003 hybrid | 60/10000 | collapsed | 13 | 63.9% [63.6%, 64.2%] | 0.100 |
| covariate FD003 covariate | 60/10000 | all | 200 | 37.1% [36.5%, 37.7%] | 0.0550 |
| covariate FD003 covariate | 60/10000 | noncollapsed | 200 | 37.1% [36.5%, 37.7%] | 0.0550 |
| covariate FD003 covariate | 60/10000 | collapsed | 0 | NA [NA, NA] | NA |
| parametric FD003 independent exact family | 60/10000 | all | 200 | 13.7% [13.5%, 14.0%] | 0.0146 |
| parametric FD003 independent exact family | 60/10000 | noncollapsed | 200 | 13.7% [13.5%, 14.0%] | 0.0146 |
| parametric FD003 independent exact family | 60/10000 | collapsed | 0 | NA [NA, NA] | NA |
| temporal FD004 lstm | 149/10000 | all | 30 | 29.4% [28.9%, 29.9%] | 0.0465 |
| temporal FD004 lstm | 149/10000 | noncollapsed | 30 | 29.4% [28.9%, 29.9%] | 0.0465 |
| temporal FD004 lstm | 149/10000 | collapsed | 0 | NA [NA, NA] | NA |
| temporal FD004 hybrid | 149/10000 | all | 30 | 44.7% [44.7%, 44.8%] | 0.0521 |
| temporal FD004 hybrid | 149/10000 | noncollapsed | 18 | 32.6% [32.3%, 32.8%] | 0.0252 |
| temporal FD004 hybrid | 149/10000 | collapsed | 12 | 63.0% [62.8%, 63.3%] | 0.0925 |
| covariate FD004 covariate | 149/10000 | all | 200 | 14.4% [14.2%, 14.7%] | 0.0214 |
| covariate FD004 covariate | 149/10000 | noncollapsed | 200 | 14.4% [14.2%, 14.7%] | 0.0214 |
| covariate FD004 covariate | 149/10000 | collapsed | 0 | NA [NA, NA] | NA |
| parametric FD004 independent exact family | 149/10000 | all | 200 | 5.8% [5.7%, 5.9%] | 0.00587 |
| parametric FD004 independent exact family | 149/10000 | noncollapsed | 200 | 5.8% [5.7%, 5.9%] | 0.00587 |
| parametric FD004 independent exact family | 149/10000 | collapsed | 0 | NA [NA, NA] | NA |

## Table S1b. Temporal cross-pipeline numerical comparisons, all strata; not a benchmark

Source: `comparison_temporal.csv`. Rows: 24. The full source is in `validation_data`.

| Real group | Fit / null / real engines | Stratum | Pipeline fits | Real rate | Pipeline 97.5th | Exceeds |
|---|---|---|---|---|---|---|
| FD001 LSTM | 60/10000/100 | all | 30 | 20.4% | 100.0% | False |
| FD001 LSTM | 60/10000/100 | noncollapsed | 22 | 20.4% | 100.0% | False |
| FD001 LSTM | 60/10000/100 | collapsed | 8 | 20.4% | 100.0% | False |
| FD001 Hybrid | 60/10000/100 | all | 30 | 13.6% | 100.0% | False |
| FD001 Hybrid | 60/10000/100 | noncollapsed | 5 | 13.6% | 55.2% | False |
| FD001 Hybrid | 60/10000/100 | collapsed | 25 | 13.6% | 100.0% | False |
| FD002 LSTM | 156/10000/259 | all | 30 | 9.6% | 57.5% | False |
| FD002 LSTM | 156/10000/259 | noncollapsed | 30 | 9.6% | 57.5% | False |
| FD002 LSTM | 156/10000/259 | collapsed | 0 | 9.6% | NA | NA |
| FD002 Hybrid | 156/10000/259 | all | 30 | 8.9% | 100.0% | False |
| FD002 Hybrid | 156/10000/259 | noncollapsed | 10 | 8.9% | 88.8% | False |
| FD002 Hybrid | 156/10000/259 | collapsed | 20 | 8.9% | 100.0% | False |
| FD003 LSTM | 60/10000/100 | all | 30 | 12.8% | 100.0% | False |
| FD003 LSTM | 60/10000/100 | noncollapsed | 28 | 12.8% | 100.0% | False |
| FD003 LSTM | 60/10000/100 | collapsed | 2 | 12.8% | 96.5% | False |
| FD003 Hybrid | 60/10000/100 | all | 30 | 11.8% | 97.9% | False |
| FD003 Hybrid | 60/10000/100 | noncollapsed | 17 | 11.8% | 79.3% | False |
| FD003 Hybrid | 60/10000/100 | collapsed | 13 | 11.8% | 99.1% | False |
| FD004 LSTM | 149/10000/248 | all | 30 | 16.6% | 60.2% | False |
| FD004 LSTM | 149/10000/248 | noncollapsed | 30 | 16.6% | 60.2% | False |
| FD004 LSTM | 149/10000/248 | collapsed | 0 | 16.6% | NA | NA |
| FD004 Hybrid | 149/10000/248 | all | 30 | 12.7% | 96.8% | False |
| FD004 Hybrid | 149/10000/248 | noncollapsed | 18 | 12.7% | 94.5% | False |
| FD004 Hybrid | 149/10000/248 | collapsed | 12 | 12.7% | 97.9% | False |

## Table S1c. Covariate cross-pipeline numerical comparisons, all strata; not a benchmark

Source: `comparison_covariate.csv`. Rows: 24. The full source is in `validation_data`.

| Real group | Fit / null / real engines | Stratum | Pipeline fits | Real rate | Pipeline 97.5th | Exceeds |
|---|---|---|---|---|---|---|
| FD001 LSTM | 60/10000/100 | all | 200 | 20.4% | 60.6% | False |
| FD001 Hybrid | 60/10000/100 | all | 200 | 13.6% | 60.6% | False |
| FD001 LSTM | 60/10000/100 | noncollapsed | 200 | 20.4% | 60.6% | False |
| FD001 Hybrid | 60/10000/100 | noncollapsed | 200 | 13.6% | 60.6% | False |
| FD001 LSTM | 60/10000/100 | collapsed | 0 | 20.4% | NA | NA |
| FD001 Hybrid | 60/10000/100 | collapsed | 0 | 13.6% | NA | NA |
| FD002 LSTM | 156/10000/259 | all | 200 | 9.6% | 50.3% | False |
| FD002 Hybrid | 156/10000/259 | all | 200 | 8.9% | 50.3% | False |
| FD002 LSTM | 156/10000/259 | noncollapsed | 200 | 9.6% | 50.3% | False |
| FD002 Hybrid | 156/10000/259 | noncollapsed | 200 | 8.9% | 50.3% | False |
| FD002 LSTM | 156/10000/259 | collapsed | 0 | 9.6% | NA | NA |
| FD002 Hybrid | 156/10000/259 | collapsed | 0 | 8.9% | NA | NA |
| FD003 LSTM | 60/10000/100 | all | 200 | 12.8% | 69.3% | False |
| FD003 Hybrid | 60/10000/100 | all | 200 | 11.8% | 69.3% | False |
| FD003 LSTM | 60/10000/100 | noncollapsed | 200 | 12.8% | 69.3% | False |
| FD003 Hybrid | 60/10000/100 | noncollapsed | 200 | 11.8% | 69.3% | False |
| FD003 LSTM | 60/10000/100 | collapsed | 0 | 12.8% | NA | NA |
| FD003 Hybrid | 60/10000/100 | collapsed | 0 | 11.8% | NA | NA |
| FD004 LSTM | 149/10000/248 | all | 200 | 16.6% | 50.3% | False |
| FD004 Hybrid | 149/10000/248 | all | 200 | 12.7% | 50.3% | False |
| FD004 LSTM | 149/10000/248 | noncollapsed | 200 | 16.6% | 50.3% | False |
| FD004 Hybrid | 149/10000/248 | noncollapsed | 200 | 12.7% | 50.3% | False |
| FD004 LSTM | 149/10000/248 | collapsed | 0 | 16.6% | NA | NA |
| FD004 Hybrid | 149/10000/248 | collapsed | 0 | 12.7% | NA | NA |

## Table S1d. Parametric cross-pipeline numerical comparisons, all strata; not a benchmark

Source: `comparison_parametric.csv`. Rows: 24. The full source is in `validation_data`.

| Real group | Fit / null / real engines | Stratum | Pipeline fits | Real rate | Pipeline 97.5th | Exceeds |
|---|---|---|---|---|---|---|
| FD001 LSTM | 60/10000/100 | all | 200 | 20.4% | 49.8% | False |
| FD001 Hybrid | 60/10000/100 | all | 200 | 13.6% | 49.8% | False |
| FD001 LSTM | 60/10000/100 | noncollapsed | 200 | 20.4% | 49.8% | False |
| FD001 Hybrid | 60/10000/100 | noncollapsed | 200 | 13.6% | 49.8% | False |
| FD001 LSTM | 60/10000/100 | collapsed | 0 | 20.4% | NA | NA |
| FD001 Hybrid | 60/10000/100 | collapsed | 0 | 13.6% | NA | NA |
| FD002 LSTM | 156/10000/259 | all | 200 | 9.6% | 50.1% | False |
| FD002 Hybrid | 156/10000/259 | all | 200 | 8.9% | 50.1% | False |
| FD002 LSTM | 156/10000/259 | noncollapsed | 200 | 9.6% | 50.1% | False |
| FD002 Hybrid | 156/10000/259 | noncollapsed | 200 | 8.9% | 50.1% | False |
| FD002 LSTM | 156/10000/259 | collapsed | 0 | 9.6% | NA | NA |
| FD002 Hybrid | 156/10000/259 | collapsed | 0 | 8.9% | NA | NA |
| FD003 LSTM | 60/10000/100 | all | 200 | 12.8% | 49.9% | False |
| FD003 Hybrid | 60/10000/100 | all | 200 | 11.8% | 49.9% | False |
| FD003 LSTM | 60/10000/100 | noncollapsed | 200 | 12.8% | 49.9% | False |
| FD003 Hybrid | 60/10000/100 | noncollapsed | 200 | 11.8% | 49.9% | False |
| FD003 LSTM | 60/10000/100 | collapsed | 0 | 12.8% | NA | NA |
| FD003 Hybrid | 60/10000/100 | collapsed | 0 | 11.8% | NA | NA |
| FD004 LSTM | 149/10000/248 | all | 200 | 16.6% | 50.2% | False |
| FD004 Hybrid | 149/10000/248 | all | 200 | 12.7% | 50.2% | False |
| FD004 LSTM | 149/10000/248 | noncollapsed | 200 | 16.6% | 50.2% | False |
| FD004 Hybrid | 149/10000/248 | noncollapsed | 200 | 12.7% | 50.2% | False |
| FD004 LSTM | 149/10000/248 | collapsed | 0 | 16.6% | NA | NA |
| FD004 Hybrid | 149/10000/248 | collapsed | 0 | 12.7% | NA | NA |

## Table S2. Oracle quantiles with true probability and controlled quantile noise

Source: `synthetic_oracle_noise.csv`. Rows: 64. The full source is in `validation_data`.

| Subset / policy | Fit / test engines | Noise | Rate [95% CI] | Mean distance |
|---|---|---|---|---|
| FD001 final | 0/100 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD001 final | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD001 final | 0/100 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD001 final | 0/10000 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00000212 |
| FD001 final | 0/100 | 10.0% | 1.0% [0.7%, 1.2%] | 0.00261 |
| FD001 final | 0/10000 | 10.0% | 1.2% [1.1%, 1.2%] | 0.00308 |
| FD001 final | 0/100 | 20.0% | 11.6% [10.9%, 12.4%] | 0.0401 |
| FD001 final | 0/10000 | 20.0% | 12.2% [12.1%, 12.3%] | 0.0401 |
| FD001 uniform | 0/100 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD001 uniform | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD001 uniform | 0/100 | 5.0% | 0.7% [0.0%, 1.9%] | 0.00000950 |
| FD001 uniform | 0/10000 | 5.0% | 0.2% [0.2%, 0.2%] | 0.00000500 |
| FD001 uniform | 0/100 | 10.0% | 1.6% [0.6%, 3.0%] | 0.00287 |
| FD001 uniform | 0/10000 | 10.0% | 0.9% [0.9%, 1.0%] | 0.00242 |
| FD001 uniform | 0/100 | 20.0% | 9.4% [7.9%, 11.1%] | 0.0364 |
| FD001 uniform | 0/10000 | 20.0% | 8.1% [8.0%, 8.3%] | 0.0334 |
| FD002 final | 0/259 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD002 final | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD002 final | 0/259 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD002 final | 0/10000 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00000148 |
| FD002 final | 0/259 | 10.0% | 1.1% [1.0%, 1.3%] | 0.00307 |
| FD002 final | 0/10000 | 10.0% | 1.1% [1.1%, 1.2%] | 0.00309 |
| FD002 final | 0/259 | 20.0% | 12.4% [11.8%, 12.9%] | 0.0403 |
| FD002 final | 0/10000 | 20.0% | 12.1% [12.1%, 12.2%] | 0.0399 |
| FD002 uniform | 0/259 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD002 uniform | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD002 uniform | 0/259 | 5.0% | 0.2% [0.1%, 0.5%] | 0.0000230 |
| FD002 uniform | 0/10000 | 5.0% | 0.2% [0.1%, 0.2%] | 0.00000587 |
| FD002 uniform | 0/259 | 10.0% | 1.2% [0.8%, 1.8%] | 0.00289 |
| FD002 uniform | 0/10000 | 10.0% | 1.0% [0.9%, 1.0%] | 0.00236 |
| FD002 uniform | 0/259 | 20.0% | 8.5% [7.7%, 9.4%] | 0.0341 |
| FD002 uniform | 0/10000 | 20.0% | 8.1% [8.0%, 8.3%] | 0.0332 |
| FD003 final | 0/100 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD003 final | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD003 final | 0/100 | 5.0% | 0.0% [0.0%, 0.0%] | 0.0000212 |
| FD003 final | 0/10000 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00000127 |
| FD003 final | 0/100 | 10.0% | 1.2% [1.0%, 1.5%] | 0.00337 |
| FD003 final | 0/10000 | 10.0% | 1.2% [1.1%, 1.2%] | 0.00310 |
| FD003 final | 0/100 | 20.0% | 12.5% [11.7%, 13.3%] | 0.0419 |
| FD003 final | 0/10000 | 20.0% | 12.2% [12.2%, 12.3%] | 0.0402 |
| FD003 uniform | 0/100 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD003 uniform | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD003 uniform | 0/100 | 5.0% | 0.0% [0.0%, 0.0%] | 6.52e-7 |
| FD003 uniform | 0/10000 | 5.0% | 0.2% [0.1%, 0.2%] | 0.00000567 |
| FD003 uniform | 0/100 | 10.0% | 0.8% [0.6%, 1.2%] | 0.00262 |
| FD003 uniform | 0/10000 | 10.0% | 1.0% [0.9%, 1.0%] | 0.00243 |
| FD003 uniform | 0/100 | 20.0% | 8.5% [7.2%, 9.9%] | 0.0365 |
| FD003 uniform | 0/10000 | 20.0% | 8.2% [8.1%, 8.3%] | 0.0335 |
| FD004 final | 0/248 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD004 final | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD004 final | 0/248 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD004 final | 0/10000 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00000233 |
| FD004 final | 0/248 | 10.0% | 1.1% [1.0%, 1.3%] | 0.00290 |
| FD004 final | 0/10000 | 10.0% | 1.2% [1.1%, 1.2%] | 0.00310 |
| FD004 final | 0/248 | 20.0% | 12.5% [12.0%, 13.0%] | 0.0414 |
| FD004 final | 0/10000 | 20.0% | 12.2% [12.1%, 12.3%] | 0.0402 |
| FD004 uniform | 0/248 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD004 uniform | 0/10000 | 0.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD004 uniform | 0/248 | 5.0% | 0.0% [0.0%, 0.0%] | 0.00 |
| FD004 uniform | 0/10000 | 5.0% | 0.2% [0.1%, 0.2%] | 0.00000481 |
| FD004 uniform | 0/248 | 10.0% | 0.5% [0.4%, 0.7%] | 0.00225 |
| FD004 uniform | 0/10000 | 10.0% | 0.9% [0.9%, 1.0%] | 0.00239 |
| FD004 uniform | 0/248 | 20.0% | 7.8% [7.1%, 8.5%] | 0.0343 |
| FD004 uniform | 0/10000 | 20.0% | 8.2% [8.1%, 8.4%] | 0.0337 |

## Table S3. Perturbation sensitivity, all groups and noise levels

Source: `perturbation_summary.csv`. Rows: 32. The full source is in `validation_data`.

| Group | Test engines | Noise | Rate [95% CI] | Change, pp [95% CI] | Mean distance | Crossing rate |
|---|---|---|---|---|---|---|
| FD001 lstm | 100 | 0.0% | 20.4% [14.4%, 26.8%] | 0.0 [0.0, 0.0] | 0.0210 | 0.0% |
| FD001 lstm | 100 | 5.0% | 20.5% [14.7%, 26.8%] | 0.1 [-0.5, 0.7] | 0.0217 | 0.0% |
| FD001 lstm | 100 | 10.0% | 20.4% [14.6%, 26.6%] | -0.0 [-0.9, 0.9] | 0.0230 | 0.0% |
| FD001 lstm | 100 | 20.0% | 21.0% [15.4%, 27.1%] | 0.6 [-0.8, 2.0] | 0.0276 | 3.6% |
| FD001 hybrid | 100 | 0.0% | 13.6% [8.8%, 19.2%] | 0.0 [0.0, 0.0] | 0.0138 | 0.0% |
| FD001 hybrid | 100 | 5.0% | 13.1% [8.4%, 18.4%] | -0.5 [-1.1, -0.0] | 0.0133 | 0.0% |
| FD001 hybrid | 100 | 10.0% | 13.0% [8.4%, 18.2%] | -0.6 [-1.6, 0.2] | 0.0134 | 0.0% |
| FD001 hybrid | 100 | 20.0% | 13.0% [8.7%, 18.0%] | -0.6 [-2.0, 0.7] | 0.0149 | 2.1% |
| FD002 lstm | 259 | 0.0% | 9.6% [6.9%, 12.7%] | 0.0 [0.0, 0.0] | 0.00671 | 0.0% |
| FD002 lstm | 259 | 5.0% | 9.9% [7.3%, 12.9%] | 0.3 [-0.0, 0.8] | 0.00711 | 0.0% |
| FD002 lstm | 259 | 10.0% | 10.4% [7.7%, 13.3%] | 0.8 [0.2, 1.4] | 0.00783 | 0.0% |
| FD002 lstm | 259 | 20.0% | 12.0% [9.5%, 14.7%] | 2.4 [1.4, 3.4] | 0.0105 | 2.5% |
| FD002 hybrid | 259 | 0.0% | 8.9% [6.5%, 11.5%] | 0.0 [0.0, 0.0] | 0.00720 | 0.0% |
| FD002 hybrid | 259 | 5.0% | 8.9% [6.7%, 11.5%] | 0.1 [-0.3, 0.4] | 0.00773 | 0.0% |
| FD002 hybrid | 259 | 10.0% | 9.5% [7.3%, 12.0%] | 0.7 [0.1, 1.2] | 0.00882 | 0.0% |
| FD002 hybrid | 259 | 20.0% | 11.4% [9.1%, 13.9%] | 2.5 [1.7, 3.4] | 0.0119 | 3.0% |
| FD003 lstm | 100 | 0.0% | 12.8% [8.4%, 17.8%] | 0.0 [0.0, 0.0] | 0.0150 | 0.0% |
| FD003 lstm | 100 | 5.0% | 12.9% [8.5%, 17.8%] | 0.1 [-0.5, 0.8] | 0.0156 | 0.0% |
| FD003 lstm | 100 | 10.0% | 13.3% [8.9%, 18.2%] | 0.5 [-0.4, 1.7] | 0.0167 | 0.0% |
| FD003 lstm | 100 | 20.0% | 14.6% [10.2%, 19.3%] | 1.8 [0.4, 3.4] | 0.0196 | 1.7% |
| FD003 hybrid | 100 | 0.0% | 11.8% [8.0%, 16.4%] | 0.0 [0.0, 0.0] | 0.0149 | 0.0% |
| FD003 hybrid | 100 | 5.0% | 11.7% [7.9%, 16.1%] | -0.1 [-0.7, 0.4] | 0.0151 | 0.0% |
| FD003 hybrid | 100 | 10.0% | 11.4% [7.7%, 15.8%] | -0.4 [-1.0, 0.2] | 0.0155 | 0.0% |
| FD003 hybrid | 100 | 20.0% | 11.9% [8.2%, 16.2%] | 0.1 [-0.7, 0.8] | 0.0168 | 1.4% |
| FD004 lstm | 248 | 0.0% | 16.6% [13.0%, 20.4%] | 0.0 [0.0, 0.0] | 0.0137 | 0.0% |
| FD004 lstm | 248 | 5.0% | 16.6% [13.1%, 20.4%] | 0.0 [-0.4, 0.4] | 0.0143 | 0.0% |
| FD004 lstm | 248 | 10.0% | 17.0% [13.5%, 20.8%] | 0.4 [-0.2, 1.0] | 0.0162 | 0.1% |
| FD004 lstm | 248 | 20.0% | 18.5% [15.2%, 22.1%] | 1.9 [0.9, 2.9] | 0.0215 | 3.4% |
| FD004 hybrid | 248 | 0.0% | 12.7% [9.8%, 15.8%] | 0.0 [0.0, 0.0] | 0.00857 | 0.0% |
| FD004 hybrid | 248 | 5.0% | 12.7% [9.9%, 15.8%] | 0.0 [-0.3, 0.4] | 0.00902 | 0.0% |
| FD004 hybrid | 248 | 10.0% | 13.2% [10.5%, 16.2%] | 0.6 [0.0, 1.1] | 0.0104 | 0.1% |
| FD004 hybrid | 248 | 20.0% | 14.9% [12.2%, 17.9%] | 2.2 [1.4, 3.1] | 0.0145 | 4.1% |

## Table S4a. Real calibration-only collapse classification

Source: `real_collapse_fractions.csv`. Rows: 8. The full source is in `validation_data`.

| Group | Fit / cal / test engines | Fits | Collapsed fits | Collapsed fraction |
|---|---|---|---|---|
| FD001 lstm | 60/20/100 | 5 | 0 | 0.0% |
| FD001 hybrid | 60/20/100 | 5 | 0 | 0.0% |
| FD002 lstm | 156/52/259 | 5 | 0 | 0.0% |
| FD002 hybrid | 156/52/259 | 5 | 0 | 0.0% |
| FD003 lstm | 60/20/100 | 5 | 0 | 0.0% |
| FD003 hybrid | 60/20/100 | 5 | 0 | 0.0% |
| FD004 lstm | 149/50/248 | 5 | 0 | 0.0% |
| FD004 hybrid | 149/50/248 | 5 | 0 | 0.0% |

## Table S4b. Initialization-only intervention safeguards

Source: `fix_success_checks.csv`. Rows: 4. The full source is in `validation_data`.

| Architecture / objective | Fit / test engines | Completed / failed | Collapsed fits | Oracle MAE change [95% CI] |
|---|---|---|---|---|
| lstm weighted | 60/10000 | 30/0 | 0 | -14.5 [-14.5, -14.5] |
| lstm unweighted | 60/10000 | 30/0 | 0 | -14.6 [-14.6, -14.6] |
| hybrid weighted | 60/10000 | 30/0 | 0 | -12.6 [-12.7, -12.6] |
| hybrid unweighted | 60/10000 | 30/0 | 0 | -12.7 [-12.7, -12.6] |

## Table S4c. Initialization-only intervention: final-window all-fit rates

Source: `fixed_init_summary.csv`. Rows: 6. The full source is in `validation_data`.

| Group / variant | Fit / test engines | Fits | Rate [95% CI] | Mean distance |
|---|---|---|---|---|
| FD001 lstm weighted raw | 60/10000 | 30 | 40.0% [39.8%, 40.1%] | 0.0121 |
| FD001 lstm weighted corrected | 60/10000 | 30 | 64.0% [63.7%, 64.4%] | 0.0859 |
| FD001 lstm unweighted | 60/10000 | 30 | 61.5% [61.1%, 61.9%] | 0.0722 |
| FD001 hybrid weighted raw | 60/10000 | 30 | 38.3% [38.1%, 38.4%] | 0.0215 |
| FD001 hybrid weighted corrected | 60/10000 | 30 | 37.0% [36.4%, 37.7%] | 0.0525 |
| FD001 hybrid unweighted | 60/10000 | 30 | 34.5% [34.0%, 35.1%] | 0.0222 |

## Table S5. All factorial main/interaction contrast summaries

Source: `factorial_contrast_summary.csv`. Rows: 90. The full source is in `validation_data`.

| Architecture / factors | Metric | Fit / test engines | Paired fleets | Mean contrast | Min / max contrast |
|---|---|---|---|---|---|
| lstm clipping disabled | collapsed | 60/10000 | 3 | 0.00 | 0.00/0.00 |
| lstm clipping disabled | rate | 60/10000 | 3 | 0.0655 | 0.0349/0.0923 |
| lstm clipping disabled | distance | 60/10000 | 3 | -0.000820 | -0.00393/0.00195 |
| lstm initialization | collapsed | 60/10000 | 3 | -0.5 | -1.0/0.00 |
| lstm initialization | rate | 60/10000 | 3 | -0.418 | -0.672/-0.241 |
| lstm initialization | distance | 60/10000 | 3 | -0.153 | -0.239/-0.0762 |
| lstm initialization*clipping disabled | collapsed | 60/10000 | 3 | 0.00 | 0.00/0.00 |
| lstm initialization*clipping disabled | rate | 60/10000 | 3 | -0.00399 | -0.141/0.0705 |
| lstm initialization*clipping disabled | distance | 60/10000 | 3 | 0.00149 | -0.00676/0.0135 |
| lstm initialization*lr tripled | collapsed | 60/10000 | 3 | 0.167 | 0.00/0.5 |
| lstm initialization*lr tripled | rate | 60/10000 | 3 | 0.182 | -0.176/0.499 |
| lstm initialization*lr tripled | distance | 60/10000 | 3 | 0.218 | 0.147/0.277 |
| lstm initialization*lr tripled*clipping disabled | collapsed | 60/10000 | 3 | -0.333 | -1.0/0.00 |
| lstm initialization*lr tripled*clipping disabled | rate | 60/10000 | 3 | -0.227 | -0.345/-0.0553 |
| lstm initialization*lr tripled*clipping disabled | distance | 60/10000 | 3 | -0.00918 | -0.0158/-0.00584 |
| lstm initialization*pinball normalized | collapsed | 60/10000 | 3 | 0.00 | 0.00/0.00 |
| lstm initialization*pinball normalized | rate | 60/10000 | 3 | 0.369 | 0.205/0.477 |
| lstm initialization*pinball normalized | distance | 60/10000 | 3 | 0.00205 | -0.121/0.174 |
| lstm initialization*pinball normalized*clipping disabled | collapsed | 60/10000 | 3 | 0.00 | 0.00/0.00 |
| lstm initialization*pinball normalized*clipping disabled | rate | 60/10000 | 3 | 0.0209 | -0.141/0.249 |
| lstm initialization*pinball normalized*clipping disabled | distance | 60/10000 | 3 | 0.00563 | 0.00449/0.00781 |
| lstm initialization*pinball normalized*lr tripled | collapsed | 60/10000 | 3 | 0.333 | 0.00/1.0 |
| lstm initialization*pinball normalized*lr tripled | rate | 60/10000 | 3 | -0.311 | -0.520/-0.0459 |
| lstm initialization*pinball normalized*lr tripled | distance | 60/10000 | 3 | -0.162 | -0.372/0.253 |
| lstm initialization*pinball normalized*lr tripled*clipping disabled | collapsed | 60/10000 | 3 | 0.667 | 0.00/2.0 |
| lstm initialization*pinball normalized*lr tripled*clipping disabled | rate | 60/10000 | 3 | 0.481 | 0.254/0.690 |
| lstm initialization*pinball normalized*lr tripled*clipping disabled | distance | 60/10000 | 3 | 0.00329 | -0.00643/0.0118 |
| lstm lr tripled | collapsed | 60/10000 | 3 | -0.0833 | -0.25/0.00 |
| lstm lr tripled | rate | 60/10000 | 3 | -0.470 | -0.639/-0.300 |
| lstm lr tripled | distance | 60/10000 | 3 | -0.137 | -0.175/-0.0921 |
| lstm lr tripled*clipping disabled | collapsed | 60/10000 | 3 | 0.167 | 0.00/0.5 |
| lstm lr tripled*clipping disabled | rate | 60/10000 | 3 | 0.0213 | -0.0584/0.139 |
| lstm lr tripled*clipping disabled | distance | 60/10000 | 3 | 0.00707 | 0.00290/0.0129 |
| lstm pinball normalized | collapsed | 60/10000 | 3 | 0.00 | 0.00/0.00 |
| lstm pinball normalized | rate | 60/10000 | 3 | -0.00962 | -0.129/0.109 |
| lstm pinball normalized | distance | 60/10000 | 3 | 0.0271 | -0.0550/0.0781 |
| lstm pinball normalized*clipping disabled | collapsed | 60/10000 | 3 | 0.00 | 0.00/0.00 |
| lstm pinball normalized*clipping disabled | rate | 60/10000 | 3 | -0.116 | -0.185/-0.0341 |
| lstm pinball normalized*clipping disabled | distance | 60/10000 | 3 | -0.000110 | -0.00390/0.00249 |
| lstm pinball normalized*lr tripled | collapsed | 60/10000 | 3 | -0.167 | -0.5/0.00 |
| lstm pinball normalized*lr tripled | rate | 60/10000 | 3 | -0.204 | -0.441/0.0417 |
| lstm pinball normalized*lr tripled | distance | 60/10000 | 3 | 0.0271 | -0.165/0.127 |
| lstm pinball normalized*lr tripled*clipping disabled | collapsed | 60/10000 | 3 | -0.333 | -1.0/0.00 |
| lstm pinball normalized*lr tripled*clipping disabled | rate | 60/10000 | 3 | -0.0119 | -0.257/0.117 |
| lstm pinball normalized*lr tripled*clipping disabled | distance | 60/10000 | 3 | -0.00149 | -0.00757/0.00889 |
| hybrid clipping disabled | collapsed | 60/10000 | 3 | -0.0417 | -0.125/0.00 |
| hybrid clipping disabled | rate | 60/10000 | 3 | -0.0485 | -0.146/0.0409 |
| hybrid clipping disabled | distance | 60/10000 | 3 | -0.0230 | -0.0563/-0.00228 |
| hybrid initialization | collapsed | 60/10000 | 3 | -0.875 | -1.0/-0.625 |
| hybrid initialization | rate | 60/10000 | 3 | -0.429 | -0.548/-0.351 |
| hybrid initialization | distance | 60/10000 | 3 | -0.114 | -0.159/-0.0652 |
| hybrid initialization*clipping disabled | collapsed | 60/10000 | 3 | 0.0833 | 0.00/0.25 |
| hybrid initialization*clipping disabled | rate | 60/10000 | 3 | 0.125 | 0.0817/0.210 |
| hybrid initialization*clipping disabled | distance | 60/10000 | 3 | 0.0441 | 0.00588/0.114 |
| hybrid initialization*lr tripled | collapsed | 60/10000 | 3 | 0.0833 | 0.00/0.25 |
| hybrid initialization*lr tripled | rate | 60/10000 | 3 | -0.0295 | -0.0833/0.0729 |
| hybrid initialization*lr tripled | distance | 60/10000 | 3 | 0.0130 | -0.0175/0.0507 |
| hybrid initialization*lr tripled*clipping disabled | collapsed | 60/10000 | 3 | -0.167 | -0.5/0.00 |
| hybrid initialization*lr tripled*clipping disabled | rate | 60/10000 | 3 | -0.0302 | -0.331/0.138 |
| hybrid initialization*lr tripled*clipping disabled | distance | 60/10000 | 3 | -0.0831 | -0.202/0.00557 |
| hybrid initialization*pinball normalized | collapsed | 60/10000 | 3 | -0.0833 | -0.25/0.00 |
| hybrid initialization*pinball normalized | rate | 60/10000 | 3 | 0.129 | -0.0529/0.278 |
| hybrid initialization*pinball normalized | distance | 60/10000 | 3 | 0.0345 | 0.0109/0.0581 |
| hybrid initialization*pinball normalized*clipping disabled | collapsed | 60/10000 | 3 | -0.5 | -1.5/0.00 |
| hybrid initialization*pinball normalized*clipping disabled | rate | 60/10000 | 3 | -0.650 | -1.51/-0.154 |
| hybrid initialization*pinball normalized*clipping disabled | distance | 60/10000 | 3 | -0.170 | -0.479/0.0184 |
| hybrid initialization*pinball normalized*lr tripled | collapsed | 60/10000 | 3 | 0.167 | 0.00/0.5 |
| hybrid initialization*pinball normalized*lr tripled | rate | 60/10000 | 3 | -0.0159 | -0.194/0.284 |
| hybrid initialization*pinball normalized*lr tripled | distance | 60/10000 | 3 | -0.0386 | -0.108/0.0940 |
| hybrid initialization*pinball normalized*lr tripled*clipping disabled | collapsed | 60/10000 | 3 | -0.333 | -1.0/0.00 |
| hybrid initialization*pinball normalized*lr tripled*clipping disabled | rate | 60/10000 | 3 | -0.483 | -0.548/-0.375 |
| hybrid initialization*pinball normalized*lr tripled*clipping disabled | distance | 60/10000 | 3 | -0.132 | -0.268/-0.0297 |
| hybrid lr tripled | collapsed | 60/10000 | 3 | -0.0417 | -0.125/0.00 |
| hybrid lr tripled | rate | 60/10000 | 3 | -0.0254 | -0.0417/-0.0101 |
| hybrid lr tripled | distance | 60/10000 | 3 | -0.0129 | -0.0263/0.00114 |
| hybrid lr tripled*clipping disabled | collapsed | 60/10000 | 3 | 0.0833 | 0.00/0.25 |
| hybrid lr tripled*clipping disabled | rate | 60/10000 | 3 | 0.0153 | -0.109/0.0863 |
| hybrid lr tripled*clipping disabled | distance | 60/10000 | 3 | 0.0279 | -0.0272/0.0981 |
| hybrid pinball normalized | collapsed | 60/10000 | 3 | 0.0417 | 0.00/0.125 |
| hybrid pinball normalized | rate | 60/10000 | 3 | -0.0457 | -0.359/0.149 |
| hybrid pinball normalized | distance | 60/10000 | 3 | -0.000639 | -0.00449/0.00292 |
| hybrid pinball normalized*clipping disabled | collapsed | 60/10000 | 3 | 0.25 | 0.00/0.75 |
| hybrid pinball normalized*clipping disabled | rate | 60/10000 | 3 | 0.210 | -0.0769/0.691 |
| hybrid pinball normalized*clipping disabled | distance | 60/10000 | 3 | 0.0773 | -0.0150/0.241 |
| hybrid pinball normalized*lr tripled | collapsed | 60/10000 | 3 | -0.0833 | -0.25/0.00 |
| hybrid pinball normalized*lr tripled | rate | 60/10000 | 3 | 0.0498 | -0.0198/0.142 |
| hybrid pinball normalized*lr tripled | distance | 60/10000 | 3 | 0.0314 | 0.0108/0.0472 |
| hybrid pinball normalized*lr tripled*clipping disabled | collapsed | 60/10000 | 3 | 0.167 | 0.00/0.5 |
| hybrid pinball normalized*lr tripled*clipping disabled | rate | 60/10000 | 3 | 0.00555 | -0.187/0.134 |
| hybrid pinball normalized*lr tripled*clipping disabled | distance | 60/10000 | 3 | 0.0451 | -0.00740/0.130 |

## Table S6a. Weighting attribution: all paired contrasts

Source: `real_weighting_attribution.csv`. Rows: 12. The full source is in `validation_data`.

| Group / comparison | Fit / test engines | Before rate | After rate | Reduction, pp [95% CI] | Resolved / introduced |
|---|---|---|---|---|---|
| FD001 lstm weighted raw minus fixed weight correction | 60/100 | 20.4% | 18.0% | 2.4 [-4.4, 9.8] | 11.0%/8.6% |
| FD001 lstm weighted raw minus unweighted retrain | 60/100 | 20.4% | 18.8% | 1.6 [-5.2, 9.0] | 12.2%/10.6% |
| FD001 lstm corrected weighted minus unweighted retrain | 60/100 | 18.0% | 18.8% | -0.8 [-3.8, 1.8] | 3.6%/4.4% |
| FD001 hybrid weighted raw minus fixed weight correction | 60/100 | 13.6% | 12.2% | 1.4 [-2.8, 6.0] | 8.6%/7.2% |
| FD001 hybrid weighted raw minus unweighted retrain | 60/100 | 13.6% | 21.6% | -8.0 [-14.2, -2.4] | 6.2%/14.2% |
| FD001 hybrid corrected weighted minus unweighted retrain | 60/100 | 12.2% | 21.6% | -9.4 [-13.4, -5.6] | 4.6%/14.0% |
| FD002 lstm weighted raw minus fixed weight correction | 156/259 | 9.6% | 3.5% | 6.1 [3.5, 8.9] | 8.6%/2.5% |
| FD002 hybrid weighted raw minus fixed weight correction | 156/259 | 8.9% | 6.6% | 2.2 [-0.2, 4.8] | 6.9%/4.6% |
| FD003 lstm weighted raw minus fixed weight correction | 60/100 | 12.8% | 7.0% | 5.8 [1.0, 10.4] | 10.2%/4.4% |
| FD003 hybrid weighted raw minus fixed weight correction | 60/100 | 11.8% | 8.6% | 3.2 [-0.2, 7.0] | 8.4%/5.2% |
| FD004 lstm weighted raw minus fixed weight correction | 149/248 | 16.6% | 5.9% | 10.7 [7.6, 14.0] | 13.6%/2.9% |
| FD004 hybrid weighted raw minus fixed weight correction | 149/248 | 12.7% | 13.2% | -0.6 [-4.2, 2.7] | 11.0%/11.6% |

## Table S6b. Complete compatibility and Brier by probability method

Source: `tableS21_cross_head.md`.

| Group/method | Test engines | Incompatible | Mean distance | Brier |
|---|---|---|---|---|
| FD001 LSTM Raw | 100 | 20.4 ± 4.6% | 0.0210 ± 0.0061 | 0.03561 ± 0.00429 |
| FD001 LSTM TrainOff | 100 | 18.0 ± 2.4% | 0.0228 ± 0.0042 | 0.05276 ± 0.00569 |
| FD001 LSTM Temp | 100 | 31.4 ± 2.3% | 0.0369 ± 0.0108 | 0.04191 ± 0.00368 |
| FD001 LSTM TrainOff+Temp | 100 | 19.2 ± 2.7% | 0.0260 ± 0.0089 | 0.05722 ± 0.00906 |
| FD001 Hybrid Raw | 100 | 13.6 ± 3.9% | 0.0138 ± 0.0075 | 0.03477 ± 0.00728 |
| FD001 Hybrid TrainOff | 100 | 12.2 ± 4.7% | 0.0156 ± 0.0065 | 0.04555 ± 0.00874 |
| FD001 Hybrid Temp | 100 | 18.6 ± 5.0% | 0.0197 ± 0.0097 | 0.03656 ± 0.00793 |
| FD001 Hybrid TrainOff+Temp | 100 | 13.2 ± 3.9% | 0.0176 ± 0.0066 | 0.05030 ± 0.01049 |
| FD002 LSTM Raw | 259 | 9.6 ± 1.4% | 0.0067 ± 0.0021 | 0.02510 ± 0.00343 |
| FD002 LSTM TrainOff | 259 | 3.5 ± 1.2% | 0.0008 ± 0.0003 | 0.01361 ± 0.00301 |
| FD002 LSTM Temp | 259 | 11.2 ± 0.9% | 0.0141 ± 0.0057 | 0.03357 ± 0.00673 |
| FD002 LSTM TrainOff+Temp | 259 | 11.4 ± 0.2% | 0.0079 ± 0.0010 | 0.01507 ± 0.00702 |
| FD002 Hybrid Raw | 259 | 8.9 ± 2.7% | 0.0072 ± 0.0040 | 0.03333 ± 0.01419 |
| FD002 Hybrid TrainOff | 259 | 6.6 ± 2.6% | 0.0060 ± 0.0036 | 0.02090 ± 0.00967 |
| FD002 Hybrid Temp | 259 | 13.4 ± 6.9% | 0.0129 ± 0.0075 | 0.03598 ± 0.01190 |
| FD002 Hybrid TrainOff+Temp | 259 | 12.8 ± 1.0% | 0.0131 ± 0.0045 | 0.02314 ± 0.00930 |
| FD003 LSTM Raw | 100 | 12.8 ± 4.1% | 0.0150 ± 0.0081 | 0.02666 ± 0.00860 |
| FD003 LSTM TrainOff | 100 | 7.0 ± 2.7% | 0.0024 ± 0.0016 | 0.02669 ± 0.00261 |
| FD003 LSTM Temp | 100 | 25.0 ± 5.8% | 0.0263 ± 0.0106 | 0.03403 ± 0.00747 |
| FD003 LSTM TrainOff+Temp | 100 | 11.0 ± 3.8% | 0.0053 ± 0.0033 | 0.02708 ± 0.00329 |
| FD003 Hybrid Raw | 100 | 11.8 ± 3.3% | 0.0149 ± 0.0113 | 0.02915 ± 0.01492 |
| FD003 Hybrid TrainOff | 100 | 8.6 ± 4.3% | 0.0081 ± 0.0025 | 0.02207 ± 0.00476 |
| FD003 Hybrid Temp | 100 | 36.2 ± 12.4% | 0.0398 ± 0.0160 | 0.03750 ± 0.01141 |
| FD003 Hybrid TrainOff+Temp | 100 | 23.8 ± 10.2% | 0.0248 ± 0.0095 | 0.03268 ± 0.01069 |
| FD004 LSTM Raw | 248 | 16.6 ± 2.1% | 0.0137 ± 0.0029 | 0.05290 ± 0.00297 |
| FD004 LSTM TrainOff | 248 | 5.9 ± 1.7% | 0.0013 ± 0.0005 | 0.03499 ± 0.00236 |
| FD004 LSTM Temp | 248 | 16.7 ± 2.8% | 0.0186 ± 0.0067 | 0.05904 ± 0.00580 |
| FD004 LSTM TrainOff+Temp | 248 | 19.6 ± 2.3% | 0.0124 ± 0.0028 | 0.04141 ± 0.00720 |
| FD004 Hybrid Raw | 248 | 12.7 ± 2.5% | 0.0086 ± 0.0031 | 0.04484 ± 0.00384 |
| FD004 Hybrid TrainOff | 248 | 13.2 ± 3.6% | 0.0102 ± 0.0053 | 0.03787 ± 0.00415 |
| FD004 Hybrid Temp | 248 | 15.3 ± 6.6% | 0.0126 ± 0.0072 | 0.05017 ± 0.00972 |
| FD004 Hybrid TrainOff+Temp | 248 | 19.8 ± 3.4% | 0.0225 ± 0.0069 | 0.04513 ± 0.00622 |

## Table S7a. All real associations, including incremental probability adjustment

Source: `real_associations.csv`. Rows: 152. The full source is in `validation_data`.

| Group / metric | Fit / test engines | Incomp / comp engines | Effect [95% CI] | Undefined draws |
|---|---|---|---|---|
| FD001 lstm median squared error mean incompatible | 60/100 | 35/93 | 175 [47.9, 407] | 0 |
| FD001 lstm median squared error mean compatible | 60/100 | 35/93 | 228 [170, 294] | 0 |
| FD001 lstm median squared error unadjusted difference | 60/100 | 35/93 | -53.0 [-200, 179] | 0 |
| FD001 lstm Brier mean incompatible | 60/100 | 35/93 | 0.10110 [0.05167, 0.15650] | 0 |
| FD001 lstm Brier mean compatible | 60/100 | 35/93 | 0.01882 [0.00422, 0.04074] | 0 |
| FD001 lstm Brier unadjusted difference | 60/100 | 35/93 | 0.0823 [0.0380, 0.133] | 0 |
| FD001 lstm median squared error adjusted flag | 60/100 | 35/93 | 69.7 [-167, 405] | 0 |
| FD001 lstm Brier adjusted flag | 60/100 | 35/93 | 0.0426 [-0.0369, 0.124] | 0 |
| FD001 lstm median squared error adjusted distance per 0.1 | 60/100 | 35/93 | 79.3 [-112, 326] | 0 |
| FD001 lstm Brier adjusted distance per 0.1 | 60/100 | 35/93 | 0.0433 [-0.0228, 0.101] | 0 |
| FD001 lstm median squared error RUL bin standardized difference | 60/100 | 35/93 | 712 [657, 768] | 1219 |
| FD001 lstm Brier RUL bin standardized difference | 60/100 | 35/93 | 0.175 [0.133, 0.207] | 1219 |
| FD001 lstm near threshold rate 20 to 40 | 60/100 | 35/93 | 50.7% [33.3%, 68.0%] | 0 |
| FD001 lstm near threshold distance 20 to 40 | 60/100 | 35/93 | 0.0731 [0.0417, 0.104] | 0 |
| FD001 lstm near threshold rate elsewhere | 60/100 | 35/93 | 15.1% [9.3%, 21.5%] | 0 |
| FD001 lstm near threshold distance elsewhere | 60/100 | 35/93 | 0.0118 [0.00556, 0.0193] | 0 |
| FD001 lstm near threshold rate difference | 60/100 | 35/93 | 35.6 [18.0, 54.0] | 0 |
| FD001 lstm Brier distance beyond raw p per 0.1 | 60/100 | 35/93 | -0.000773 [-0.0394, 0.0398] | 0 |
| FD001 lstm Brier incremental in sample R squared | 60/100 | 35/93 | 0.00000656 [0.00000612, 0.0449] | 0 |
| FD001 hybrid median squared error mean incompatible | 60/100 | 25/98 | 104 [40.9, 193] | 0 |
| FD001 hybrid median squared error mean compatible | 60/100 | 25/98 | 283 [210, 367] | 0 |
| FD001 hybrid median squared error unadjusted difference | 60/100 | 25/98 | -179 [-267, -96.0] | 0 |
| FD001 hybrid Brier mean incompatible | 60/100 | 25/98 | 0.09590 [0.04213, 0.17398] | 0 |
| FD001 hybrid Brier mean compatible | 60/100 | 25/98 | 0.02515 [0.00758, 0.04921] | 0 |
| FD001 hybrid Brier unadjusted difference | 60/100 | 25/98 | 0.0708 [0.0266, 0.141] | 0 |
| FD001 hybrid median squared error adjusted flag | 60/100 | 25/98 | -250 [-415, -95.3] | 0 |
| FD001 hybrid Brier adjusted flag | 60/100 | 25/98 | -0.0143 [-0.0887, 0.0550] | 0 |
| FD001 hybrid median squared error adjusted distance per 0.1 | 60/100 | 25/98 | -99.2 [-182, -33.0] | 0 |
| FD001 hybrid Brier adjusted distance per 0.1 | 60/100 | 25/98 | 0.0203 [-0.0276, 0.0710] | 0 |
| FD001 hybrid median squared error RUL bin standardized difference | 60/100 | 25/98 | 416 [310, 484] | 1266 |
| FD001 hybrid Brier RUL bin standardized difference | 60/100 | 25/98 | 0.117 [0.0703, 0.151] | 1266 |
| FD001 hybrid near threshold rate 20 to 40 | 60/100 | 25/98 | 53.3% [36.7%, 68.6%] | 0 |
| FD001 hybrid near threshold distance 20 to 40 | 60/100 | 25/98 | 0.0563 [0.0333, 0.0832] | 0 |
| FD001 hybrid near threshold rate elsewhere | 60/100 | 25/98 | 6.6% [3.0%, 10.9%] | 0 |
| FD001 hybrid near threshold distance elsewhere | 60/100 | 25/98 | 0.00629 [0.00222, 0.0114] | 0 |
| FD001 hybrid near threshold rate difference | 60/100 | 25/98 | 46.7 [29.7, 62.9] | 0 |
| FD001 hybrid Brier distance beyond raw p per 0.1 | 60/100 | 25/98 | -0.0215 [-0.0772, 0.0331] | 0 |
| FD001 hybrid Brier incremental in sample R squared | 60/100 | 25/98 | 0.00514 [0.0000230, 0.0498] | 0 |
| FD002 lstm median squared error mean incompatible | 156/259 | 46/255 | 51.7 [34.5, 71.4] | 0 |
| FD002 lstm median squared error mean compatible | 156/259 | 46/255 | 222 [171, 280] | 0 |
| FD002 lstm median squared error unadjusted difference | 156/259 | 46/255 | -170 [-232, -118] | 0 |
| FD002 lstm Brier mean incompatible | 156/259 | 46/255 | 0.15612 [0.07903, 0.23981] | 0 |
| FD002 lstm Brier mean compatible | 156/259 | 46/255 | 0.01122 [0.00468, 0.02001] | 0 |
| FD002 lstm Brier unadjusted difference | 156/259 | 46/255 | 0.145 [0.0724, 0.226] | 0 |
| FD002 lstm median squared error adjusted flag | 156/259 | 46/255 | -138 [-240, -51.0] | 0 |
| FD002 lstm Brier adjusted flag | 156/259 | 46/255 | 0.0908 [0.0332, 0.155] | 0 |
| FD002 lstm median squared error adjusted distance per 0.1 | 156/259 | 46/255 | -83.3 [-162, -31.7] | 0 |
| FD002 lstm Brier adjusted distance per 0.1 | 156/259 | 46/255 | 0.123 [0.0631, 0.182] | 0 |
| FD002 lstm median squared error RUL bin standardized difference | 156/259 | 46/255 | -14.0 [-87.5, 48.4] | 735 |
| FD002 lstm Brier RUL bin standardized difference | 156/259 | 46/255 | 0.0393 [0.00617, 0.0740] | 735 |
| FD002 lstm near threshold rate 20 to 40 | 156/259 | 46/255 | 54.5% [38.9%, 69.6%] | 0 |
| FD002 lstm near threshold distance 20 to 40 | 156/259 | 46/255 | 0.0514 [0.0320, 0.0729] | 0 |
| FD002 lstm near threshold rate elsewhere | 156/259 | 46/255 | 5.4% [3.4%, 7.7%] | 0 |
| FD002 lstm near threshold distance elsewhere | 156/259 | 46/255 | 0.00256 [0.00138, 0.00402] | 0 |
| FD002 lstm near threshold rate difference | 156/259 | 46/255 | 49.1 [33.3, 64.2] | 0 |
| FD002 lstm Brier distance beyond raw p per 0.1 | 156/259 | 46/255 | 0.0199 [-0.0233, 0.0724] | 0 |
| FD002 lstm Brier incremental in sample R squared | 156/259 | 46/255 | 0.00190 [0.00000397, 0.0257] | 0 |
| FD002 hybrid median squared error mean incompatible | 156/259 | 49/256 | 118 [67.4, 189] | 0 |
| FD002 hybrid median squared error mean compatible | 156/259 | 49/256 | 252 [198, 312] | 0 |
| FD002 hybrid median squared error unadjusted difference | 156/259 | 49/256 | -134 [-208, -62.2] | 0 |
| FD002 hybrid Brier mean incompatible | 156/259 | 49/256 | 0.19796 [0.12007, 0.26964] | 0 |
| FD002 hybrid Brier mean compatible | 156/259 | 49/256 | 0.01729 [0.00845, 0.02851] | 0 |
| FD002 hybrid Brier unadjusted difference | 156/259 | 49/256 | 0.181 [0.106, 0.252] | 0 |
| FD002 hybrid median squared error adjusted flag | 156/259 | 49/256 | -149 [-311, -4.99] | 0 |
| FD002 hybrid Brier adjusted flag | 156/259 | 49/256 | 0.103 [0.0365, 0.171] | 0 |
| FD002 hybrid median squared error adjusted distance per 0.1 | 156/259 | 49/256 | -97.0 [-173, -43.6] | 0 |
| FD002 hybrid Brier adjusted distance per 0.1 | 156/259 | 49/256 | 0.137 [0.0907, 0.171] | 0 |
| FD002 hybrid median squared error RUL bin standardized difference | 156/259 | 49/256 | 947 [881, 994] | 1221 |
| FD002 hybrid Brier RUL bin standardized difference | 156/259 | 49/256 | 0.0296 [0.0114, 0.0487] | 1221 |
| FD002 hybrid near threshold rate 20 to 40 | 156/259 | 49/256 | 41.8% [30.0%, 53.0%] | 0 |
| FD002 hybrid near threshold distance 20 to 40 | 156/259 | 49/256 | 0.0432 [0.0225, 0.0645] | 0 |
| FD002 hybrid near threshold rate elsewhere | 156/259 | 49/256 | 5.8% [3.7%, 8.1%] | 0 |
| FD002 hybrid near threshold distance elsewhere | 156/259 | 49/256 | 0.00386 [0.00173, 0.00652] | 0 |
| FD002 hybrid near threshold rate difference | 156/259 | 49/256 | 36.0 [23.7, 47.6] | 0 |
| FD002 hybrid Brier distance beyond raw p per 0.1 | 156/259 | 49/256 | 0.0596 [0.0104, 0.106] | 0 |
| FD002 hybrid Brier incremental in sample R squared | 156/259 | 49/256 | 0.0202 [0.000443, 0.0936] | 0 |
| FD003 lstm median squared error mean incompatible | 60/100 | 26/97 | 88.9 [49.4, 143] | 0 |
| FD003 lstm median squared error mean compatible | 60/100 | 26/97 | 358 [231, 500] | 0 |
| FD003 lstm median squared error unadjusted difference | 60/100 | 26/97 | -269 [-411, -137] | 0 |
| FD003 lstm Brier mean incompatible | 60/100 | 26/97 | 0.13123 [0.03956, 0.25404] | 0 |
| FD003 lstm Brier mean compatible | 60/100 | 26/97 | 0.01131 [0.00355, 0.02339] | 0 |
| FD003 lstm Brier unadjusted difference | 60/100 | 26/97 | 0.120 [0.0340, 0.237] | 0 |
| FD003 lstm median squared error adjusted flag | 60/100 | 26/97 | -320 [-595, -71.0] | 0 |
| FD003 lstm Brier adjusted flag | 60/100 | 26/97 | 0.0822 [0.0155, 0.179] | 0 |
| FD003 lstm median squared error adjusted distance per 0.1 | 60/100 | 26/97 | -110 [-226, -22.3] | 0 |
| FD003 lstm Brier adjusted distance per 0.1 | 60/100 | 26/97 | 0.0471 [0.00669, 0.111] | 0 |
| FD003 lstm median squared error RUL bin standardized difference | 60/100 | 26/97 | -92.4 [-261, 56.8] | 934 |
| FD003 lstm Brier RUL bin standardized difference | 60/100 | 26/97 | 0.0427 [-0.000513, 0.106] | 934 |
| FD003 lstm near threshold rate 20 to 40 | 60/100 | 26/97 | 62.0% [48.9%, 76.7%] | 0 |
| FD003 lstm near threshold distance 20 to 40 | 60/100 | 26/97 | 0.0871 [0.0450, 0.139] | 0 |
| FD003 lstm near threshold rate elsewhere | 60/100 | 26/97 | 7.3% [3.7%, 11.4%] | 0 |
| FD003 lstm near threshold distance elsewhere | 60/100 | 26/97 | 0.00696 [0.00262, 0.0127] | 0 |
| FD003 lstm near threshold rate difference | 60/100 | 26/97 | 54.7 [41.0, 69.2] | 0 |
| FD003 lstm Brier distance beyond raw p per 0.1 | 60/100 | 26/97 | -0.00252 [-0.0408, 0.0500] | 0 |
| FD003 lstm Brier incremental in sample R squared | 60/100 | 26/97 | 0.000105 [0.0000151, 0.0570] | 0 |
| FD003 hybrid median squared error mean incompatible | 60/100 | 28/99 | 111 [50.8, 197] | 0 |
| FD003 hybrid median squared error mean compatible | 60/100 | 28/99 | 251 [183, 329] | 0 |
| FD003 hybrid median squared error unadjusted difference | 60/100 | 28/99 | -139 [-238, -35.8] | 0 |
| FD003 hybrid Brier mean incompatible | 60/100 | 28/99 | 0.17405 [0.07676, 0.27455] | 0 |
| FD003 hybrid Brier mean compatible | 60/100 | 28/99 | 0.00976 [0.00398, 0.01753] | 0 |
| FD003 hybrid Brier unadjusted difference | 60/100 | 28/99 | 0.164 [0.0708, 0.262] | 0 |
| FD003 hybrid median squared error adjusted flag | 60/100 | 28/99 | -99.9 [-230, 29.0] | 0 |
| FD003 hybrid Brier adjusted flag | 60/100 | 28/99 | 0.129 [0.0524, 0.209] | 0 |
| FD003 hybrid median squared error adjusted distance per 0.1 | 60/100 | 28/99 | -17.0 [-71.4, 37.2] | 0 |
| FD003 hybrid Brier adjusted distance per 0.1 | 60/100 | 28/99 | 0.0743 [0.0366, 0.119] | 0 |
| FD003 hybrid median squared error RUL bin standardized difference | 60/100 | 28/99 | -5.95 [-90.0, 71.9] | 342 |
| FD003 hybrid Brier RUL bin standardized difference | 60/100 | 28/99 | 0.0904 [0.0355, 0.132] | 342 |
| FD003 hybrid near threshold rate 20 to 40 | 60/100 | 28/99 | 52.0% [35.6%, 70.0%] | 0 |
| FD003 hybrid near threshold distance 20 to 40 | 60/100 | 28/99 | 0.0782 [0.0402, 0.114] | 0 |
| FD003 hybrid near threshold rate elsewhere | 60/100 | 28/99 | 7.3% [4.2%, 11.1%] | 0 |
| FD003 hybrid near threshold distance elsewhere | 60/100 | 28/99 | 0.00791 [0.00336, 0.0133] | 0 |
| FD003 hybrid near threshold rate difference | 60/100 | 28/99 | 44.7 [28.2, 62.4] | 0 |
| FD003 hybrid Brier distance beyond raw p per 0.1 | 60/100 | 28/99 | 0.0150 [-0.0179, 0.0504] | 0 |
| FD003 hybrid Brier incremental in sample R squared | 60/100 | 28/99 | 0.00385 [0.00000821, 0.0456] | 0 |
| FD004 lstm median squared error mean incompatible | 149/248 | 69/236 | 176 [82.9, 330] | 0 |
| FD004 lstm median squared error mean compatible | 149/248 | 69/236 | 295 [229, 366] | 0 |
| FD004 lstm median squared error unadjusted difference | 149/248 | 69/236 | -119 [-234, 29.2] | 0 |
| FD004 lstm Brier mean incompatible | 149/248 | 69/236 | 0.21846 [0.13797, 0.30776] | 0 |
| FD004 lstm Brier mean compatible | 149/248 | 69/236 | 0.01992 [0.01072, 0.03108] | 0 |
| FD004 lstm Brier unadjusted difference | 149/248 | 69/236 | 0.199 [0.121, 0.288] | 0 |
| FD004 lstm median squared error adjusted flag | 149/248 | 69/236 | -36.3 [-276, 258] | 0 |
| FD004 lstm Brier adjusted flag | 149/248 | 69/236 | 0.124 [0.0554, 0.202] | 0 |
| FD004 lstm median squared error adjusted distance per 0.1 | 149/248 | 69/236 | 37.0 [-166, 301] | 0 |
| FD004 lstm Brier adjusted distance per 0.1 | 149/248 | 69/236 | 0.107 [0.0572, 0.154] | 0 |
| FD004 lstm median squared error RUL bin standardized difference | 149/248 | 69/236 | 545 [60.3, 853] | 121 |
| FD004 lstm Brier RUL bin standardized difference | 149/248 | 69/236 | 0.143 [0.0379, 0.208] | 121 |
| FD004 lstm near threshold rate 20 to 40 | 149/248 | 69/236 | 62.8% [51.1%, 74.5%] | 0 |
| FD004 lstm near threshold distance 20 to 40 | 149/248 | 69/236 | 0.0698 [0.0488, 0.0925] | 0 |
| FD004 lstm near threshold rate elsewhere | 149/248 | 69/236 | 10.5% [7.4%, 13.9%] | 0 |
| FD004 lstm near threshold distance elsewhere | 149/248 | 69/236 | 0.00630 [0.00409, 0.00902] | 0 |
| FD004 lstm near threshold rate difference | 149/248 | 69/236 | 52.3 [40.3, 64.4] | 0 |
| FD004 lstm Brier distance beyond raw p per 0.1 | 149/248 | 69/236 | 0.0385 [-0.00714, 0.0892] | 0 |
| FD004 lstm Brier incremental in sample R squared | 149/248 | 69/236 | 0.00684 [0.0000225, 0.0351] | 0 |
| FD004 hybrid median squared error mean incompatible | 149/248 | 72/245 | 215 [75.9, 475] | 0 |
| FD004 hybrid median squared error mean compatible | 149/248 | 72/245 | 282 [224, 346] | 0 |
| FD004 hybrid median squared error unadjusted difference | 149/248 | 72/245 | -67.2 [-230, 191] | 0 |
| FD004 hybrid Brier mean incompatible | 149/248 | 72/245 | 0.17295 [0.09377, 0.26135] | 0 |
| FD004 hybrid Brier mean compatible | 149/248 | 72/245 | 0.02627 [0.01450, 0.03968] | 0 |
| FD004 hybrid Brier unadjusted difference | 149/248 | 72/245 | 0.147 [0.0696, 0.233] | 0 |
| FD004 hybrid median squared error adjusted flag | 149/248 | 72/245 | 90.2 [-147, 429] | 0 |
| FD004 hybrid Brier adjusted flag | 149/248 | 72/245 | 0.103 [0.0247, 0.187] | 0 |
| FD004 hybrid median squared error adjusted distance per 0.1 | 149/248 | 72/245 | 234 [-140, 670] | 0 |
| FD004 hybrid Brier adjusted distance per 0.1 | 149/248 | 72/245 | 0.128 [0.0264, 0.186] | 0 |
| FD004 hybrid median squared error RUL bin standardized difference | 149/248 | 72/245 | 622 [105, 882] | 756 |
| FD004 hybrid Brier RUL bin standardized difference | 149/248 | 72/245 | 0.160 [0.0200, 0.229] | 756 |
| FD004 hybrid near threshold rate 20 to 40 | 149/248 | 72/245 | 31.7% [20.8%, 43.4%] | 0 |
| FD004 hybrid near threshold distance 20 to 40 | 149/248 | 72/245 | 0.0233 [0.0106, 0.0430] | 0 |
| FD004 hybrid near threshold rate elsewhere | 149/248 | 72/245 | 10.1% [7.5%, 13.2%] | 0 |
| FD004 hybrid near threshold distance elsewhere | 149/248 | 72/245 | 0.00662 [0.00323, 0.0112] | 0 |
| FD004 hybrid near threshold rate difference | 149/248 | 72/245 | 21.6 [10.4, 33.4] | 0 |
| FD004 hybrid Brier distance beyond raw p per 0.1 | 149/248 | 72/245 | 0.0399 [-0.0328, 0.121] | 0 |
| FD004 hybrid Brier incremental in sample R squared | 149/248 | 72/245 | 0.00742 [0.0000179, 0.0706] | 0 |

## Table S7b. All pre-specified real RUL-bin contrasts

Source: `real_RUL_bins.csv`. Rows: 48. The full source is in `validation_data`.

| Group / RUL bin | Fit / test / bin engines | Incomp / comp engines | Median error difference [95% CI] | Brier difference [95% CI] |
|---|---|---|---|---|
| FD001 lstm [0,20) | 60/100/13 | 12/11 | 49.7 [-9.68, 150] | 0.0187 [0.00150, 0.0507] |
| FD001 lstm [20,40] | 60/100/15 | 13/12 | 35.3 [-47.9, 115] | -0.0313 [-0.195, 0.0754] |
| FD001 lstm (40,60] | 60/100/11 | 8/9 | -191 [-305, -87.7] | 0.0563 [-0.0290, 0.158] |
| FD001 lstm (60,80] | 60/100/6 | 1/6 | -358 [-732, 194] | 0.0494 [0.0493, 0.0494] |
| FD001 lstm (80,100] | 60/100/22 | 1/22 | 2.31e+3 [2.22e+3, 2.36e+3] | 0.503 [0.498, 0.503] |
| FD001 lstm (100,125] | 60/100/33 | 0/33 | NA [NA, NA] | NA [NA, NA] |
| FD001 hybrid [0,20) | 60/100/13 | 3/12 | 48.8 [-15.7, 75.2] | 0.0273 [-0.00449, 0.0400] |
| FD001 hybrid [20,40] | 60/100/15 | 13/14 | -63.8 [-199, 32.0] | -0.155 [-0.346, -0.0148] |
| FD001 hybrid (40,60] | 60/100/11 | 7/11 | -393 [-640, -96.6] | 0.0714 [0.0114, 0.152] |
| FD001 hybrid (60,80] | 60/100/6 | 1/6 | -637 [-1.12e+3, 59.4] | 0.0422 [0.0308, 0.0432] |
| FD001 hybrid (80,100] | 60/100/22 | 1/22 | 1.65e+3 [1.43e+3, 1.71e+3] | 0.400 [0.381, 0.401] |
| FD001 hybrid (100,125] | 60/100/33 | 0/33 | NA [NA, NA] | NA [NA, NA] |
| FD002 lstm [0,20) | 156/259/53 | 12/53 | 31.0 [15.9, 46.3] | 0.00363 [0.000236, 0.0114] |
| FD002 lstm [20,40] | 156/259/22 | 18/18 | -110 [-298, 11.7] | 0.0871 [-0.0606, 0.229] |
| FD002 lstm (40,60] | 156/259/27 | 15/27 | -159 [-351, -9.76] | 0.101 [-0.00281, 0.231] |
| FD002 lstm (60,80] | 156/259/28 | 1/28 | 115 [-138, 330] | 0.00978 [0.00964, 0.00986] |
| FD002 lstm (80,100] | 156/259/37 | 0/37 | NA [NA, NA] | NA [NA, NA] |
| FD002 lstm (100,125] | 156/259/92 | 0/92 | NA [NA, NA] | NA [NA, NA] |
| FD002 hybrid [0,20) | 156/259/53 | 9/53 | 7.41 [-5.50, 21.7] | 0.000790 [-0.000792, 0.00296] |
| FD002 hybrid [20,40] | 156/259/22 | 18/21 | -85.4 [-242, 11.1] | 0.0610 [-0.0929, 0.213] |
| FD002 hybrid (40,60] | 156/259/27 | 16/25 | -239 [-514, -25.1] | 0.165 [0.0460, 0.301] |
| FD002 hybrid (60,80] | 156/259/28 | 4/28 | -72.9 [-464, 243] | 0.00862 [0.000578, 0.0425] |
| FD002 hybrid (80,100] | 156/259/37 | 1/37 | 764 [666, 858] | 0.0378 [0.0378, 0.0378] |
| FD002 hybrid (100,125] | 156/259/92 | 1/92 | 2.47e+3 [2.35e+3, 2.53e+3] | 0.00220 [0.000984, 0.00249] |
| FD003 lstm [0,20) | 60/100/13 | 5/11 | 56.4 [0.309, 145] | 0.0139 [-0.00381, 0.0967] |
| FD003 lstm [20,40] | 60/100/10 | 10/9 | -0.354 [-26.3, 23.4] | 0.0131 [-0.132, 0.158] |
| FD003 lstm (40,60] | 60/100/18 | 8/18 | -673 [-1.17e+3, -213] | 0.131 [0.00757, 0.346] |
| FD003 lstm (60,80] | 60/100/12 | 2/12 | 76.5 [-486, 437] | 0.0162 [0.0137, 0.0174] |
| FD003 lstm (80,100] | 60/100/15 | 1/15 | 279 [101, 416] | 0.00262 [0.00260, 0.00263] |
| FD003 lstm (100,125] | 60/100/32 | 0/32 | NA [NA, NA] | NA [NA, NA] |
| FD003 hybrid [0,20) | 60/100/13 | 2/13 | 46.3 [21.4, 90.1] | 0.000139 [-0.00104, 0.000557] |
| FD003 hybrid [20,40] | 60/100/10 | 10/9 | 11.5 [-2.25, 26.3] | 0.133 [-0.0306, 0.248] |
| FD003 hybrid (40,60] | 60/100/18 | 13/18 | -232 [-405, -68.5] | 0.101 [0.0218, 0.172] |
| FD003 hybrid (60,80] | 60/100/12 | 3/12 | 262 [-10.3, 482] | 0.137 [0.0110, 0.243] |
| FD003 hybrid (80,100] | 60/100/15 | 0/15 | NA [NA, NA] | NA [NA, NA] |
| FD003 hybrid (100,125] | 60/100/32 | 0/32 | NA [NA, NA] | NA [NA, NA] |
| FD004 lstm [0,20) | 149/248/40 | 20/35 | 15.7 [3.15, 32.4] | 0.000152 [-0.0000508, 0.000352] |
| FD004 lstm [20,40] | 149/248/29 | 26/22 | 38.0 [-31.6, 109] | 0.230 [0.0784, 0.380] |
| FD004 lstm (40,60] | 149/248/22 | 16/22 | -483 [-907, -90.0] | 0.0863 [-0.00970, 0.194] |
| FD004 lstm (60,80] | 149/248/22 | 4/22 | -153 [-466, 150] | 0.0161 [0.00869, 0.0241] |
| FD004 lstm (80,100] | 149/248/35 | 3/35 | 2.65e+3 [763, 3.90e+3] | 0.352 [0.00292, 0.587] |
| FD004 lstm (100,125] | 149/248/100 | 0/100 | NA [NA, NA] | NA [NA, NA] |
| FD004 hybrid [0,20) | 149/248/40 | 31/39 | 4.27 [-11.0, 17.8] | -0.000760 [-0.00202, 0.000178] |
| FD004 hybrid [20,40] | 149/248/29 | 20/28 | 86.0 [9.77, 202] | 0.149 [-0.0322, 0.329] |
| FD004 hybrid (40,60] | 149/248/22 | 17/21 | -487 [-941, -88.3] | 0.150 [0.00367, 0.321] |
| FD004 hybrid (60,80] | 149/248/22 | 1/22 | -178 [-386, 27.7] | 0.00610 [0.00593, 0.00619] |
| FD004 hybrid (80,100] | 149/248/35 | 3/35 | 2.97e+3 [928, 3.98e+3] | 0.457 [0.00337, 0.684] |
| FD004 hybrid (100,125] | 149/248/100 | 0/100 | NA [NA, NA] | NA [NA, NA] |

## Table S8. All primary family-level oracle association coefficients

Source: `synthetic_family_confirmation.csv`. Rows: 8. The full source is in `validation_data`.

| Family / outcome / predictor | Fit engines | Test engines / subset | Coefficient [95% CI] | Pass |
|---|---|---|---|---|
| temporal oracle probability squared deviation flag | 60/156/60/149 | 10000 | 0.00501 [0.00492, 0.00511] | True |
| temporal oracle probability squared deviation distance per 0.1 | 60/156/60/149 | 10000 | 0.00141 [0.00138, 0.00145] | True |
| temporal oracle quantile MAE flag | 60/156/60/149 | 10000 | 1.21 [1.19, 1.24] | True |
| temporal oracle quantile MAE distance per 0.1 | 60/156/60/149 | 10000 | 0.428 [0.420, 0.437] | True |
| covariate oracle probability squared deviation flag | 60/156/60/149 | 10000 | -0.00124 [-0.00151, -0.000952] | False |
| covariate oracle probability squared deviation distance per 0.1 | 60/156/60/149 | 10000 | 0.000923 [0.000811, 0.00104] | True |
| covariate oracle quantile MAE flag | 60/156/60/149 | 10000 | -1.89 [-1.91, -1.86] | False |
| covariate oracle quantile MAE distance per 0.1 | 60/156/60/149 | 10000 | -0.655 [-0.670, -0.640] | False |

All setting-specific oracle coefficients, group means and sensitivity results are retained in the full-precision companion `synthetic_associations.csv`. Table S8 contains every primary confirmation component.

## Table S9a. Real Brier flag association after probability, band and RUL adjustment

Source: `real_Brier_adjusted.csv`. Rows: 8. The full source is in `validation_data`.

| Group | Fit / test engines | Band / elsewhere engines | Incomp / comp engines | Coefficient [95% CI] | Pass |
|---|---|---|---|---|---|
| FD001 lstm | 60/100 | 15/85 | 35/93 | 0.0242 [-0.0271, 0.0765] | False |
| FD001 hybrid | 60/100 | 15/85 | 25/98 | -0.110 [-0.206, -0.0112] | False |
| FD002 lstm | 156/259 | 22/237 | 46/255 | -0.00565 [-0.0482, 0.0400] | False |
| FD002 hybrid | 156/259 | 22/237 | 49/256 | 0.0128 [-0.0417, 0.0661] | False |
| FD003 lstm | 60/100 | 10/90 | 26/97 | -0.0105 [-0.0733, 0.0527] | False |
| FD003 hybrid | 60/100 | 10/90 | 28/99 | 0.0481 [0.00764, 0.0878] | True |
| FD004 lstm | 149/248 | 29/219 | 69/236 | 0.0145 [-0.0519, 0.0796] | False |
| FD004 hybrid | 149/248 | 29/219 | 72/245 | 0.0541 [-0.0116, 0.120] | False |

## Table S9b. Real near-threshold and elsewhere rates

Source: `near_threshold_table.csv`. Rows: 8. The full source is in `validation_data`.

| Group | Fit / test engines | Band / elsewhere engines | Band rate [95% CI] | Elsewhere rate [95% CI] |
|---|---|---|---|---|
| FD001 lstm | 60/100 | 15/85 | 50.7% [33.3%, 68.0%] | 15.1% [9.3%, 21.5%] |
| FD001 hybrid | 60/100 | 15/85 | 53.3% [36.7%, 68.6%] | 6.6% [3.0%, 10.9%] |
| FD002 lstm | 156/259 | 22/237 | 54.5% [38.9%, 69.6%] | 5.4% [3.4%, 7.7%] |
| FD002 hybrid | 156/259 | 22/237 | 41.8% [30.0%, 53.0%] | 5.8% [3.7%, 8.1%] |
| FD003 lstm | 60/100 | 10/90 | 62.0% [48.9%, 76.7%] | 7.3% [3.7%, 11.4%] |
| FD003 hybrid | 60/100 | 10/90 | 52.0% [35.6%, 70.0%] | 7.3% [4.2%, 11.1%] |
| FD004 lstm | 149/248 | 29/219 | 62.8% [51.1%, 74.5%] | 10.5% [7.4%, 13.9%] |
| FD004 hybrid | 149/248 | 29/219 | 31.7% [20.8%, 43.4%] | 10.1% [7.5%, 13.2%] |

## Table S10. All synthetic near-threshold rates, both endpoint policies and fleet sizes

Source: `synthetic_band_rates_wide.csv`. Rows: 144. The full source is in `validation_data`.

| Group / variant / policy | Fit / test engines | Band / elsewhere engines | Fits | Band rate [95% CI] | Elsewhere rate [95% CI] | Difference, pp [95% CI] |
|---|---|---|---|---|---|---|
| FD001 lstm weighted raw final | 60/100 | 24/76 | 30 | 68.5% [67.8%, 69.1%] | 67.5% [67.1%, 67.8%] | 1.0 [0.2, 1.8] |
| FD001 lstm weighted raw final | 60/10000 | 2062/7938 | 30 | 67.8% [67.7%, 67.8%] | 67.5% [67.4%, 67.5%] | 0.3 [0.2, 0.4] |
| FD001 lstm weighted corrected final | 60/100 | 24/76 | 30 | 54.9% [53.6%, 56.2%] | 53.6% [53.0%, 54.1%] | 1.3 [-0.1, 2.7] |
| FD001 lstm weighted corrected final | 60/10000 | 2062/7938 | 30 | 53.6% [53.5%, 53.8%] | 53.5% [53.4%, 53.6%] | 0.1 [-0.0, 0.3] |
| FD001 lstm unweighted final | 60/100 | 24/76 | 30 | 55.1% [53.8%, 56.5%] | 53.7% [53.2%, 54.3%] | 1.4 [-0.0, 3.0] |
| FD001 lstm unweighted final | 60/10000 | 2062/7938 | 30 | 54.0% [53.9%, 54.1%] | 53.8% [53.7%, 53.8%] | 0.2 [0.1, 0.4] |
| FD001 lstm weighted raw uniform | 60/100 | 22/78 | 30 | 67.7% [67.1%, 68.4%] | 68.1% [67.6%, 68.6%] | -0.4 [-1.2, 0.4] |
| FD001 lstm weighted raw uniform | 60/10000 | 1734/8266 | 30 | 68.3% [68.2%, 68.4%] | 68.4% [68.3%, 68.4%] | -0.0 [-0.2, 0.1] |
| FD001 lstm weighted corrected uniform | 60/100 | 22/78 | 30 | 56.5% [55.1%, 58.1%] | 56.5% [55.7%, 57.3%] | 0.0 [-1.7, 1.8] |
| FD001 lstm weighted corrected uniform | 60/10000 | 1734/8266 | 30 | 56.4% [56.2%, 56.5%] | 56.6% [56.5%, 56.7%] | -0.2 [-0.4, -0.1] |
| FD001 lstm unweighted uniform | 60/100 | 22/78 | 30 | 56.2% [54.9%, 57.7%] | 56.4% [55.6%, 57.1%] | -0.2 [-1.7, 1.4] |
| FD001 lstm unweighted uniform | 60/10000 | 1734/8266 | 30 | 56.4% [56.3%, 56.6%] | 56.5% [56.5%, 56.6%] | -0.1 [-0.3, 0.1] |
| FD001 hybrid weighted raw final | 60/100 | 24/76 | 30 | 58.5% [53.3%, 64.3%] | 66.0% [62.3%, 69.6%] | -7.5 [-14.0, -0.8] |
| FD001 hybrid weighted raw final | 60/10000 | 2062/7938 | 30 | 62.2% [61.5%, 62.9%] | 66.6% [66.2%, 66.9%] | -4.3 [-5.1, -3.5] |
| FD001 hybrid weighted corrected final | 60/100 | 24/76 | 30 | 93.9% [91.3%, 96.3%] | 89.8% [88.4%, 91.4%] | 4.1 [1.1, 6.9] |
| FD001 hybrid weighted corrected final | 60/10000 | 2062/7938 | 30 | 91.5% [91.2%, 91.8%] | 89.6% [89.5%, 89.8%] | 1.9 [1.6, 2.2] |
| FD001 hybrid unweighted final | 60/100 | 24/76 | 30 | 95.1% [92.2%, 97.8%] | 90.8% [89.1%, 92.6%] | 4.3 [1.0, 7.6] |
| FD001 hybrid unweighted final | 60/10000 | 2062/7938 | 30 | 93.0% [92.7%, 93.4%] | 90.8% [90.7%, 91.0%] | 2.2 [1.8, 2.6] |
| FD001 hybrid weighted raw uniform | 60/100 | 22/78 | 30 | 68.6% [61.8%, 74.9%] | 67.1% [63.4%, 70.6%] | 1.5 [-5.9, 9.2] |
| FD001 hybrid weighted raw uniform | 60/10000 | 1734/8266 | 30 | 67.3% [66.6%, 68.0%] | 66.8% [66.4%, 67.1%] | 0.6 [-0.3, 1.4] |
| FD001 hybrid weighted corrected uniform | 60/100 | 22/78 | 30 | 90.2% [87.1%, 93.5%] | 90.2% [88.7%, 91.9%] | -0.1 [-3.6, 3.6] |
| FD001 hybrid weighted corrected uniform | 60/10000 | 1734/8266 | 30 | 90.7% [90.4%, 91.1%] | 90.8% [90.6%, 90.9%] | -0.0 [-0.4, 0.4] |
| FD001 hybrid unweighted uniform | 60/100 | 22/78 | 30 | 90.3% [87.2%, 93.8%] | 90.1% [88.6%, 91.7%] | 0.2 [-3.4, 3.9] |
| FD001 hybrid unweighted uniform | 60/10000 | 1734/8266 | 30 | 90.7% [90.3%, 91.0%] | 90.6% [90.4%, 90.8%] | 0.1 [-0.3, 0.5] |
| FD001 covariate weighted raw final | 60/100 | 24/76 | 200 | 49.4% [37.9%, 59.6%] | 33.7% [26.8%, 40.9%] | 15.7 [2.5, 28.2] |
| FD001 covariate weighted raw final | 60/10000 | 2062/7938 | 200 | 40.9% [39.6%, 42.3%] | 32.4% [31.7%, 33.1%] | 8.5 [7.0, 10.1] |
| FD001 covariate weighted corrected final | 60/100 | 24/76 | 200 | 25.1% [18.9%, 30.6%] | 16.4% [12.7%, 20.2%] | 8.7 [1.7, 15.5] |
| FD001 covariate weighted corrected final | 60/10000 | 2062/7938 | 200 | 20.3% [19.6%, 21.0%] | 15.7% [15.3%, 16.1%] | 4.6 [3.8, 5.4] |
| FD001 covariate unweighted final | 60/100 | 24/76 | 200 | 27.4% [20.6%, 33.4%] | 18.0% [14.1%, 22.2%] | 9.4 [1.7, 16.7] |
| FD001 covariate unweighted final | 60/10000 | 2062/7938 | 200 | 22.3% [21.6%, 23.1%] | 17.3% [16.9%, 17.7%] | 5.0 [4.1, 5.9] |
| FD001 covariate weighted raw uniform | 60/100 | 22/78 | 200 | 31.5% [18.8%, 45.2%] | 33.0% [26.3%, 40.0%] | -1.6 [-16.6, 13.3] |
| FD001 covariate weighted raw uniform | 60/10000 | 1734/8266 | 200 | 34.0% [32.5%, 35.5%] | 34.7% [34.0%, 35.4%] | -0.8 [-2.4, 0.9] |
| FD001 covariate weighted corrected uniform | 60/100 | 22/78 | 200 | 15.1% [8.4%, 22.3%] | 15.7% [12.2%, 19.4%] | -0.6 [-8.4, 7.1] |
| FD001 covariate weighted corrected uniform | 60/10000 | 1734/8266 | 200 | 16.4% [15.6%, 17.2%] | 16.7% [16.3%, 17.0%] | -0.3 [-1.1, 0.6] |
| FD001 covariate unweighted uniform | 60/100 | 22/78 | 200 | 16.3% [9.1%, 24.2%] | 16.8% [13.0%, 20.7%] | -0.4 [-8.9, 7.9] |
| FD001 covariate unweighted uniform | 60/10000 | 1734/8266 | 200 | 17.5% [16.7%, 18.4%] | 17.7% [17.3%, 18.1%] | -0.2 [-1.1, 0.7] |
| FD002 lstm weighted raw final | 156/259 | 53/206 | 30 | 34.5% [28.0%, 41.0%] | 25.4% [21.9%, 28.8%] | 9.1 [1.7, 16.7] |
| FD002 lstm weighted raw final | 156/10000 | 2052/7948 | 30 | 32.3% [31.3%, 33.3%] | 25.3% [24.8%, 25.8%] | 7.0 [5.8, 8.1] |
| FD002 lstm weighted corrected final | 156/259 | 53/206 | 30 | 22.8% [17.6%, 27.8%] | 15.5% [12.8%, 18.0%] | 7.3 [1.7, 13.0] |
| FD002 lstm weighted corrected final | 156/10000 | 2052/7948 | 30 | 20.4% [19.6%, 21.2%] | 15.2% [14.9%, 15.6%] | 5.1 [4.2, 6.1] |
| FD002 lstm unweighted final | 156/259 | 53/206 | 30 | 23.8% [18.5%, 29.0%] | 16.0% [13.3%, 18.7%] | 7.8 [2.0, 13.9] |
| FD002 lstm unweighted final | 156/10000 | 2052/7948 | 30 | 20.8% [20.0%, 21.6%] | 15.5% [15.1%, 15.9%] | 5.3 [4.4, 6.2] |
| FD002 lstm weighted raw uniform | 156/259 | 42/217 | 30 | 36.0% [27.3%, 44.7%] | 33.9% [30.0%, 37.9%] | 2.0 [-7.6, 11.7] |
| FD002 lstm weighted raw uniform | 156/10000 | 1761/8239 | 30 | 35.0% [33.6%, 36.3%] | 35.9% [35.2%, 36.5%] | -0.9 [-2.4, 0.6] |
| FD002 lstm weighted corrected uniform | 156/259 | 42/217 | 30 | 23.1% [16.1%, 30.1%] | 21.6% [18.5%, 24.7%] | 1.5 [-6.1, 9.3] |
| FD002 lstm weighted corrected uniform | 156/10000 | 1761/8239 | 30 | 22.4% [21.3%, 23.4%] | 23.0% [22.5%, 23.5%] | -0.6 [-1.8, 0.6] |
| FD002 lstm unweighted uniform | 156/259 | 42/217 | 30 | 23.5% [16.3%, 30.6%] | 22.2% [19.0%, 25.5%] | 1.2 [-6.6, 9.1] |
| FD002 lstm unweighted uniform | 156/10000 | 1761/8239 | 30 | 22.9% [21.8%, 24.0%] | 23.5% [23.0%, 24.0%] | -0.6 [-1.8, 0.6] |
| FD002 hybrid weighted raw final | 156/259 | 53/206 | 30 | 40.8% [37.2%, 44.2%] | 45.0% [43.4%, 46.7%] | -4.3 [-8.1, -0.6] |
| FD002 hybrid weighted raw final | 156/10000 | 2052/7948 | 30 | 42.8% [42.3%, 43.3%] | 45.6% [45.3%, 45.8%] | -2.8 [-3.4, -2.2] |
| FD002 hybrid weighted corrected final | 156/259 | 53/206 | 30 | 71.9% [69.9%, 74.1%] | 70.6% [69.7%, 71.7%] | 1.2 [-1.1, 3.6] |
| FD002 hybrid weighted corrected final | 156/10000 | 2052/7948 | 30 | 72.8% [72.5%, 73.1%] | 71.3% [71.1%, 71.4%] | 1.5 [1.2, 1.9] |
| FD002 hybrid unweighted final | 156/259 | 53/206 | 30 | 70.5% [68.4%, 72.7%] | 68.9% [67.9%, 70.0%] | 1.6 [-0.9, 4.0] |
| FD002 hybrid unweighted final | 156/10000 | 2052/7948 | 30 | 71.2% [70.9%, 71.6%] | 69.4% [69.2%, 69.5%] | 1.9 [1.5, 2.3] |
| FD002 hybrid weighted raw uniform | 156/259 | 42/217 | 30 | 38.5% [33.6%, 43.2%] | 38.8% [36.8%, 41.0%] | -0.3 [-5.6, 4.7] |
| FD002 hybrid weighted raw uniform | 156/10000 | 1761/8239 | 30 | 38.9% [38.1%, 39.6%] | 38.2% [37.8%, 38.5%] | 0.7 [-0.1, 1.5] |
| FD002 hybrid weighted corrected uniform | 156/259 | 42/217 | 30 | 66.4% [65.3%, 67.7%] | 65.6% [65.3%, 66.0%] | 0.8 [-0.4, 2.1] |
| FD002 hybrid weighted corrected uniform | 156/10000 | 1761/8239 | 30 | 66.2% [66.1%, 66.4%] | 65.8% [65.7%, 65.9%] | 0.4 [0.3, 0.6] |
| FD002 hybrid unweighted uniform | 156/259 | 42/217 | 30 | 65.6% [64.5%, 66.7%] | 64.9% [64.6%, 65.3%] | 0.6 [-0.5, 1.8] |
| FD002 hybrid unweighted uniform | 156/10000 | 1761/8239 | 30 | 65.5% [65.4%, 65.7%] | 65.2% [65.1%, 65.3%] | 0.3 [0.1, 0.5] |
| FD002 covariate weighted raw final | 156/259 | 53/206 | 200 | 15.5% [12.5%, 18.5%] | 11.7% [10.2%, 13.3%] | 3.7 [0.5, 7.2] |
| FD002 covariate weighted raw final | 156/10000 | 2052/7948 | 200 | 14.8% [14.3%, 15.3%] | 11.5% [11.3%, 11.8%] | 3.3 [2.8, 3.8] |
| FD002 covariate weighted corrected final | 156/259 | 53/206 | 200 | 11.7% [9.1%, 14.4%] | 8.8% [7.3%, 10.4%] | 2.8 [-0.2, 6.0] |
| FD002 covariate weighted corrected final | 156/10000 | 2052/7948 | 200 | 12.1% [11.7%, 12.6%] | 9.1% [8.9%, 9.4%] | 3.0 [2.5, 3.5] |
| FD002 covariate unweighted final | 156/259 | 53/206 | 200 | 11.5% [9.1%, 13.9%] | 8.3% [7.0%, 9.7%] | 3.2 [0.5, 6.0] |
| FD002 covariate unweighted final | 156/10000 | 2052/7948 | 200 | 11.3% [10.9%, 11.7%] | 8.5% [8.2%, 8.7%] | 2.8 [2.4, 3.3] |
| FD002 covariate weighted raw uniform | 156/259 | 42/217 | 200 | 15.4% [10.9%, 20.1%] | 15.6% [13.4%, 17.7%] | -0.2 [-5.2, 5.1] |
| FD002 covariate weighted raw uniform | 156/10000 | 1761/8239 | 200 | 15.2% [14.5%, 15.9%] | 16.4% [16.0%, 16.7%] | -1.2 [-2.0, -0.4] |
| FD002 covariate weighted corrected uniform | 156/259 | 42/217 | 200 | 9.1% [6.3%, 12.0%] | 9.0% [7.6%, 10.2%] | 0.1 [-3.0, 3.4] |
| FD002 covariate weighted corrected uniform | 156/10000 | 1761/8239 | 200 | 8.7% [8.3%, 9.2%] | 9.4% [9.2%, 9.7%] | -0.7 [-1.2, -0.3] |
| FD002 covariate unweighted uniform | 156/259 | 42/217 | 200 | 10.5% [7.3%, 13.9%] | 10.4% [8.9%, 11.9%] | 0.1 [-3.5, 3.8] |
| FD002 covariate unweighted uniform | 156/10000 | 1761/8239 | 200 | 10.1% [9.6%, 10.7%] | 11.0% [10.7%, 11.2%] | -0.8 [-1.4, -0.3] |
| FD003 lstm weighted raw final | 60/100 | 18/82 | 30 | 42.2% [35.7%, 49.0%] | 42.8% [39.4%, 46.2%] | -0.5 [-8.0, 6.8] |
| FD003 lstm weighted raw final | 60/10000 | 1998/8002 | 30 | 46.3% [45.7%, 46.9%] | 42.0% [41.7%, 42.4%] | 4.3 [3.5, 5.0] |
| FD003 lstm weighted corrected final | 60/100 | 18/82 | 30 | 18.0% [13.8%, 22.8%] | 19.1% [16.7%, 21.6%] | -1.2 [-6.3, 4.2] |
| FD003 lstm weighted corrected final | 60/10000 | 1998/8002 | 30 | 20.1% [19.7%, 20.6%] | 17.7% [17.5%, 17.9%] | 2.4 [1.9, 3.0] |
| FD003 lstm unweighted final | 60/100 | 18/82 | 30 | 16.3% [12.9%, 20.0%] | 16.5% [14.8%, 18.1%] | -0.2 [-3.9, 3.8] |
| FD003 lstm unweighted final | 60/10000 | 1998/8002 | 30 | 17.6% [17.3%, 17.9%] | 15.9% [15.7%, 16.0%] | 1.7 [1.4, 2.1] |
| FD003 lstm weighted raw uniform | 60/100 | 21/79 | 30 | 40.5% [34.6%, 46.4%] | 40.0% [37.2%, 42.7%] | 0.5 [-6.2, 7.3] |
| FD003 lstm weighted raw uniform | 60/10000 | 1786/8214 | 30 | 38.6% [38.0%, 39.1%] | 39.7% [39.4%, 40.0%] | -1.1 [-1.8, -0.5] |
| FD003 lstm weighted corrected uniform | 60/100 | 21/79 | 30 | 14.9% [12.5%, 17.8%] | 13.5% [12.6%, 14.6%] | 1.4 [-1.3, 4.4] |
| FD003 lstm weighted corrected uniform | 60/10000 | 1786/8214 | 30 | 13.1% [12.9%, 13.3%] | 13.3% [13.2%, 13.4%] | -0.2 [-0.4, 0.0] |
| FD003 lstm unweighted uniform | 60/100 | 21/79 | 30 | 15.2% [12.8%, 17.8%] | 15.4% [14.2%, 16.7%] | -0.2 [-2.8, 2.7] |
| FD003 lstm unweighted uniform | 60/10000 | 1786/8214 | 30 | 14.8% [14.5%, 15.0%] | 15.4% [15.3%, 15.5%] | -0.6 [-0.9, -0.3] |
| FD003 hybrid weighted raw final | 60/100 | 18/82 | 30 | 46.1% [42.4%, 50.0%] | 47.2% [45.3%, 49.1%] | -1.0 [-5.3, 3.5] |
| FD003 hybrid weighted raw final | 60/10000 | 1998/8002 | 30 | 48.2% [47.8%, 48.5%] | 46.8% [46.6%, 47.0%] | 1.3 [0.9, 1.7] |
| FD003 hybrid weighted corrected final | 60/100 | 18/82 | 30 | 65.4% [57.8%, 72.9%] | 65.7% [61.8%, 69.7%] | -0.4 [-9.4, 8.1] |
| FD003 hybrid weighted corrected final | 60/10000 | 1998/8002 | 30 | 70.0% [69.3%, 70.7%] | 65.3% [64.9%, 65.7%] | 4.7 [3.9, 5.5] |
| FD003 hybrid unweighted final | 60/100 | 18/82 | 30 | 69.3% [60.5%, 77.7%] | 69.9% [65.9%, 74.1%] | -0.7 [-10.5, 8.3] |
| FD003 hybrid unweighted final | 60/10000 | 1998/8002 | 30 | 73.6% [72.9%, 74.4%] | 69.3% [68.9%, 69.7%] | 4.4 [3.5, 5.2] |
| FD003 hybrid weighted raw uniform | 60/100 | 21/79 | 30 | 45.2% [42.9%, 47.6%] | 43.0% [41.6%, 44.4%] | 2.2 [-0.6, 4.9] |
| FD003 hybrid weighted raw uniform | 60/10000 | 1786/8214 | 30 | 43.0% [42.7%, 43.3%] | 43.0% [42.9%, 43.1%] | 0.0 [-0.3, 0.3] |
| FD003 hybrid weighted corrected uniform | 60/100 | 21/79 | 30 | 62.2% [56.3%, 68.2%] | 60.8% [58.0%, 63.6%] | 1.4 [-5.2, 8.0] |
| FD003 hybrid weighted corrected uniform | 60/10000 | 1786/8214 | 30 | 59.2% [58.6%, 59.8%] | 60.1% [59.8%, 60.3%] | -0.9 [-1.5, -0.3] |
| FD003 hybrid unweighted uniform | 60/100 | 21/79 | 30 | 60.5% [55.4%, 66.4%] | 59.6% [57.3%, 62.2%] | 0.9 [-4.8, 7.3] |
| FD003 hybrid unweighted uniform | 60/10000 | 1786/8214 | 30 | 58.6% [58.1%, 59.0%] | 58.6% [58.4%, 58.8%] | -0.0 [-0.6, 0.5] |
| FD003 covariate weighted raw final | 60/100 | 18/82 | 200 | 36.4% [21.0%, 52.1%] | 35.4% [28.6%, 42.2%] | 1.1 [-15.7, 17.3] |
| FD003 covariate weighted raw final | 60/10000 | 1998/8002 | 200 | 44.3% [42.9%, 45.7%] | 35.3% [34.6%, 36.0%] | 9.0 [7.3, 10.5] |
| FD003 covariate weighted corrected final | 60/100 | 18/82 | 200 | 17.6% [9.4%, 25.8%] | 16.9% [13.2%, 20.5%] | 0.7 [-8.3, 9.3] |
| FD003 covariate weighted corrected final | 60/10000 | 1998/8002 | 200 | 21.4% [20.7%, 22.2%] | 16.5% [16.1%, 16.9%] | 4.9 [4.0, 5.7] |
| FD003 covariate unweighted final | 60/100 | 18/82 | 200 | 18.9% [10.2%, 27.5%] | 18.3% [14.3%, 22.3%] | 0.5 [-9.2, 9.7] |
| FD003 covariate unweighted final | 60/10000 | 1998/8002 | 200 | 23.1% [22.3%, 23.9%] | 17.8% [17.4%, 18.2%] | 5.3 [4.4, 6.2] |
| FD003 covariate weighted raw uniform | 60/100 | 21/79 | 200 | 35.7% [21.5%, 49.9%] | 35.0% [27.9%, 41.6%] | 0.7 [-15.1, 16.6] |
| FD003 covariate weighted raw uniform | 60/10000 | 1786/8214 | 200 | 31.9% [30.4%, 33.4%] | 35.3% [34.7%, 36.0%] | -3.4 [-5.1, -1.8] |
| FD003 covariate weighted corrected uniform | 60/100 | 21/79 | 200 | 17.4% [9.9%, 24.6%] | 17.0% [13.3%, 20.5%] | 0.4 [-7.8, 8.5] |
| FD003 covariate weighted corrected uniform | 60/10000 | 1786/8214 | 200 | 15.3% [14.5%, 16.1%] | 17.0% [16.6%, 17.4%] | -1.7 [-2.6, -0.8] |
| FD003 covariate unweighted uniform | 60/100 | 21/79 | 200 | 18.5% [10.6%, 26.3%] | 18.0% [14.1%, 21.8%] | 0.5 [-8.2, 9.2] |
| FD003 covariate unweighted uniform | 60/10000 | 1786/8214 | 200 | 16.3% [15.5%, 17.2%] | 18.1% [17.7%, 18.4%] | -1.7 [-2.6, -0.8] |
| FD004 lstm weighted raw final | 149/248 | 50/198 | 30 | 36.9% [29.9%, 44.0%] | 27.6% [24.2%, 31.4%] | 9.3 [1.0, 17.0] |
| FD004 lstm weighted raw final | 149/10000 | 1940/8060 | 30 | 34.8% [33.7%, 35.9%] | 28.1% [27.5%, 28.7%] | 6.7 [5.5, 8.0] |
| FD004 lstm weighted corrected final | 149/248 | 50/198 | 30 | 21.9% [16.7%, 27.2%] | 15.8% [13.3%, 18.5%] | 6.2 [0.1, 12.0] |
| FD004 lstm weighted corrected final | 149/10000 | 1940/8060 | 30 | 21.5% [20.7%, 22.3%] | 16.6% [16.1%, 17.0%] | 4.9 [4.0, 5.9] |
| FD004 lstm unweighted final | 149/248 | 50/198 | 30 | 20.5% [16.0%, 25.0%] | 16.5% [14.4%, 18.9%] | 4.0 [-1.1, 9.0] |
| FD004 lstm unweighted final | 149/10000 | 1940/8060 | 30 | 21.1% [20.4%, 21.9%] | 17.0% [16.7%, 17.4%] | 4.1 [3.3, 4.9] |
| FD004 lstm weighted raw uniform | 149/248 | 44/204 | 30 | 31.8% [23.3%, 40.8%] | 28.6% [24.4%, 32.3%] | 3.2 [-5.9, 12.8] |
| FD004 lstm weighted raw uniform | 149/10000 | 1823/8177 | 30 | 28.0% [26.7%, 29.4%] | 29.5% [28.9%, 30.2%] | -1.5 [-2.9, 0.0] |
| FD004 lstm weighted corrected uniform | 149/248 | 44/204 | 30 | 19.5% [14.1%, 25.2%] | 16.8% [14.2%, 19.1%] | 2.7 [-3.2, 9.0] |
| FD004 lstm weighted corrected uniform | 149/10000 | 1823/8177 | 30 | 17.2% [16.3%, 18.1%] | 17.5% [17.1%, 17.9%] | -0.3 [-1.3, 0.6] |
| FD004 lstm unweighted uniform | 149/248 | 44/204 | 30 | 24.2% [18.4%, 30.3%] | 21.8% [19.1%, 24.3%] | 2.4 [-3.9, 8.9] |
| FD004 lstm unweighted uniform | 149/10000 | 1823/8177 | 30 | 21.5% [20.6%, 22.4%] | 22.6% [22.2%, 23.0%] | -1.1 [-2.1, -0.1] |
| FD004 hybrid weighted raw final | 149/248 | 50/198 | 30 | 45.4% [44.3%, 46.6%] | 44.8% [44.3%, 45.4%] | 0.6 [-0.6, 1.8] |
| FD004 hybrid weighted raw final | 149/10000 | 1940/8060 | 30 | 45.0% [44.8%, 45.2%] | 44.7% [44.6%, 44.8%] | 0.3 [0.1, 0.5] |
| FD004 hybrid weighted corrected final | 149/248 | 50/198 | 30 | 57.7% [53.5%, 62.0%] | 52.1% [50.1%, 54.2%] | 5.7 [0.9, 10.3] |
| FD004 hybrid weighted corrected final | 149/10000 | 1940/8060 | 30 | 55.9% [55.3%, 56.6%] | 52.4% [52.1%, 52.7%] | 3.6 [2.8, 4.3] |
| FD004 hybrid unweighted final | 149/248 | 50/198 | 30 | 61.4% [57.2%, 65.7%] | 55.0% [53.0%, 57.1%] | 6.4 [1.5, 11.0] |
| FD004 hybrid unweighted final | 149/10000 | 1940/8060 | 30 | 59.3% [58.6%, 59.9%] | 55.8% [55.4%, 56.1%] | 3.5 [2.8, 4.3] |
| FD004 hybrid weighted raw uniform | 149/248 | 44/204 | 30 | 46.1% [44.6%, 47.5%] | 46.0% [45.4%, 46.7%] | 0.0 [-1.6, 1.6] |
| FD004 hybrid weighted raw uniform | 149/10000 | 1823/8177 | 30 | 46.0% [45.8%, 46.3%] | 46.3% [46.2%, 46.4%] | -0.3 [-0.5, -0.0] |
| FD004 hybrid weighted corrected uniform | 149/248 | 44/204 | 30 | 46.6% [44.6%, 48.7%] | 45.3% [44.5%, 46.2%] | 1.3 [-0.9, 3.6] |
| FD004 hybrid weighted corrected uniform | 149/10000 | 1823/8177 | 30 | 45.6% [45.2%, 45.9%] | 45.5% [45.3%, 45.6%] | 0.1 [-0.3, 0.4] |
| FD004 hybrid unweighted uniform | 149/248 | 44/204 | 30 | 47.5% [45.8%, 49.5%] | 46.5% [45.8%, 47.3%] | 1.0 [-0.9, 3.1] |
| FD004 hybrid unweighted uniform | 149/10000 | 1823/8177 | 30 | 47.1% [46.8%, 47.4%] | 46.4% [46.3%, 46.6%] | 0.6 [0.3, 0.9] |
| FD004 covariate weighted raw final | 149/248 | 50/198 | 200 | 17.2% [13.7%, 20.6%] | 14.5% [12.7%, 16.6%] | 2.6 [-1.4, 6.5] |
| FD004 covariate weighted raw final | 149/10000 | 1940/8060 | 200 | 16.0% [15.4%, 16.6%] | 14.1% [13.8%, 14.3%] | 1.9 [1.3, 2.6] |
| FD004 covariate weighted corrected final | 149/248 | 50/198 | 200 | 14.9% [11.5%, 18.3%] | 10.6% [9.1%, 12.4%] | 4.3 [0.4, 8.1] |
| FD004 covariate weighted corrected final | 149/10000 | 1940/8060 | 200 | 13.6% [13.0%, 14.1%] | 10.8% [10.5%, 11.1%] | 2.8 [2.2, 3.4] |
| FD004 covariate unweighted final | 149/248 | 50/198 | 200 | 13.5% [10.4%, 16.5%] | 9.8% [8.4%, 11.5%] | 3.6 [0.1, 7.1] |
| FD004 covariate unweighted final | 149/10000 | 1940/8060 | 200 | 12.4% [11.9%, 12.8%] | 9.9% [9.6%, 10.1%] | 2.5 [1.9, 3.0] |
| FD004 covariate weighted raw uniform | 149/248 | 44/204 | 200 | 15.7% [11.4%, 20.4%] | 16.1% [13.7%, 18.2%] | -0.3 [-5.0, 4.6] |
| FD004 covariate weighted raw uniform | 149/10000 | 1823/8177 | 200 | 14.5% [13.8%, 15.2%] | 16.5% [16.2%, 16.9%] | -2.0 [-2.8, -1.2] |
| FD004 covariate weighted corrected uniform | 149/248 | 44/204 | 200 | 9.2% [6.5%, 11.9%] | 9.2% [7.8%, 10.5%] | -0.0 [-2.8, 3.0] |
| FD004 covariate weighted corrected uniform | 149/10000 | 1823/8177 | 200 | 8.5% [8.1%, 8.9%] | 9.6% [9.3%, 9.8%] | -1.1 [-1.5, -0.6] |
| FD004 covariate unweighted uniform | 149/248 | 44/204 | 200 | 10.3% [7.2%, 13.4%] | 10.2% [8.7%, 11.7%] | 0.1 [-3.1, 3.4] |
| FD004 covariate unweighted uniform | 149/10000 | 1823/8177 | 200 | 9.4% [8.9%, 9.9%] | 10.6% [10.4%, 10.9%] | -1.2 [-1.7, -0.7] |

```{=latex}
\begin{landscape}
```

## Table S11. Full non-collapsed pipeline-check percentiles and real rates

Source: `null_distribution.csv`; all rates are percentages. These are descriptive pipeline-check values, not a real-data reference benchmark.

| Group | Fit / pipeline / real engines | Pipeline fits | Real rate | Min | 2.5 | 25 | 50 | 75 | 97.5 | Max | Location |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FD001 lstm | 60/10000/100 | 22 | 20.4% | 0.0% | 0.0% | 0.3% | 99.7% | 100.0% | 100.0% | 100.0% | inside |
| FD001 hybrid | 60/10000/100 | 5 | 13.6% | 10.7% | 14.3% | 46.6% | 49.8% | 50.3% | 55.2% | 55.8% | below |
| FD002 lstm | 156/10000/259 | 30 | 9.6% | 0.7% | 1.0% | 5.8% | 25.5% | 47.8% | 57.5% | 76.9% | inside |
| FD002 hybrid | 156/10000/259 | 10 | 8.9% | 0.0% | 0.8% | 7.9% | 18.4% | 26.2% | 88.8% | 100.0% | inside |
| FD003 lstm | 60/10000/100 | 28 | 12.8% | 0.0% | 0.0% | 6.4% | 37.6% | 58.7% | 100.0% | 100.0% | inside |
| FD003 hybrid | 60/10000/100 | 17 | 11.8% | 1.3% | 7.1% | 22.1% | 31.2% | 42.2% | 79.3% | 97.0% | inside |
| FD004 lstm | 149/10000/248 | 30 | 16.6% | 3.9% | 4.3% | 12.8% | 30.2% | 43.8% | 60.2% | 64.0% | inside |
| FD004 hybrid | 149/10000/248 | 18 | 12.7% | 2.0% | 3.6% | 10.1% | 22.8% | 41.0% | 94.5% | 95.5% | inside |

```{=latex}
\end{landscape}
```


## Table S12. Per-fit difficulty: all retained synthetic and real fits

Source: `difficulty_per_fit.csv`. Rows: 200. The full source is in `validation_data`.

| Group / cohort | Fit ID | Fit / test engines | Capped RMSE | AUC | Event base rate | Median raw width |
|---|---|---|---|---|---|---|
| FD001 lstm synthetic noncollapsed | 1 | 60/10000 | 45.4 | 0.651377 | 41.5% | 36.8 |
| FD001 lstm synthetic noncollapsed | 3 | 60/10000 | 47.7 | 0.636140 | 41.5% | 39.8 |
| FD001 lstm synthetic noncollapsed | 4 | 60/10000 | 46.3 | 0.575869 | 41.5% | 67.6 |
| FD001 lstm synthetic noncollapsed | 5 | 60/10000 | 46.0 | 0.643054 | 41.5% | 42.4 |
| FD001 lstm synthetic noncollapsed | 6 | 60/10000 | 42.9 | 0.629793 | 41.5% | 89.4 |
| FD001 lstm synthetic noncollapsed | 7 | 60/10000 | 45.3 | 0.365872 | 41.5% | 43.7 |
| FD001 lstm synthetic noncollapsed | 8 | 60/10000 | 42.8 | 0.645371 | 41.5% | 83.4 |
| FD001 lstm synthetic noncollapsed | 10 | 60/10000 | 48.0 | 0.654428 | 41.5% | 42.0 |
| FD001 lstm synthetic noncollapsed | 11 | 60/10000 | 43.9 | 0.653568 | 41.5% | 62.4 |
| FD001 lstm synthetic noncollapsed | 13 | 60/10000 | 43.5 | 0.623041 | 41.5% | 102 |
| FD001 lstm synthetic noncollapsed | 14 | 60/10000 | 47.4 | 0.634451 | 41.5% | 39.3 |
| FD001 lstm synthetic noncollapsed | 15 | 60/10000 | 42.8 | 0.526458 | 41.5% | 69.5 |
| FD001 lstm synthetic noncollapsed | 16 | 60/10000 | 47.2 | 0.649005 | 41.5% | 43.0 |
| FD001 lstm synthetic noncollapsed | 17 | 60/10000 | 48.1 | 0.349689 | 41.5% | 34.1 |
| FD001 lstm synthetic noncollapsed | 19 | 60/10000 | 42.0 | 0.653508 | 41.5% | 89.6 |
| FD001 lstm synthetic noncollapsed | 20 | 60/10000 | 43.0 | 0.633582 | 41.5% | 83.9 |
| FD001 lstm synthetic noncollapsed | 21 | 60/10000 | 47.1 | 0.620804 | 41.5% | 46.9 |
| FD001 lstm synthetic noncollapsed | 24 | 60/10000 | 49.5 | 0.653424 | 41.5% | 48.2 |
| FD001 lstm synthetic noncollapsed | 25 | 60/10000 | 50.0 | 0.588560 | 41.5% | 24.6 |
| FD001 lstm synthetic noncollapsed | 27 | 60/10000 | 42.5 | 0.656526 | 41.5% | 74.6 |
| FD001 lstm synthetic noncollapsed | 28 | 60/10000 | 44.5 | 0.554706 | 41.5% | 48.6 |
| FD001 lstm synthetic noncollapsed | 29 | 60/10000 | 41.6 | 0.653305 | 41.5% | 56.7 |
| FD001 lstm real | 1101 | 60/100 | 13.7 | 0.986667 | 25.0% | 66.3 |
| FD001 lstm real | 1202 | 60/100 | 14.6 | 0.986667 | 25.0% | 83.1 |
| FD001 lstm real | 1303 | 60/100 | 14.9 | 0.985600 | 25.0% | 77.4 |
| FD001 lstm real | 1404 | 60/100 | 15.4 | 0.982400 | 25.0% | 68.2 |
| FD001 lstm real | 1505 | 60/100 | 14.9 | 0.989867 | 25.0% | 68.7 |
| FD001 hybrid synthetic noncollapsed | 9 | 60/10000 | 46.1 | 0.353316 | 41.5% | 119 |
| FD001 hybrid synthetic noncollapsed | 14 | 60/10000 | 42.7 | 0.643639 | 41.5% | 73.4 |
| FD001 hybrid synthetic noncollapsed | 16 | 60/10000 | 40.5 | 0.651309 | 41.5% | 122 |
| FD001 hybrid synthetic noncollapsed | 17 | 60/10000 | 42.1 | 0.654745 | 41.5% | 107 |
| FD001 hybrid synthetic noncollapsed | 25 | 60/10000 | 43.0 | 0.651765 | 41.5% | 112 |
| FD001 hybrid real | 1101 | 60/100 | 15.3 | 0.993600 | 25.0% | 51.9 |
| FD001 hybrid real | 1202 | 60/100 | 18.1 | 0.988800 | 25.0% | 54.5 |
| FD001 hybrid real | 1303 | 60/100 | 15.0 | 0.989333 | 25.0% | 46.1 |
| FD001 hybrid real | 1404 | 60/100 | 15.8 | 0.985067 | 25.0% | 50.3 |
| FD001 hybrid real | 1505 | 60/100 | 15.3 | 0.988800 | 25.0% | 47.4 |
| FD002 lstm synthetic noncollapsed | 0 | 156/10000 | 41.7 | 0.596202 | 42.0% | 131 |
| FD002 lstm synthetic noncollapsed | 1 | 156/10000 | 41.0 | 0.624169 | 42.0% | 124 |
| FD002 lstm synthetic noncollapsed | 2 | 156/10000 | 41.1 | 0.649220 | 42.0% | 105 |
| FD002 lstm synthetic noncollapsed | 3 | 156/10000 | 40.1 | 0.649437 | 42.0% | 99.7 |
| FD002 lstm synthetic noncollapsed | 4 | 156/10000 | 39.7 | 0.647219 | 42.0% | 127 |
| FD002 lstm synthetic noncollapsed | 5 | 156/10000 | 40.0 | 0.645868 | 42.0% | 109 |
| FD002 lstm synthetic noncollapsed | 6 | 156/10000 | 40.4 | 0.649271 | 42.0% | 87.6 |
| FD002 lstm synthetic noncollapsed | 7 | 156/10000 | 44.0 | 0.648324 | 42.0% | 93.5 |
| FD002 lstm synthetic noncollapsed | 8 | 156/10000 | 41.3 | 0.651367 | 42.0% | 92.4 |
| FD002 lstm synthetic noncollapsed | 9 | 156/10000 | 40.2 | 0.642646 | 42.0% | 129 |
| FD002 lstm synthetic noncollapsed | 10 | 156/10000 | 39.6 | 0.647341 | 42.0% | 102 |
| FD002 lstm synthetic noncollapsed | 11 | 156/10000 | 45.9 | 0.643299 | 42.0% | 130 |
| FD002 lstm synthetic noncollapsed | 12 | 156/10000 | 41.3 | 0.647874 | 42.0% | 130 |
| FD002 lstm synthetic noncollapsed | 13 | 156/10000 | 41.5 | 0.648776 | 42.0% | 88.5 |
| FD002 lstm synthetic noncollapsed | 14 | 156/10000 | 40.4 | 0.649796 | 42.0% | 97.0 |
| FD002 lstm synthetic noncollapsed | 15 | 156/10000 | 40.9 | 0.650887 | 42.0% | 106 |
| FD002 lstm synthetic noncollapsed | 16 | 156/10000 | 39.4 | 0.647913 | 42.0% | 100 |
| FD002 lstm synthetic noncollapsed | 17 | 156/10000 | 39.7 | 0.650548 | 42.0% | 89.2 |
| FD002 lstm synthetic noncollapsed | 18 | 156/10000 | 43.1 | 0.648572 | 42.0% | 130 |
| FD002 lstm synthetic noncollapsed | 19 | 156/10000 | 41.1 | 0.645755 | 42.0% | 123 |
| FD002 lstm synthetic noncollapsed | 20 | 156/10000 | 39.8 | 0.647266 | 42.0% | 103 |
| FD002 lstm synthetic noncollapsed | 21 | 156/10000 | 41.4 | 0.651885 | 42.0% | 114 |
| FD002 lstm synthetic noncollapsed | 22 | 156/10000 | 39.7 | 0.648628 | 42.0% | 126 |
| FD002 lstm synthetic noncollapsed | 23 | 156/10000 | 40.4 | 0.649780 | 42.0% | 87.4 |
| FD002 lstm synthetic noncollapsed | 24 | 156/10000 | 42.0 | 0.620205 | 42.0% | 128 |
| FD002 lstm synthetic noncollapsed | 25 | 156/10000 | 43.9 | 0.626810 | 42.0% | 123 |
| FD002 lstm synthetic noncollapsed | 26 | 156/10000 | 40.3 | 0.649071 | 42.0% | 90.5 |
| FD002 lstm synthetic noncollapsed | 27 | 156/10000 | 39.5 | 0.649668 | 42.0% | 123 |
| FD002 lstm synthetic noncollapsed | 28 | 156/10000 | 40.5 | 0.649401 | 42.0% | 111 |
| FD002 lstm synthetic noncollapsed | 29 | 156/10000 | 39.4 | 0.648729 | 42.0% | 110 |
| FD002 lstm real | 1101 | 156/259 | 13.6 | 0.997516 | 23.6% | 53.7 |
| FD002 lstm real | 1202 | 156/259 | 14.2 | 0.998013 | 23.6% | 53.5 |
| FD002 lstm real | 1303 | 156/259 | 15.1 | 0.998427 | 23.6% | 56.6 |
| FD002 lstm real | 1404 | 156/259 | 14.4 | 0.999089 | 23.6% | 55.9 |
| FD002 lstm real | 1505 | 156/259 | 14.3 | 0.999006 | 23.6% | 54.5 |
| FD002 hybrid synthetic noncollapsed | 3 | 156/10000 | 40.3 | 0.647316 | 42.0% | 88.4 |
| FD002 hybrid synthetic noncollapsed | 7 | 156/10000 | 40.2 | 0.647343 | 42.0% | 60.3 |
| FD002 hybrid synthetic noncollapsed | 18 | 156/10000 | 42.2 | 0.645214 | 42.0% | 119 |
| FD002 hybrid synthetic noncollapsed | 22 | 156/10000 | 39.5 | 0.648462 | 42.0% | 84.3 |
| FD002 hybrid synthetic noncollapsed | 23 | 156/10000 | 40.3 | 0.650413 | 42.0% | 62.2 |
| FD002 hybrid synthetic noncollapsed | 24 | 156/10000 | 42.2 | 0.603965 | 42.0% | 114 |
| FD002 hybrid synthetic noncollapsed | 25 | 156/10000 | 40.4 | 0.649820 | 42.0% | 110 |
| FD002 hybrid synthetic noncollapsed | 26 | 156/10000 | 39.9 | 0.649607 | 42.0% | 105 |
| FD002 hybrid synthetic noncollapsed | 28 | 156/10000 | 41.7 | 0.648452 | 42.0% | 91.1 |
| FD002 hybrid synthetic noncollapsed | 29 | 156/10000 | 39.9 | 0.646238 | 42.0% | 95.7 |
| FD002 hybrid real | 1101 | 156/259 | 15.0 | 0.998261 | 23.6% | 56.6 |
| FD002 hybrid real | 1202 | 156/259 | 14.5 | 0.997268 | 23.6% | 51.2 |
| FD002 hybrid real | 1303 | 156/259 | 15.3 | 0.998510 | 23.6% | 54.3 |
| FD002 hybrid real | 1404 | 156/259 | 14.3 | 0.997019 | 23.6% | 56.1 |
| FD002 hybrid real | 1505 | 156/259 | 17.9 | 0.991389 | 23.6% | 53.0 |
| FD003 lstm synthetic noncollapsed | 0 | 60/10000 | 41.6 | 0.653232 | 40.8% | 124 |
| FD003 lstm synthetic noncollapsed | 1 | 60/10000 | 42.7 | 0.605508 | 40.8% | 137 |
| FD003 lstm synthetic noncollapsed | 2 | 60/10000 | 44.1 | 0.367174 | 40.8% | 124 |
| FD003 lstm synthetic noncollapsed | 3 | 60/10000 | 39.9 | 0.654099 | 40.8% | 114 |
| FD003 lstm synthetic noncollapsed | 4 | 60/10000 | 42.2 | 0.653868 | 40.8% | 130 |
| FD003 lstm synthetic noncollapsed | 5 | 60/10000 | 42.3 | 0.648748 | 40.8% | 125 |
| FD003 lstm synthetic noncollapsed | 6 | 60/10000 | 41.3 | 0.651551 | 40.8% | 117 |
| FD003 lstm synthetic noncollapsed | 7 | 60/10000 | 40.7 | 0.656477 | 40.8% | 132 |
| FD003 lstm synthetic noncollapsed | 8 | 60/10000 | 40.7 | 0.640693 | 40.8% | 129 |
| FD003 lstm synthetic noncollapsed | 9 | 60/10000 | 39.7 | 0.647266 | 40.8% | 129 |
| FD003 lstm synthetic noncollapsed | 10 | 60/10000 | 40.5 | 0.654240 | 40.8% | 111 |
| FD003 lstm synthetic noncollapsed | 11 | 60/10000 | 39.9 | 0.656205 | 40.8% | 128 |
| FD003 lstm synthetic noncollapsed | 12 | 60/10000 | 44.1 | 0.373762 | 40.8% | 126 |
| FD003 lstm synthetic noncollapsed | 14 | 60/10000 | 39.3 | 0.655992 | 40.8% | 136 |
| FD003 lstm synthetic noncollapsed | 15 | 60/10000 | 41.1 | 0.654917 | 40.8% | 133 |
| FD003 lstm synthetic noncollapsed | 16 | 60/10000 | 40.6 | 0.654715 | 40.8% | 90.3 |
| FD003 lstm synthetic noncollapsed | 17 | 60/10000 | 45.3 | 0.654830 | 40.8% | 115 |
| FD003 lstm synthetic noncollapsed | 18 | 60/10000 | 39.9 | 0.655229 | 40.8% | 119 |
| FD003 lstm synthetic noncollapsed | 19 | 60/10000 | 43.7 | 0.622473 | 40.8% | 129 |
| FD003 lstm synthetic noncollapsed | 20 | 60/10000 | 40.3 | 0.654709 | 40.8% | 130 |
| FD003 lstm synthetic noncollapsed | 21 | 60/10000 | 40.1 | 0.655043 | 40.8% | 108 |
| FD003 lstm synthetic noncollapsed | 22 | 60/10000 | 40.5 | 0.618995 | 40.8% | 129 |
| FD003 lstm synthetic noncollapsed | 23 | 60/10000 | 40.5 | 0.655291 | 40.8% | 117 |
| FD003 lstm synthetic noncollapsed | 24 | 60/10000 | 40.9 | 0.655598 | 40.8% | 121 |
| FD003 lstm synthetic noncollapsed | 26 | 60/10000 | 42.8 | 0.629315 | 40.8% | 132 |
| FD003 lstm synthetic noncollapsed | 27 | 60/10000 | 42.2 | 0.656059 | 40.8% | 125 |
| FD003 lstm synthetic noncollapsed | 28 | 60/10000 | 50.1 | 0.379198 | 40.8% | 129 |
| FD003 lstm synthetic noncollapsed | 29 | 60/10000 | 41.5 | 0.656169 | 40.8% | 124 |
| FD003 lstm real | 1101 | 60/100 | 17.6 | 0.990625 | 20.0% | 49.3 |
| FD003 lstm real | 1202 | 60/100 | 16.3 | 0.994375 | 20.0% | 42.7 |
| FD003 lstm real | 1303 | 60/100 | 17.8 | 0.997500 | 20.0% | 46.0 |
| FD003 lstm real | 1404 | 60/100 | 18.7 | 0.995000 | 20.0% | 45.1 |
| FD003 lstm real | 1505 | 60/100 | 19.1 | 0.990625 | 20.0% | 50.9 |
| FD003 hybrid synthetic noncollapsed | 2 | 60/10000 | 43.6 | 0.631133 | 40.8% | 102 |
| FD003 hybrid synthetic noncollapsed | 3 | 60/10000 | 44.4 | 0.643094 | 40.8% | 96.7 |
| FD003 hybrid synthetic noncollapsed | 4 | 60/10000 | 48.0 | 0.627756 | 40.8% | 67.2 |
| FD003 hybrid synthetic noncollapsed | 7 | 60/10000 | 42.1 | 0.650906 | 40.8% | 64.0 |
| FD003 hybrid synthetic noncollapsed | 10 | 60/10000 | 43.8 | 0.654172 | 40.8% | 54.5 |
| FD003 hybrid synthetic noncollapsed | 15 | 60/10000 | 42.0 | 0.656168 | 40.8% | 81.8 |
| FD003 hybrid synthetic noncollapsed | 16 | 60/10000 | 45.6 | 0.656474 | 40.8% | 101 |
| FD003 hybrid synthetic noncollapsed | 17 | 60/10000 | 46.8 | 0.635551 | 40.8% | 54.0 |
| FD003 hybrid synthetic noncollapsed | 19 | 60/10000 | 49.6 | 0.547727 | 40.8% | 112 |
| FD003 hybrid synthetic noncollapsed | 20 | 60/10000 | 40.1 | 0.653901 | 40.8% | 129 |
| FD003 hybrid synthetic noncollapsed | 21 | 60/10000 | 45.8 | 0.653898 | 40.8% | 83.0 |
| FD003 hybrid synthetic noncollapsed | 22 | 60/10000 | 39.4 | 0.656982 | 40.8% | 128 |
| FD003 hybrid synthetic noncollapsed | 23 | 60/10000 | 52.1 | 0.650920 | 40.8% | 38.9 |
| FD003 hybrid synthetic noncollapsed | 24 | 60/10000 | 41.6 | 0.654955 | 40.8% | 67.5 |
| FD003 hybrid synthetic noncollapsed | 26 | 60/10000 | 40.8 | 0.654610 | 40.8% | 105 |
| FD003 hybrid synthetic noncollapsed | 27 | 60/10000 | 42.5 | 0.639832 | 40.8% | 90.9 |
| FD003 hybrid synthetic noncollapsed | 29 | 60/10000 | 44.1 | 0.654791 | 40.8% | 58.9 |
| FD003 hybrid real | 1101 | 60/100 | 15.9 | 1.000000 | 20.0% | 34.9 |
| FD003 hybrid real | 1202 | 60/100 | 14.1 | 0.997500 | 20.0% | 31.7 |
| FD003 hybrid real | 1303 | 60/100 | 16.1 | 0.996875 | 20.0% | 30.4 |
| FD003 hybrid real | 1404 | 60/100 | 14.9 | 0.996875 | 20.0% | 29.3 |
| FD003 hybrid real | 1505 | 60/100 | 15.3 | 0.993125 | 20.0% | 30.0 |
| FD004 lstm synthetic noncollapsed | 0 | 149/10000 | 42.5 | 0.654165 | 40.3% | 103 |
| FD004 lstm synthetic noncollapsed | 1 | 149/10000 | 39.2 | 0.654963 | 40.3% | 106 |
| FD004 lstm synthetic noncollapsed | 2 | 149/10000 | 40.8 | 0.648706 | 40.3% | 97.2 |
| FD004 lstm synthetic noncollapsed | 3 | 149/10000 | 40.3 | 0.657896 | 40.3% | 102 |
| FD004 lstm synthetic noncollapsed | 4 | 149/10000 | 41.3 | 0.648631 | 40.3% | 85.9 |
| FD004 lstm synthetic noncollapsed | 5 | 149/10000 | 40.1 | 0.641142 | 40.3% | 132 |
| FD004 lstm synthetic noncollapsed | 6 | 149/10000 | 39.1 | 0.657810 | 40.3% | 110 |
| FD004 lstm synthetic noncollapsed | 7 | 149/10000 | 40.8 | 0.630992 | 40.3% | 130 |
| FD004 lstm synthetic noncollapsed | 8 | 149/10000 | 41.0 | 0.659329 | 40.3% | 101 |
| FD004 lstm synthetic noncollapsed | 9 | 149/10000 | 39.8 | 0.648891 | 40.3% | 116 |
| FD004 lstm synthetic noncollapsed | 10 | 149/10000 | 40.2 | 0.651344 | 40.3% | 128 |
| FD004 lstm synthetic noncollapsed | 11 | 149/10000 | 40.8 | 0.653304 | 40.3% | 123 |
| FD004 lstm synthetic noncollapsed | 12 | 149/10000 | 39.5 | 0.657494 | 40.3% | 116 |
| FD004 lstm synthetic noncollapsed | 13 | 149/10000 | 42.9 | 0.634775 | 40.3% | 126 |
| FD004 lstm synthetic noncollapsed | 14 | 149/10000 | 39.6 | 0.656848 | 40.3% | 110 |
| FD004 lstm synthetic noncollapsed | 15 | 149/10000 | 41.8 | 0.654296 | 40.3% | 117 |
| FD004 lstm synthetic noncollapsed | 16 | 149/10000 | 39.5 | 0.647248 | 40.3% | 93.6 |
| FD004 lstm synthetic noncollapsed | 17 | 149/10000 | 42.1 | 0.656949 | 40.3% | 110 |
| FD004 lstm synthetic noncollapsed | 18 | 149/10000 | 41.4 | 0.632280 | 40.3% | 128 |
| FD004 lstm synthetic noncollapsed | 19 | 149/10000 | 40.7 | 0.657172 | 40.3% | 112 |
| FD004 lstm synthetic noncollapsed | 20 | 149/10000 | 41.5 | 0.637755 | 40.3% | 129 |
| FD004 lstm synthetic noncollapsed | 21 | 149/10000 | 41.1 | 0.647240 | 40.3% | 122 |
| FD004 lstm synthetic noncollapsed | 22 | 149/10000 | 39.7 | 0.651512 | 40.3% | 120 |
| FD004 lstm synthetic noncollapsed | 23 | 149/10000 | 39.9 | 0.654650 | 40.3% | 123 |
| FD004 lstm synthetic noncollapsed | 24 | 149/10000 | 39.6 | 0.653477 | 40.3% | 111 |
| FD004 lstm synthetic noncollapsed | 25 | 149/10000 | 42.7 | 0.656256 | 40.3% | 94.0 |
| FD004 lstm synthetic noncollapsed | 26 | 149/10000 | 40.4 | 0.658399 | 40.3% | 98.4 |
| FD004 lstm synthetic noncollapsed | 27 | 149/10000 | 40.6 | 0.654655 | 40.3% | 106 |
| FD004 lstm synthetic noncollapsed | 28 | 149/10000 | 41.8 | 0.657068 | 40.3% | 102 |
| FD004 lstm synthetic noncollapsed | 29 | 149/10000 | 45.4 | 0.653490 | 40.3% | 130 |
| FD004 lstm real | 1101 | 149/248 | 16.9 | 0.989453 | 21.4% | 47.1 |
| FD004 lstm real | 1202 | 149/248 | 16.2 | 0.987325 | 21.4% | 46.0 |
| FD004 lstm real | 1303 | 149/248 | 16.2 | 0.990227 | 21.4% | 44.1 |
| FD004 lstm real | 1404 | 149/248 | 16.9 | 0.988582 | 21.4% | 46.1 |
| FD004 lstm real | 1505 | 149/248 | 16.6 | 0.987712 | 21.4% | 48.9 |
| FD004 hybrid synthetic noncollapsed | 0 | 149/10000 | 41.2 | 0.655310 | 40.3% | 78.6 |
| FD004 hybrid synthetic noncollapsed | 1 | 149/10000 | 39.6 | 0.651249 | 40.3% | 104 |
| FD004 hybrid synthetic noncollapsed | 2 | 149/10000 | 40.0 | 0.654923 | 40.3% | 91.3 |
| FD004 hybrid synthetic noncollapsed | 3 | 149/10000 | 40.5 | 0.398778 | 40.3% | 103 |
| FD004 hybrid synthetic noncollapsed | 5 | 149/10000 | 39.5 | 0.655795 | 40.3% | 114 |
| FD004 hybrid synthetic noncollapsed | 9 | 149/10000 | 39.1 | 0.649828 | 40.3% | 87.0 |
| FD004 hybrid synthetic noncollapsed | 10 | 149/10000 | 40.2 | 0.497859 | 40.3% | 105 |
| FD004 hybrid synthetic noncollapsed | 14 | 149/10000 | 39.4 | 0.650692 | 40.3% | 97.2 |
| FD004 hybrid synthetic noncollapsed | 16 | 149/10000 | 39.6 | 0.370025 | 40.3% | 103 |
| FD004 hybrid synthetic noncollapsed | 17 | 149/10000 | 43.7 | 0.657076 | 40.3% | 77.9 |
| FD004 hybrid synthetic noncollapsed | 18 | 149/10000 | 41.8 | 0.653260 | 40.3% | 93.1 |
| FD004 hybrid synthetic noncollapsed | 19 | 149/10000 | 41.7 | 0.656687 | 40.3% | 98.8 |
| FD004 hybrid synthetic noncollapsed | 20 | 149/10000 | 39.6 | 0.650846 | 40.3% | 112 |
| FD004 hybrid synthetic noncollapsed | 21 | 149/10000 | 42.8 | 0.653903 | 40.3% | 109 |
| FD004 hybrid synthetic noncollapsed | 22 | 149/10000 | 39.8 | 0.462007 | 40.3% | 108 |
| FD004 hybrid synthetic noncollapsed | 23 | 149/10000 | 39.4 | 0.654686 | 40.3% | 83.2 |
| FD004 hybrid synthetic noncollapsed | 25 | 149/10000 | 43.5 | 0.654073 | 40.3% | 91.0 |
| FD004 hybrid synthetic noncollapsed | 29 | 149/10000 | 41.9 | 0.471059 | 40.3% | 116 |
| FD004 hybrid real | 1101 | 149/248 | 16.8 | 0.991388 | 21.4% | 45.0 |
| FD004 hybrid real | 1202 | 149/248 | 16.3 | 0.983745 | 21.4% | 38.9 |
| FD004 hybrid real | 1303 | 149/248 | 17.0 | 0.989550 | 21.4% | 47.9 |
| FD004 hybrid real | 1404 | 149/248 | 16.3 | 0.982003 | 21.4% | 43.8 |
| FD004 hybrid real | 1505 | 149/248 | 16.3 | 0.982777 | 21.4% | 42.5 |

## Source and uncertainty notes

Synthetic shape is 1, with scale(x)=60 exp(0.5x), x in {-1,+1}. Training lifetimes are 30 plus an exponential excess lifetime. Final-window residual RUL depends on x but is age-independent conditional on x; uniform-endpoint conditional RUL depends on age and x. Raw widths are unprojected. Bootstrap CIs resample engines, preserving fixed fits. The paired factorial ranges are not CIs. Negative results, empty strata and shared FD001/FD003 covariate states remain recorded in the source tables. Independent human review has not been performed.

## Table S13a. Positive controls: every group, subset-combined and pooled estimate

Source: `A_controls.csv`. Rates are percentages; distances are probability units.

| Group / scope / control | Fit / test engines | Fits | Rate [95% CI] | Distance [95% CI] |
|---|---|---|---|---|
| FD001 lstm group raw | 60/100 | 5 | 20.4% [14.2%, 26.6%] | 0.021 [0.0129, 0.0301] |
| FD001 lstm group uniform | 60/100 | 5 | 88.7% [85.9%, 91.2%] | 0.401 [0.378, 0.421] |
| FD001 lstm group one minus p | 60/100 | 5 | 92.0% [87.0%, 96.4%] | 0.806 [0.75, 0.857] |
| FD001 lstm group logit plus 1 | 60/100 | 5 | 20.8% [14.0%, 28.4%] | 0.0468 [0.0289, 0.0676] |
| FD001 lstm group logit minus 1 | 60/100 | 5 | 20.2% [13.8%, 27.2%] | 0.0147 [0.00948, 0.0204] |
| FD001 hybrid group raw | 60/100 | 5 | 13.6% [8.4%, 19.0%] | 0.0138 [0.0079, 0.0206] |
| FD001 hybrid group uniform | 60/100 | 5 | 89.2% [86.4%, 91.7%] | 0.404 [0.382, 0.424] |
| FD001 hybrid group one minus p | 60/100 | 5 | 97.2% [95.4%, 98.8%] | 0.836 [0.789, 0.879] |
| FD001 hybrid group logit plus 1 | 60/100 | 5 | 18.6% [12.4%, 25.2%] | 0.0283 [0.017, 0.0413] |
| FD001 hybrid group logit minus 1 | 60/100 | 5 | 12.0% [7.6%, 16.6%] | 0.0115 [0.0052, 0.0195] |
| FD002 lstm group raw | 156/259 | 5 | 9.6% [6.7%, 12.5%] | 0.00671 [0.00416, 0.00952] |
| FD002 lstm group uniform | 156/259 | 5 | 90.2% [88.5%, 91.6%] | 0.412 [0.399, 0.424] |
| FD002 lstm group one minus p | 156/259 | 5 | 97.3% [95.8%, 98.7%] | 0.865 [0.839, 0.89] |
| FD002 lstm group logit plus 1 | 156/259 | 5 | 15.4% [11.5%, 19.4%] | 0.0182 [0.0122, 0.0246] |
| FD002 lstm group logit minus 1 | 156/259 | 5 | 3.5% [2.2%, 4.9%] | 0.0011 [0.000497, 0.00189] |
| FD002 hybrid group raw | 156/259 | 5 | 8.9% [6.6%, 11.4%] | 0.0072 [0.00431, 0.0104] |
| FD002 hybrid group uniform | 156/259 | 5 | 89.3% [87.7%, 90.7%] | 0.405 [0.392, 0.417] |
| FD002 hybrid group one minus p | 156/259 | 5 | 97.1% [95.8%, 98.3%] | 0.845 [0.818, 0.871] |
| FD002 hybrid group logit plus 1 | 156/259 | 5 | 14.9% [11.6%, 18.3%] | 0.0192 [0.0131, 0.0257] |
| FD002 hybrid group logit minus 1 | 156/259 | 5 | 5.6% [3.9%, 7.2%] | 0.00407 [0.00236, 0.00593] |
| FD003 lstm group raw | 60/100 | 5 | 12.8% [8.2%, 18.0%] | 0.015 [0.00787, 0.0237] |
| FD003 lstm group uniform | 60/100 | 5 | 87.8% [84.8%, 90.5%] | 0.393 [0.367, 0.415] |
| FD003 lstm group one minus p | 60/100 | 5 | 95.8% [92.8%, 98.2%] | 0.823 [0.771, 0.87] |
| FD003 lstm group logit plus 1 | 60/100 | 5 | 22.6% [15.8%, 30.2%] | 0.0304 [0.0184, 0.0443] |
| FD003 lstm group logit minus 1 | 60/100 | 5 | 5.8% [3.2%, 9.0%] | 0.00608 [0.0027, 0.0102] |
| FD003 hybrid group raw | 60/100 | 5 | 11.8% [7.6%, 16.4%] | 0.0149 [0.00814, 0.0223] |
| FD003 hybrid group uniform | 60/100 | 5 | 89.6% [87.4%, 91.7%] | 0.408 [0.389, 0.425] |
| FD003 hybrid group one minus p | 60/100 | 5 | 96.6% [94.4%, 98.4%] | 0.846 [0.801, 0.886] |
| FD003 hybrid group logit plus 1 | 60/100 | 5 | 17.4% [11.6%, 23.6%] | 0.0311 [0.019, 0.0449] |
| FD003 hybrid group logit minus 1 | 60/100 | 5 | 8.2% [5.0%, 11.8%] | 0.00738 [0.00391, 0.0116] |
| FD004 lstm group raw | 149/248 | 5 | 16.6% [13.1%, 20.3%] | 0.0137 [0.00992, 0.018] |
| FD004 lstm group uniform | 149/248 | 5 | 86.7% [84.8%, 88.5%] | 0.385 [0.37, 0.4] |
| FD004 lstm group one minus p | 149/248 | 5 | 95.2% [93.1%, 96.9%] | 0.81 [0.777, 0.841] |
| FD004 lstm group logit plus 1 | 149/248 | 5 | 24.0% [19.4%, 28.9%] | 0.032 [0.0237, 0.041] |
| FD004 lstm group logit minus 1 | 149/248 | 5 | 8.5% [6.0%, 11.1%] | 0.00383 [0.00245, 0.0054] |
| FD004 hybrid group raw | 149/248 | 5 | 12.7% [9.8%, 15.6%] | 0.00857 [0.00502, 0.0134] |
| FD004 hybrid group uniform | 149/248 | 5 | 86.2% [84.4%, 88.1%] | 0.38 [0.365, 0.394] |
| FD004 hybrid group one minus p | 149/248 | 5 | 97.0% [95.3%, 98.4%] | 0.804 [0.772, 0.834] |
| FD004 hybrid group logit plus 1 | 149/248 | 5 | 19.2% [15.5%, 23.1%] | 0.0205 [0.0141, 0.0283] |
| FD004 hybrid group logit minus 1 | 149/248 | 5 | 9.0% [6.9%, 11.3%] | 0.00451 [0.00258, 0.00717] |
| FD001 combined subset combined raw | 60/100 | 10 | 17.0% [11.8%, 22.4%] | 0.0174 [0.011, 0.0244] |
| FD001 combined subset combined uniform | 60/100 | 10 | 88.9% [86.2%, 91.4%] | 0.402 [0.38, 0.422] |
| FD001 combined subset combined one minus p | 60/100 | 10 | 94.6% [91.3%, 97.5%] | 0.821 [0.77, 0.868] |
| FD001 combined subset combined logit plus 1 | 60/100 | 10 | 19.7% [13.3%, 26.8%] | 0.0376 [0.0237, 0.0536] |
| FD001 combined subset combined logit minus 1 | 60/100 | 10 | 16.1% [11.4%, 20.8%] | 0.0131 [0.00833, 0.0187] |
| FD002 combined subset combined raw | 156/259 | 10 | 9.2% [6.9%, 11.8%] | 0.00695 [0.00469, 0.00944] |
| FD002 combined subset combined uniform | 156/259 | 10 | 89.7% [88.2%, 91.1%] | 0.408 [0.396, 0.42] |
| FD002 combined subset combined one minus p | 156/259 | 10 | 97.2% [95.9%, 98.4%] | 0.855 [0.829, 0.88] |
| FD002 combined subset combined logit plus 1 | 156/259 | 10 | 15.1% [11.8%, 18.5%] | 0.0187 [0.0134, 0.0243] |
| FD002 combined subset combined logit minus 1 | 156/259 | 10 | 4.5% [3.3%, 5.8%] | 0.00259 [0.00158, 0.00371] |
| FD003 combined subset combined raw | 60/100 | 10 | 12.3% [8.4%, 16.6%] | 0.015 [0.00894, 0.0219] |
| FD003 combined subset combined uniform | 60/100 | 10 | 88.7% [86.1%, 91.0%] | 0.4 [0.379, 0.419] |
| FD003 combined subset combined one minus p | 60/100 | 10 | 96.2% [93.9%, 98.1%] | 0.834 [0.789, 0.877] |
| FD003 combined subset combined logit plus 1 | 60/100 | 10 | 20.0% [14.1%, 26.4%] | 0.0308 [0.0198, 0.0431] |
| FD003 combined subset combined logit minus 1 | 60/100 | 10 | 7.0% [4.5%, 9.9%] | 0.00673 [0.00363, 0.0103] |
| FD004 combined subset combined raw | 149/248 | 10 | 14.6% [11.8%, 17.8%] | 0.0111 [0.008, 0.0151] |
| FD004 combined subset combined uniform | 149/248 | 10 | 86.5% [84.6%, 88.2%] | 0.383 [0.367, 0.397] |
| FD004 combined subset combined one minus p | 149/248 | 10 | 96.1% [94.4%, 97.5%] | 0.807 [0.775, 0.837] |
| FD004 combined subset combined logit plus 1 | 149/248 | 10 | 21.6% [17.7%, 25.7%] | 0.0262 [0.0197, 0.0336] |
| FD004 combined subset combined logit minus 1 | 149/248 | 10 | 8.8% [6.7%, 10.8%] | 0.00417 [0.0028, 0.00593] |
| FD001-FD004 combined pooled raw | 425/707 | 40 | 12.7% [11.1%, 14.4%] | 0.011 [0.00915, 0.0131] |
| FD001-FD004 combined pooled uniform | 425/707 | 40 | 88.3% [87.3%, 89.3%] | 0.397 [0.389, 0.405] |
| FD001-FD004 combined pooled one minus p | 425/707 | 40 | 96.3% [95.4%, 97.2%] | 0.831 [0.813, 0.847] |
| FD001-FD004 combined pooled logit plus 1 | 425/707 | 40 | 18.7% [16.5%, 21.1%] | 0.0257 [0.0217, 0.0301] |
| FD001-FD004 combined pooled logit minus 1 | 425/707 | 40 | 8.0% [6.9%, 9.2%] | 0.00522 [0.00419, 0.00635] |

## Table S13b. Projection: every test/calibration score and paired difference

Source: `B_projection.csv`. Rate changes are percentage points; other changes retain score units.

| Group / role / metric | Fit / evaluation engines | Raw [CI] | Projected [CI] | Paired difference [CI] |
|---|---|---|---|---|
| FD001 lstm test Brier | 60/100 | 0.0356 [0.0146, 0.0614] | 0.0371 [0.0176, 0.0619] | 0.00149 [-0.00668, 0.00964] |
| FD001 lstm test NLL | 60/100 | 0.123 [0.0614, 0.201] | 0.122 [0.0627, 0.198] | -0.000982 [-0.0193, 0.0177] |
| FD001 lstm test ECE5 | 60/100 | 0.0166 [0.0106, 0.0513] | 0.0153 [0.0108, 0.0501] | -0.00132 [-0.0226, 0.0226] |
| FD001 lstm test ECE10 | 60/100 | 0.038 [0.032, 0.0757] | 0.027 [0.0195, 0.0628] | -0.011 [-0.0344, 0.00546] |
| FD001 lstm test incompatibility rate | 60/100 | 20.4% [14.2%, 26.6%] | 0.0% [0.0%, 0.0%] | -20.4% [-26.6%, -14.2%] |
| FD001 lstm calibration Brier | 60/20 | 0.0425 [0.000184, 0.124] | 0.0408 [9.77e-05, 0.122] | -0.00172 [-0.00443, 0] |
| FD001 lstm calibration NLL | 60/20 | 0.137 [0.00364, 0.386] | 0.128 [0.00248, 0.374] | -0.0087 [-0.022, 0] |
| FD001 lstm calibration ECE5 | 60/20 | 0.0538 [0.00299, 0.151] | 0.047 [0.000601, 0.14] | -0.0068 [-0.0185, 0.000902] |
| FD001 lstm calibration ECE10 | 60/20 | 0.0552 [0.00355, 0.151] | 0.048 [0.00242, 0.141] | -0.00718 [-0.0192, 0.000157] |
| FD001 lstm calibration incompatibility rate | 60/20 | 11.0% [0.0%, 23.0%] | 0.0% [0.0%, 0.0%] | -11.0% [-23.0%, 0.0%] |
| FD001 hybrid test Brier | 60/100 | 0.0348 [0.0131, 0.0625] | 0.0326 [0.0122, 0.0591] | -0.00217 [-0.00689, 0.00197] |
| FD001 hybrid test NLL | 60/100 | 0.121 [0.0484, 0.217] | 0.113 [0.0438, 0.205] | -0.00855 [-0.0231, 0.0037] |
| FD001 hybrid test ECE5 | 60/100 | 0.0161 [0.00992, 0.0505] | 0.0113 [0.00882, 0.0457] | -0.00481 [-0.0146, 0.0112] |
| FD001 hybrid test ECE10 | 60/100 | 0.0394 [0.0282, 0.0767] | 0.029 [0.0214, 0.0637] | -0.0103 [-0.0187, -0.000511] |
| FD001 hybrid test incompatibility rate | 60/100 | 13.6% [8.4%, 19.0%] | 0.0% [0.0%, 0.0%] | -13.6% [-19.0%, -8.4%] |
| FD001 hybrid calibration Brier | 60/20 | 0.0386 [3.44e-05, 0.114] | 0.037 [3.36e-05, 0.111] | -0.00151 [-0.00391, 0] |
| FD001 hybrid calibration NLL | 60/20 | 0.116 [0.00146, 0.332] | 0.11 [0.00145, 0.322] | -0.00625 [-0.0158, 0] |
| FD001 hybrid calibration ECE5 | 60/20 | 0.0511 [0.00144, 0.142] | 0.0458 [0.00137, 0.133] | -0.00529 [-0.0136, 1.62e-05] |
| FD001 hybrid calibration ECE10 | 60/20 | 0.0516 [0.00144, 0.143] | 0.0463 [0.00144, 0.134] | -0.00529 [-0.0136, 1.62e-05] |
| FD001 hybrid calibration incompatibility rate | 60/20 | 6.0% [0.0%, 13.0%] | 0.0% [0.0%, 0.0%] | -6.0% [-13.0%, 0.0%] |
| FD002 lstm test Brier | 156/259 | 0.0251 [0.0124, 0.0402] | 0.0212 [0.0105, 0.0344] | -0.00385 [-0.00698, -0.00112] |
| FD002 lstm test NLL | 156/259 | 0.0816 [0.0425, 0.131] | 0.0709 [0.038, 0.112] | -0.0108 [-0.0199, -0.0033] |
| FD002 lstm test ECE5 | 156/259 | 0.036 [0.0201, 0.0558] | 0.0302 [0.0148, 0.0477] | -0.0058 [-0.00966, -0.00346] |
| FD002 lstm test ECE10 | 156/259 | 0.0364 [0.0226, 0.0563] | 0.0304 [0.0188, 0.0485] | -0.00597 [-0.00891, -0.00271] |
| FD002 lstm test incompatibility rate | 156/259 | 9.6% [6.7%, 12.5%] | 0.0% [0.0%, 0.0%] | -9.6% [-12.5%, -6.7%] |
| FD002 lstm calibration Brier | 156/52 | 0.00839 [0.000767, 0.0196] | 0.00721 [0.000414, 0.0174] | -0.00118 [-0.00242, -0.000209] |
| FD002 lstm calibration NLL | 156/52 | 0.0329 [0.00823, 0.0668] | 0.0291 [0.00683, 0.0607] | -0.00374 [-0.00828, 9.41e-05] |
| FD002 lstm calibration ECE5 | 156/52 | 0.0238 [0.00476, 0.0495] | 0.0191 [0.00524, 0.0444] | -0.0047 [-0.00823, 0.00109] |
| FD002 lstm calibration ECE10 | 156/52 | 0.0267 [0.00779, 0.052] | 0.024 [0.00664, 0.0484] | -0.00273 [-0.00651, 0.000424] |
| FD002 lstm calibration incompatibility rate | 156/52 | 10.8% [4.6%, 18.1%] | 0.0% [0.0%, 0.0%] | -10.8% [-18.1%, -4.6%] |
| FD002 hybrid test Brier | 156/259 | 0.0333 [0.0197, 0.0483] | 0.0283 [0.016, 0.0417] | -0.00504 [-0.00864, -0.00194] |
| FD002 hybrid test NLL | 156/259 | 0.118 [0.0706, 0.173] | 0.0992 [0.0576, 0.15] | -0.019 [-0.033, -0.00723] |
| FD002 hybrid test ECE5 | 156/259 | 0.0477 [0.0302, 0.0682] | 0.0411 [0.025, 0.0603] | -0.00665 [-0.00996, -0.00368] |
| FD002 hybrid test ECE10 | 156/259 | 0.0472 [0.0335, 0.0687] | 0.0419 [0.0297, 0.0622] | -0.00527 [-0.009, -0.00178] |
| FD002 hybrid test incompatibility rate | 156/259 | 8.9% [6.6%, 11.4%] | 0.0% [0.0%, 0.0%] | -8.9% [-11.4%, -6.6%] |
| FD002 hybrid calibration Brier | 156/52 | 0.0236 [0.00635, 0.0435] | 0.0176 [0.00452, 0.0348] | -0.00594 [-0.0142, 0.000826] |
| FD002 hybrid calibration NLL | 156/52 | 0.0795 [0.026, 0.141] | 0.059 [0.0207, 0.108] | -0.0205 [-0.0493, 0.00259] |
| FD002 hybrid calibration ECE5 | 156/52 | 0.0426 [0.0141, 0.0776] | 0.0333 [0.0131, 0.0664] | -0.00928 [-0.0169, 0.000671] |
| FD002 hybrid calibration ECE10 | 156/52 | 0.0474 [0.0187, 0.0819] | 0.0431 [0.0173, 0.0761] | -0.00428 [-0.0125, 0.00321] |
| FD002 hybrid calibration incompatibility rate | 156/52 | 8.5% [3.8%, 13.8%] | 0.0% [0.0%, 0.0%] | -8.5% [-13.8%, -3.8%] |
| FD003 lstm test Brier | 60/100 | 0.0267 [0.00832, 0.0519] | 0.026 [0.0104, 0.0469] | -0.000682 [-0.00803, 0.00643] |
| FD003 lstm test NLL | 60/100 | 0.0935 [0.0361, 0.174] | 0.0879 [0.0402, 0.153] | -0.00563 [-0.0282, 0.0131] |
| FD003 lstm test ECE5 | 60/100 | 0.0299 [0.0143, 0.0612] | 0.0163 [0.0105, 0.0458] | -0.0136 [-0.0194, 0.00167] |
| FD003 lstm test ECE10 | 60/100 | 0.0382 [0.0231, 0.0704] | 0.0261 [0.0197, 0.0543] | -0.0122 [-0.0202, 0.00503] |
| FD003 lstm test incompatibility rate | 60/100 | 12.8% [8.2%, 18.0%] | 0.0% [0.0%, 0.0%] | -12.8% [-18.0%, -8.2%] |
| FD003 lstm calibration Brier | 60/20 | 0.0503 [7.98e-08, 0.139] | 0.0403 [7.98e-08, 0.111] | -0.01 [-0.0284, 0.000173] |
| FD003 lstm calibration NLL | 60/20 | 0.143 [7.74e-05, 0.393] | 0.119 [7.74e-05, 0.324] | -0.0234 [-0.0691, 0.00266] |
| FD003 lstm calibration ECE5 | 60/20 | 0.0666 [7.74e-05, 0.178] | 0.0575 [7.74e-05, 0.154] | -0.00917 [-0.0233, 0.00257] |
| FD003 lstm calibration ECE10 | 60/20 | 0.0671 [7.74e-05, 0.178] | 0.0586 [7.74e-05, 0.155] | -0.00844 [-0.0225, 0.00257] |
| FD003 lstm calibration incompatibility rate | 60/20 | 8.0% [0.0%, 18.0%] | 0.0% [0.0%, 0.0%] | -8.0% [-18.0%, 0.0%] |
| FD003 hybrid test Brier | 60/100 | 0.0291 [0.0118, 0.0515] | 0.0227 [0.0095, 0.0409] | -0.00643 [-0.0129, -0.000557] |
| FD003 hybrid test NLL | 60/100 | 0.0933 [0.0436, 0.159] | 0.0767 [0.0362, 0.132] | -0.0166 [-0.0326, -0.00188] |
| FD003 hybrid test ECE5 | 60/100 | 0.0425 [0.0219, 0.0722] | 0.0284 [0.0181, 0.0543] | -0.0141 [-0.0214, -0.000427] |
| FD003 hybrid test ECE10 | 60/100 | 0.047 [0.0283, 0.0777] | 0.0361 [0.0241, 0.0606] | -0.011 [-0.0205, 0.00123] |
| FD003 hybrid test incompatibility rate | 60/100 | 11.8% [7.6%, 16.4%] | 0.0% [0.0%, 0.0%] | -11.8% [-16.4%, -7.6%] |
| FD003 hybrid calibration Brier | 60/20 | 0.0827 [5.85e-05, 0.208] | 0.066 [5.85e-05, 0.165] | -0.0167 [-0.0438, 0] |
| FD003 hybrid calibration NLL | 60/20 | 0.295 [0.00212, 0.759] | 0.237 [0.00212, 0.607] | -0.0578 [-0.152, 0] |
| FD003 hybrid calibration ECE5 | 60/20 | 0.0895 [0.00209, 0.226] | 0.0777 [0.00209, 0.195] | -0.0118 [-0.0311, 0] |
| FD003 hybrid calibration ECE10 | 60/20 | 0.09 [0.00209, 0.226] | 0.0786 [0.00209, 0.196] | -0.0114 [-0.0307, 0] |
| FD003 hybrid calibration incompatibility rate | 60/20 | 5.0% [0.0%, 14.0%] | 0.0% [0.0%, 0.0%] | -5.0% [-14.0%, 0.0%] |
| FD004 lstm test Brier | 149/248 | 0.0529 [0.0339, 0.0746] | 0.0457 [0.0289, 0.0651] | -0.00721 [-0.0124, -0.00267] |
| FD004 lstm test NLL | 149/248 | 0.173 [0.108, 0.249] | 0.146 [0.0939, 0.207] | -0.0267 [-0.0486, -0.00783] |
| FD004 lstm test ECE5 | 149/248 | 0.0563 [0.0323, 0.0844] | 0.0426 [0.0198, 0.0689] | -0.0137 [-0.0179, -0.00919] |
| FD004 lstm test ECE10 | 149/248 | 0.0593 [0.0405, 0.0886] | 0.0459 [0.0292, 0.073] | -0.0134 [-0.019, -0.00907] |
| FD004 lstm test incompatibility rate | 149/248 | 16.6% [13.1%, 20.3%] | 0.0% [0.0%, 0.0%] | -16.6% [-20.3%, -13.1%] |
| FD004 lstm calibration Brier | 149/50 | 0.0143 [0.00139, 0.033] | 0.00866 [0.00056, 0.0195] | -0.00569 [-0.0135, -0.000315] |
| FD004 lstm calibration NLL | 149/50 | 0.0472 [0.011, 0.0985] | 0.0335 [0.00816, 0.0679] | -0.0137 [-0.0316, -0.000622] |
| FD004 lstm calibration ECE5 | 149/50 | 0.0314 [0.00797, 0.0652] | 0.0218 [0.00483, 0.0481] | -0.00958 [-0.0173, -0.00217] |
| FD004 lstm calibration ECE10 | 149/50 | 0.0337 [0.00995, 0.0666] | 0.0273 [0.00793, 0.0536] | -0.00637 [-0.0145, -2.57e-05] |
| FD004 lstm calibration incompatibility rate | 149/50 | 12.0% [5.2%, 20.0%] | 0.0% [0.0%, 0.0%] | -12.0% [-20.0%, -5.2%] |
| FD004 hybrid test Brier | 149/248 | 0.0448 [0.0279, 0.0642] | 0.0403 [0.0248, 0.0576] | -0.00456 [-0.01, -0.000215] |
| FD004 hybrid test NLL | 149/248 | 0.146 [0.0912, 0.208] | 0.128 [0.0823, 0.179] | -0.0186 [-0.0389, -0.00249] |
| FD004 hybrid test ECE5 | 149/248 | 0.0379 [0.0177, 0.065] | 0.0295 [0.0114, 0.0546] | -0.0084 [-0.0128, -0.00201] |
| FD004 hybrid test ECE10 | 149/248 | 0.0462 [0.0336, 0.0742] | 0.0381 [0.0285, 0.0643] | -0.00802 [-0.0144, -0.00162] |
| FD004 hybrid test incompatibility rate | 149/248 | 12.7% [9.8%, 15.6%] | 0.0% [0.0%, 0.0%] | -12.7% [-15.6%, -9.8%] |
| FD004 hybrid calibration Brier | 149/50 | 0.0191 [0.00198, 0.048] | 0.0145 [0.00179, 0.0329] | -0.0046 [-0.0158, 0.00213] |
| FD004 hybrid calibration NLL | 149/50 | 0.0625 [0.0129, 0.143] | 0.0504 [0.0129, 0.103] | -0.0122 [-0.0408, 0.00517] |
| FD004 hybrid calibration ECE5 | 149/50 | 0.035 [0.00719, 0.0757] | 0.026 [0.00703, 0.0593] | -0.00901 [-0.0186, 0.00119] |
| FD004 hybrid calibration ECE10 | 149/50 | 0.0387 [0.0119, 0.0782] | 0.0318 [0.0111, 0.0644] | -0.00682 [-0.0169, 0.00234] |
| FD004 hybrid calibration incompatibility rate | 149/50 | 10.0% [4.4%, 16.4%] | 0.0% [0.0%, 0.0%] | -10.0% [-16.4%, -4.4%] |
| FD001 combined test Brier | 60/100 | 0.0352 [0.0143, 0.0617] | 0.0348 [0.0151, 0.0603] | -0.000343 [-0.00646, 0.00523] |
| FD001 combined test NLL | 60/100 | 0.122 [0.0557, 0.208] | 0.117 [0.0536, 0.201] | -0.00477 [-0.0204, 0.00936] |
| FD001 combined test ECE5 | 60/100 | 0.0163 [0.0121, 0.0504] | 0.0133 [0.0117, 0.0464] | -0.00307 [-0.0175, 0.0157] |
| FD001 combined test ECE10 | 60/100 | 0.0387 [0.0312, 0.0745] | 0.028 [0.0224, 0.061] | -0.0106 [-0.025, 0.00149] |
| FD001 combined test incompatibility rate | 60/100 | 17.0% [11.8%, 22.4%] | 0.0% [0.0%, 0.0%] | -17.0% [-22.4%, -11.8%] |
| FD001 combined calibration Brier | 60/20 | 0.0405 [0.000109, 0.119] | 0.0389 [7.96e-05, 0.116] | -0.00162 [-0.00406, 0] |
| FD001 combined calibration NLL | 60/20 | 0.127 [0.00255, 0.359] | 0.119 [0.00205, 0.348] | -0.00747 [-0.019, 0] |
| FD001 combined calibration ECE5 | 60/20 | 0.0524 [0.00249, 0.146] | 0.0464 [0.00107, 0.137] | -0.00605 [-0.0164, 0.000459] |
| FD001 combined calibration ECE10 | 60/20 | 0.0534 [0.00249, 0.147] | 0.0472 [0.00201, 0.137] | -0.00623 [-0.0164, 8.65e-05] |
| FD001 combined calibration incompatibility rate | 60/20 | 8.5% [0.0%, 18.0%] | 0.0% [0.0%, 0.0%] | -8.5% [-18.0%, 0.0%] |
| FD002 combined test Brier | 156/259 | 0.0292 [0.0162, 0.044] | 0.0248 [0.0137, 0.0378] | -0.00444 [-0.0072, -0.00199] |
| FD002 combined test NLL | 156/259 | 0.0999 [0.0572, 0.15] | 0.085 [0.049, 0.128] | -0.0149 [-0.024, -0.00663] |
| FD002 combined test ECE5 | 156/259 | 0.0418 [0.0254, 0.0618] | 0.0356 [0.0201, 0.0535] | -0.00622 [-0.00913, -0.00415] |
| FD002 combined test ECE10 | 156/259 | 0.0418 [0.0283, 0.0618] | 0.0362 [0.0245, 0.0549] | -0.00562 [-0.00809, -0.00299] |
| FD002 combined test incompatibility rate | 156/259 | 9.2% [6.9%, 11.8%] | 0.0% [0.0%, 0.0%] | -9.2% [-11.8%, -6.9%] |
| FD002 combined calibration Brier | 156/52 | 0.016 [0.00394, 0.0314] | 0.0124 [0.00244, 0.0261] | -0.00356 [-0.00786, 1.29e-05] |
| FD002 combined calibration NLL | 156/52 | 0.0562 [0.0187, 0.102] | 0.0441 [0.0141, 0.0835] | -0.0121 [-0.0279, 0.000456] |
| FD002 combined calibration ECE5 | 156/52 | 0.0332 [0.00998, 0.0634] | 0.0262 [0.00942, 0.0547] | -0.00699 [-0.012, -0.000139] |
| FD002 combined calibration ECE10 | 156/52 | 0.0371 [0.0136, 0.0666] | 0.0336 [0.0122, 0.0615] | -0.0035 [-0.00917, 0.00148] |
| FD002 combined calibration incompatibility rate | 156/52 | 9.6% [4.4%, 15.6%] | 0.0% [0.0%, 0.0%] | -9.6% [-15.6%, -4.4%] |
| FD003 combined test Brier | 60/100 | 0.0279 [0.0108, 0.0512] | 0.0243 [0.0103, 0.043] | -0.00356 [-0.00974, 0.00238] |
| FD003 combined test NLL | 60/100 | 0.0934 [0.0411, 0.164] | 0.0823 [0.0387, 0.14] | -0.0111 [-0.0287, 0.00455] |
| FD003 combined test ECE5 | 60/100 | 0.0362 [0.0196, 0.0662] | 0.0223 [0.0157, 0.049] | -0.0138 [-0.0193, -0.000698] |
| FD003 combined test ECE10 | 60/100 | 0.0426 [0.0265, 0.0728] | 0.0311 [0.0225, 0.0567] | -0.0116 [-0.0189, 0.00223] |
| FD003 combined test incompatibility rate | 60/100 | 12.3% [8.4%, 16.6%] | 0.0% [0.0%, 0.0%] | -12.3% [-16.6%, -8.4%] |
| FD003 combined calibration Brier | 60/20 | 0.0665 [2.92e-05, 0.174] | 0.0531 [2.92e-05, 0.138] | -0.0134 [-0.0361, 8.65e-05] |
| FD003 combined calibration NLL | 60/20 | 0.219 [0.00108, 0.576] | 0.178 [0.00108, 0.464] | -0.0406 [-0.111, 0.00133] |
| FD003 combined calibration ECE5 | 60/20 | 0.0781 [0.00106, 0.202] | 0.0676 [0.00106, 0.175] | -0.0105 [-0.0272, 0.00129] |
| FD003 combined calibration ECE10 | 60/20 | 0.0785 [0.00106, 0.202] | 0.0686 [0.00106, 0.176] | -0.00991 [-0.0266, 0.00129] |
| FD003 combined calibration incompatibility rate | 60/20 | 6.5% [0.0%, 14.0%] | 0.0% [0.0%, 0.0%] | -6.5% [-14.0%, 0.0%] |
| FD004 combined test Brier | 149/248 | 0.0489 [0.0314, 0.0692] | 0.043 [0.0271, 0.0614] | -0.00588 [-0.0105, -0.00205] |
| FD004 combined test NLL | 149/248 | 0.159 [0.1, 0.227] | 0.137 [0.0891, 0.194] | -0.0226 [-0.0407, -0.00728] |
| FD004 combined test ECE5 | 149/248 | 0.0471 [0.0252, 0.0744] | 0.036 [0.0161, 0.0615] | -0.0111 [-0.0149, -0.00629] |
| FD004 combined test ECE10 | 149/248 | 0.0527 [0.0378, 0.0812] | 0.042 [0.0298, 0.0683] | -0.0107 [-0.0158, -0.0062] |
| FD004 combined test incompatibility rate | 149/248 | 14.6% [11.8%, 17.8%] | 0.0% [0.0%, 0.0%] | -14.6% [-17.8%, -11.8%] |
| FD004 combined calibration Brier | 149/50 | 0.0167 [0.00221, 0.04] | 0.0116 [0.00181, 0.0257] | -0.00514 [-0.0141, 0.000347] |
| FD004 combined calibration NLL | 149/50 | 0.0549 [0.0136, 0.118] | 0.042 [0.0118, 0.0835] | -0.0129 [-0.0351, 0.000975] |
| FD004 combined calibration ECE5 | 149/50 | 0.0332 [0.0081, 0.0688] | 0.0239 [0.00643, 0.0535] | -0.0093 [-0.0173, -0.000832] |
| FD004 combined calibration ECE10 | 149/50 | 0.0362 [0.012, 0.0718] | 0.0296 [0.0102, 0.0583] | -0.00659 [-0.0148, 0.000369] |
| FD004 combined calibration incompatibility rate | 149/50 | 11.0% [5.4%, 17.4%] | 0.0% [0.0%, 0.0%] | -11.0% [-17.4%, -5.4%] |
| FD001-FD004 combined test Brier | 425/707 | 0.0368 [0.0276, 0.0467] | 0.0325 [0.0244, 0.0414] | -0.00424 [-0.00647, -0.00226] |
| FD001-FD004 combined test NLL | 425/707 | 0.123 [0.0917, 0.155] | 0.107 [0.0814, 0.135] | -0.0156 [-0.0236, -0.00874] |
| FD001-FD004 combined test ECE5 | 425/707 | 0.0393 [0.0301, 0.0535] | 0.0307 [0.0237, 0.0444] | -0.00855 [-0.0109, -0.00443] |
| FD001-FD004 combined test ECE10 | 425/707 | 0.0453 [0.0393, 0.0612] | 0.0363 [0.0319, 0.0507] | -0.00896 [-0.0118, -0.00584] |
| FD001-FD004 combined test incompatibility rate | 425/707 | 12.7% [11.1%, 14.4%] | 0.0% [0.0%, 0.0%] | -12.7% [-14.4%, -11.1%] |
| FD001-FD004 combined calibration Brier | 425/142 | 0.0268 [0.0109, 0.0465] | 0.0216 [0.00792, 0.0387] | -0.00522 [-0.00964, -0.00163] |
| FD001-FD004 combined calibration NLL | 425/142 | 0.0886 [0.0387, 0.149] | 0.0728 [0.0304, 0.125] | -0.0158 [-0.0286, -0.00501] |
| FD001-FD004 combined calibration ECE5 | 425/142 | 0.0422 [0.0205, 0.0678] | 0.0341 [0.0159, 0.0578] | -0.00817 [-0.0119, -0.00358] |
| FD001-FD004 combined calibration ECE10 | 425/142 | 0.0449 [0.0238, 0.07] | 0.039 [0.0206, 0.062] | -0.00588 [-0.00992, -0.00192] |
| FD001-FD004 combined calibration incompatibility rate | 425/142 | 9.5% [6.3%, 13.0%] | 0.0% [0.0%, 0.0%] | -9.5% [-13.0%, -6.3%] |

## Table S14. All adjusted effects, relative upper endpoints and approximate MDEs

Source: `C_effect_sizes_power.csv`. Each ratio uses its outcome's observed mean MSE. Pooled estimates are engine-count-weighted averages of group-specific effects; normal/Wald MDEs are approximate.

| Group / outcome | Fit / test engines | Coefficient [CI] | Mean MSE | Upper CI / mean | MDE (MDE / mean) |
|---|---|---|---|---|---|
| FD001 lstm median squared error | 60/100 | 69.7 [-167, 405] | 217 | 187.0% | 429 (198.1%) |
| FD001 lstm Brier | 60/100 | 0.0426 [-0.0369, 0.124] | 0.0356 | 348.9% | 0.115 (324.3%) |
| FD001 hybrid median squared error | 60/100 | -250 [-415, -95.3] | 259 | -36.8% | 227 (87.6%) |
| FD001 hybrid Brier | 60/100 | -0.0143 [-0.0887, 0.055] | 0.0348 | 158.1% | 0.105 (301.0%) |
| FD002 lstm median squared error | 156/259 | -138 [-240, -51] | 205 | -24.8% | 136 (66.3%) |
| FD002 lstm Brier | 156/259 | 0.0908 [0.0332, 0.155] | 0.0251 | 615.7% | 0.0889 (354.4%) |
| FD002 hybrid median squared error | 156/259 | -149 [-311, -4.99] | 241 | -2.1% | 214 (88.7%) |
| FD002 hybrid Brier | 156/259 | 0.103 [0.0365, 0.171] | 0.0333 | 513.2% | 0.0945 (283.6%) |
| FD003 lstm median squared error | 60/100 | -320 [-595, -71] | 323 | -22.0% | 380 (117.6%) |
| FD003 lstm Brier | 60/100 | 0.0822 [0.0155, 0.179] | 0.0267 | 672.7% | 0.12 (450.5%) |
| FD003 hybrid median squared error | 60/100 | -99.9 [-230, 29] | 234 | 12.4% | 186 (79.3%) |
| FD003 hybrid Brier | 60/100 | 0.129 [0.0524, 0.209] | 0.0291 | 716.3% | 0.113 (387.4%) |
| FD004 lstm median squared error | 149/248 | -36.3 [-276, 258] | 275 | 93.8% | 384 (139.6%) |
| FD004 lstm Brier | 149/248 | 0.124 [0.0554, 0.202] | 0.0529 | 382.0% | 0.106 (200.6%) |
| FD004 hybrid median squared error | 149/248 | 90.2 [-147, 429] | 274 | 156.5% | 430 (157.0%) |
| FD004 hybrid Brier | 149/248 | 0.103 [0.0247, 0.187] | 0.0448 | 416.7% | 0.117 (260.6%) |
| FD001 combined median squared error | 60/100 | -90.2 [-271, 118] | 238 | 49.7% | 285 (120.0%) |
| FD001 combined Brier | 60/100 | 0.0141 [-0.0532, 0.0796] | 0.0352 | 226.2% | 0.097 (275.8%) |
| FD002 combined median squared error | 156/259 | -144 [-270, -34.6] | 223 | -15.5% | 167 (74.8%) |
| FD002 combined Brier | 156/259 | 0.0971 [0.0447, 0.148] | 0.0292 | 506.2% | 0.0745 (254.9%) |
| FD003 combined median squared error | 60/100 | -210 [-390, -42.2] | 279 | -15.1% | 254 (91.1%) |
| FD003 combined Brier | 60/100 | 0.106 [0.0437, 0.18] | 0.0279 | 644.3% | 0.0967 (346.6%) |
| FD004 combined median squared error | 149/248 | 27 [-204, 343] | 274 | 125.0% | 401 (146.2%) |
| FD004 combined Brier | 149/248 | 0.113 [0.049, 0.186] | 0.0489 | 381.0% | 0.0965 (197.5%) |
| FD001-FD004 combined median squared error | 425/707 | -85.6 [-191, 37.1] | 251 | 14.8% | 162 (64.4%) |
| FD001-FD004 combined Brier | 425/707 | 0.0922 [0.0589, 0.126] | 0.0368 | 343.7% | 0.0485 (131.9%) |

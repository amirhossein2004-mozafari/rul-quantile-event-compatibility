# Threshold-proximity follow-up

# Step 0 consistency check (existing files only)

Locked rule, verbatim:

> User clarification: require both real outcomes and both synthetic deviations in both families. The same at least six of eight real groups must have positive flag coefficients with 95% engine-bootstrap CIs excluding zero for BOTH median squared error and Brier after the specified RUL adjustment. Synthetic confirmation requires positive adjusted flag AND distance coefficients, with 95% CIs excluding zero, for BOTH squared oracle probability deviation and mean absolute oracle quantile deviation in BOTH families. Family-level effects are the equally weighted mean of the eight temporal subset/architecture coefficients or four covariate subset coefficients, using weighted-raw, final-window, 10,000-engine settings only. Bootstrap draws share engine resamples within each subset across architectures/variants, independently across subsets. Every individual setting is also reported; no choice of favorable settings. Rank-deficient required components fail the rule. If either real or synthetic condition fails, report "not informative" under this rule. No subgroup search or post-result revision.

Numerical addendum, verbatim:

> Before rerunning: preserve the identical regression column space, use the Moore-Penrose solution for redundant nuisance columns, and check target identifiability using the target row of I-A^+A. Return NA only when the target is unidentifiable. SVD relative tolerance 1e-10; target null-space row norm tolerance 1e-6. Report full matrix rank, target identifiability, and condition diagnostics in a separate ledger. Use the same correction for all settings. This changes numerical handling, not outcome definitions, covariates, resampling, cohorts, decision thresholds or hypothesis. The original requirement to report rank-deficient point regressions as NA is retained for genuinely unidentifiable target effects; redundant nuisance parameterizations are disclosed. Both initial nominal-rank-screen outputs and corrected estimable-target results remain available.

| Component | Existing result | Engines |
|---|---|---|
| Real median error positive, CI excludes zero | 0/8 | 100/259/100/248 per subset |
| Real Brier positive, CI excludes zero | 6/8 | Same engines |
| Real both outcomes in same groups | 0/8, requires >=6/8 | 707 unique |
| Temporal synthetic required coefficients | 4/4 pass | 10,000/subset |
| Covariate synthetic required coefficients | 1/4 pass | 10,000/subset |

Level reached: **not informative**. No partially informative level is defined. Earlier verdict agrees; no verdict discrepancy. Both original locks verified.

## New analysis

Protocol SHA256 `85b017765d300244e024aef8259c9c71fc4d552b6e7ef8d430f223812ff2430c`. All predictions were already saved. No training or changes to earlier files.

Question A operational verdict: **explained by or confounded with threshold proximity** (1/8 groups positive with 95% CI excluding zero; requires >=6/8). Adjustment includes cubic raw probability, inclusive RUL 20–40 band, original cubic capped RUL, and seed intercepts. This label does not establish a causal explanation.

| Subset | Model | Fit/test engines | Band/elsewhere engines | Flag effect [95% CI] |
|---|---|---|---|---|
| FD001 | lstm | 60/100 | 15/85 | 0.024220 [-0.027104, 0.076516] |
| FD001 | hybrid | 60/100 | 15/85 | -0.109898 [-0.206340, -0.011177] |
| FD002 | lstm | 156/259 | 22/237 | -0.005648 [-0.048179, 0.040001] |
| FD002 | hybrid | 156/259 | 22/237 | 0.012794 [-0.041699, 0.066119] |
| FD003 | lstm | 60/100 | 10/90 | -0.010498 [-0.073282, 0.052694] |
| FD003 | hybrid | 60/100 | 10/90 | 0.048059 [0.007641, 0.087816] |
| FD004 | lstm | 149/248 | 29/219 | 0.014526 [-0.051866, 0.079561] |
| FD004 | hybrid | 149/248 | 29/219 | 0.054148 [-0.011633, 0.119681] |

Question B: synthetic_band_rates.csv reports all 144 settings, each with both rates and their difference (432 rows). Rates are fractions. Band membership uses realized capped RUL, never oracle median. Evaluation counts and engine/run counts accompany every row; state counts do not add independent engines. Empty-band/draw estimates remain NA. Bootstrap intervals condition on saved fits; 2,000 engine draws preserve all states per engine. FD003 covariate states shared with FD001 are identified. All unfavorable results are retained.

Independent human review is still missing. AI identifiers and command/source provenance are archived alongside this report. No new overall diagnostic-informativeness verdict replaces Step 0.

## Synthetic weighted-raw final-window results (large fleets)

All matching settings are shown below; the complete 144-setting table is synthetic_band_rates_wide.csv. Rates and differences below are percentages and percentage points; CSV values are fractions.

| Subset | Architecture | Fitting engines | Band/elsewhere engines | Band rate | Elsewhere rate | Difference [95% CI] |
|---|---|---|---|---|---|---|
| FD001 | lstm | 60 | 2062/7938 | 67.76% | 67.48% | +0.29 [+0.21, +0.37] |
| FD001 | hybrid | 60 | 2062/7938 | 62.22% | 66.55% | -4.33 [-5.13, -3.52] |
| FD001 | covariate | 60 | 2062/7938 | 40.92% | 32.38% | +8.54 [+6.98, +10.05] |
| FD002 | lstm | 156 | 2052/7948 | 32.29% | 25.34% | +6.96 [+5.77, +8.14] |
| FD002 | hybrid | 156 | 2052/7948 | 42.76% | 45.57% | -2.81 [-3.39, -2.23] |
| FD002 | covariate | 156 | 2052/7948 | 14.82% | 11.53% | +3.29 [+2.75, +3.85] |
| FD003 | lstm | 60 | 1998/8002 | 46.30% | 42.04% | +4.26 [+3.54, +4.99] |
| FD003 | hybrid | 60 | 1998/8002 | 48.16% | 46.83% | +1.33 [+0.92, +1.75] |
| FD003 | covariate | 60 | 1998/8002 | 44.28% | 35.29% | +8.99 [+7.35, +10.54] |
| FD004 | lstm | 149 | 1940/8060 | 34.83% | 28.10% | +6.73 [+5.49, +8.01] |
| FD004 | hybrid | 149 | 1940/8060 | 45.03% | 44.68% | +0.34 [+0.14, +0.53] |
| FD004 | covariate | 149 | 1940/8060 | 16.02% | 14.07% | +1.95 [+1.30, +2.57] |

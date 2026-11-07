# Compatibility follow-up report

Report date: 2026-11-01 (Asia/Tehran).

Follow-up protocol SHA256: `145fcf5a3ec9e4c2c0a9658c9f4bbd1fe33ac61dd4a57afd9674deb2af1d157e`. Parent protocol: `434ee931df6455e2af6273d3ec9590ad19cdd6755cb3e74b39f6cc4fe3a27764` (archived as protocol_v1_locked.md).

## Definition, roles and completeness

Collapse is median raw q50-q05 <1.25 cycles (1% of cap 125). Synthetic labels use the 10,000-engine uniform-endpoint audit fleet; final-window evaluation uses a different fleet. Real labels use fixed calibration endpoints only. All original real group means retain all five seeds and all official-test engines. No official-test outcome selected a fit, threshold, model or hyperparameter.

Original temporal fits: 30 per architecture/subset/objective. Covariate/parametric controls: 200 per setting. Every original result remains in the three-way tables. Original fitting sizes FD00160, FD002156, FD00360, FD004149; evaluation fleets100/259/100/248 and10,000 engines.

New training executions: 120 fixed-initialization fits, 84 non-baseline factorial ablations, 6 instrumented default replays, and 10 real unweighted refits. Failed executions: 0. Six fixed-init factorial cells reuse their identical validation-cohort states, and the 6 default replays are duplicate computations, not new independent samples.

CSV rates/proportions are fractions; rate differences are also fractions. Prose reports percentages/percentage points. Mean distances are in probability units and quantile errors in cycles.

All confidence intervals are 95% engine-resampling intervals, conditional on fitted models and fixed classification labels. Models/seeds are averaged within engine and are never resampled as independent engines. Training-fleet rate spread is reported separately. Uniform evaluation reuses audit features, so it is a conditional sensitivity; final evaluation uses independent engine features.

## Real collapse fraction

0/40 frozen real states are collapsed on 142 calibration engines across the four subsets. Calibration-engine-bootstrap interval for the descriptive fraction: [0.00%, 0.00%]. This does not assert absence of collapse at every possible input. Per-fit/group engine counts and median-gap intervals are in real_collapse_labels.csv and real_collapse_fractions.csv.

## All / non-collapsed / collapsed null comparison

Each family has its own comparison table: comparison_temporal.csv, comparison_covariate.csv, comparison_parametric.csv. Each contains the actual real means, null rates/distances/CIs, retained fit counts,97.5th-percentile thresholds and statuses. Empty strata are NA; selected counts<20 are SPARSE_STRATUM, and one-fit tails are SINGLE_FIT.

- temporal, all: 0/8 defined real groups exceed the empirical null 97.5th percentile; 0 undefined groups; 0 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- temporal, noncollapsed: 0/8 defined real groups exceed the empirical null 97.5th percentile; 0 undefined groups; 4 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- temporal, collapsed: 0/6 defined real groups exceed the empirical null 97.5th percentile; 2 undefined groups; 4 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- covariate, all: 0/8 defined real groups exceed the empirical null 97.5th percentile; 0 undefined groups; 0 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- covariate, noncollapsed: 0/8 defined real groups exceed the empirical null 97.5th percentile; 0 undefined groups; 0 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- covariate, collapsed: 0/0 defined real groups exceed the empirical null 97.5th percentile; 8 undefined groups; 0 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- parametric, all: 0/8 defined real groups exceed the empirical null 97.5th percentile; 0 undefined groups; 0 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- parametric, noncollapsed: 0/8 defined real groups exceed the empirical null 97.5th percentile; 0 undefined groups; 0 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.
- parametric, collapsed: 0/0 defined real groups exceed the empirical null 97.5th percentile; 8 undefined groups; 0 sparse/single-fit groups. Fitting engines 60/156/60/149; null evaluation 10,000; real evaluation 100/259/100/248.

The comparison is descriptive. Real means average five initializations on one fitting fleet, while null replication rates use independent fitting fleets and one initialization. Conditioning on gap quality changes the reference distribution; it is not an unconditional finite-sample null or a new p-value. Source roles, epoch-vs-update-budget differences, known-law specificity and distinct control information budgets remain limitations.

## Fixed initialization intervention

The original model modules and paper states remain unchanged. Only the new experimental initialization sets final lower/upper gap-head weights to zero and biases to inverse_softplus(20/80). The model parameter count, forward function, default loss, LR, epochs, optimizer and clipping remain identical in this validation cohort. No gap floor is used.

- lstm, weighted: 0/30 collapsed, 0 failed; literal removal=True; mean oracle quantile-MAE change -14.512 cycles (95% engine CI [-14.536, -14.488]); passes pre-specified gap/quality safeguard=True. Fitting 60 engines; classification/evaluation10,000 each.
- lstm, unweighted: 0/30 collapsed, 0 failed; literal removal=True; mean oracle quantile-MAE change -14.608 cycles (95% engine CI [-14.632, -14.584]); passes pre-specified gap/quality safeguard=True. Fitting 60 engines; classification/evaluation10,000 each.
- hybrid, weighted: 0/30 collapsed, 0 failed; literal removal=True; mean oracle quantile-MAE change -12.627 cycles (95% engine CI [-12.664, -12.588]); passes pre-specified gap/quality safeguard=True. Fitting 60 engines; classification/evaluation10,000 each.
- hybrid, unweighted: 0/30 collapsed, 0 failed; literal removal=True; mean oracle quantile-MAE change -12.698 cycles (95% engine CI [-12.750, -12.645]); passes pre-specified gap/quality safeguard=True. Fitting 60 engines; classification/evaluation10,000 each.
- Fixed-init lstm weighted_raw: null mean rate 39.95%, null 97.5th percentile 100.00%, real raw mean 20.40%, exceeds=False. Fitting 60 engines; null evaluation 10,000; real evaluation 100. Corrected/unweighted-to-real-raw comparisons have different probability conventions.
- Fixed-init lstm weighted_corrected: null mean rate 64.00%, null 97.5th percentile 100.00%, real raw mean 20.40%, exceeds=False. Fitting 60 engines; null evaluation 10,000; real evaluation 100. Corrected/unweighted-to-real-raw comparisons have different probability conventions.
- Fixed-init lstm unweighted: null mean rate 61.52%, null 97.5th percentile 100.00%, real raw mean 20.40%, exceeds=False. Fitting 60 engines; null evaluation 10,000; real evaluation 100. Corrected/unweighted-to-real-raw comparisons have different probability conventions.
- Fixed-init hybrid weighted_raw: null mean rate 38.25%, null 97.5th percentile 97.27%, real raw mean 13.60%, exceeds=False. Fitting 60 engines; null evaluation 10,000; real evaluation 100. Corrected/unweighted-to-real-raw comparisons have different probability conventions.
- Fixed-init hybrid weighted_corrected: null mean rate 37.02%, null 97.5th percentile 59.37%, real raw mean 13.60%, exceeds=False. Fitting 60 engines; null evaluation 10,000; real evaluation 100. Corrected/unweighted-to-real-raw comparisons have different probability conventions.
- Fixed-init hybrid unweighted: null mean rate 34.54%, null 97.5th percentile 66.54%, real raw mean 13.60%, exceeds=False. Fitting 60 engines; null evaluation 10,000; real evaluation 100. Corrected/unweighted-to-real-raw comparisons have different probability conventions.

Gap removal does not remove incompatibility. The fixed-init rates remain substantial despite improved mean oracle quantile error; this intervention is not evidence of calibrated probabilities or a complete explanation of the diagnostic rate. All fixed_init_vs_real.csv comparisons remain reported.

This validates the fixed initialization only for the tested FD001-shaped synthetic setting. It does not prove universal removal, calibrated probabilities, or a need to modify the frozen real models. Per-quantile tradeoffs remain in fix_per_quantile_quality.csv. All fixed-init rates, distances and strata appear in fixed_init_summary.csv.

## Cause investigation

The complete 2x2x2x2 factorial uses default/fixed initialization, raw/125-normalized pinball loss, inherited/tripled LR, and clipping1/disabled; both architectures, three paired fitting fleets per cell (60 engines each). No best cell is selected. factorial_all_runs.csv retains all 96 state/configuration results and their rate/distance engine CIs; factorial_cell_summary.csv retains all 32 cells. All15 main/interaction contrasts per architecture and metric, including every paired replication, are retained in factorial_all_interactions.csv.

The following main-effect collapse contrasts are high-level minus low-level, averaged over the other factors and the three paired fitting fleets. They are descriptive fitted-state contrasts, not independent-model significance tests.

- lstm, clipping_disabled: mean collapse contrast +0.000; range across 3 paired fleets [+0.000, +0.000]. Fitting 60 engines; classification 10,000 engines.
- lstm, initialization: mean collapse contrast -0.500; range across 3 paired fleets [-1.000, +0.000]. Fitting 60 engines; classification 10,000 engines.
- lstm, lr_tripled: mean collapse contrast -0.083; range across 3 paired fleets [-0.250, +0.000]. Fitting 60 engines; classification 10,000 engines.
- lstm, pinball_normalized: mean collapse contrast +0.000; range across 3 paired fleets [+0.000, +0.000]. Fitting 60 engines; classification 10,000 engines.
- hybrid, clipping_disabled: mean collapse contrast -0.042; range across 3 paired fleets [-0.125, +0.000]. Fitting 60 engines; classification 10,000 engines.
- hybrid, initialization: mean collapse contrast -0.875; range across 3 paired fleets [-1.000, -0.625]. Fitting 60 engines; classification 10,000 engines.
- hybrid, lr_tripled: mean collapse contrast -0.042; range across 3 paired fleets [-0.125, +0.000]. Fitting 60 engines; classification 10,000 engines.
- hybrid, pinball_normalized: mean collapse contrast +0.042; range across 3 paired fleets [+0.000, +0.125]. Fitting 60 engines; classification 10,000 engines.

Loss/gradient/clipping histories and initial/final Softplus derivatives are retained. The measured initialization intervention can be assessed separately from the loss-scale/LR/clipping effects; interactions prevent assigning a unique general cause from three fleets. No structural model edit or outcomes-driven fallback fix was performed.

## Real weighting attribution

real_variant_summary.csv provides raw, fixed-weight-corrected and retrained-unweighted rates/distances with engine CIs. real_weighting_attribution.csv provides all paired net reductions, resolved and introduced violations, distance changes, and proportional reductions, including negative values. Correction holds q/r fixed and shifts only the logit. Unweighted retraining changes both learned tasks and is a different intervention; the effects must not be added.

- FD001 lstm, weighted_raw_minus_fixed_weight_correction: 20.40% -> 18.00%; net reduction +2.40 percentage points (95% engine CI [-4.40, +9.80]); net proportional reduction +11.76%. Fitting 60 engines; test 100 engines, five paired seeds.
- FD001 lstm, weighted_raw_minus_unweighted_retrain: 20.40% -> 18.80%; net reduction +1.60 percentage points (95% engine CI [-5.20, +9.00]); net proportional reduction +7.84%. Fitting 60 engines; test 100 engines, five paired seeds.
- FD001 hybrid, weighted_raw_minus_fixed_weight_correction: 13.60% -> 12.20%; net reduction +1.40 percentage points (95% engine CI [-2.80, +6.00]); net proportional reduction +10.29%. Fitting 60 engines; test 100 engines, five paired seeds.
- FD001 hybrid, weighted_raw_minus_unweighted_retrain: 13.60% -> 21.60%; net reduction -8.00 percentage points (95% engine CI [-14.20, -2.40]); net proportional reduction -58.82%. Fitting 60 engines; test 100 engines, five paired seeds.
- FD002 lstm, weighted_raw_minus_fixed_weight_correction: 9.58% -> 3.47%; net reduction +6.10 percentage points (95% engine CI [+3.47, +8.88]); net proportional reduction +63.71%. Fitting 156 engines; test 259 engines, five paired seeds.
- FD002 hybrid, weighted_raw_minus_fixed_weight_correction: 8.88% -> 6.64%; net reduction +2.24 percentage points (95% engine CI [-0.15, +4.79]); net proportional reduction +25.22%. Fitting 156 engines; test 259 engines, five paired seeds.
- FD003 lstm, weighted_raw_minus_fixed_weight_correction: 12.80% -> 7.00%; net reduction +5.80 percentage points (95% engine CI [+1.00, +10.40]); net proportional reduction +45.31%. Fitting 60 engines; test 100 engines, five paired seeds.
- FD003 hybrid, weighted_raw_minus_fixed_weight_correction: 11.80% -> 8.60%; net reduction +3.20 percentage points (95% engine CI [-0.20, +7.00]); net proportional reduction +27.12%. Fitting 60 engines; test 100 engines, five paired seeds.
- FD004 lstm, weighted_raw_minus_fixed_weight_correction: 16.61% -> 5.89%; net reduction +10.73 percentage points (95% engine CI [+7.58, +13.95]); net proportional reduction +64.56%. Fitting 149 engines; test 248 engines, five paired seeds.
- FD004 hybrid, weighted_raw_minus_fixed_weight_correction: 12.66% -> 13.23%; net reduction -0.56 percentage points (95% engine CI [-4.20, +2.74]); net proportional reduction -4.46%. Fitting 149 engines; test 248 engines, five paired seeds.

The term explained is limited to the measured operational contrast. A smaller incompatibility rate does not establish probability calibration, and a point net reduction with an interval crossing zero does not establish a stable reduction. Negative changes and cases where mean distance worsens remain reported. FD001 retraining results do not establish effects on the other subsets or N-CMAPSS.

## Files and provenance

- null_stratified_summary.csv / null_per_replication.csv / null_collapse_labels.csv: every original setting, all three strata and both sampling/fleet-size sensitivities.
- real_vs_null_strata.csv: all variants and all comparison statuses; the three family tables show the weighted-raw large-final comparison.
- fix_success_checks.csv / fixed_init_summary.csv / fixed_init_per_replication.csv / fix_per_quantile_quality.csv: complete initialization validation.
- factorial_all_runs.csv / factorial_cell_summary.csv / factorial_all_interactions.csv / factorial_contrast_summary.csv: all diagnostic cells and interactions.
- checkpoint_derivative_diagnostics.csv: all 210 initial/final deterministic training-window probes, with actual probe-engine counts.
- real_collapse_labels.csv / real_collapse_fractions.csv / real_unweighted_collapse_labels.csv: calibration-only collapse labels.
- real_variant_summary.csv / real_weighting_attribution.csv / real_probability_variant_per_seed.csv: all real probability variants and paired attribution.

The original protocol and results remain archived. This addendum was hashed before new classifications/fits, with previous findings already known. Numerical data come from executed code; AI configured-model/build identifiers are recorded in ai_provenance.json and app_build.json. Exact served checkpoints remain unexposed. External independent review remains REVIEW_UNAVAILABLE.
# Frozen-model incompatibility association analysis

Verdict under the locked joint rule: **not informative**. 0/8 real groups pass both RUL-adjusted outcomes; synthetic joint confirmation=False.

Protocol SHA256 `da781da5c725624ab53503d65cff89037e5ce15f0769a23b27e6d6a04eeb4540`. All results use 2,000 engine-cluster bootstrap draws, preserving fixed states/seeds. Real evaluation: 707 unique engines across subsets; each architecture uses the same engines. Synthetic: 10,000 unique engines per subset/policy, reused across states; small fleets are prefixes. Engine-group counts overlap when a fixed engine changes flag across states.

The temporal experiment includes approximation and optimization effects. Conditional bootstrap intervals exclude fitting uncertainty. Brier is determined by probability and event label; probability-adjusted residual associations depend on the fixed cubic regression specification and are not held-out predictive gains. No models were trained or selected.

Tables: real_associations.csv (all effects, means, intervals and counts), real_engine_run.csv, real_RUL_bins.csv (all bins including empty), real_per_seed.csv, synthetic_associations.csv, synthetic_per_fit.csv, synthetic_family_confirmation.csv, real_decision_components.csv. Undefined/singular results are NA/NaN with undefined-draw counts, never silently removed from decision components.

## Documented numerical correction

The initial full-matrix rank screen returned undefined synthetic final-window regressions because the oracle has only two distinct probability/quantile pairs. Cubic nuisance columns are redundant. Initial partial outputs are preserved under initial_rank_screen. A separately hashed numerical_addendum.md was written before the corrected run, which uses an SVD generalized inverse and explicitly checks target identifiability. This retains the specified adjustment column space. Rank-deficient nuisance coefficients are not individually interpreted. Truly unidentifiable target coefficients remain NA. The initial run was interrupted and the full cohort was rerun; no fits were removed. All corrected point target coefficients were checked against direct least squares with the matching SVD cutoff. regression_rank_diagnostics.csv records point ranks, target identifiability and undefined bootstrap counts.

## Real adjusted associations

- FD001 lstm, median_squared_error_adjusted_flag: 69.736 [-167.07, 405.43]. Engines: fitting 60, evaluation 100, ever incompatible 35, ever compatible 93 (overlap allowed).
- FD001 lstm, Brier_adjusted_flag: 0.042556 [-0.036852, 0.12424]. Engines: fitting 60, evaluation 100, ever incompatible 35, ever compatible 93 (overlap allowed).
- FD001 hybrid, median_squared_error_adjusted_flag: -250.16 [-414.68, -95.299]. Engines: fitting 60, evaluation 100, ever incompatible 25, ever compatible 98 (overlap allowed).
- FD001 hybrid, Brier_adjusted_flag: -0.014288 [-0.088711, 0.054969]. Engines: fitting 60, evaluation 100, ever incompatible 25, ever compatible 98 (overlap allowed).
- FD002 lstm, median_squared_error_adjusted_flag: -138.46 [-239.59, -50.981]. Engines: fitting 156, evaluation 259, ever incompatible 46, ever compatible 255 (overlap allowed).
- FD002 lstm, Brier_adjusted_flag: 0.090814 [0.033178, 0.15454]. Engines: fitting 156, evaluation 259, ever incompatible 46, ever compatible 255 (overlap allowed).
- FD002 hybrid, median_squared_error_adjusted_flag: -148.61 [-310.98, -4.9893]. Engines: fitting 156, evaluation 259, ever incompatible 49, ever compatible 256 (overlap allowed).
- FD002 hybrid, Brier_adjusted_flag: 0.10338 [0.036485, 0.17104]. Engines: fitting 156, evaluation 259, ever incompatible 49, ever compatible 256 (overlap allowed).
- FD003 lstm, median_squared_error_adjusted_flag: -320.08 [-595.39, -70.972]. Engines: fitting 60, evaluation 100, ever incompatible 26, ever compatible 97 (overlap allowed).
- FD003 lstm, Brier_adjusted_flag: 0.082161 [0.015468, 0.17933]. Engines: fitting 60, evaluation 100, ever incompatible 26, ever compatible 97 (overlap allowed).
- FD003 hybrid, median_squared_error_adjusted_flag: -99.936 [-229.56, 28.99]. Engines: fitting 60, evaluation 100, ever incompatible 28, ever compatible 99 (overlap allowed).
- FD003 hybrid, Brier_adjusted_flag: 0.12925 [0.052428, 0.20879]. Engines: fitting 60, evaluation 100, ever incompatible 28, ever compatible 99 (overlap allowed).
- FD004 lstm, median_squared_error_adjusted_flag: -36.251 [-275.98, 257.85]. Engines: fitting 149, evaluation 248, ever incompatible 69, ever compatible 236 (overlap allowed).
- FD004 lstm, Brier_adjusted_flag: 0.12385 [0.055356, 0.20209]. Engines: fitting 149, evaluation 248, ever incompatible 69, ever compatible 236 (overlap allowed).
- FD004 hybrid, median_squared_error_adjusted_flag: 90.213 [-146.55, 428.51]. Engines: fitting 149, evaluation 248, ever incompatible 72, ever compatible 245 (overlap allowed).
- FD004 hybrid, Brier_adjusted_flag: 0.10253 [0.024725, 0.18687]. Engines: fitting 149, evaluation 248, ever incompatible 72, ever compatible 245 (overlap allowed).

## Synthetic joint components

- temporal, oracle_probability_squared_deviation, flag: 0.0050127 [0.0049235, 0.0051078], pass=True. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.
- temporal, oracle_probability_squared_deviation, distance_per_0.1: 0.0014134 [0.0013756, 0.0014506], pass=True. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.
- temporal, oracle_quantile_MAE, flag: 1.2145 [1.1927, 1.2374], pass=True. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.
- temporal, oracle_quantile_MAE, distance_per_0.1: 0.42805 [0.4197, 0.43682], pass=True. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.
- covariate, oracle_probability_squared_deviation, flag: -0.0012427 [-0.0015092, -0.00095215], pass=False. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.
- covariate, oracle_probability_squared_deviation, distance_per_0.1: 0.00092283 [0.00081099, 0.0010396], pass=True. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.
- covariate, oracle_quantile_MAE, flag: -1.8873 [-1.9135, -1.8612], pass=False. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.
- covariate, oracle_quantile_MAE, distance_per_0.1: -0.65512 [-0.67048, -0.63993], pass=False. Evaluation 10,000 engines/subset (40,000 unique/family); fitting 60/156/60/149.

## Near-threshold and incremental probability adjustment

- FD001 lstm: near-band rate 50.67% (n=15), elsewhere 15.06% (n=85); Brier distance coefficient beyond raw probability -0.00077278 [-0.039408, 0.039837], evaluation n=100, fitting n=60. All rate/distance CIs and incremental R² are in real_associations.csv.
- FD001 hybrid: near-band rate 53.33% (n=15), elsewhere 6.59% (n=85); Brier distance coefficient beyond raw probability -0.021509 [-0.077222, 0.03305], evaluation n=100, fitting n=60. All rate/distance CIs and incremental R² are in real_associations.csv.
- FD002 lstm: near-band rate 54.55% (n=22), elsewhere 5.40% (n=237); Brier distance coefficient beyond raw probability 0.019862 [-0.023289, 0.072382], evaluation n=259, fitting n=156. All rate/distance CIs and incremental R² are in real_associations.csv.
- FD002 hybrid: near-band rate 41.82% (n=22), elsewhere 5.82% (n=237); Brier distance coefficient beyond raw probability 0.05958 [0.010367, 0.10568], evaluation n=259, fitting n=156. All rate/distance CIs and incremental R² are in real_associations.csv.
- FD003 lstm: near-band rate 62.00% (n=10), elsewhere 7.33% (n=90); Brier distance coefficient beyond raw probability -0.0025165 [-0.040783, 0.050021], evaluation n=100, fitting n=60. All rate/distance CIs and incremental R² are in real_associations.csv.
- FD003 hybrid: near-band rate 52.00% (n=10), elsewhere 7.33% (n=90); Brier distance coefficient beyond raw probability 0.014989 [-0.017875, 0.050352], evaluation n=100, fitting n=60. All rate/distance CIs and incremental R² are in real_associations.csv.
- FD004 lstm: near-band rate 62.76% (n=29), elsewhere 10.50% (n=219); Brier distance coefficient beyond raw probability 0.038514 [-0.0071406, 0.089237], evaluation n=248, fitting n=149. All rate/distance CIs and incremental R² are in real_associations.csv.
- FD004 hybrid: near-band rate 31.72% (n=29), elsewhere 10.14% (n=219); Brier distance coefficient beyond raw probability 0.039935 [-0.032784, 0.12123], evaluation n=248, fitting n=149. All rate/distance CIs and incremental R² are in real_associations.csv.

The criterion fails if either branch fails, even when selected individual associations are positive. Negative median-error associations are retained. This verdict does not establish universal uselessness. No N-CMAPSS association experiment was requested or executed here. External independent review: REVIEW_UNAVAILABLE.

Compact tables: real_primary_table.csv, near_threshold_table.csv, incremental_Brier_table.csv. Per-fit/seed group differences are descriptive; cohort effects and their uncertainty are in the association tables. The scientific figure real_adjusted_associations.pdf/png shows every real primary coefficient.

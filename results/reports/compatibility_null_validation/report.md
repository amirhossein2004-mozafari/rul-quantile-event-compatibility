# Compatibility null validation

Protocol SHA-256: `434ee931df6455e2af6273d3ec9590ad19cdd6755cb3e74b39f6cc4fe3a27764`.

All eight frozen Table2 raw means and sample SDs reproduced. Strict d>0 and d>1e-6 agreed for those predictions.

## Complete result tables

- results_table.csv: requested setting, fitting/evaluation engine counts, rate, distance and 95% engine-bootstrap CIs. Rates are fractions, distances are in probability units.
- synthetic_summary.csv: cohort means and conditional CIs, plus training-replication ranges/percentiles and oracle-error diagnostics.
- synthetic_per_replication.csv: every replication and its engine-bootstrap CIs.
- real_vs_synthetic.csv: every prespecified groupwise comparison.
- synthetic_oracle_noise.csv: oracle sanity checks and all noisy-quantile levels.
- auxiliary_cuda_results.csv and auxiliary_cuda_inventory.json: every auxiliary CUDA result and the interrupted state.

## Counts and uncertainty

Temporal: 30 independent fitting fleets per 8 configurations, two separately trained objectives (480 fits). Covariate: 200 per 3 fitting sizes/objectives (1200 CPU fits). Parametric: 200 fitting fleets per 3 sizes / 2 endpoint policies (1200 fitted control configurations; each has independently estimated quantile and event functions).

Fitting engines: FD001 60, FD002 156, FD003 60, FD004 149. Evaluation engines: small 100/259/100/248; large 10,000 per subset/policy. Each small fleet is a prefix of its large fleet. Evaluation engine IDs recur across fits and variants; model/seed counts never multiply the engine count.

The 95% percentile engine-bootstrap CIs condition on the complete fitted cohort. They do not include fitting uncertainty. The separately reported replication spread varies independent fitting fleets and is not a bootstrap over seeds.

## Investigation of extreme temporal rates

Across all 480 temporal fits, 144 fitted states had q50-q05 below 0.001 cycles on more than 99% of their 10,000 evaluation engines. Fitting counts were 60/156/60/149 engines for FD001-FD004. This is a descriptive count of fitted states, without a model-level independence assumption.

Some extreme rates coincide with inaccurate lower quantiles, sometimes almost equal to the median. All original fits remain in the tables. The fixed post-hoc probes used FD001 replication 0, 60 fitting engines and all 4,209 fitting windows per model; gradients were measured without an optimizer step.

- lstm, weighted=True, fitting engines 60: mean softplus derivative 0.06708; lower-head gradient norm 0.3801; median-head norm 7.948.
- lstm, weighted=False, fitting engines 60: mean softplus derivative 0.0003285; lower-head gradient norm 0.002725; median-head norm 8.175.
- hybrid, weighted=True, fitting engines 60: mean softplus derivative 1.521e-10; lower-head gradient norm 4.928e-09; median-head norm 1.231.
- hybrid, weighted=False, fitting engines 60: mean softplus derivative 1.712e-09; lower-head gradient norm 3.267e-08; median-head norm 0.7201.

The two hybrid probes demonstrate lower-offset saturation at those checkpoints. The LSTM probes differ, so a single explanation for every extreme fit is not established. No longer-budget convergence-control refit was run. These results cannot be attributed purely to estimation noise; the no-exceedance counts describe the locked pipelines and controls, and do not establish that estimation noise explains the real-data incompatibility. See temporal_extreme_rate_investigation.csv, temporal_lower_gap_all_fits.csv, lower_head_gradient_probes.csv and investigation_protocol.md.

## Groupwise exceedance of the locked synthetic benchmark

The locked descriptive criterion compares each reproduced real point estimate with the 97.5th percentile of independent fitting-replication rates on the 10,000-engine final-window synthetic fleet. This is not a universal null test or a significance statement.

- temporal, weighted_raw: 0/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- temporal, weighted_corrected: 0/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- temporal, unweighted: 0/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- covariate, weighted_raw: 0/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- covariate, weighted_corrected: 0/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- covariate, unweighted: 0/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- parametric, weighted_raw: 0/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- parametric, weighted_corrected: 8/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.
- parametric, unweighted: 8/8 real subset/architecture results exceed the specified synthetic benchmark. See every group and engine count in real_vs_synthetic.csv.

Only weighted_raw null comparisons share the raw Table2 event-output convention. Corrected and unweighted comparisons against the raw real rate are descriptive cross-variant contrasts, not matched real-data tests. Neural epoch/LR/batch schedules match the inherited budget; synthetic lifetime lengths produce different window and optimizer-step counts, which are retained in training_integrity_checks.csv.

The counts describe the prespecified synthetic settings; they do not establish a universal finite-sample null for C-MAPSS.

The real Table2 statistic averages five initializations on one fitting fleet. Each synthetic replication has a fresh fitting fleet with one initialization per objective. The upper-tail comparison is therefore a descriptive benchmark, not a matched five-initialization null test.

## Scope and numerical findings

Temporal and covariate neural experiments are known-law training-pipeline nulls including approximation, optimization, weighting and endpoint-sampling effects. They are not pure estimation-noise measurements. Parametric functions include the known conditional law, but their endpoint-only fitting data have a different information budget from the neural full-window fitting data; the differences do not isolate a causal approximation-error component.

Weibull shape 1 is the exponential special case. Final-window ages reproduce empirical input-file truncation-length marginals; NASA's latent censoring mechanism is not identified. Uniform complete-lifetime endpoints have a different analytic conditional law (E1 exponential integral). Oracle quantiles are computed analytically or by deterministic inversion, never from a trained model.

Final-policy saturated parametric quantile and event functions are independently fitted loss minimizers on the same data. Their exact solutions are compatible despite finite-sample error. Exact integer arithmetic verified this; one floating-point strict violation has maximum distance 5.551115123125783e-17. Strict results remain in tables alongside the 1e-6 sensitivity; this numerical artifact is not estimation noise.

True-quantile/true-probability sanity checks have zero incompatibility and zero distance for every fleet/policy. This is an implementation identity, not evidence of predictive calibration.

Training integrity checks verify budgets, units, class weights, source identities and parameter counts. Selected saved full-fleet forwards were independently replayed on CPU. Convergence histories and oracle errors remain reported; fixed budgets were not extended after inspecting outcomes.

The covariate compute-only CPU amendment was based on random-input timing. The 11 completed auxiliary CUDA fits and interrupted state are retained separately; no performance criterion selected the CPU cohort.

## AI provenance and review

Configured assistant model: gpt-6.1-sol, medium reasoning, from current-chat metadata. Exposed Codex runtime: 0.166.0-alpha.5.1. Exact served checkpoint/build is not exposed. Reference truth came from the declared law; predictions came from fitted research models. The assistant authored and executed code. See ai_provenance.json/session_provenance.json and build_provenance.json (desktop app 26.1027.3384.0 and runtime executable SHA256).

External independent review: REVIEW_UNAVAILABLE. Executor checks are not an independent scientific audit. All commands/configurations and the retained initial collector failure are logged.
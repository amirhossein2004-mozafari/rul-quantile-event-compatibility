# Threshold-proximity follow-up, 2026-11-01 (Asia/Tehran)

Prospective read-only analysis of existing saved predictions. Prior association results are known. No training, new predictions, changes to earlier results/protocols/hashes, new outcomes, new thresholds, or subgroup searching. All outputs go in this new directory. The earlier association decision remains governed solely by its locked rule.

## Question A: real Brier association

Use all 40 equal-search frozen runs: FD001–FD004, LSTM/hybrid, five seeds, official-test final windows. Fitting engines: 60/156/60/149; evaluation engines: 100/259/100/248 (707 unique). Source: existing association/real_engine_run.csv, cross-checked against its saved associations. Outcomes and flag unchanged: Brier contribution, raw probability, exact h=30 incompatibility flag, capped true RUL, inclusive band 20<=true capped RUL<=40.

Primary OLS: Brier = seed intercepts + flag + cubic polynomial of raw probability + cubic polynomial of capped RUL/125 + band indicator. Retain the earlier continuous RUL adjustment and add BOTH requested probability and band controls. No interactions or selected terms. Report flag coefficient in Brier units, 95% percentile engine-cluster bootstrap CI, incompatible/compatible unique engine and engine/run counts, band/elsewhere counts, evaluation and fitting engine counts. Engines may appear in both flag groups across seeds. All eight groups retained.

Decision fixed before running: call the Brier association "not explained by threshold proximity" only if the flag coefficient remains positive with 95% CI excluding zero in at least 6/8 groups after both adjustments. Otherwise call it "explained by or confounded with threshold proximity". This is the requested operational label, not proof of a causal explanation or absence of unmeasured confounding. No new diagnostic-informativeness decision is substituted for the earlier rule.

## Question B: synthetic band rates

Use ONLY existing original temporal and covariate-only saved fitted predictions, all fits retained including collapsed fits. Temporal: 30 fits per subset/architecture/objective. Covariate: 200 fits per setting/objective. Use saved association/engine_arrays and existing synthetic/evaluation_SUBSET_POLICY.npz. Define band using the saved realized capped RUL y, not oracle median or predicted RUL. Verify engine IDs/order. Report weighted raw, corrected weighted, and unweighted separately; both final-window and uniform-endpoint fleets; small fleets 100/259/100/248 and large fleets 10,000. All 144 settings retained. FD003 covariate shares FD001 fitted states, disclosed without treating them as independent fitting evidence.

For each setting average fixed-fit flags within each engine, then estimate rates within band and elsewhere and the near-minus-elsewhere difference. Report both rates and difference with CIs, band/elsewhere unique engine counts, fit counts, fitting/evaluation engine counts, and engine/run flag counts within each band. Empty bands produce explicit NA. No model/fleet/variant chosen from results.

## Uncertainty, checks, records

Reuse previous engine bootstrap scheme exactly: 2,000 draws; seed 2026110103 +1000*subset_index +100*(uniform policy) +1*(n=10000); multinomial engine weights. Preserve every seed/fitted-state output for a resampled engine. No seed/model bootstrap. CIs are conditional on frozen fits and fixed evaluation population. Report undefined draws. For OLS use within-seed centering, generalized inverse covariance with relative SVD tolerance 1e-10 and target null-row norm tolerance 1e-6, as documented by the existing numerical correction; genuinely unidentifiable targets remain NA. Cross-check point coefficients against direct least squares with matching design cutoff 1e-5.

Verify previous real raw incompatibility rates and Brier contributions; verify synthetic raw rates against the saved association group counts, plus engine IDs, finite predictions and y cap. Hash earlier report/result/protocol files before and after; require unchanged. Save a verbatim Step 0 consistency record using existing result files only. Archive exact tool inputs, commands/configuration, source and input hashes, available AI model/runtime/build identifiers; exact served checkpoint unavailable if unexposed. Independent human review is still missing. Hash this protocol before calculating either new analysis. Report all unfavorable and undefined results.

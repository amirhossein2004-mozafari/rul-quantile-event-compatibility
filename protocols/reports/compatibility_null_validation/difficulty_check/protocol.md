# Read-only null-distribution and difficulty check

Date: 2026-11-01 (Asia/Tehran). Prior results are already known. This protocol is written before the requested percentile/difficulty calculations. No training, inference, fitting, selection changes or edits to earlier protocols/results/hashes. Write only new analysis artifacts here.

## Cohorts

Primary synthetic cohort: original temporal, weighted_raw, final-window, 10000 evaluation engines; retain the previously fixed non-collapsed classification from the uniform-endpoint 10000-engine audit fleet. Do not reclassify or select fits using final-window outcomes. Real cohort: all five original equal-search frozen fits in each FD001–FD004/LSTM-hybrid group, final official-test window, test counts 100/259/100/248; fitting counts 60/156/60/149. Seeds and fits do not add independent engines.

## Requested distribution table

Use saved per-replication incompatibility rates. For each of the eight groups calculate min, 2.5th, 25th, 50th, 75th, 97.5th and max using NumPy linear interpolation. Compare with the same group's saved five-seed real weighted_raw mean rate. Classify strictly below the 2.5th percentile as below; strictly above the 97.5th as above; both boundaries are inside. Rates are fractions. Preserve retained-fit counts and real/synthetic evaluation and fitting-engine counts. Cross-check min, 2.5th, 97.5th and max against previous non-collapsed summaries. No bootstrap or new hypothesis test is requested here.

## Difficulty metrics

Calculate metrics only from saved prediction/target arrays; load no checkpoint and run no forward pass. Each synthetic retained fit uses all 10000 final-window evaluation engines. Each real fit uses its official-test fleet. Capped test RMSE = sqrt(mean((clip(q50,0,125)-min(raw_RUL,125))^2)); event AUC uses raw probability and label 1[raw_RUL<=30]; event base rate is the mean of that label; width is median raw q95-q05, without clipping endpoints. One metric row per fit; AUC is NA if a fleet contains only one class. No engine weighting beyond one final window per engine. Event base rates are evaluation-fleet quantities, repeated across fits sharing a fleet.

The requested difficulty tables compare the same non-collapsed synthetic cohort against all real fits. Save all per-fit metric rows, and arithmetic means across fixed fits for a compact comparison table per subset. A mean of fit-level median widths is labelled mean_fit_median_width; it is not a pooled median. Also save the per-fit tables separately so no fit is hidden. These are descriptive summaries, with no claim of matched difficulty or independent-model uncertainty. Any user clarification about display preference may change presentation only; retain per-fit and mean tables either way.

## Hazard/design record

Read the existing generator/configuration/protocol and state the exact Weibull shape, covariate support, scale function, and conditional law for final and uniform endpoint policies. Distinguish age dependence of the endpoint-conditioned RUL law from feature availability and from the capped atom. Do not fit or simulate a new law. Record source line ranges. No interpretation about what this implies for the diagnostic.

## Checks and output

Cross-check saved incompatibility flags/rates against arrays and prior real summaries; verify engine IDs/order and non-collapsed membership. Retain every selected fit and report any absent prediction or undefined metric explicitly as MISSING/NA. Hash all input files used before/after and require unchanged. Copy available AI model/runtime/build identifiers from saved provenance, recording unavailable served checkpoint; independent human review remains missing. Archive command/tool inputs and source hashes. Hash this protocol before computing requested statistics. Display new calculations to six decimals, with unrounded values retained in CSV. Report tables and design facts only, without explanatory interpretation.

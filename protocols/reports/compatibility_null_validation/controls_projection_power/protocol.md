# Frozen-prediction controls, projection, effect size and dependence

Date: 2026-11-01 (Asia/Tehran). Prior compatibility and association results have been examined. This protocol fixes every outcome, threshold, analysis and criterion below before the new calculations. Use existing predictions only, with no checkpoint loading, forward inference, training, calibration fitting, test-selected variant or edits to earlier results/protocols/claims. All new artifacts go in this directory.

## Cohort and unit

Eight groups: FD001–FD004 × LSTM/hybrid, seeds 1101/1202/1303/1404/1505. Test endpoints: official final window; test engines 100/259/100/248. Calibration: the previously fixed saved endpoints, engines 20/52/20/50. Fitting engines 60/156/60/149. Within a subset/role, architectures and seeds share engines; retain all repeated outputs when resampling that engine. IDs are namespaced by subset and role; test and calibration are never pooled. Independent evaluation units: 707 test engines and 142 calibration engines. No seed/model resampling.

Read raw q05/q50/q95 and saved logits from each frozen run. Assign calibration IDs from the saved calibration_endpoints.csv order and verify raw targets match. Check engine/target equality across seeds/architectures. Horizon h=30 and quantile levels .05/.50/.95 remain fixed. L=max({0}∪{tau:q_tau<=30}), U=min({1}∪{tau:q_tau>30}), d=max(L-p,p-U,0), incompatibility flag d>0, without tolerance, quantile clipping or sorting. Require L<=U for every row; a failure is investigated and reported, never filtered.

## A. Controlled event probabilities (test only)

Retain raw sigmoid(r) as reference and evaluate: Uniform(0,1), 1-p, sigmoid(r+1), sigmoid(r-1). Quantiles stay fixed. Uniform uses 100 independent fixed realizations per engine/run, seed 2026110104+1000*subset_index+100*architecture_index. Store draws; average their metrics within seed and engine before the primary group bootstrap. These CIs condition on those realized uniform draws, not on an additional randomization bootstrap. Save per-draw/per-seed rates and distances so no random draw or seed disappears. All four controls are reported regardless of direction. Do not assume that every transformed probability is empirically worse or that flags must increase.

Outcomes: incompatibility rate and mean distance, averaged over engines and all five fixed seeds. Report both point estimates and 95% engine-bootstrap CIs. Save per-seed summaries. No label-based choice of control or random realization.

## B. Direct probability projection (test and calibration separately)

p_proj=clip(p,L,U), applied directly to each saved raw probability without fitting. Report raw and projected Brier, NLL, ECE5, ECE10 and incompatibility rate, with paired projected-minus-raw differences and 95% engine-bootstrap CIs; raw/projected marginal CIs are also retained. Projection incompatibility must be exactly zero under the ordered bounds; any nonzero value triggers investigation before reporting.

Brier uses (p-y)^2 with event y=1[raw RUL<=30]. NLL uses only scoring-time clipping to [1e-15,1-1e-15] and -y*log(p)-(1-y)*log1p(-p). Projection itself and Brier/ECE/flags use unclipped probabilities. ECE5 is the primary ECE convention: five probability-quantile bins separately for each frozen seed/role/variant, with duplicate boundaries collapsed, interior unique quantile cuts, and ties never split by labels. ECE10 with ten fixed equal-width bins is a pre-specified sensitivity, not an alternative selected afterward. All bin edges are label-free, saved, and frozen across bootstrap draws. Recompute bin weights, predicted means and event means in each draw. ECE is averaged across the fixed seed-specific ECE values, not evaluated on a model-averaged probability. Retain ECE5 effective occupied-bin counts.

The same saved calibration engines are reported as a distinct evaluation role; this is a deterministic projection and does not refit a calibrator or supply independent calibration validation. No method is chosen using either role's labels.

## C. Adjusted effects and approximate detectable effects (test only)

Use the previous RUL-adjusted flag regressions, unchanged: outcome = seed intercept + flag + cubic polynomial of true capped RUL/125. Outcomes are (unprojected q50 - capped true RUL)^2 and raw Brier. Read their original point coefficients/CIs and existing engine-bootstrap coefficient draws, verifying setting keys. Do not substitute the probability/band-adjusted regressions. Report every group's coefficient, 95% percentile CI, outcome mean, and signed upper CI endpoint / observed group mean outcome ×100. User clarification: each outcome uses its own mean squared error denominator—mean median squared error for point error, and mean Brier (event MSE) for the Brier outcome. Do not truncate negative coefficients or relative bounds. The denominator is the observed fixed-fit/engine mean, not a bootstrapped ratio bound.

Approximate minimum detectable positive effect at 80% power: bootstrap standard error = sample SD (ddof=1) of the 2000 saved engine-bootstrap coefficient estimates; MDE=(Phi^-1(.975)+Phi^-1(.80))*SE. This is a two-sided alpha=.05 normal/Wald power approximation using an engine-bootstrap SE, not a simulated exact power result and not an observed-effect/post-hoc power test. Report MDE in outcome units and as percent of the same outcome mean. Percentile CIs remain the original CIs even though the power approximation is normal. Report undefined draws; no silently omitted required group.

## D. Shared engines and pooling

Save engine-ID lists/hashes and a dependence table. For A and B, add subset-combined estimates (equal LSTM/hybrid weight within each engine) and pooled estimates across subsets weighted by their fixed engine counts. Use independent within-subset engine bootstrap resamples and the same resamples for all architectures, seeds and variants. Pooled ECE is the engine-count-weighted average of fixed-model ECE values, explicitly not ECE of a probability mixture.

For C, pool the already adjusted coefficients descriptively: average LSTM/hybrid coefficients within each subset, then weight subset coefficients by test-engine counts /707. Apply those same weights to synchronized bootstrap coefficient draws. This is an engine-count-weighted average of group-specific adjusted effects, not a common-slope regression. The subset and pooled denominator is the same weighted mean outcome. Report subset-combined and overall pooled coefficients, CIs, relative upper bounds and approximate MDE using the same rule. Pooling does not create independent model/seed units.

## Bootstrap, checks, reporting and record

2000 percentile engine-cluster bootstrap draws. Reuse the prior test resampling scheme: NumPy multinomial(n,1/n), seed 2026110103+1000*subset_index for official-test fleets; this preserves alignment with saved regression draws. Calibration uses separate seed 2026110105+1000*subset_index, same draw across architectures and variants. Percentile endpoints .025/.975. Retain all seeds/engines. CIs condition on fixed fitted models, fixed endpoint populations, fixed ECE cuts and fixed uniform random draws. Report independent engine counts, fitting-engine counts, fixed fit counts and undefined draws next to every result.

Check raw test flags/distances/Brier against previous summaries, raw probabilities against saved outputs, regression keys and original CIs, calibration endpoint order/targets, ECE implementation against a direct calculation, probability bounds/finite scores, and projection zero incompatibility. Treat undefined AUC as irrelevant because AUC is not an outcome here. Hash all inputs before/after and require unchanged; earlier protocol hashes/claims remain untouched. No outcome, threshold, estimator or decision criterion may change after this lock. Implementation corrections, if necessary, must be recorded transparently and cannot silently replace this protocol.

Save complete tables, per-seed and random-draw outputs, pooled estimates, bootstrap definitions, exact command/tool inputs and available AI model/runtime/build identifiers. Exact served checkpoint is unavailable if not exposed. Independent human review is still missing. Report every unfavorable result. New display: rates/changes as percentages/percentage points to one decimal; other estimates/CIs to three significant figures; full precision retained in CSVs. No earlier claim is rewritten.

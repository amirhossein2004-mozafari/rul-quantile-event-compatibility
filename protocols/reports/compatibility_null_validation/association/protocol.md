# Association validation protocol — FINAL, locked before analysis

Date: 2026-11-01, Asia/Tehran. This is a new prospective association analysis of existing frozen predictions. Prior incompatibility rates and collapse analyses are already known. No association analysis or model fitting has been run under this protocol. Parent protocols and locks remain unchanged.

## Hypothesis and scope

Higher incompatibility indicates larger prediction error after accounting for location in the RUL distribution. The temporal synthetic experiment is a known-law training-pipeline analysis including approximation and optimization error. Associations are descriptive and cannot establish a causal effect of incompatibility. Official-test predictions are used only for this requested frozen-model analysis, never for model selection, filtering, tuning or further training.

## Locked decision rule

User clarification: require both real outcomes and both synthetic deviations in both families. The same at least six of eight real groups must have positive flag coefficients with 95% engine-bootstrap CIs excluding zero for BOTH median squared error and Brier after the specified RUL adjustment. Synthetic confirmation requires positive adjusted flag AND distance coefficients, with 95% CIs excluding zero, for BOTH squared oracle probability deviation and mean absolute oracle quantile deviation in BOTH families. Family-level effects are the equally weighted mean of the eight temporal subset/architecture coefficients or four covariate subset coefficients, using weighted-raw, final-window, 10,000-engine settings only. Bootstrap draws share engine resamples within each subset across architectures/variants, independently across subsets. Every individual setting is also reported; no choice of favorable settings. Rank-deficient required components fail the rule. If either real or synthetic condition fails, report "not informative" under this rule. No subgroup search or post-result revision.
## Real cohort and measurements

All forty equal-search frozen models: FD001–FD004, LSTM/hybrid, five seeds (1101,1202,1303,1404,1505). Use official-test final window for every engine. Unique evaluation-engine counts are 100/259/100/248 (707 across subsets), fitting-engine counts 60/156/60/149. Seeds do not add independent engines.

For each engine/run save engine ID, subset, architecture, seed, true RUL capped at 125, event label 1[RUL<=30], raw probability sigmoid(r), raw quantiles, flag 1[d>0], distance d, median squared error, and Brier contribution (p-label)^2. Use the exact existing h=30 diagnostic and strict inequalities, without tolerance, clipping quantiles or collapsing fits out of the analysis. Cross-check raw sigmoid against saved p_Raw and engine/target ordering across seeds.

For each of eight groups and each error outcome report unadjusted incompatible-minus-compatible mean difference and outcome means. Count distinct engines ever appearing in each flag group plus engine/run counts; the same engine may appear in both groups across seeds. Report per-seed results as descriptive sensitivity, retaining every seed.

RUL bins fixed in advance: [0,20), [20,40], (40,60], (60,80], (80,100], (100,125]. Report every bin, including empty and one-flag-only bins. A standardized within-bin difference uses fixed observed engine/run bin proportions renormalized over bins containing both flags; state retained engine count and excluded bins. This overlap estimand is supplementary, not a replacement for the regression.

Primary adjusted regression: outcome = intercept + flag + cubic polynomial of capped RUL/125 + four seed indicators. Report flag coefficient in original outcome units. Supplementary continuous-distance regression replaces flag with d, reporting effect per 0.1 probability-distance unit. No interactions or variable selection. Use OLS as a conditional mean association, without distributional normality assumptions for intervals.

Incremental Brier analysis: Brier = intercept + d/0.1 + cubic polynomial of raw p + cubic polynomial of capped RUL/125 + four seed indicators. Report distance coefficient, in-sample incremental R-squared over the same regression without d, and engine-bootstrap intervals. This tests a specified functional adjustment, not general predictive utility or held-out improvement. Brier is algebraically determined by p and the event label; interpret any residual association cautiously, especially after conditioning on true RUL.

Near-threshold band is inclusive capped RUL 20–40. Report incompatibility rates in band and elsewhere, difference, distances, unique engines and engine/run counts, with engine-bootstrap CIs. No alternative bands.

## Synthetic cohorts and oracle targets

Use every existing original temporal (30 fits per architecture/subset/objective) and covariate-only (200 fits per setting/objective) fit; no new training and no collapse filtering. Report weighted raw, training-weight-corrected and unweighted variants separately, both final-window and uniform-endpoint fleets, both original small fleets (100/259/100/248 engines) and 10,000-engine fleets. FD003 control states reused from FD001 remain labelled as shared states, not extra independent training evidence. New initialization interventions and factorial ablations are outside this requested original-fit analysis.

Use the saved known-law conditional oracle probabilities and quantiles, generated independently of fitted outputs. Outcomes: squared probability deviation (p-p_oracle)^2 and mean absolute quantile deviation over .05/.50/.95. Supplementary absolute probability deviation and mean squared quantile deviation are also reported. Save per-engine oracle and fitted predictions in compressed arrays with source metadata.

For each family/subset/architecture/variant/policy/size report flag-group means, incompatible-minus-compatible differences, and distance slopes (per 0.1). Models are fixed repeated measurements; include fitted-state intercepts in regressions via within-fit centering. Adjusted synthetic regressions control cubic oracle median/125 and cubic oracle probability, removing between-state intercept differences. Report flag and d separately. All-fit cohort effects average states equally; report every fit's unadjusted effects and flag-group engine counts as well. Empty groups/constant predictors are explicit NA, not zero. Decision evaluation will use only weighted-raw final-window 10,000-engine settings; all other variants/policies/sizes are fixed sensitivities.

## Uncertainty, completeness and checks

Use 2,000 percentile cluster-bootstrap replicates, seed 2026110103 plus deterministic setting offsets. Within subset/evaluation fleet resample engine IDs with replacement, preserving all seeds/fits and outputs of each sampled engine. No seed/model bootstrap. Refit regressions on each draw. Report 95% CIs and number of undefined/singular draws; rank-deficient point regressions are NA. Bootstrap CIs condition on frozen fitted models; they do not include training-fleet uncertainty. Report engine counts next to every result. No multiplicity correction; the locked joint decision rule restricts the claim.

Verify diagnostic against prior raw rates, oracle arrays against engine IDs, finite predictions, target cap, and coefficient computations against a direct least-squares calculation. Investigate discrepancies before reporting. Retain all settings, empty groups, singular fits and adverse associations. No additional result-dependent subgroup analysis.

Archive every execution/edit tool input, commands, analysis configuration, source hashes and model/build identifiers available from the local AI runtime. Exact served model checkpoints may be unavailable and must be labelled unavailable. Save the final protocol SHA256 before running analyses. A negative decision is reported literally as "not informative" under this rule, without claiming universal uselessness.

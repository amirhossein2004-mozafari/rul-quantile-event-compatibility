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

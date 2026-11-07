# M5 locally locked retrospective calibration correction

Freeze before new inference. Reuse all20 original hybrid models and fitting-only
preprocessors; no training, tuning or selection on new outcomes. Calibration
uses every saved held-out engine, disjoint from model fitting. Predict EVERY
prefix cycle1 through lifetime-1, repeating the first observation to pad early
30-cycle windows. No failure-time endpoint. Labels are lifetime-cycle, with a
separate capped=min(raw,125) target. Official tests use final observed windows.

For both targets compare six fixed methods: historical restricted nonnegative;
original signed CQR on the same restricted endpoints; signed CQR on one
unrestricted endpoint per held-out engine; engine-balanced all-prefix signed
scores; engine-maximum all-prefix signed scores; and cycle-density-weighted
signed CQR on the unrestricted single endpoints. Keep negative cutoffs and empty
sets in signed CQR; never reorder bounds to hide emptiness. Finite-sample rank
ceil((n+1)*.9), +infinity when necessary. Scores are max(q05-y,y-q95), no zero
truncation except the explicitly historical arm. Capped projection intersects
with[0,125]; raw lifetime projection intersects with[0,infinity), without upper
capping. Empty intervals have width0 and are uncovered; interval score is
reported only for nonempty sets, with empty counts explicit.

Choose the unrestricted endpoint by PCG64 seed161600+seed+10000*subset_index,
uniformly over cycles1..L-1 in sorted engine order. For all-prefix empirical
quantiles each engine has total weight1. The engine-max arm has one max score
per engine, so its effective n is engine count, never window count. It concerns
simultaneous prefix coverage conditional on exchangeable full engine paths;
that condition is not established for the official test fleet. No CV+ or
Jackknife+ claim: frozen predictors are not cross-fitted predictors.

Weighted sensitivity: bins of observed cycle[0,30,60,90,120,150,200,300,infinity).
Estimate target/source bin probabilities using ONLY unrestricted calibration
cycles and unlabeled official-test cycles, with add-one smoothing in all8bins.
Weight=p_test_bin/p_cal_bin. For each test point append its positive weight at
score+infinity; take the left weighted .9 quantile. Source/target score laws
need not differ only through cycle. Estimated ratios, small support and possible
conditional shift preclude a distribution-free coverage claim. This is NOT a
proved correction of the original label-restricted selection mechanism.

Report all20 runs, all methods, capped AND raw target coverage/width, cutoffs,
empty/infinite counts and per-engine outcomes. Stratify official tests by raw
RUL<=125 versus>125 and padded versus full history, counting unique engines
per subset (not seeds times engines). Also report coverage of all observed
calibration prefixes only as an in-calibration diagnostic, never held-out
performance. No method chosen after test scoring. All results exploratory;
previous data and calibration labels examined. Existing47 tables unchanged.

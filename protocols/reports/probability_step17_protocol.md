# M6 probability calibration and reference correction

Local retrospective lock before new fitting. No neural retraining or test-based
method selection. Study original20 hybrid models and all80 matched-budget
LSTM/hybrid/TCN/GRU final models. Reuse fitting-only preprocessors and saved
fit/calibration engines. For original models reuse step16 all-prefix predictions;
for matched models infer every saved calibration-engine prefix cycle1..L-1,
with the same repeated-first-row padding. Event is raw RUL<=30 throughout.

Each calibration engine has total fitting weight1, distributed equally among
its prefixes; normalize sample weights to sum one in the mean-loss objective.
Report event rows AND engines with event/non-event support. These windows do
not create independent engines, and this calibration population does not match
the unknown official truncation mechanism. Endpoint-sampled prior is retained
as a separate constant reference, never relabeled the test prior.

Five engine-disjoint calibration folds, deterministic SHA256 ordering with
fixed domain step17, modulo5. Fit only on four folds, predict the held-out
engine fold. Final calibrators refit on all calibration engines after OOF.
No fitting-only neural engine enters calibration. No neural CV+/new-fleet claim.

Fixed methods: Raw; TrainWeightOffset=sigmoid(logit-log(w_train));
CalibrationPriorOffset=sigmoid(logit-log(w_train)+logit(pi_cal)-logit(pi_train));
InterceptFit (unit slope); Platt (nonnegative slope + intercept); temperature
and offset+temperature with T in[.1,10]; monotone Isotonic; monotone Beta
(nonnegative coefficients of log(p) and -log(1-p), free intercept); calibration
constant, pseudo-count-smoothed calibration constant (legacy code label
CalConstantJeffreys; a smoothing heuristic, not a binomial posterior for
dependent prefixes), endpoint constant; and raw
last-observation FeatureLogistic and its Platt-calibrated version. Beta uses
p clipped to[1e-12,1-1e-12] for feature evaluation only. Sigmoid calibrators
minimize weighted binary NLL plus fixed1e-4 squared coefficient/intercept
penalty (except temperatures). No test selection of regularization or method.
Record numerical success/boundaries; do not silently accept failed fits.

Class support: flexible calibrators require at least5 distinct training engines
containing positive events AND5 containing negatives. Temperature/intercept
require both classes. Missing fits are reported NA, not replaced by invented
parameters. Full trajectories usually give every calibration engine both
classes; dependence still remains. Existing one-positive endpoint fits are
historical and are not used to fit the new flexible calibrators.

FeatureLogistic: LogisticRegression(C=1,max_iter=2000,tol=1e-8, no class weights),
using the18 scaled features at each complete training window's final cycle,
fitting engines only, raw RUL event labels. No additional feature scaling or
hyperparameter selection.20 original splits plus4 shared matched splits give
24 unique linear fits, reused across matched neural architectures/seeds as
appropriate, not100 independent new baselines.

Endpoint-constant OOF predictions use endpoint labels from the four training
folds only; final endpoint constants use all calibration engines. Original
training weights are checked against archived verification metadata; matched
weights are checked against archived calibration fits, allowing float32 rounding.

Primary metrics: Brier and stable logit-based binary NLL; Brier skill against BOTH the
endpoint constant and the engine-balanced all-prefix calibration constant.
ECE5 uses label-free equal-frequency probability-bin boundaries with duplicate
boundaries collapsed; identical probabilities are never arbitrarily split.
Isotonic probabilities remain exactly zero/one where fitted, with counts
reported; only their NLL evaluation clips probabilities to[1e-15,1-1e-15].
Constants use this same clipping for finite log-odds, including possible
zero-event fold endpoint references. ECE edges use unweighted probability
quantiles; OOF bin contributions use engine-balanced weights.
Also retain ECE10 equal-width, ROC-AUC and event support. No inference from
ROC-AUC to calibration. OOF metrics concern the calibration-prefix distribution.

Uncertainty:1000 paired crossed draws resample five fitted runs and the SAME
official-test engine IDs for all methods in each study/subset/architecture.
Seed171700+group_index (Original then Matched, subset order, model lexical).
Save Brier, ECE5 and delta-Brier vs Raw and FeatureLogistic percentile95% bounds.
ECE bin edges are fixed at their original label-free empirical values within
each model/method during resampling. These intervals exclude calibrator
refitting/bin-edge estimation and new training-population uncertainty. No
significance declarations or population calibration guarantee. All outcomes,
including harm/negative skill/boundary fits, remain.

Rename display Bayes to Weight offset, retaining historical field/code names
with an explicit mapping. This is training-class-weight log-odds adjustment,
not a Bayesian neural network or an identified population-prior correction.

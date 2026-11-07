# Remaining required/recommended experiments: retrospective local lock

Prior C-MAPSS outcomes have been inspected. This is not preregistration, unseen
validation or independent review. No official-test score chooses a method.
Items13/14 (window/cap sensitivity, end-to-end cost study) are excluded by user.

Reuse the fixed step2 fit/validation/calibration roles and fitting-only preprocessing.
New complete-output arms: TCN last-token pooling (otherwise identical TCN),
Transformer (18->64, sinusoidal position, two encoder layers, four heads,
feedforward128/dropout.1, last-token pooling, existing ordered quantile/risk heads),
and GRU Gaussian-NLL regression. Gaussian mean and scale are in RUL/125 units;
reported outputs convert back to cycles. Scale is125*(softplus(s)+.001).
The Gaussian law induces its quantiles and P(RUL<=30); it has no independent
binary head. Its continuous Gaussian NLL is a working score on capped targets,
not a correctly censored likelihood for actual lifetime or its cap atom.
It differs in objective and head structure; comparisons do not isolate the loss.

Each new arm/subset searches learning rates .0002/.0005/.001 for16 epochs,
tuning seed101; validation capped RMSE selects rate/epoch by candidate order
then earliest epoch. Five final seeds1101/1202/1303/1404/1505 retrain fitting
engines only.36 candidates and60 final fits. Same optimizer, batch128, clipping1,
weight decay.0001; quantile arms retain summed pinball+.5 weighted BCE.
The five Gaussian members also form one equal-weight mixture per subset;
mixture CDF inversion supplies quantiles and event probabilities, not averaged
quantiles or a moment-matched Normal. Four ensembles are not20 independent runs.

LSTM and hybrid additionally select configuration using three-fold engine CV
WITHIN the existing fitting engines, preserving the original external validation
and calibration engines outside all new CV training/selection. Inner preprocessors
fit only inner-training engines. Uniform held-out endpoints (cycles30..L-1)
and engine folds are fixed before training.72 inner candidates; pooled held-out
engine MSE chooses rate/epoch;40 final fits on the full original fitting role.
This is internal CV, not nested outer-CV or exhaustive search. Final training
roles remain matched to the earlier study; the selection rule differs.

CV+ reuses ONLY the three inner models with fixed LR.0005/final epoch16 for each
LSTM/hybrid/subset, irrespective of which CV configuration wins. Thus24 reused
fold models are not counted as new fits. Whole held-out engines supply either
one prespecified endpoint absolute residual or their maximum absolute residual
over every prefix1..L-1. Each engine contributes one score. For n engines use
lower order floor(.1*(n+1)) of fold prediction minus residual, upper order
ceil(.9*(n+1)) of fold prediction plus residual, with infinity at missing ranks.
Report before/after capped-domain projection. CVPlusEndpoint is the canonical
point-regression construction; CVPlusEngineMax is an engine-path adaptation,
without a proved CV+ guarantee for this path statistic. Neither construction
establishes exchangeability with official truncation or a new-fleet guarantee.
Three folds and nominal .9 are disclosed; nominal is not a claimed lower bound.

Matched literature-family interval controls: absolute-residual point split CP,
signed CQR, and separately calibrated asymmetric CQR (.025 lower/.075 upper
tail allocation, fixed before results). Evaluate on all earlier80 matched neural
fits and new60 fits using the SAME saved calibration endpoints and test fleet.
GradientBoostingRegressor controls use last-observation18 features,200 trees,
depth3,LR.05; squared-loss point model and .05/.95 quantile models give12 unique
fits (three per subset). Their interval methods follow the same endpoint protocol.
These are explicitly literature-family controls inspired by Javanmardi/Robinson,
not exact reproductions of their preprocessing, tuning or full published systems.
Retain negative signed scores, empty/infinite sets, and unmatched-family limits.
Existing step16 signed/engine-max/estimated-weighted CP remains part of evidence.

Prior-shift diagnostic:24 unique step17 fitting/calibration partitions, both event
classes. Reconstruct last-observation fitting windows and all calibration prefixes.
For each class compare source window-weighted feature mean with target mean under
engine-balanced-prefix weights. Bootstrap independent fitting/calibration engines
1999 times; use centered, studentized maximum absolute18-feature contrast for an
approximate omnibus null test. Holm adjusts48 class/partition tests. Save all
feature contrasts and simultaneous within-test max-statistic intervals. This tests
conditional feature moments under the stated sampling policies, not equality of
full window distributions or the weighted-BCE population identity. Preprocessing
is fixed during bootstrap; no official-test labels enter this diagnostic. Failure
to reject does not establish label shift. Prior repeated data inspection remains.

All neural/GB fits freeze before new test scoring. Record all fits/failures/boundaries.
Metrics: capped RMSE/MAE, raw quantile coverage/width/Winkler, Brier/stable binary
NLL/ECE5 for event output; Gaussian/mixture continuous RUL NLL is separate. Main
neural contrasts use paired1000-draw crossed fitted-run/engine bootstrap; conditional
on fits/configurations, excluding tuning/refitting uncertainty. No universal or
multiplicity-adjusted architecture superiority. All metadata/source hashes, weights,
roles, predictions, selection histories and numerical reconstruction remain.

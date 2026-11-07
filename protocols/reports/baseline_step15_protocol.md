# M4: bounded matched-budget architecture extension

Locked before any new fitting. Previously examined C-MAPSS; retrospective.
Reuse the exact step2 fitting/validation/calibration engine roles, fitting-only
preprocessing, training tensors and validation/calibration endpoints. No test
data select configurations. LSTM/hybrid step2 final fits are reused unchanged.

Add the canonical complete-output four-block TCN (global mean pooling; kernel3,
dilations1,2,4,8, two causal convolutions per block, receptive field61) and a
64-unit one-layer GRU with last-timestep encoding. Both share the existing
64-unit fusion and ordered three-quantile/event heads. QuantileRiskBase defines
the heads. Widths are fixed before fitting, not tuned from test outcomes.

Exactly the existing three learning rates .0002,.0005,.001, tuning seed101,
16 epochs per candidate, AdamW decay.0001, batch128, clipping1, summed pinball
plus .5 weighted BCE. Select minimum capped validation RMSE, candidate order
then earliest epoch. Retrain each chosen configuration at seeds1101,1202,1303,
1404,1505. Four subsets:24 new tuning candidates,40 new final fits;40 reused
LSTM/hybrid fits. All new final weights freeze before any new official-test
scoring. Calibration uses calibration engines only; identical step2 routines.
Six one-thread workers; retain checkpoints/history, no adverse-outcome removal.

Primary comparison: paired capped RMSE, hybrid minus each control on matching
seeds, with paired SD and 10,000-draw empirical crossed run/engine intervals.
Bootstrap seeds171500+3*subset_index+control_index (lstm,tcn,gru).
All metrics and all twelve contrasts are retained. No significance declarations
from these multiple descriptive contrasts. Conditional fixed split/configuration;
five fits are not five independent datasets. No adequate power or population
coverage claim. Configuration-selection and training-pool uncertainty omitted.

This equal candidate/epoch budget is not equal compute time, exhaustive tuning
or nested cross-validation. No claim of state of the art. Transformer, CNN,
MC-dropout and deep ensembles remain outside this bounded correction; Bayesian
weight correction in the existing manuscript is not a Bayesian neural network.
NLL for the binary event is distinct from a predictive density over full RUL.
Existing median-only historical notebook models are not eligible comparators
for quantile/event performance. Prior weak TCN results remain historical.

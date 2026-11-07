# Post-hoc investigation of extreme temporal null rates

Status: diagnostic follow-up after all original fits and results; not prospective
confirmation and not a replacement benchmark. Original protocol SHA256:
434ee931df6455e2af6273d3ec9590ad19cdd6755cb3e74b39f6cc4fe3a27764.

Observation motivating investigation: some temporal fits give100% incompatibility
on10000 evaluation engines; FD001 replication0 has q05 almost equal to q50.
Hypothesis: extremely small softplus lower offsets and their derivatives accompany
these results, indicating a fitted-head/optimization problem rather than a clean
measurement of estimation noise. Do not claim this accounts for every bad fit.

No new fitting, model selection, real-data evaluation, or changed predictions.
Describe lower gaps for ALL480 original temporal fits, keeping engine counts.
Use a fixed probe set: FD001replication0, BOTH LSTM/hybrid and BOTH objectives,
60 original fitting engines each, using all original4209 windows. Reconstruct the
saved training tensors with their recorded seed, load frozen final weights,
disable dropout for deterministic probes, and compute gradients without any
optimizer step. No official-test input, label or output enters these probes.

Metrics: mean/min/max lower offset q50-q05, fraction below.001 cycles and exactly
zero, raw lower-head logits, mean sigmoid(logit) (softplus derivative), and
unclipped full-fitting-window average gradient L2 norms of lower/median/upper heads.
The derivative is a deterministic checkpoint measurement, not an engine-independent
sample or a new statistical test. Do not bootstrap windows or claim a gradient CI.

If gaps/derivatives are not small, do not attribute high rates to lower-gap
saturation. If nonfinite tensors, reconstruction errors or saved-weight mismatch
occur, block interpretation and investigate. Retain every probe and every original
result. A small derivative supports saturation at that checkpoint; it does not
prove the whole cause, convergence, or how a longer-budget refit would behave.
No convergence-control refit will be claimed without actually running one.

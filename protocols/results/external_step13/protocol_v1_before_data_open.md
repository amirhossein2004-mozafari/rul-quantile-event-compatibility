# Frozen prospective second-benchmark protocol: N-CMAPSS DS01

Written 2026-10-29 before opening any N-CMAPSS HDF5 arrays, fitting a model,
or generating/evaluating N-CMAPSS predictions in this project. The official
archive headers have been inspected solely for acquisition: DS01 is the first
HDF5 member. Published metadata and literature were consulted, so this is not
a claim of ignorance of published results or a public preregistration.

## Purpose and fixed dataset selection

Address the absence of a second benchmark by evaluating a prospective,
specified protocol on N-CMAPSS DS01-005, the first HDF5 file in the official
NASA item-17 nested archive. Selection is based on archive order and acquisition
feasibility, not model performance. No fallback subset will be substituted
after scoring. Simulated engine responses are driven by recorded flight
conditions. This is a second simulation benchmark with untouched project-level
test results, not a real-fleet study or independent human review.

Official source: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
Archive: https://phm-datasets.s3.amazonaws.com/NASA/17.+Turbofan+Engine+Degradation+Simulation+Data+Set+2.zip
Descriptor: https://doi.org/10.3390/data6010005 ; NASA record
https://ntrs.nasa.gov/citations/20210020068 . The descriptor is already cited.

## Hypotheses and reportable outcomes

H1: the nominal quantile/event incompatibility observed on C-MAPSS can recur
on another benchmark when separately trained quantile and event heads share
representations. Primary endpoint: raw-head incompatible fraction with exactly
the Section 4.13 levels (.05,.50,.95), event threshold 30 and tolerance 1e-6.
Report every engine and seed, even zero conflicts. This is a replication question,
not a prespecified positive result or a universal prevalence claim.

H2: capped RMSE alone need not select the same architecture as probability and
interval scores. Report paired hybrid-minus-LSTM engine-balanced RMSE, Brier,
raw 90% Winkler and H1 rate for every seed. Directional disagreement is
descriptive; do not declare significance or equivalence. If directions agree,
report that the prior disagreement did not recur under this protocol.

FD003 component interventions remain hypothesis-generating. They do not become
confirmatory through this different whole-architecture experiment. No claim of
cross-dataset confirmation of individual components, calibration guarantees,
deployment, temperature-scaling effects or universal architectural superiority.

## Data, roles and prediction schedule

Use the publisher-provided development/test arrays. Test engine identifiers
and numeric values must not enter fitting, normalization, class weights, epoch
selection or protocol changes. No retuning on the official test set.

Use W_dev/W_test operating variables and X_s_dev/X_s_test measured sensors only.
Exclude X_v, T, and auxiliary flight-class/health-state values from inputs.
A's unit and cycle columns are grouping identifiers only. Use Y_dev/Y_test
official RUL labels; never reconstruct truth from predictions. Verify row
alignment, finiteness, ordered flights and constant within-flight labels.

For each unit/flight, select raw row offsets 0,10,...,290: one 30-step window
covering the first 290 seconds at 0.1Hz. No window crosses a flight. Flights
shorter than 291 raw rows are excluded and enumerated before fitting. This
fixed elapsed-time schedule needs no future RUL/failure time to choose an
endpoint. Report the different time semantics from 30 operating cycles in
C-MAPSS. All eligible flights are retained, including early/late RUL phases.

Use every development engine for fitting. No validation tuning or fitted
post-calibrator is performed. Standardize the selected W+X_s training windows
with fitting-only per-feature mean/SD (zero SD replaced by 1), then freeze.
This is in-benchmark retraining of two architectures, not zero-shot transfer
of C-MAPSS weights or a harmonized comparison of absolute dataset scores.

## Fixed training and analysis

Use the existing simple_quantile_risk.make_model LSTM and hybrid modules,
same hidden dimensions/heads. Permit only input_size to follow the measured
channel count if the public schema differs; record the count and parameters.
Cap RUL at 125 flight cycles; event is official uncapped RUL<=30 flight cycles.
Use naive MT: mean of three pinball losses plus 0.5 weighted BCE, with class
weight from fitting windows alone. Batch 64, AdamW lr .0005, weight decay
.0001, 16 epochs exactly, clip gradient norm 1, no early stopping/search.
Final seeds: 2101,2202,2303,2404,2505. Keep identical permutation seeds across
architectures; initialize separately with that seed. CPU deterministic mode,
one torch thread. Save all final weights, preprocessor and fitting histories.

Training weights each development flight equally (one window/flight). Primary
test aggregation first averages loss or conflict within each engine, then
averages engines equally. RMSE is sqrt of this engine-balanced MSE; MAE,
Brier, raw interval coverage/width/Winkler and compatibility average the same
way. Clip point/interval predictions to [0,125] for scoring, as in C-MAPSS;
use unmodified nominal quantiles for compatibility. Also retain unaggregated
window/engine records and ordinary window-weighted metrics as secondary.
Use raw sigmoid probabilities and the fixed training-weight offset (Bayes)
as secondary, with no temperature fitting. Never choose a winner/correction
from these new test scores. Brier uses official binary labels.

Compute one engine-level test report only after all ten final model checkpoints
and histories are complete and their hashes frozen. Training code may inspect
only development tensors. Score all ten frozen fits in one batch; no retrain
or protocol change after scoring. Save source/protocol hashes and timestamps
for fit-complete and evaluation-start. Small engine counts limit inference;
do not treat flights or five seeds as independent fleets or calculate a pooled
population interval. Raw intervals have no coverage guarantee. No conformal
fit or full-path guarantee is claimed with these small independent groups.

## Failure and amendment rules

First implement parser and train/eval separation. A development-only smoke
check may check shapes/finiteness and implementation, without test scoring.
Record bugs and their fixes; preserve interrupted outputs. A source-code fix
before test evaluation must be entered in an append-only implementation log,
with old/new hashes. Any result-informed change after evaluation is a new
exploratory protocol, never silently substituted into this experiment.

This local timestamp/hash lock is prospective within this workspace. It is
not immutable public preregistration, independent custody or a guarantee that
humans cannot access the public test set. Preserve all prior C-MAPSS evidence.
Do not retrospectively label prior C-MAPSS studies confirmatory. The resulting
claim must state actual scope, selected subset, engine counts and limitations.

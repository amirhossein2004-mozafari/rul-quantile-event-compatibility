# Compatibility diagnostic validation protocol

Date: 2026-10-31 (Asia/Tehran).
Status: PRE-EXECUTION DRAFT; clarification required before implementation or execution.
Only repository listing and source/protocol inspection preceded this document.
No synthetic draws, fitting, checkpoint evaluation, or experimental metrics have run.
This is a local prospective protocol for these new experiments, not a claim of public preregistration.

## Objective and hypothesis

Validate the h=30 diagnostic, quantify sensitivity to quantile error, and measure
estimation-induced incompatibility under explicitly specified synthetic nulls.
The oracle hypothesis is exactly zero incompatibility for quantiles and event
probability derived from the same known continuous conditional distribution.
No universal finite-sample incompatibility rate follows from engine count alone.
The finite-sample rate depends on the distribution, covariates, engine trajectories,
estimator, training objective, optimization, and prediction sampling policy.
No monotonic sensitivity curve is assumed: controlled noise can both create and
remove violations. Report measured curves including decreases.

## Diagnostic and numerical conventions

Use all paper quantiles (.05,.50,.95), pending confirmation that the quoted real
rates use this same grid. At h=30 define L=max({0} union {tau:q_tau<=30}),
U=min({1} union {tau:q_tau>30}), d=max(L-p,p-U,0).
Primary incompatibility indicator is d>0; report any floating point tolerance
sensitivity separately, never replace the primary definition silently.
Test equality at the horizon, probabilities at L/U, empty bounding sets, and
ordered oracle quantiles. Record crossing incidence under perturbations.
If L>U, retain the row, flag the empty compatibility interval, and report its
contribution; never silently sort, clip, or remove perturbed predictions.
For continuous oracle laws q_tau<=h implies tau<=F(h), so zero is an algebraic
identity and an implementation control, not an empirical model-performance claim.

## Source evidence inspected

reports/remaining_step19_protocol.md specifies ordered quantile/risk heads and
summed pinball plus .5 weighted BCE. src/training/pcgrad_ablation.py task_losses
implements that objective. src/models/hybrid_lstm_tcn.py defines ordered heads.
README.md identifies several frozen cohorts, including equal-search and later
fits; no cohort has been selected for this experiment yet.
With positive-class weight w, the population weighted-BCE optimum is
s=w*p/(1-p+w*p). Thus raw s is generally not F(h). Estimation noise, weighting,
model misspecification, and optimizer error must not be conflated.
Any weight-inverted output p=s/[w-(w-1)*s] is a separately named diagnostic arm;
it is not asserted to be calibrated merely by this transformation.

## Data roles and freezing

Synthetic fitting, optional development, and evaluation engines are disjoint.
Fit preprocessing and class weights using fitting engines only. No official-test
scores, labels, predictions, or quoted 9-20% range select settings, noise levels,
seeds, stopping, methods, or exclusions. Freeze the complete configuration before
reading held-out predictions for perturbation evaluation. Previously inspected
real results remain retrospective context, not unseen evidence.
Use existing development/calibration endpoints for perturbation unless the user
requests frozen official-test evaluation; explicitly record role and engine IDs.
Retain every requested dataset/subset/method/seed, failures, and missing artifacts.
Do not replace an unavailable cohort with a convenient subset without clarification.

## (a) Known-law synthetic experiment

Proposed law (requires confirmation): x~Uniform(-1,1), Y|x~Weibull(shape=2,
scale=30*exp(.7*x)). Y is positive and in cycles. Compute exact quantiles
scale*(-log(1-tau))**(1/2) and p=1-exp(-(30/scale)**2).
No clipping at the paper cap is implicit; any cap/training normalization must be
specified and preserve the event definition.
Proposed evaluation: 10,000 independent synthetic engines, one endpoint per engine,
shared across arms; 20 prespecified fitting replicates. These are proposed design
counts, not observed counts or a power calculation. Fitting sizes 60/156/149.
The covariate-to-sequence mapping and within-engine training-window counts need
clarification before claiming the paper architecture/training protocol is matched.
Train the selected paper architecture with its exact frozen loss, weights,
normalization, schedule and optimizer; save weights, histories, and configuration.
Report raw event-head and any prespecified weight-inverted results separately.
Evaluate (i) oracle q/oracle p, (ii) learned q/learned event head,
(iii) oracle p with noisy q. Proposed independent additive Gaussian noise SDs:
0,1,2,5,10,20 cycles, applied separately to q05/q95; leave q50 fixed.
Use prespecified common Gaussian draws scaled by SD. Show all levels and crossing
rates, with no post-hoc repair; an ordered-noise arm would require a separate lock.

## (b) Frozen-model perturbation

Use the user-confirmed complete frozen cohort and evaluation role. Freeze artifact
paths/hashes, methods, seed IDs, endpoints, engine IDs, and probability variants
before computing baseline or perturbed diagnostics. Perturb q05/q95 using the
same proposed SD grid; hold q50 and event output fixed. Include SD=0.
Proposed 100 independent noise replicates per model/level; noise replicates are
Monte Carlo replicates, not independent engines. Retain rowwise noise and results.
Report per-model curves and an equal-weight aggregate across the full cohort;
never pool model-engine pairs as independent engines.

## (c) Finite-sample null

Distinguish two possible definitions; user must select intended interpretation:
1. Coherent correctly specified Weibull likelihood estimator: estimate distribution
parameters from 60/156/149 independent fitting engines, then derive q and p from
that same fitted CDF. Incompatibility is algebraically zero despite parameter
uncertainty. This is a control, not a null for independently learned heads.
2. Correctly specified separately estimated quantile/event functions under the
known law: finite-data estimates can disagree. Exact estimator families and loss
(unweighted proper probability loss versus paper weighted BCE) must be locked.
The paper neural model is an additional training-pipeline null; its discrepancies
include optimization/approximation/weighting and cannot be called purely estimation
noise without evidence separating those contributions.
Run all locked fitting sizes and replicates, with independent fit sets and a shared
independent evaluation fleet. Report fitting/evaluation engine counts separately.
Engine count matching alone does not match information in many correlated training
windows. Preserve or explicitly vary the agreed engine/window sampling policy.

## Metrics and engine bootstrap

For each engine compute its mean indicator and mean distance over its prespecified
endpoints; fleet metrics average engines equally. With one endpoint these reduce
to the requested endpoint metrics. Record both engine and endpoint counts.
Primary table columns: setting, fitting engines, evaluation engines,
incompatibility rate (95% CI), mean distance (95% CI). Distance is in probability
units; rate may be shown as a percentage. Include subset/method/seed/noise level.
Proposed 2,000 percentile bootstrap draws resample evaluation engine IDs with
replacement, preserving every endpoint, method, model and noise replicate belonging
to a sampled engine. Paired contrasts use the same resampled IDs. Average model/noise
replicates within each draw; do not bootstrap seeds as engines.
These CIs condition on fitted models. Separately display the full distribution of
rates over independent synthetic fitting datasets to show training variability;
do not treat reuse of one evaluation fleet across fits as additional engines.
Bootstrap seeds, fit seeds and perturbation seeds must be saved before execution.

## Failure criteria and bug investigation

Any oracle violation, incorrect horizon equality, invalid probabilities, nonfinite
output, or mismatch between saved and recomputed diagnostic blocks interpretation
until investigated. Preserve failed outputs and the corrective amendment.
A poor synthetic model requires checking units, target normalization, class weights,
quantile order, event prevalence, convergence, and analytic truth before reporting
it as a scientific result. Report all unsuccessful fits and unresolved errors.
Large zero-noise discontinuities or missing-engine mismatches also block comparison.
No positive minimum sensitivity slope is required or selected after seeing curves.

## Comparison with the quoted real-data range

The 9-20% range is user supplied and has not been reproduced in this task.
Compare only after identifying exact real cohorts, quantile grid, probability
variant, engine counts and endpoint weighting. Report each matched real result
beside each finite-sample setting and its conditional CI/training-replicate range.
A real value above a synthetic interval establishes only exceedance of that
specified synthetic benchmark. Overlap is inconclusive. Neither establishes a
universal real-data null or isolates a causal reason for incompatibility.
If definitions or information budgets differ, mark the comparison unmatched and
withhold a categorical conclusion. Do not infer significance from the range alone.

## Reproducibility and amendments

Append every tool/shell command to commands.log, including read-only inspections.
Archive exact configuration, code/version hashes, dependency versions, engine
roles, RNG states/seeds, checkpoints, predictions, bootstrap indices, and failures.
No experiment runs until the unresolved choices below are answered and a final
configuration is saved. Amendments are dated and justified before dependent work.

## Clarifications required

1. Which frozen cohort and evaluation role should (b) use, and which exact
   real-data results/engine counts underlie 9-20%?
2. Does (c) mean a coherent fitted distribution, independently estimated correctly
   specified heads, or the exact paper training pipeline (including weighted BCE)?
3. For (a), use the full temporal architecture with a specified synthetic engine
   trajectory/window process, or a covariate-only network using the same heads/loss?
   Confirm the proposed Weibull law, counts, SD grid and bootstrap plan or revise.

## Amendment 1: user-confirmed scope and mandatory reproduction gate

Before any synthetic/perturbation experiment, independently recompute all eight
Table 2 raw means from saved predictions for the 40 equal-search models, official
test final windows, five seeds per subset/architecture. Table source:
paper/tables/compact_table2.md. Pass requires all eight recomputed percentage means
round to their published two-decimal values, all engine counts match, and exactly
five distinct seeds occur per group. Compare published sample SD as an extra check.
Reproduce the table's d>1e-6 convention AND report the requested strict d>0
convention separately; never silently substitute the tolerance. Use raw nominal
q05/q50/q95 and raw saved probabilities; no clipping or calibration.
If any published raw mean fails the rounding/count/completeness check, STOP and
report the mismatch. No tuning, filtering or synthetic experiments follow a failure.
This check uses official-test predictions solely to verify a fixed published result.

After a passing gate, the requested experiment scope is: primary full temporal
LSTM/hybrid synthetic trajectories, independent fitted heads, three event variants
(weighted raw, the SAME weighted fit corrected by sigmoid(r-log(w)), and separate
unweighted training); secondary covariate-only heads. All use known Weibull laws.
Noise SD levels are 0/.05/.10/.20 times the unperturbed q95-q05 per engine;
q50 and p remain fixed. Bootstrap resamples engine IDs, not seeds.
Before those runs, a further complete configuration must freeze the trajectory
law and conditional-truth construction, training budgets, replication counts,
endpoint rules, evaluation fleet sizes, RNG seeds and comparison criteria.
No synthetic/perturbation runs are authorized by an incomplete configuration.

## Amendment 2: perturbation execution lock (before perturbation run)

Reproduction gate PASS, all 8 means/SDs match; strict and tolerance rates agree.
For (b), run all 40 frozen equal-search models and all eight groups on official-test
final endpoints; raw nominal quantiles and p_Raw only. No training/selection changes.
100 noise replications per model; SD fractions [0,.05,.10,.20] of each unperturbed
(q95-q05). Independent standard normal draws for lower/upper quantiles and each
model/replicate/engine; common draws reused across fractions. q50 unchanged.
Seed 2026103101 for noise; seed 2026103102 for bootstrap. Retain negative/crossed
quantiles, flag crossings and L>U, do not reorder or clip. Compute the requested
max-bound distance directly even for crossings; label it as an empty-interval
conflict rather than evidence of quantile coherence. Save predictions/noise arrays.
Report strict d>0 primary and d>1e-6 sensitivity, distance, crossing fraction and
paired change from SD=0. Average 100 noise replications and 5 fitted models within
each engine before fleet averaging. Each group has 100/259/100/248 independent
engines, not 500/1295/500/1240. 2,000 percentile engine bootstrap draws with the
same engine draws across noise levels; CIs condition on frozen models and noise.
Save bootstrap indices. No independent-seed significance tests.
Pass/fail: SD=0 must reproduce the gate; all source predictions must be finite,
ordered, and complete. All 40 models, all levels and all 100 noise replications
must be retained. Failed checks block interpretation, with failures saved.
No requirement of monotonic response, no level/seed selected by response.
Primary synthetic replication target: 30 independent fitting fleets per temporal
configuration; secondary target: 200 fitting fleets per fitting size and objective.
These are locked targets, not completed-run counts. Synthetic execution awaits
resolution of censoring and correct-specification questions, followed by a complete
law/budget/evaluation/seed lock. No synthetic fits have run.

## Amendment 3: FINAL synthetic design lock, 2026-10-31

User authorized the known-law training-pipeline interpretation and independently
estimated exactly representable controls. This amendment supersedes unresolved
questions and earlier proposed shape-2/continuous-x law and proposed absolute noise.
No synthetic draws, fits or oracle computations preceded this amendment.

### Claims and design limits
Temporal LSTM/hybrid and covariate MLP results are known-law training-pipeline
nulls, including finite-sample variation, approximation, optimization, weighting
and sampling-policy shift. They are NOT pure estimation-noise measurements.
The exactly representable control fits quantile and event functions independently;
it does not derive both from a common fitted distribution. Separate-head fitting
uses the same data, as in the paper, not artificially independent data splits.
Correct specification refers to inclusion of the true function, not oracle fitting
or proof the numerical optimizer finds the population optimum. The controls use
one endpoint per fitting engine (per evaluation policy); neural fitting uses all
eligible windows. Their information budgets differ, so contrasts do not isolate a
causal numerical decomposition of approximation versus estimation error.

### Known law and temporal features
For each independent fitting engine draw x uniformly from {-1,+1}; let
lambda(x)=60*exp(.5*x). Draw T=30+Weibull(shape=1,scale=lambda). This is a continuous
shifted lifetime law; no artificial cap on lifetime. Training endpoints are integer
ages a=30,...,floor(T); the positive continuous target is T-a, capped at125 only
for the pinball loss, as in the paper. Event is uncapped T-a<=30.
Each endpoint uses a full30x18 window at ages a-29,...,a. Features are x,
age/125, and16 noisy sensors: sensor j=(j/16)*x + .25*age/lambda + Normal(0,.25).
Sensor noise is independent of lifetime given x/age and is shared for overlapping
training windows of an engine. Thus no noisy sensor secretly reveals its lifetime.
The covariate network sees x and age/125; neural residual-lifetime prediction can
use their known association with RUL. No claim of realistic turbofan physics.
Features are in these fixed dimensionless units; no fitted preprocessing is needed.
Neural outputs/targets are in cycles, NOT divided by125. q quantiles concern capped
RUL; because30<125 the oracle compatibility implication still holds at h=30.

### Endpoint laws and empirical truncation matching
Final-window evaluation samples censoring age uniformly from the observed engine
maximum cycle lengths in each raw C-MAPSS official-test INPUT file. No test RUL,
output, performance or labels determine any synthetic parameter. This matches the
empirical marginal truncation-age distribution, not NASA's unidentified latent
censoring mechanism or conditional sensor/lifetime distribution. Draw x independently
and draw T conditional on T>a: T=a+Exponential(lambda(x)). Censoring ages and x are
fixed design variables, so sampling survivors does not silently reweight x.
Uniform-endpoint evaluation draws T from the original shifted law and
A~Uniform(30,T), independently per engine. The 30-point histories have fractional
ages where appropriate. These are separate evaluation fleets, not repeated endpoints
counted as engines. Small fleets are the first n=100/259/100/248 of the associated
large fleet of10,000 engines; report nesting, not independence between fleet sizes.

### Conditional oracle (no Monte Carlo reference)
Final sampling: residual survival S(r|x,a)=exp(-r/lambda), hence
q_tau=min(125,-lambda*log(1-tau)); p=-expm1(-30/lambda).
Uniform sampling: S(r|x,a)=E1((a-30+r)/lambda)/E1((a-30)/lambda), where E1 is the
exponential integral. Evaluate p from that ratio and invert S by deterministic
bisection for q, capped at125. This is analytic conditional truth with numerical
special-function evaluation/inversion, not Monte Carlo ground truth. Endpoint
selection changes the conditional law: pooled neural windows obey survival-at-age
sampling whereas one-uniform-endpoint-per-engine includes inverse-lifetime weighting.
Report this distribution shift explicitly; do not attribute it to estimation noise.
All oracle probabilities and quantiles must satisfy d=0 at both fleet sizes/policies.
Also perturb true q05/q95 with the same fractional noise grid and true p to measure
noise-induced incompatibility independently of the learned event head.

### Fitting roles, budgets and replication
Primary: all8 subset/architecture configurations,30 independently generated fitting
fleets per configuration, fitting counts FD00160,FD002156,FD00360,FD004149. For each
fit fleet train weighted and unweighted models from paired initial RNG seeds;
weighted raw and corrected sigmoid(r-log(w)) reuse the SAME weighted model.
Total480 temporal fits,720 probability-variant evaluations before endpoint/fleet
multiplication. Quantile heads share the backbone, event head has its own parameters;
no coherence constraint or common fitted CDF couples their outputs.
Use exact source architectures (34116 LSTM,115095 hybrid parameters). Inherit the
already validation-selected learning-rate/epoch configurations in
results/fair_comparison_step2/selection.json; no new selection or test-driven tuning.
AdamW, weight_decay=.0001, batch128, gradient clipping1, naive sum of three mean
pinballs plus .5 BCE, positive weight n_negative_windows/n_positive_windows.
All eligible fitting windows retained; no engine/seed/method dropped. No calibration
or validation fitting is needed because all configurations are fixed in advance.
Original fit/validation/calibration partitions remain untouched.
Secondary: n=60/156/149;200 independent fitting fleets per n, same full-window
sampling, separate weighted/unweighted fits (1200 total). Covariate MLP uses input2
->64 with ReLU, followed by the exact QuantileRiskBase fusion/ordered heads/risk
heads. Fixed16 epochs,LR.0005, other loss/optimizer settings identical. This
secondary fixed budget is explicitly distinct from the inherited temporal budgets.
Parametric controls:200 fitting fleets per n and endpoint policy, one endpoint per
engine. Final sampling: independently minimize pinball in each x stratum for each
quantile using the empirical inverse-CDF minimizer; independently minimize weighted
and unweighted BCE in each stratum (saturated logistic two-intercept solution).
No probability is computed from the fitted quantile function. For uniform sampling,
each quantile head has its OWN two stratum scale parameters in the E1 quantile
function; the event function has its OWN two scale parameters, fitted separately
with weighted/unweighted BCE, including log(w) offset in the weighted family.
True scale values are representable. Search scalar log scales over[log(5),log(500)]
with fixed25-node grid then bounded minimization between neighboring grid nodes,
xatol1e-5. Record boundary minima, unsuccessful optimizers, objective values, heads,
and every failed fit. No gradient boosting control: exact-family controls are used.

### RNG, uncertainty, completion and pass/fail
Master seeds: training31415926; evaluation27182818; bootstrap16180339;
oracle-quantile noise14142135. Use deterministic derived integer seeds saved in
per-fit metadata;replicate IDs0..29/0..199 are mandatory complete cohorts.
Generate and save evaluation fleets before scoring fits; re-use identical fleet
engine IDs across models/variants/replications. Evaluate each fitted model on
both policies, small and10,000-engine fleets. Bootstrap2000 evaluation-engine
resamples (multinomial weights are equivalent), not model or training-replicate
resamples. Report both conditional-fit per-replication CIs and conditional-on-the-
full-fit-cohort mean CIs; keep per-replication rate ranges/quantiles separately.
Training-replication counts NEVER increase the number of evaluation engines.
For scalability bootstrap linear engine metrics with saved multinomial engine
weights; stream batches and store counts/indices, not independent window draws.
Primary rate d>0; sensitivity d>1e-6. Report all-engine mean distance and crossings.
Oracle noisy quantiles:100 noise replications, SD0/.05/.10/.20 times oracle width;
2000 engine-bootstrap draws after within-engine averaging of noise replicates.
Table2 reproduction already passed before synthetic runs; no further official-test
model choice. Synthetic oracle d>0, nonfinite truth/output, missing engine/variant,
wrong parameter count or target/loss units are blocking failures. Save failure
records and investigate before interpretation. No monotonic sensitivity criterion.
If a fit lacks either class, record failure; do not replace its fleet or seed.
Save training loss histories and oracle quantile MAE / probability error to inspect
underfitting. Poor neural results trigger unit, objective and convergence checks;
no result-driven extension of epochs or parameter selection.

For real-vs-null conclusions report every group and variant. A real point estimate
above the97.5th percentile of independent synthetic-fitting-replicate rates on the
10,000-engine FINAL-policy fleet is designated exceedance of that specified
training-pipeline/control benchmark (not a universal null rejection). Also give
engine-bootstrap uncertainty and full replication ranges; do not infer new-fleet
significance from seed independence. Uniform-policy comparisons are sensitivities
with different endpoint selection. No pooled9-20% conclusion without groupwise
results. Unmatched controls and their distinct endpoint-only information budgets
remain labeled. No unfavorable result or failed run may disappear.

### Execution provenance
Record exact script hashes, configuration, protocol SHA256, NumPy/SciPy/PyTorch/
Python versions, CPU/GPU model and deterministic settings. GPU acceleration if
available: float32,no AMP/TF32, deterministic algorithms and cuDNN, one Torch CPU
thread. CPU fallback uses the same budgets; never silently mixes devices inside a
fit. Resume only with identity/hashes verified. All commands append to commands.log.
AI tool: Codex desktop assistant. Exposed CLI/runtime identifier is
0.166.0-alpha.5.1. Exact assistant model checkpoint/build identifier is NOT exposed
in this session and is recorded as unavailable, rather than guessed. No AI model
is used to generate targets, predictions, oracle values, or experimental metrics.
External independent reviewer remains REVIEW_UNAVAILABLE (backend not exposed).

# Follow-up addendum: collapse-conditioned null and weighting attribution

Status: locally pre-specified for the FOLLOW-UP, with previous results already
inspected. This is not blinded/public preregistration. Original protocol remains
archived verbatim as protocol_v1_locked.md, SHA256:
434ee931df6455e2af6273d3ec9590ad19cdd6755cb3e74b39f6cc4fe3a27764.
The original lock/manifest and code snapshots remain retained. Legacy replay hash
checks refer to that archived version; the follow-up uses a separate lock and
never overwrites original model, input, prediction or result artifacts.

## Hypotheses and numerical collapse definition

Collapse = median over engines of raw nominal (q50-q05) STRICTLY below 1.25 cycles
(1% of the125-cycle RUL cap). Exactly1.25 is non-collapsed. No clipping, sorting,
changed horizon or probability-dependent threshold. Record negative gaps/crossings
separately, especially for independently estimated parametric quantiles.
This is a NEW criterion; the earlier .001-cycle investigation remains unchanged.

For synthetic fits, classify using the existing UNIFORM-ENDPOINT10000-engine
fleet, independent of fitting and of the FINAL-window evaluation fleet. Hold each
fit label fixed across final/uniform evaluation and small/large fleet sizes.
This uniform fleet was previously evaluated, so it is a follow-up classification
audit role, not newly unseen data. Uniform-policy results reuse classification
features and remain explicitly conditional/descriptive. Final-policy evaluation
uses a distinct engine fleet. Raw/corrected outputs of one weighted fit share q
and therefore one label; independently trained unweighted fits get their own label.
For real models, classify on the original fixed CALIBRATION engine endpoints only.
Do not use official-test quantiles, probabilities, labels or rates to select/filter
real fits or to define collapse. All40 original fits remain in every original
real group mean. Report the fraction collapsed among40 states and in each of the
8 groups, with calibration-engine counts. No model/seed independence inference.

Hypotheses to investigate, without presuming a favorable answer:
H1: raw-null rates differ between collapsed/non-collapsed states; neither direction
is assumed. H2: initialization, loss scaling, LR and clipping can affect collapse,
including interactions. H3: the fixed initialization intervention reduces collapse
without an architectural/forward change. H4: weighting may reduce OR increase raw
incompatibility relative to correction or unweighted training. Negative changes,
failed fits, empty strata and worsening quantile estimates are mandatory results.

## Three-way null reporting and comparisons

For ALL original temporal, covariate and parametric configurations, report ALL,
NON_COLLAPSED and COLLAPSED strata, all three probability variants, both endpoint
policies, and both existing evaluation fleet sizes. Controls are separate families;
no pooling them into a single null. The already completed parametric control is the
requested parametric/GBR alternative; no new GBR family is planned.
For each row retain planned/successful/failed/selected fit counts, fitting engines,
classification engines, evaluation engines, incompatibility rate, mean distance,
95% engine-bootstrap CIs, tolerance sensitivity d>1e-6, oracle q error and training-
fleet rate spread. Primary incompatibility remains strict d>0 at h=30.
Never multiply engine count by number of fits. Do not bootstrap seeds/models.
Use the original saved2000 engine-resampling weights; within each selected stratum
average indicators/distances over models WITHIN engine before fleet averaging.
Labels are held fixed in rate bootstrap, so these are conditional-on-label/model
CIs. Retain per-replication rows. An empty stratum is an explicit NA row, never0.

Recompute raw real group mean versus null training-rate97.5th percentile for each
family and each of three strata, particularly NON_COLLAPSED. Main comparison is
weighted_raw to weighted_raw on the FINAL10000-engine fleet. Preserve cross-variant
comparisons as labeled descriptive contrasts. Real fitting sizes60/156/60/149 and
test engines100/259/100/248 remain unchanged. Also report the small-fleet sensitivity.
With zero selected fits the threshold/comparison is undefined. With1 selected fit
show its rate as the empirical percentile but label SINGLE_FIT, not reliable tail
estimation. Counts below20 are labeled SPARSE_STRATUM; do not add replacement fits.
The real statistic still averages5 initializations on one fitting fleet; synthetic
replications still use independent fitting fleets and one initialization. This
remains a descriptive benchmark, not a matched five-seed hypothesis test.

## Collapse-cause experiment: complete four-factor factorial

Subset FD001 is fixed as the first numeric subset, smallest fitting size and the
previously examined synthetic case; it is not chosen using a real test outcome.
Use both LSTM and hybrid, synthetic fitting fleets replications0,1,2 from the
original generator/seeds, n=60. Same original final configurations and data windows,
no epoch extension. Weighted objective only for factorial diagnosis.
Factors, each with two fixed levels (all16 combinations; no winning-arm search):
I: original initialization versus the fixed gap initialization below.
S: original summed pinball versus (summed pinball)/125; weighted BCE coefficient.5
   remains fixed. Targets and predictions stay in cycles in BOTH cases.
R: inherited LR versus3 times inherited LR.
C: inherited gradient clipping1 versus no clipping.
Thus16 cells x2 architectures x3 fitting fleets =96 diagnostic configurations.
Reuse the6 exact original baseline states and the6 matching fixed-init-only states
from the validation cohort below; fit the remaining84 configurations once.
Keep all three paired fleets, all cells, all interactions and failures. No cell is
selected for the paper or for changing the predefined fix.
Record per-epoch pinball/BCE losses, preclip gradient norms, clipping fraction,
initial/final lower gaps and lower-offset derivatives. Record separate regression
and event shared-parameter gradient norms on the fixed first training batch before
updates as deterministic diagnostics (not independent-window inference). Report
factorial main-effect/interaction contrasts descriptively across the three paired
fleets; no model-level significance test or claim of definitive universal cause.

## Fixed initialization intervention: architecture unchanged

Do NOT edit src/models or the paper's checkpoints, architecture, parameter count,
forward function, loss, LR, epochs, optimizer or clipping in the FIX cohort.
After creating the original model with its original seed, set only the final
linear weights of lower_delta_head and upper_delta_head to zero, and their biases
to inverse_softplus(20) and inverse_softplus(80), respectively. These are fixed
fractions .16/.64 of the cap, not selected from outcomes. All other parameters
retain original initialization. No gap floor or modified Softplus is introduced.
The intervention is initialization only; the gap can still shrink during fitting.

Validation cohort: FD001, both architectures, both original weighted and unweighted
objectives, all original30 synthetic fitting fleets per configuration. n=60;
120 intervention fits total. Inherited budgets: LSTM LR.0002/10 epochs, hybrid
LR.001/7 epochs. Raw and corrected probability reuse each weighted state.
Evaluate on the original independent final/uniform fleets, n=100 and10000.
Literal removal criterion: zero collapsed completed states among30 per architecture
and objective, with no failed/missing state. Report actual counts even if this fails.
Quantile-quality safeguard: separately report paired mean oracle quantile-MAE change
and event-probability error. Do not call the intervention an adequate fix if gap
removal is achieved with worse mean oracle quantile error. Report incompatibility
changes irrespective of direction; do not equate compatibility with calibration.
This validates only FD001-shaped synthetic experiments, not every real subset.
No fallback intervention, retuning or extension is authorized by a disappointing
result; a failed fixed-init test is a retained outcome.

## Real-model weighting attribution

All40 frozen equal-search states: compute raw sigmoid(r) and correction
sigmoid(r-log(w)) from saved logits and original TRAINING weight. No temperature
fit, calibration fit, test-label optimization or changed nominal quantiles.
Use the five original seeds1101/1202/1303/1404/1505 in each of8 groups; all official-
test final engines remain. For each group report both rates/distances with paired
engine-bootstrap CIs, raw-minus-corrected percentage points, resolved violations,
newly introduced violations and their signed net. Report proportional net reduction
(raw-corrected)/raw without clipping; zero denominator is NA. A negative result is
mandatory. This is an operational effect of a fixed logit correction, not a causal
claim that a percentage of scientific error is explained by weighting.

Unweighted-BCE retrain: FD001 only, BOTH architectures, all5 original seeds =10
fits. Original fitting/validation/calibration partitions, preprocessor, fitting
windows, selected LR/epochs, batch128, AdamW decay.0001, clipping1, summed pinball
plus.5 BCE with w=1. Use original DEFAULT initialization, NOT the proposed gap fix,
so only the weighting objective changes. Start from each saved initial state;
verify reconstruction of the seeded initial RNG/state against it before training.
Train on CPU torch2.14.0+cpu to match frozen cohort device/build. No new selection;
no use of official-test results until these fixed refits complete. Save all states,
histories, input hashes and predictions. Verify test/cal input reconstruction
against original weighted checkpoint predictions before interpreting refits.
Report raw weighted vs corrected weighted vs retrained unweighted for FD001, with
paired seed correspondence and ENGINE-resampling CIs. The total retraining effect
can change both quantile and risk heads; it is distinct from the fixed-quantile
logit correction. Do not add the two effects or extrapolate to FD002-FD004/N-CMAPSS.
Also show quantile-gap/collapse status using calibration engines for all refits.

## Failures, checks, provenance and interpretation

All2000-draw bootstrap comparisons use common sampled engine IDs across variants,
models and paired contrasts. New real-bootstrap seeds:2026110101 (calibration),
2026110102 (test); synthetic resampling reuses original weights. Model initialization,
training data and permutations retain original paired seeds. No additional tuning
seed or outcomes-based seed/subset replacement. Failed diagnostic arms remain NA
with error files and counts, and the rest of the matrix continues when safe.
Nonfinite oracle/input/output, missing original states, changed paper model source,
wrong initial-state reconstruction or unmatched engine identities block affected
comparisons until investigated. Archive input/code/config hashes, commands, all
states and configurations. Exact AI/build provenance is inherited and refreshed
from current-session metadata where available; unexposed served checkpoints stay
unavailable. No assistant supplies numeric results. Original results are retained.

Report all favorable/unfavorable changes. Conditional non-collapsed nulls are not
unconditional reference distributions; the threshold and membership depend on a
quantile-quality diagnostic. Empty/sparse cases and the five-seed statistic mismatch
limit conclusions. Report the measured exceedance counts and weighting contrasts
without claiming that weighting/estimation/optimization contributions sum to a
causal decomposition. Failure of the initialization intervention or lack of clear
factorial effects is a completed negative result, not grounds for silent retuning.

### Pre-execution instrumentation clarification
The6 default factorial cells will additionally be replayed with instrumentation
rather than inventing absent historical clipping diagnostics. Original baseline
states/predictions remain unchanged and are used for all original-null tables.
Compare the replayed states/predictions against their originals and report any
numerical discrepancy; block affected causal comparisons if forward differences
exceed0.001 cycles/logit units or1e-5 relative tolerance. These replays are duplicate
computations of the same fitting fleets, NOT six additional independent samples.
Total new synthetic training executions:120 fixed-init fits +84 other ablation
fits +6 instrumented default replays =210. Six fixed-init-only factorial cells
reuse the identical fixed-init validation states. No outcomes were calculated
before this clarification; it resolves availability of per-step instrumentation.

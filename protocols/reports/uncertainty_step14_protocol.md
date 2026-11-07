# M3: protocol reconciliation and 20 paired split/seed replications

Written 2026-10-29 before the additional training or results. All C-MAPSS
benchmarks were previously examined. This is retrospective uncertainty
analysis, not public preregistration or fresh-data confirmation. Preserve
every historical model, table, source, partition and result.

## Cohort and computational design

Extend the fixed-schedule LSTM/hybrid comparison on all four C-MAPSS subsets
from five to 20 paired training/split replications. Reuse exactly the five
verified baseline cohorts (seeds 101,202,303,404,505). Add seeds 1001 through
1015, selected here before new scoring. Independently redraw an 80/20
fitting/held-out engine partition using sklearn train_test_split with that
seed, matching the original splitting rule. Refit preprocessing on fitting
engines only. The held-out training engines never select an epoch or model.

For each new subset/seed pair train LSTM and hybrid with the stage9 protocol:
18 features, 30-cycle complete training windows, capped RUL125, event raw
RUL<=30, summed three pinball means plus .5 weighted BCE, class weight from
fitting windows, batch128, AdamW lr .0005 weight decay .0001, clip1, final
epoch16, same task-gradient-sum wrapper with projection disabled. Per-epoch
permutations use seed*1000+epoch exactly as the controlled baseline. CPU
float32, deterministic algorithms, one thread per worker, six workers.
Different architectures cannot share identical initialization/dropout masks.

Extend FD001 PCGrad versus naive hybrid from five to 20 using the same 15 new
split/seed pairs. Use the existing PCGrad wrapper, projection only on shared
trunk, identical initial weights/data/permutations/dropout stream within each
hybrid/PCGrad pair. The new naive hybrid controls are reused here, not trained
or counted twice. No new RUL-only or TCN runs: those historical arms remain
five-replication descriptive comparisons. The equal-search comparison also
remains five final seeds on one fixed split and has unquantified selection
uncertainty; do not claim 20 reruns for it or retune configurations.

New training: 15*4*2 +15=135 models. Combined comparison: 160 architecture
results plus 20 PCGrad results, 180 unique model fits including 45 reused
historical fits. All 135 new final checkpoints must be complete and frozen
before any new official-test scoring. Save roles/scalers, class counts,
permutation/RNG hashes, initial/final hashes, history and progress. Resume only
the identical protocol and restore optimizer/RNG state; do not reroll.

## Primary statistics, fixed before new scoring

Five primary contrasts: hybrid-minus-LSTM RMSE in each of FD001-FD004 and
PCGrad-minus-naive RMSE in FD001. Calculate per-replication capped RMSE from
paired per-engine official-test predictions; report mean difference, paired
SD, median and fraction favoring the first arm. All differences have a fixed
sign convention. No engineered practical-significance threshold is asserted.

Use 10,000 deterministic bootstrap draws, RNG seed 141421. Report three
empirical percentile intervals: (a) engine-only with all fitted replications
fixed; (b) replicate-only with the observed fleet fixed; (c) crossed replicate
and engine resampling. In (c), draw 20 paired replicate indices and N engine
indices independently; reuse the same engine draw across all sampled
replications and both arms. The statistic is mean over sampled replications
of each arm's root mean squared error on sampled engines, then their
difference. Preserve arm/seed/engine pairing; do not treat each seed as a new
fleet or resample engines independently inside each seed. Also report
Bonferroni 99% crossed intervals for the five prespecified contrasts, alongside
pointwise 95% intervals. Their nominal family-wise interpretation requires
validity of each marginal bootstrap approximation and is not guaranteed here.

As conditional sensitivity, calculate two-sided exact Wilcoxon signed-rank
tests on the 20 paired replication differences (zero handling documented,
average ranks for absolute ties), with Holm adjustment over the five contrasts.
The null assumes independent exchangeable/symmetric run differences conditional
on the fixed source dataset and official test fleet. These are not tests across
20 independent datasets or fleets and do not resolve data-selection bias.
Report the assumptions, all adjusted values and all adverse/uncertain outcomes.
Do not infer equivalence from a non-rejection or use p-values to select models.

Repeat the three bootstrap decompositions descriptively for the four historical
equal-search contrasts with n=5, without a new significance claim. These
intervals capture empirical variation of only five frozen fits and engines;
they exclude tuning/configuration-selection uncertainty and new training-pool
sampling. Existing engine-only intervals remain labeled as historical,
conditional results. The new bootstrap does not turn 5 fits into 20.

## Reconciliation and limits

Audit original Table3, controlled Table7/8 and equal-search Table9 by source,
checkpoint/parameter hash, sample population, partition, sampler/RNG schedule
and checkpoint-selection rule. Archived notebook original training uses a
continuously seeded DataLoader generator and one summed-loss backward pass;
controlled training uses separately seeded epoch permutations and task-gradient
aggregation. Verify differing first-epoch orders rather than speculating about
cuDNN. Same architecture/hyperparameter labels/seed do not mean identical
training paths or identical fitted weights. Verify Table7/8 reused FD001
naive states and predictions match exactly. Attribute cross-protocol score
changes to changed experimental conditions collectively; no isolated causal
attribution to a single implementation difference without an intervention.

Resampling the observed fitted runs approximates combined partition/training
randomness. It does not separately identify optimizer versus partition variance,
refit models inside the bootstrap, model hyperparameter-selection uncertainty,
represent an independent training-engine population, or supply field validity.
All test fleets and C-MAPSS data have been inspected previously. Report the new
20-replication results separately from every original five-replication table.
Update abstract/contribution/discussion to the observed strength of evidence,
including unsupported superiority/PCGrad claims, without deleting old outcomes.

Methodological sources consulted: Owen and Eckles (2012), Bootstrapping data
arrays of arbitrary order, https://doi.org/10.1214/12-AOAS547; Holm (1979),
https://www.jstor.org/stable/4615733; Demsar (2006),
https://jmlr.org/papers/v7/demsar06a.html. Crossed resampling is used as an
empirical sensitivity analysis; those references do not guarantee coverage of
this nonlinear RMSE statistic or justify treating runs as independent datasets.

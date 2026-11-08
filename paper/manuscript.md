---
bibliography: references.bib
link-citations: true
---

# Compatibility of Quantile and Event-Probability Outputs in Remaining Useful Life Prediction: Event-Head Corruption Detection and Scoring Changes under Label-Free Projection

**Amirhossein Mozafari**  
Department of Computer Science, Sharif University of Technology, Tehran, Iran  
Corresponding author: `amir.mozafari04@sharif.edu`

## Abstract

Multi-head models for remaining useful life (RUL) prediction can report quantiles and near-term failure probabilities that disagree, complicating maintenance interpretation. We study a quantile-implied incompatibility distance $d$ and a label-free projection, $p_{\mathrm{proj}}=\operatorname{clip}(p,L,U)$. On C-MAPSS, the original eight groups share 707 test engines. Flags detect gross uniform event-head replacement and probability inversion, whereas a -1 logit shift lowers their rate. Flags concentrate near the event threshold: 49.7% within RUL 20–40 versus 8.2% elsewhere. RUL-only Brier associations are positive overall but differ in sign after probability-and-band adjustment. The pooled point-error association is undetected; its approximate 80%-power minimum detectable effect is 162 cycles squared. Across the expanded 44 groups, projection slightly lowers pooled Brier and NLL, with inconsistent group effects. Its Brier gain is resolved in FD002 and FD004 and unresolved in FD001 and FD003. TrainOff has lower pooled Brier and NLL than projection alone, largely driven by FD002, but has worse Brier than projection in 17 groups, including all 11 FD001 groups, and worse NLL in 15 by point estimate. No paired CI compares these paths. The exploratory study uses examined data from a single benchmark; projection guarantees the necessary structural bounds, while its scoring benefit remains empirical and varies across groups.

**Keywords:** remaining useful life; C-MAPSS; quantile–probability compatibility; calibration; label-free projection.

## 1. Introduction

Maintenance interpretation depends on what a prognostic output describes. Conditional RUL quantiles summarize the predicted distribution of time to failure, whereas an event head estimates the probability of failure within a specified horizon. A model that supplies both outputs should present a consistent account of the same event. A low near-term failure probability alongside quantiles that place failure before the horizon, or the converse disagreement, can make the outputs difficult to reconcile when considering maintenance actions. This study examines that structural disagreement; it does not evaluate maintenance decisions or safety outcomes.

Multi-head RUL models can estimate quantiles and event probabilities separately, without requiring them to correspond to one conditional distribution. Weighted classification losses can further displace the event probability from the unweighted target. We examine this compatibility problem on C-MAPSS [@saxena2008cmapss; @saxena2008damage]. Quantile ordering supplies necessary bounds on the event probability [@koenker1978regression], allowing disagreement to be identified without observing the outcome.

Structural compatibility, probability calibration and prediction error answer different questions. An output can satisfy the quantile-implied bounds and still be inaccurate or poorly calibrated. Conversely, a probability transformation can improve a proper score while increasing disagreement with the quantiles. The practical question is therefore whether the diagnostic identifies useful forms of disagreement and what scoring trade-offs arise when that disagreement is removed.

```{=latex}
\Needspace{12\baselineskip}
```

The study makes the following contributions:

- Formalizes a label-free compatibility diagnostic from quantile ordering and evaluates projection onto its necessary probability bounds.
- Tests sensitivity to event-head corruption and quantile perturbation, and examines threshold concentration, error associations and detectable effects on C-MAPSS.
- Compares projection with analytical training-weight correction (TrainOff) and fitted post-hoc calibrators across 44 model groups, reporting both favorable and unfavorable effects.

## 2. Related work

Probabilistic forecast assessment separates agreement with observations from concentration of the predictive distribution. Gneiting, Balabdaoui and Raftery distinguish calibration from sharpness [@gneiting2007calibrationsharpness]. Gneiting and Ranjan develop prediction spaces for forecast combination and distinguish coherence, probabilistic and conditional calibration, and dispersion [@gneiting2013combining]. These distinctions motivate assessing structural compatibility separately from outcome-based calibration. They do not establish the usefulness of the present flag or supply its finite-grid cross-head construction.

Quantile ordering provides the basis for the construction. Koenker and Bassett introduce regression quantiles for estimating conditional quantile functions [@koenker1978regression]. Chernozhukov, Fernández-Val and Galichon study monotone rearrangement to remove crossings in estimated quantile and probability curves [@chernozhukov2010crossing]. Ordering the quantiles addresses crossings within those estimates, but does not by itself make a separate event head agree with them. The bounds studied here express that additional requirement.

Proper scores assess predictions against realized outcomes. Gneiting and Raftery develop the proper-scoring framework used for our Brier and NLL comparisons [@gneiting2007scoring]. Guo et al. examine post-hoc neural-network calibration and temperature scaling [@guo2017calibration], while Silva Filho et al. review calibration definitions, metrics and post-hoc maps [@silvafilho2023calibration]. These works support comparing projection with probability calibration, without implying a particular empirical ranking on the engines studied here.

For RUL prediction, Javanmardi and Hüllermeier conformalize point predictors into intervals and evaluate them on C-MAPSS [@javanmardi2023conformal]. Their work addresses interval prediction and coverage. Our question concerns whether quantile and event-probability heads can describe the same event, even before their predictions are compared with outcomes. Compatibility is a necessary structural condition rather than an interval-coverage or calibration guarantee.

## 3. Methodology: compatibility diagnostic and post-hoc corrections

### 3.1 Quantile-implied probability bounds

Let $p$ denote the predicted probability of failure within horizon $h$. For $h=30$ and quantile levels $\tau\in\{0.05,0.50,0.95\}$, the ordered quantiles imply the bounds

$$
L(h)=\max\bigl(\{0\}\cup\{\tau:q_\tau\le h\}\bigr),\qquad
U(h)=\min\bigl(\{1\}\cup\{\tau:q_\tau>h\}\bigr),
$$

$$d=\max\{L(h)-p,\ p-U(h),\ 0\}.$$

The lower bound collects quantile levels whose predicted RUL is at or below the horizon; the upper bound collects levels whose predicted RUL is above it. The distance measures how far the event probability lies outside that interval. Satisfying these inequalities does not establish a calibrated or accurate common distribution. Disagreement can arise from separate estimation, objective weighting, approximation, optimization or sampling effects.

The primary validation flag is $d>0$. Table 2 uses the earlier $d>10^{-6}$ convention. Distances are averaged over all engines, including those with zero distance.

### 3.2 Label-free projection

Projection replaces the event probability with the closest value within the quantile-implied interval, leaving the quantiles unchanged:

$$p_{\mathrm{proj}}=\operatorname{clip}(p,L,U).$$

This operation requires no outcome labels and enforces the necessary bounds by construction. Whether the replacement improves a proper score depends on the observed outcomes and is evaluated separately. Each calibrator can also be followed by the same projection.

### 3.3 Weight correction and fitted calibration paths

Let $r$ be the event-head logit, $\sigma$ the sigmoid function and $w$ the positive-class weight used in training. The positive-class-weighted BCE population optimum differs from the target event probability. TrainOff removes the corresponding logit offset using the actual training weight; it is an analytical correction, not a map fitted to calibration labels. With temperature $T$, the three paths are

$$p_{\mathrm{TrainOff}}=\sigma(r-\log w),\qquad p_{\mathrm{Temp}}=\sigma(r/T),\qquad p_{\mathrm{TrainOff+Temp}}=\sigma((r-\log w)/T).$$

Temperature is fitted on calibration engines by minimizing binary NLL within the original implementation bounds. Platt calibration fits an affine transformation of the raw logit, $p_{\mathrm{Platt}}=\sigma(a r+c)$. Isotonic calibration fits a nondecreasing map of the raw probability. Beta calibration uses $p_{\mathrm{Beta}}=\sigma(c+a\log p-b\log(1-p))$, with the implementation’s probability clipping and unconstrained fitted coefficients. Platt and Beta use the implementation’s coefficient penalty, excluding the intercept. When calibration outcomes contain only one class, fitted calibration paths use the implementation’s smoothed constant probability.

## 4. Experimental setup

### 4.1 Benchmark, model groups and evaluation roles

The benchmark models have ordered quantile heads and a separate event head. For the original eight equal-search groups, C-MAPSS fitting/validation/calibration engine counts are 60/20/20 for FD001 and FD003, 156/52/52 for FD002, and 149/50/50 for FD004. Official testing uses each engine’s final observed window. LSTM and hybrid each use five seeds fixed before this analysis; the hybrid combines recurrent and causal convolutional branches. Model selection used validation error. Architecture details are provided in the supplement.

The expanded comparison uses existing calibration and test predictions for 44 groups and 220 fixed fits on the same 707 distinct official-test engines. It includes the original eight equal-search groups, the TCN/GRU equal-search extension, the original hybrid runs with their own calibration partitions, and extra LSTM/hybrid/GRU/TCN controls, including the additional LSTM/hybrid CV controls. The expanded roster has 518 distinct calibration engines across its recorded partitions, compared with 142 for the original eight groups. Each map is fitted separately on the calibration engines belonging to that fit. The paths are raw, projection, TrainOff, Temp, TrainOff+Temp, Platt, Isotonic and Beta, with each calibration path also followed by projection.

The point target is RUL capped at 125, and the event label is true RUL at most 30. Benchmark RMSE and MAE use projected medians in [0,125]. The error-association analysis uses squared error of the original unprojected median. Probability error is the binary quadratic contribution $(p-y)^2$, consistent with proper-scoring assessment [@gneiting2007scoring]. Seed variation in the benchmark tables is reported as sample SD.

The main evidence comes from C-MAPSS models held fixed during analysis. Quantile perturbations, weighting comparisons and event-head controls examine different sources of disagreement. The synthetic experiment is a pipeline check with a known data-generating law (Supplement S0a), with its full percentile table in Table S11. It does not validate or benchmark the real-data incompatibility rates.

### 4.2 Outcomes, uncertainty and reporting

Engine-level cluster bootstrap intervals keep each engine’s complete set of model predictions together. Within each subset, LSTM and hybrid share the same engines, and all five seeds reuse that fleet; the original eight groups are not independent. That roster contains 707 distinct test-engine clusters and 142 distinct calibration engines. The expanded 44-group roster uses the same 707 test engines and 518 distinct calibration engines across its recorded partitions. Calibration partitions differ across fits. Original pooled estimates average architectures within each subset and weight subsets by engine count. Expanded-roster estimates average fixed groups within each engine before weighting subsets by engine count. Pooled adjusted coefficients are weighted averages of group-specific coefficients, rather than a common-slope regression coefficient.

RUL-adjusted regressions use the original cubic capped-RUL covariate and seed intercepts. Additional adjustment includes raw probability and the threshold band. Minimum detectable effects use the approximation specified in Table 1; they do not replace an exact power simulation.

NLL uses scoring-time clipping at $10^{-15}$. ECE5 uses five probability-quantile bins, and ECE10 uses ten equal-width bins. Boundaries use no labels and remain fixed during bootstrap. ECE is averaged across fixed models rather than calculated from a mixture probability.

Rates and their CIs are reported as percentages to one decimal; rate differences are percentage points. Regression coefficients and CIs use three significant figures. Benchmark Brier values retain source precision. Continuous scores, differences and CIs in the controls/projection analysis use three significant figures, with full precision in the companion CSVs. The supplement identifies source files and supplies full-precision companions.

### 4.3 Analysis development and exploratory scope

The original prespecified joint rule returned “not informative” (Supplement S0). After examining benchmark and diagnostic results in the original eight groups, we added the error-association follow-ups, positive controls, detectable-effect assessment and direct projection, then expanded the comparison to 44 model groups and additional calibrators. Later protocols specified each calculation before it was run, but the questions were chosen after earlier results. The expansion tests consistency across model configurations on the same test engines; it is not validation on an independent dataset. Supplement S0d documents the full analysis sequence.

## 5. Results and discussion

### 5.1 Baseline incompatibility and perturbation robustness

Table 2 summarizes incompatibility frequency and distance in the original eight equal-search groups. Each group averages five fits on the same test engines. These rates describe disagreement between outputs, not the probability that a model is faulty.

```{=latex}
\Needspace{19\baselineskip}
\setcounter{table}{1}
```

| Subset | Model | Test engines | Raw incompatible (%) | Temp incompatible (%) | Raw mean distance |
|---|---|---|---|---|---|
| FD001 | LSTM | 100 | 20.4 ± 4.6 | 31.4 ± 2.3 | 0.0210 ± 0.0061 |
| FD001 | Hybrid | 100 | 13.6 ± 3.9 | 18.6 ± 5.0 | 0.0138 ± 0.0075 |
| FD002 | LSTM | 259 | 9.6 ± 1.4 | 11.2 ± 0.9 | 0.0067 ± 0.0021 |
| FD002 | Hybrid | 259 | 8.9 ± 2.7 | 13.4 ± 6.9 | 0.0072 ± 0.0040 |
| FD003 | LSTM | 100 | 12.8 ± 4.1 | 25.0 ± 5.8 | 0.0150 ± 0.0081 |
| FD003 | Hybrid | 100 | 11.8 ± 3.3 | 36.2 ± 12.4 | 0.0149 ± 0.0113 |
| FD004 | LSTM | 248 | 16.6 ± 2.1 | 16.7 ± 2.8 | 0.0137 ± 0.0029 |
| FD004 | Hybrid | 248 | 12.7 ± 2.5 | 15.3 ± 6.6 | 0.0086 ± 0.0031 |

: Frozen C-MAPSS compatibility results, mean ± sample SD. Rates use the retained tolerance convention; distance is in probability units. Temp changes the probability while nominal quantiles remain fixed. Engine counts are per fit, not multiplied by seeds.

To assess sensitivity to quantile changes, we added noise to the lower and upper quantiles as a fraction of their predicted width. For FD001 LSTM, incompatibility rates at noise levels 0.0%, 5.0%, 10.0% and 20.0% are 20.4%, 20.5%, 20.4% and 21.0%, respectively, on the same 100 test engines. The largest point-estimate increase at 20.0% noise is 2.5 percentage points, for FD002 hybrid on 259 test engines (95% CI [1.7, 3.4] percentage points). The full curves, distances and crossing counts appear in Table S3. Sensitivity is low under this perturbation scheme.

We also examined whether collapsed quantile gaps could explain the behavior. Collapse is defined by a median lower softplus gap below 1.25 cycles. No real-model fit collapses under this definition on the 20/52/20/50 calibration engines for FD001–FD004. Supplement S0b and Tables S4a–S4c and S5 report the synthetic initialization and optimization checks descriptively.

### 5.2 Corruption detection and threshold proximity

The positive controls alter the event head while holding the quantiles fixed in the original eight groups. Uniform replacement and 1-p are gross corruptions for which high flag rates are expected. On 707 test engines, pooled incompatibility and 95% engine-bootstrap CIs are 12.7% [11.1%, 14.4%] for raw predictions, 88.3% [87.3%, 89.3%] for uniform replacement, and 96.3% [95.4%, 97.2%] for 1-p. Uniform replacement averages 100 fixed draws per engine/run. A +1 logit shift gives 18.7% [16.5%, 21.1%], whereas a -1 shift gives 8.0% [6.9%, 9.2%]. Thus, the +1 shift raises the pooled rate only from 12.7% to 18.7%, while the -1 shift lowers it. Detection depends on corruption direction, and the modest positive-shift response is consistent with the low sensitivity to quantile noise. Table S13a gives each group’s rate and mean distance with CIs.

Across the original eight groups and 707 distinct engines, pooled incompatibility is 49.7% in the true-RUL 20–40 band (76 engines) and 8.2% elsewhere (631 engines), averaging the fixed models within each engine. The band has higher incompatibility in every original real-model group (Tables S9a–S9b). The band contains 15/22/10/29 engines and its complement 85/237/90/219 engines for FD001–FD004. For FD001 LSTM, rates are 50.7% in the band and 15.1% elsewhere (15 and 85 test engines). The band surrounds the event horizon and identifies where the outputs most often disagree in this benchmark. Its higher flag rate alone does not establish greater decision value or general fault-detection ability.

### 5.3 Error associations and minimum detectable effects

The RUL-adjusted association analysis distinguishes point error from probability error. Table 1 reports coefficients, CIs, relative upper endpoints and approximate minimum detectable effects for every original group. On 707 engines, the pooled median-error coefficient is -85.6 cycles squared, CI [-191, 37.1]. Its upper CI endpoint is 14.8% of the group-weighted mean squared error. The approximate 80%-power MDE is 162 cycles squared, or 64.4% of that mean. The undetected pooled association is therefore underpowered for effects smaller than this MDE; it does not establish their absence.

```{=latex}
\setcounter{table}{0}
```

| Group / outcome | Fit / test engines | Flag coefficient [95% CI] | Own mean MSE | Upper CI / mean | Approx. MDE (MDE / mean) |
|---|---|---|---|---|---|
| FD001 lstm median error | 60/100 | 69.7 [-167, 405] | 217 | 187.0% | 429 (198.1%) |
| FD001 lstm Brier | 60/100 | 0.0426 [-0.0369, 0.124] | 0.0356 | 348.9% | 0.115 (324.3%) |
| FD001 hybrid median error | 60/100 | -250 [-415, -95.3] | 259 | -36.8% | 227 (87.6%) |
| FD001 hybrid Brier | 60/100 | -0.0143 [-0.0887, 0.055] | 0.0348 | 158.1% | 0.105 (301.0%) |
| FD002 lstm median error | 156/259 | -138 [-240, -51] | 205 | -24.8% | 136 (66.3%) |
| FD002 lstm Brier | 156/259 | 0.0908 [0.0332, 0.155] | 0.0251 | 615.7% | 0.0889 (354.4%) |
| FD002 hybrid median error | 156/259 | -149 [-311, -4.99] | 241 | -2.1% | 214 (88.7%) |
| FD002 hybrid Brier | 156/259 | 0.103 [0.0365, 0.171] | 0.0333 | 513.2% | 0.0945 (283.6%) |
| FD003 lstm median error | 60/100 | -320 [-595, -71] | 323 | -22.0% | 380 (117.6%) |
| FD003 lstm Brier | 60/100 | 0.0822 [0.0155, 0.179] | 0.0267 | 672.7% | 0.12 (450.5%) |
| FD003 hybrid median error | 60/100 | -99.9 [-230, 29] | 234 | 12.4% | 186 (79.3%) |
| FD003 hybrid Brier | 60/100 | 0.129 [0.0524, 0.209] | 0.0291 | 716.3% | 0.113 (387.4%) |
| FD004 lstm median error | 149/248 | -36.3 [-276, 258] | 275 | 93.8% | 384 (139.6%) |
| FD004 lstm Brier | 149/248 | 0.124 [0.0554, 0.202] | 0.0529 | 382.0% | 0.106 (200.6%) |
| FD004 hybrid median error | 149/248 | 90.2 [-147, 429] | 274 | 156.5% | 430 (157.0%) |
| FD004 hybrid Brier | 149/248 | 0.103 [0.0247, 0.187] | 0.0448 | 416.7% | 0.117 (260.6%) |

: Adjusted effects and approximate power. Point-error units are cycles squared; Brier is event-probability MSE. Each ratio uses its outcome's own observed mean. MDE is (normal 97.5th percentile + normal 80th percentile) times the engine-bootstrap coefficient SD, for a two-sided 0.05 Wald approximation. It is not an exact power simulation. Signed upper bounds are retained. Table S14 gives full results, including pooled estimates.

The pooled RUL-only Brier coefficient is positive, 0.0922 [0.0589, 0.126], on 707 engines. The positive group intervals in FD002–FD004 indicate larger Brier error among flagged engines under this adjustment. FD001 does not establish that pattern. Table 1 gives every group coefficient and interval, avoiding a common-sign interpretation unsupported by the individual results.

Four median-error coefficients have engine-bootstrap CIs wholly below zero: FD001 hybrid -250 [-415, -95.3] on 100 engines; FD002 LSTM -138 [-240, -51] and hybrid -149 [-311, -4.99] on 259 engines; and FD003 LSTM -320 [-595, -71] on 100 engines. The negative associations remain unexplained. One hypothesis is that event-head displacement can produce disagreement even when the median is accurate. Another is that the cubic RUL adjustment leaves residual differences in engine difficulty or lifecycle position. Neither explanation was tested, and these associations do not show that incompatibility improves point prediction.

Adding raw probability and threshold-band adjustment leaves no detectable incremental Brier association in most original groups. In that follow-up, FD001 hybrid has a negative coefficient, -0.110, CI [-0.206, -0.0112], whereas FD003 hybrid has a positive coefficient, 0.0481, CI [0.00764, 0.0878]; each uses 100 test engines and 60 fitting engines. The sign therefore differs across groups. This adjustment removes overlapping information: the flag is determined by probability and quantiles, while Brier is determined by probability and the event label. Conditioning on probability and the band does not algebraically fix the flag, because the quantiles can still vary.

The expanded-roster reanalysis preserves this contrast. The original FD001 hybrid group has a negative probability-plus-band-adjusted Brier coefficient, -0.110, CI [-0.207, -0.0102], and the original FD003 hybrid group has a positive coefficient, 0.0481, CI [0.00852, 0.0867]; each uses 100 test engines and 60 fitting engines. These extension intervals use the extension bootstrap draws and are separate from the earlier follow-up intervals reported above.

Among the 36 added groups, RUL-only Brier coefficients are positive in 35, with CIs excluding zero in the positive direction in 28. After probability-and-band adjustment, no added group has a positive CI and one has a negative CI. RUL-only median-error CIs are negative in 7 added groups, with no positive CI. Across all 44 groups, 11 RUL-only median-error CIs lie below zero and none above it. Intervals excluding zero thus agree in sign, but the negative point-error association remains unexplained. E_associations.csv gives all coefficients, CIs, own-mean ratios, regression engine counts and approximate MDEs for both outcomes and all adjustments. Undefined bootstrap coefficients are counted explicitly rather than replaced by zero.

### 5.4 Projection, analytical weight correction and calibrators

The baseline architecture comparison provides context for the corrections. Table 3 reports point accuracy and raw Brier for the same C-MAPSS LSTM/hybrid groups. Rankings depend on the output being assessed; point accuracy and probability error should therefore be considered separately.

```{=latex}
\setcounter{table}{2}
```

| Subset | Model | Fit/test engines | RMSE (cycles) | MAE (cycles) | Raw Brier |
|---|---|---|---|---|---|
| FD001 | LSTM | 60/100 | 14.7 ± 0.639 | 10.9 ± 0.448 | 0.03561 |
| FD001 | Hybrid | 60/100 | 15.9 ± 1.25 | 11.8 ± 0.716 | 0.03477 |
| FD002 | LSTM | 156/259 | 14.3 ± 0.528 | 9.87 ± 0.445 | 0.02510 |
| FD002 | Hybrid | 156/259 | 15.4 ± 1.44 | 10.8 ± 1.42 | 0.03333 |
| FD003 | LSTM | 60/100 | 17.9 ± 1.07 | 12.5 ± 0.810 | 0.02666 |
| FD003 | Hybrid | 60/100 | 15.2 ± 0.784 | 11.0 ± 0.961 | 0.02915 |
| FD004 | LSTM | 149/248 | 16.6 ± 0.340 | 11.1 ± 0.429 | 0.05290 |
| FD004 | Hybrid | 149/248 | 16.5 ± 0.336 | 11.6 ± 0.518 | 0.04484 |

: Secondary architecture comparison. RMSE and MAE show mean ± sample SD to three significant figures; Brier retains source precision. Fitting and test engines are explicit for each row. Seeds reuse the same engines.

Weight correction and unweighted retraining affect different learned quantities. For FD001 LSTM, raw incompatibility is 20.4%, TrainOff gives 18.0% on 100 test engines, and unweighted retraining gives 18.8% on 100 test engines with 60 fitting engines. For FD001 hybrid, raw and TrainOff rates are 13.6% and 12.2%, whereas unweighted retraining gives an adverse 21.6% on 100 test engines with 60 fitting engines. The correction and retraining effects are not added (Tables S6a–S6b).

Table 4 compares Raw, TrainOff, Temp and TrainOff+Temp in the original eight groups. Section 5.4 and A_all_scores.csv give the expanded comparison with Platt, Isotonic, Beta and projection. Temperature increases the Table 2 mean incompatibility in every group, while its Brier changes differ across groups. For FD001 LSTM, TrainOff lowers incompatibility from 20.4% to 18.0% but increases Brier from 0.03561 to 0.05276 on 100 test engines. Compatibility and probability error therefore require separate assessment.

| Subset | Model | Test engines | Raw Brier | TrainOff Brier | Temp Brier | TrainOff+Temp Brier |
|---|---|---|---|---|---|---|
| FD001 | LSTM | 100 | 0.03561 ± 0.00429 | 0.05276 ± 0.00569 | 0.04191 ± 0.00368 | 0.05722 ± 0.00906 |
| FD001 | Hybrid | 100 | 0.03477 ± 0.00728 | 0.04555 ± 0.00874 | 0.03656 ± 0.00793 | 0.05030 ± 0.01049 |
| FD002 | LSTM | 259 | 0.02510 ± 0.00343 | 0.01361 ± 0.00301 | 0.03357 ± 0.00673 | 0.01507 ± 0.00702 |
| FD002 | Hybrid | 259 | 0.03333 ± 0.01419 | 0.02090 ± 0.00967 | 0.03598 ± 0.01190 | 0.02314 ± 0.00930 |
| FD003 | LSTM | 100 | 0.02666 ± 0.00860 | 0.02669 ± 0.00261 | 0.03403 ± 0.00747 | 0.02708 ± 0.00329 |
| FD003 | Hybrid | 100 | 0.02915 ± 0.01492 | 0.02207 ± 0.00476 | 0.03750 ± 0.01141 | 0.03268 ± 0.01069 |
| FD004 | LSTM | 248 | 0.05290 ± 0.00297 | 0.03499 ± 0.00236 | 0.05904 ± 0.00580 | 0.04141 ± 0.00720 |
| FD004 | Hybrid | 248 | 0.04484 ± 0.00384 | 0.03787 ± 0.00415 | 0.05017 ± 0.00972 | 0.04513 ± 0.00622 |

: Secondary calibration comparison for the original eight groups, showing Raw, TrainOff, Temp and TrainOff+Temp Brier mean ± sample SD at source precision. These paths use the same test engines within each row. Section 5.4 and the expanded-calibrator supplementary file A_all_scores.csv contain Platt, Isotonic, Beta and projection paths; Table S6b gives the original compatibility-by-method source table.

For the original eight groups, projection produces exactly 0.0% incompatibility on every calibration and test output. On 707 test engines, projected-minus-raw Brier is -0.00424 [-0.00647, -0.00226]. The corresponding changes are NLL -0.0156 [-0.0236, -0.00874], ECE5 -0.00855 [-0.0109, -0.00443], and ECE10 -0.00896 [-0.0118, -0.00584]. Calibration Brier changes by -0.00522 [-0.00964, -0.00163] on the original roster’s 142 distinct calibration engines. These observed scoring changes accompany the structural guarantee; they are not guaranteed by it.

Within the original roster, subset-level projected-minus-raw test Brier is FD001 -0.000343 [-0.006465, 0.005235] on 100 engines. For FD002, it is -0.004445 [-0.007203, -0.001986] on 259 engines. The FD003 difference is -0.003555 [-0.009740, 0.002375] on 100 engines. The FD004 difference is -0.005885 [-0.010457, -0.002046] on 248 engines. The subset-pooled gain is resolved in FD002 and FD004 and unresolved in FD001 and FD003. The FD001 LSTM point estimate is unfavorable, 0.00149 [-0.00668, 0.00964], on 100 engines. Table S13b gives all raw/projected scores and paired CIs for both roles, including the specified ECE5 and ECE10 conventions.

In the expanded roster, pooled raw and projected Brier are 0.036746 and 0.033041, with projected-minus-raw difference -0.003705 [-0.005605, -0.001977]. Pooled raw and projected NLL are 0.124702 and 0.111594, with difference -0.013108 [-0.019727, -0.007370]. TrainOff has lower pooled Brier, 0.028727, and NLL, 0.097836, than projection alone; its pooled advantage is driven largely by FD002. TrainOff followed by projection gives pooled Brier 0.028081 and difference versus raw -0.008665 (95% CI [-0.014042, -0.003373]). Its pooled NLL is 0.095831, with difference versus raw -0.028872 (95% CI [-0.047089, -0.011553]). No paired CI compares this combined path with either TrainOff or projection alone.

Temp, Platt, Isotonic and Beta worsen pooled NLL relative to raw, and Isotonic followed by projection also has an unfavorable NLL difference CI. A_all_scores.csv supplies every Brier, NLL, ECE5 and ECE10 comparison, including adverse results. These comparisons distinguish the effect of fitted calibration from the additional structural constraint imposed by projection.

TrainOff’s pooled advantage is not uniform. Its Brier differences versus raw classify 15 groups as better, 1 as worse and 28 as unresolved, using the same CI zero-exclusion rule as for projection. Point estimates are worse than raw in 14 of 44 groups, including all FD001 groups: equal-search LSTM, hybrid, TCN and GRU; original hybrid; and extra lstm_gpu, hybrid_gpu, gru_gpu, tcn_gpu, lstm_cv and hybrid_cv. They are also worse in FD003 equal-search LSTM and TCN and extra hybrid_cv. Only FD001 extra lstm_cv has a TrainOff-minus-raw CI wholly above zero. Against projection alone, TrainOff has worse Brier point estimates in 17 of 44 groups (FD001 11, FD002 0, FD003 5, FD004 1) and worse NLL in 15 of 44. It is worse in Brier in every FD001 group. No paired TrainOff-versus-projection CI is reported.

For projection-minus-raw Brier, 20 groups have CIs below zero, none has a CI above zero and 24 are unresolved; 11 point estimates are unfavorable. For NLL, the corresponding counts are 22, none and 22, with 6 unfavorable point estimates. Figure 1 shows the group-specific Brier differences. Because the groups share engines, these counts are not independent replications. C_dose_response.csv and D_mechanism.csv report the specified distance bins and mechanism results; mean predicted probability does not move uniformly toward the event base rate across groups.

![Projection-minus-raw Brier across the expanded 44-group roster. Points and 95% engine-bootstrap CIs are copied from A_all_scores.csv; lower values favor projection. Labels show test engines per group: FD001 100, FD002 259, FD003 100 and FD004 248. All 44 groups share 707 distinct official-test engines; fixed fits do not multiply these counts.](projection_brier_44_groups.png){width=95%}

```{=latex}
\FloatBarrier
```

For practitioners, these results support reporting compatibility alongside proper scores. Projection can enforce the quantile-implied bounds without calibration labels, but should not be selected on an assumption of uniform scoring improvement. Training-weight correction addresses a different source of probability displacement and should likewise be assessed for the relevant subset and outcome. The present comparisons do not establish a benefit for maintenance decisions or operational safety.

## 6. Limitations and conclusion

The diagnostic detects the tested gross event-head corruptions, with sensitivity that depends on corruption direction. Its threshold concentration and adjusted associations do not establish general fault detection, and the negative median-error associations remain unexplained. This is an exploratory study using examined data from a single benchmark. The expanded 44 groups share the same 707 engines, so additional model configurations do not supply independent-engine replication. Bootstrap CIs condition on the fitted models, calibration maps and analysis choices. DS01 (4 test engines) was descriptive only and was not validated [@ariaschao2021ncmapss].

Projection supplies a label-free guarantee of the necessary structural bounds, with a small and inconsistent scoring gain. TrainOff has lower pooled Brier and NLL than projection alone, largely driven by FD002, while individual groups can favor projection. Neither compatibility alone nor a favorable pooled proper score establishes that a correction is suitable for every deployment. PHM evaluations should retain the distinction between structural agreement, probability error and point error, and report the adverse group results alongside pooled improvements.

## Data and code availability

The repository https://github.com/amirhossein2004-mozafari/rul-quantile-event-compatibility contains code, protocols, result CSVs, saved predictions, reports, manuscript sources and the supplement. It excludes 185 hash-referenced files, including checkpoints, tensors, raw NASA data and other inputs, so the public release cannot support full retraining or full lock verification. NASA data can be downloaded from the NASA Prognostics Center of Excellence repository (https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/). Code is licensed under MIT, and derived results and saved predictions are licensed under CC BY 4.0. The validation supplement contains Tables S1–S14 with source-file labels and full-precision companion tables. The repository also includes the added-model comparisons. Monitoring, PCGrad, component ablations, path-maximum CV+ and multi-study comparisons remain supplementary.

## Authorship, funding and competing interests

Amirhossein Mozafari: conceptualization, methodology, software, validation, analysis, investigation, data curation, writing, visualization and project administration. No specific external funding was received. The author declares no known competing financial interests or personal relationships affecting this work.

## Declaration of generative AI assistance

Generative AI tools assisted with code scripting and correction, analysis scripts, figure preparation and formatting, language editing, manuscript revision, and numerical checks. The author has manually reviewed, verified, and takes full responsibility for all methodology, code, numerical results, and manuscript content.

## References

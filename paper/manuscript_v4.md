---
bibliography: references.bib
link-citations: true
---

# Compatibility of Quantile and Event-Probability Outputs in Remaining Useful Life Prediction: Event-Head Corruption Detection and Scoring Changes under Label-Free Projection

**Amir Hossein Mozafari**  
Department of Computer Science, Sharif University of Technology, Tehran, Iran  
Corresponding author: `amir.mozafari04@sharif.edu`

## Abstract

In the original eight C-MAPSS groups on 707 test engines, compatibility flags detect gross uniform event-head replacement and probability inversion. A -1 logit shift lowers the rate.

Flags concentrate near the event threshold: 49.7% within RUL 20–40 versus 8.2% elsewhere in this original roster. RUL-adjusted Brier associations are positive overall but vary in sign after probability-and-band adjustment. The pooled point-error association is undetected, with an approximate 80%-power MDE of 162 cycles squared.

In the expanded 44-group roster, TrainOff has lower pooled Brier and NLL than projection alone, largely driven by FD002. TrainOff has worse Brier than projection alone in 17 groups, including all 11 FD001 groups, and worse NLL than projection alone in 15 by point estimate. No paired CI compares these paths. Projection guarantees structural compatibility, with inconsistent scoring gains. Its pooled Brier gain is resolved in FD002 and FD004 and unresolved in FD001 and FD003. This is a single-benchmark, exploratory study that uses examined data and has not had independent human review. 

**Keywords:** remaining useful life; C-MAPSS; quantile–probability compatibility; calibration; label-free projection.

## 1. Problem and diagnostic definition

A joint RUL predictor may report conditional quantiles and a separately trained probability of near-term failure. Those outputs answer related questions but need not correspond to one conditional distribution. We examine their compatibility on C-MAPSS [@saxena2008cmapss; @saxena2008damage]. The diagnostic follows from quantile ordering [@koenker1978regression]. It is not an additional accuracy or calibration score.

For horizon $h=30$, quantile levels $\tau\in\{0.05,0.50,0.95\}$ and event probability $p$, define

$$
L(h)=\max\bigl(\{0\}\cup\{\tau:q_\tau\le h\}\bigr),\qquad
U(h)=\min\bigl(\{1\}\cup\{\tau:q_\tau>h\}\bigr),
$$

$$d=\max\{L(h)-p,\ p-U(h),\ 0\}.$$

The primary validation flag is $d>0$. Table 2 uses the earlier $d>10^{-6}$ convention. The reproduction check confirms its displayed raw means. We average distances over all engines, including those with zero distance. Passing this necessary condition does not establish a calibrated or accurate common distribution. Failure can arise from independently estimated outputs, objective weighting, approximation, optimization, or sampling effects.

**Central claim.** In the original eight groups, the flag detects the tested gross event-head corruptions and concentrates near the event threshold. Error associations require adjustment and power assessment. In the expanded 44 groups, projection slightly lowers pooled Brier and NLL, with 24 groups unresolved for Brier and 11 unfavorable point estimates. TrainOff has lower pooled Brier and NLL than projection alone.

The benchmark models have ordered quantile heads and a separate event head. For the original eight equal-search groups, the C-MAPSS fitting/validation/calibration engine counts are 60/20/20 for FD001 and FD003, 156/52/52 for FD002, and 149/50/50 for FD004; official testing uses each engine's final observed window. LSTM and hybrid each use five seeds fixed before this analysis. The hybrid combines recurrent and causal convolutional branches. The supplement gives full architecture details. Model selection used validation error. Section 2.6 describes the later analysis choices.

The point target is RUL capped at 125, and the event label is true RUL at most 30. Benchmark RMSE and MAE use projected medians in [0,125]. The error-association analysis uses squared error of the original unprojected median. Probability error uses the binary quadratic contribution $(p-y)^2$, consistent with the accessible proper-scoring treatment [@gneiting2007scoring]. All association intervals resample engines and keep each engine's complete set of model predictions. Seed variation in benchmark tables is reported separately as sample SD.

Within each subset, LSTM and hybrid share the same engines, and all five seeds reuse that fleet. The eight groups are therefore not independent. The original eight-group roster contains 707 distinct test-engine clusters across the four subsets and 142 distinct calibration engines. The expanded 44-group roster uses the same 707 test engines and 518 distinct calibration engines across its recorded partitions. Calibration partitions differ across fits. The original pooled estimates average architectures within each subset and weight subsets by engine count. The expanded roster in Section 2.8 averages its fixed groups within each engine before weighting subsets by engine count. CIs keep all repeated predictions when resampling an engine. Pooled adjusted coefficients are weighted averages of group-specific coefficients, rather than coefficients from a common-slope regression.

### 1.1 Related work

Gneiting, Balabdaoui and Raftery distinguish calibration, which concerns agreement between forecasts and observations, from sharpness, which concerns the concentration of the predictive distributions [@gneiting2007calibrationsharpness]. This supports assessing compatibility separately from outcome-based calibration and sharpness; it does not establish the empirical usefulness of this flag.

Gneiting and Ranjan study forecast combination through prediction spaces and distinguish coherence, probabilistic and conditional calibration, and dispersion [@gneiting2013combining]. This supports separating compatibility from calibration. Their paper concerns combining predictive distributions; the finite-grid cross-head bounds used here are our diagnostic construction. Chernozhukov, Fernández-Val and Galichon study monotone rearrangement to remove crossings in estimated quantile and probability curves [@chernozhukov2010crossing]. That work supports the quantile-ordering comparison, not a guarantee that a separately fitted event head agrees with those quantiles.

Gneiting and Raftery develop proper scoring rules for evaluating forecasts against realized outcomes [@gneiting2007scoring]. The Brier score is evaluated using the binary quadratic contribution defined above; proper-scoring theory supports this outcome-based comparison, not the empirical usefulness of the flag. Guo et al. evaluate post-hoc neural-network calibration and temperature scaling [@guo2017calibration]. Silva Filho et al. review calibration definitions, evaluation metrics and post-hoc maps [@silvafilho2023calibration]. These works support comparing probability transformations with projection; they do not predict the ranking of calibrators on these engines.

Koenker and Bassett introduce regression quantiles for estimating conditional quantile functions [@koenker1978regression]. Javanmardi and Hüllermeier conformalize point RUL predictors into intervals and evaluate them on C-MAPSS [@javanmardi2023conformal]. These works support distinguishing quantile estimation and interval prediction from the cross-head compatibility question studied here. The citation-to-claim checklist identifies the source used for each statement and the remaining author-verification item.

## 2. Validation of the diagnostic

We report rates and their CIs as percentages to one decimal. Differences in rates are percentage points. Regression coefficients and their CIs use three significant figures. Benchmark Brier values keep the source precision. The controls/projection analysis uses three significant figures for continuous scores, differences and CIs. Its companion CSVs give full precision. Counts, thresholds and protocol identifiers are unchanged. The validation supplement gives source files and full-precision machine-readable companions.

### 2.1 Real-model evidence and scope

The primary evidence comes from C-MAPSS models held fixed during analysis. We examine controlled quantile perturbations, RUL-adjusted error associations, probability and threshold-proximity adjustment, and weighting contrasts. The synthetic experiment serves only as a pipeline check with a known data-generating law in Supplement S0a. Table S11 gives its full percentile table. It is not used to validate or benchmark the real-data incompatibility rates.

### 2.2 Perturbation sensitivity and gap collapse

The perturbation experiment adds noise to the lower and upper quantiles as a fraction of their predicted width. For FD001 LSTM, rates at noise levels 0.0%, 5.0%, 10.0% and 20.0% are respectively 20.4%, 20.5%, 20.4%, 21.0% on the same 100 test engines. Across all groups, the largest saved point-estimate increase at 20.0% noise is 2.5 percentage points (FD002 hybrid, 259 test engines; increase and 95% CI: 2.5 [1.7, 3.4] percentage points). The full curves, distances and crossing counts are in Table S3. This perturbation response indicates low sensitivity under the tested noise scheme.

Gap collapse is defined by a median lower softplus gap below 1.25 cycles. The real-model fits show no collapse under this definition on 20/52/20/50 calibration engines for FD001–FD004. Supplement S0b and Tables S4a–S4c and S5 report the synthetic initialization and optimization checks descriptively.

### 2.3 Weighting attribution

The positive-class-weighted BCE population optimum differs from the target event probability. We therefore name the fixed correction $\operatorname{sigmoid}(r-\log w)$ **TrainOff**, temperature scaling **Temp**, and the combination $\operatorname{sigmoid}((r-\log w)/T)$ **TrainOff+Temp**. TrainOff uses the actual training weight. It differs from probability calibration fitted on calibration engines.

For FD001 LSTM, Table 2's raw rate is 20.4%, while TrainOff gives 18.0% on 100 test engines; the unweighted retrain rate is 18.8%, also on 100 test engines with 60 fitting engines. For FD001 hybrid, raw and TrainOff rates are 13.6% and 12.2%, while the unweighted retrain rate is 21.6% on 100 test engines with 60 fitting engines. Unweighted retraining therefore has an adverse outcome for this hybrid comparison. The analytic correction and retraining affect different learned quantities and their effects are not added (Tables S6a–S6b).

### 2.4 Adjusted effect sizes and detectable effects

The RUL-adjusted regressions use the original cubic capped-RUL covariate and seed intercepts. Table 1 reports both outcomes' coefficients, CIs, relative upper endpoints and approximate minimum detectable effects for every group. The pooled median-error coefficient is -85.6 cycles squared, CI [-191, 37.1], on 707 engines. Its upper CI endpoint is 14.8% of the group-weighted mean squared error. The approximate 80%-power MDE is 162 cycles squared (64.4% of that mean). The pooled result is underpowered for effects smaller than its reported MDE. The group results below also include negative associations.

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

The pooled RUL-only Brier coefficient is positive: 0.0922 [0.0589, 0.126] on 707 engines. The group coefficients in Table 1 are FD001 LSTM 0.0426 [-0.0369, 0.124], FD001 hybrid -0.0143 [-0.0887, 0.055], FD002 LSTM 0.0908 [0.0332, 0.155], FD002 hybrid 0.103 [0.0365, 0.171], FD003 LSTM 0.0822 [0.0155, 0.179], FD003 hybrid 0.129 [0.0524, 0.209], FD004 LSTM 0.124 [0.0554, 0.202], and FD004 hybrid 0.103 [0.0247, 0.187]. The positive intervals in FD002–FD004 indicate larger Brier error among flagged engines under the RUL-only adjustment; FD001 does not establish that pattern.

Four median-error coefficients are significantly negative in the sense that their engine-bootstrap CIs exclude zero: FD001 hybrid -250 [-415, -95.3] on 100 engines, FD002 LSTM -138 [-240, -51] and hybrid -149 [-311, -4.99] on 259 engines, and FD003 LSTM -320 [-595, -71] on 100 engines. These associations are unexplained. One hypothesis is that disagreement reflects event-head displacement even when the median is accurate. A second hypothesis is that the cubic RUL adjustment leaves residual differences in engine difficulty or lifecycle position. Neither hypothesis was tested by this study.

### 2.5 Threshold proximity

Across the original eight groups and 707 distinct engines, pooled incompatibility is 49.7% in the true-RUL 20–40 band (76 engines) and 8.2% elsewhere (631 engines), averaging the fixed models within each engine. The band has higher incompatibility in every original real-model group (Tables S9a–S9b). The band contains 15/22/10/29 engines and its complement 85/237/90/219 engines for FD001–FD004. For FD001 LSTM, rates are 50.7% in the band and 15.1% elsewhere (15 and 85 test engines). After adjustment for raw probability, the band and the original RUL/seed terms, the flag has no detectable incremental Brier association in most groups. In the original eight-group follow-up, FD001 hybrid has a negative adjusted Brier coefficient, -0.110, CI [-0.206, -0.0112], and FD003 hybrid has a positive coefficient, 0.0481, CI [0.00764, 0.0878]; each uses 100 test engines and 60 fitting engines. The adjusted association differs in sign across groups. This adjustment is close to mechanical. The flag is a deterministic function of p and the quantiles, while Brier is determined by p and the event label. Conditioning on p and the band therefore removes overlapping information, although it does not algebraically fix the flag because quantiles can still vary. The added-model comparison in Section 2.8 examines the same distinction.

### 2.6 Exploratory status

The original locked joint rule gave the verdict “not informative” (protocol SHA256 `da781da5c725624ab53503d65cff89037e5ce15f0769a23b27e6d6a04eeb4540`; Supplement S0). We chose positive controls, minimum detectable effects, direct projection and added-model replication after seeing earlier results. Later protocols specified each analysis before its calculations, but those choices still followed earlier results. 

The grouped sequence below identifies stages chosen after earlier results. Supplement S0d gives the full chronological table and its verification limits. 

| Grouped analysis stage, in chronological order | Chosen after earlier results? |
|---|---|
| Initial benchmark and equal-search design; reproduction gate and synthetic/quantile-perturbation validation | Initial scientific-choice history unknown; the later design and validation followed examined benchmark rates. |
| Extreme-null investigation; collapse cutoff/conditioned null; factorial, initialization and weighting/unweighted-retraining comparisons | Yes; chosen after the corresponding extreme-null and collapse results. |
| RUL-adjusted error associations, RUL bins, incremental probability and threshold-band analyses | Yes; followed incompatibility/collapse results; the band preceded the first association calculation. |
| Probability-plus-band flag adjustment and operational rule; synthetic percentile/difficulty comparisons | Yes; followed association and synthetic results, respectively. |
| Positive controls, projection, own-mean ratios, MDEs and pooled effects | Yes; followed compatibility/association results. |
| Expanded calibrators/projection, consistency counts, distance bins, mechanism checks and replicated adjusted associations | Yes; followed earlier controls/projection/association results. |

### 2.7 Positive controls and direct projection

For the original eight groups, the positive controls change the event-head predictions and keep the quantiles fixed. Uniform replacement and 1-p are gross event-head corruptions for which a high flag rate is expected. Pooled incompatibility rates and 95% engine-bootstrap CIs on 707 test engines are raw: 12.7% [11.1%, 14.4%]; uniform replacement: 88.3% [87.3%, 89.3%]; 1-p: 96.3% [95.4%, 97.2%]; logit +1: 18.7% [16.5%, 21.1%]; logit -1: 8.0% [6.9%, 9.2%]. Uniform replacement averages 100 fixed draws per engine/run. The -1 logit shift lowers the rate, whereas uniform replacement and 1-p raise it, so detection depends on the corruption direction. The +1 logit shift raises the pooled rate only from 12.7% to 18.7%, consistent with the low sensitivity to quantile noise. Table S13a reports every group's rate and mean distance, with CIs.

For direct projection, $p_{\mathrm{proj}}=\operatorname{clip}(p,L,U)$. NLL uses scoring-time clipping at $10^{-15}$. ECE5 uses five probability-quantile bins and ECE10 ten equal-width bins. Their boundaries use no labels and stay fixed during bootstrap. ECE is averaged across fixed models, rather than computed from a mixture probability. This transformation uses no labels and gives exactly 0.0% incompatibility on all test and calibration outputs. On 707 test engines, projected-minus-raw Brier is -0.00424 [-0.00647, -0.00226]; corresponding changes are NLL -0.0156 [-0.0236, -0.00874], ECE5 -0.00855 [-0.0109, -0.00443], ECE10 -0.00896 [-0.0118, -0.00584]. For the original eight groups, subset-level projected-minus-raw test Brier is FD001 -0.000343 [-0.006465, 0.005235] on 100 engines, FD002 -0.004445 [-0.007203, -0.001986] on 259 engines, FD003 -0.003555 [-0.009740, 0.002375] on 100 engines, and FD004 -0.005885 [-0.010457, -0.002046] on 248 engines. The pooled Brier gain is resolved within FD002 and FD004 and unresolved within FD001 and FD003. For the original eight groups, calibration Brier changes by -0.00522 [-0.00964, -0.00163] on their 142 distinct calibration engines. The unfavorable FD001 LSTM test Brier change is 0.00149 [-0.00668, 0.00964] on 100 engines. Projection enforces the necessary bounds but its scoring effect is empirical. Table S13b contains every raw/projected score and paired CI for both roles, including the pre-specified ECE5 and ECE10 conventions. The expanded comparison below includes every prespecified probability path.

### 2.8 Added-model replication and standard calibrators

The expanded saved-prediction comparison retains 44 groups and 220 fixed fits on the same 707 distinct official-test engines: the original eight equal-search groups, the TCN/GRU equal-search extension, the original hybrid runs with their own calibration partitions, and the saved extra LSTM/hybrid/GRU/TCN controls, including the additional LSTM/hybrid CV controls. The expanded 44-group roster has 518 distinct calibration engines across its recorded partitions, compared with 142 distinct calibration engines for the original eight groups. We fit each map separately on the calibration engines for that fit. TrainOff uses the recorded training-weight offset. The fixed paths are raw, projection, TrainOff, Temp, TrainOff+Temp, Platt, Isotonic and Beta, with each calibration path also followed by projection. The extension protocol and its hash remain unchanged in the evidence archive.

In this expanded roster, pooled raw Brier is 0.036746 and projected Brier is 0.033041. Projected-minus-raw Brier is -0.003705 [-0.005605, -0.001977]. Pooled raw NLL is 0.124702 and projected NLL is 0.111594. The difference is -0.013108 [-0.019727, -0.007370]. TrainOff has pooled Brier 0.028727 and NLL 0.097836, both lower than projection alone. The pooled advantage of TrainOff is driven largely by FD002. TrainOff followed by projection has pooled Brier 0.028081, with a paired difference versus raw of -0.008665 (95% CI [-0.014042, -0.003373]), and pooled NLL 0.095831, with a paired difference versus raw of -0.028872 (95% CI [-0.047089, -0.011553]). No paired CI compares TrainOff followed by projection with either TrainOff or projection alone. Projection guarantees satisfaction of the quantile-implied bounds. Temp, Platt, Isotonic and Beta worsen pooled NLL relative to raw; Isotonic followed by projection also has an unfavorable NLL difference CI. The companion A_all_scores.csv reports all Brier, NLL, ECE5 and ECE10 comparisons, including every adverse result.

The TrainOff-minus-raw Brier CIs classify 15 groups as better, 1 as worse and 28 as unresolved. These counts use the same zero-exclusion rule as the projection counts. TrainOff worsens Brier versus raw by point estimate in 14 of 44 groups, including all FD001 groups: equal-search LSTM, hybrid, TCN and GRU; original hybrid; and extra lstm_gpu, hybrid_gpu, gru_gpu, tcn_gpu, lstm_cv and hybrid_cv. Its point estimates also worsen in FD003 equal-search LSTM and TCN and extra hybrid_cv. Only FD001 extra lstm_cv has a TrainOff-minus-raw CI wholly above zero. Against projection alone, TrainOff has worse Brier by point estimate in 17 of 44 groups (FD001 11, FD002 0, FD003 5, FD004 1), including every FD001 group, and worse NLL in 15 of 44 groups. No paired TrainOff-versus-projection CI is reported.

For projection-minus-raw Brier, 20 groups have CIs below zero, none has a CI above zero and 24 are unresolved; 11 point estimates are unfavorable. For NLL, the corresponding counts are 22, none and 22, with 6 unfavorable point estimates. These groups share engines. C_dose_response.csv and D_mechanism.csv report the fixed distance bins and mechanism results. Movement of mean probability toward the event base rate is not uniform across groups.

In the expanded-roster reanalysis, the original FD001 hybrid group again has a negative probability-plus-band-adjusted Brier coefficient, -0.110, CI [-0.207, -0.0102], whereas the original FD003 hybrid group has a positive coefficient, 0.0481, CI [0.00852, 0.0867]; each uses 100 test engines and 60 fitting engines. These signs differ across groups. These extension CIs use the extension bootstrap draws. Section 2.5 reports the earlier follow-up CIs without substituting the extension intervals.

Among the 36 added groups, RUL-only Brier coefficients are positive in 35 groups and their CIs exclude zero in the positive direction in 28. After adjustment for raw probability and the threshold band, no added group has a positive CI and one has a negative CI. RUL-only median-error CIs are negative in 7 added groups, with no positive CI. Across all 44 groups, 11 RUL-only median-error CIs lie below zero and none lie above it. The intervals that exclude zero therefore agree in sign, and the pattern remains unexplained. These findings extend the original distinction between probability error and point error without resolving the negative median-error associations. E_associations.csv reports every coefficient, CI, own-mean ratio, regression engine count and approximate MDE for both outcomes and all adjustments. Undefined bootstrap coefficients are counted explicitly rather than replaced by zero.

![Projection-minus-raw Brier across the expanded 44-group roster. Points and 95% engine-bootstrap CIs are copied from A_all_scores.csv; lower values favor projection. Labels show test engines per group: FD001 100, FD002 259, FD003 100 and FD004 248. All 44 groups share 707 distinct official-test engines; fixed fits do not multiply these counts.](figures/projection_brier_44_groups.png){width=95%}

The requested pooled true-RUL-bin incompatibility figure is unavailable without new aggregation: no saved CSV supplies the original eight-group pooled bin rates with their engine-bootstrap CIs. The existing real_RUL_bins.csv supplies group-specific bin counts and error contrasts, and near_threshold_table.csv supplies group-specific band/elsewhere summaries; neither contains the requested pooled bin-rate intervals. No substitute pooled intervals were calculated.

## 3. Benchmark compatibility results

### 3.1 C-MAPSS

Table 2 reports the eight equal-search rows using the same percentage-display rule. Each group averages five fits on the same test engines. The values describe incompatibility frequency and distance, rather than the probability that a model is faulty.

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

## 4. Secondary calibration and architecture results

The architecture comparisons show changes that depend on the output rather than a common ranking. Table 3 reports point accuracy and raw Brier for the same C-MAPSS LSTM/hybrid groups. The display records each output separately.

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

Table 4 shows the four original probability-processing paths for the original eight groups: Raw, TrainOff, Temp and TrainOff+Temp. Section 2.8 and the expanded-calibrator supplementary file A_all_scores.csv report Platt, Isotonic, Beta and projection paths. Temperature increases the Table 2 incompatibility mean in each group while its Brier changes differ across groups. For FD001 LSTM, TrainOff changes incompatibility from 20.4% to 18.0% but Brier from 0.03561 to 0.05276 on 100 test engines. Compatibility and probability error are therefore separate assessment targets.

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

: Secondary calibration comparison for the original eight groups, showing Raw, TrainOff, Temp and TrainOff+Temp Brier mean ± sample SD at source precision. These paths use the same test engines within each row. Section 2.8 and the expanded-calibrator supplementary file A_all_scores.csv contain Platt, Isotonic, Beta and projection paths; Table S6b gives the original compatibility-by-method source table.

## 5. Limitations and conclusion

The flag detects the tested gross corruptions, with a response that depends on corruption direction. Its threshold concentration and adjusted error associations do not establish general fault detection. The negative median-error associations remain unexplained. In the expanded 44 groups, TrainOff has lower pooled Brier and NLL than projection alone, largely driven by FD002. By point estimate, TrainOff has worse Brier than projection alone in 17 groups, including all 11 FD001 groups, and worse NLL in 15 groups. TrainOff also has worse Brier than raw in 14 groups, with one CI wholly above zero. Projection supplies a structural guarantee with a small, inconsistent scoring gain, and no paired TrainOff-versus-projection CI is reported. These groups share the same 707 engines, so their counts are not independent evidence. This exploratory, single-benchmark study reuses examined data. Its bootstrap CIs condition on the fits, calibration maps and analysis choices. DS01 (4 test engines) was descriptive only and was not validated [@ariaschao2021ncmapss]. Independent human review is still missing.

## Data and code availability

The repository https://github.com/amirhossein2004-mozafari/rul-quantile-event-compatibility contains code, protocols, result CSVs, saved predictions, reports, manuscript sources and the supplement. It excludes 185 hash-referenced files, including checkpoints, tensors, raw NASA data and other inputs, so the public release cannot support full retraining or full lock verification. NASA data can be downloaded from the NASA Prognostics Center of Excellence repository (https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/). Code is licensed under MIT, and derived results and saved predictions are licensed under CC BY 4.0. The validation supplement contains Tables S1–S14 with source-file labels and full-precision companion tables. The repository also includes the added-model comparisons. Monitoring, PCGrad, component ablations, path-maximum CV+ and multi-study comparisons remain supplementary.

## Authorship, funding and competing interests

Amir Hossein Mozafari: conceptualization, methodology, software, validation, analysis, investigation, data curation, writing, visualization and project administration. No specific external funding was received. The author declares no known competing financial interests or personal relationships affecting this work.

## Declaration of generative AI assistance

OpenAI Codex was used for code implementation and correction, analysis scripts, figure preparation, language editing, manuscript revision, and implementation and numerical checks. Those checks were run by the same tool that generated or edited the code and text. The author remains responsible for reviewing the methods, results, citations and submitted manuscript.

Configured model: `gpt-6.1-sol`; runtime: `0.166.0-alpha.5.1`; preceding manuscript revision date: 2026-11-01; current desktop build: `26.1027.3384.0`. The exact served checkpoint identifier is unavailable.

## References

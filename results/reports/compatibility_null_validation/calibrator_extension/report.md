# Exploratory calibration and projection extension

Protocol SHA256: `9d769fd8a7a22f112654dea1d7723bbe20f11e3df31c8337d97a3f73401d4e9d`. Locked before new calculations. No outcome, threshold, subgroup or decision criterion changed. One label-type implementation correction is documented separately.

Every analysis and estimate in this report is exploratory. Independent human review is still missing. No training, checkpoint loading or forward inference ran. All 588 input files were hashed before numerical analysis and remained unchanged. The original eight groups’ 64 raw/projected score estimates reproduce the preceding analysis to 1e-12.

44 groups, 220 fixed fits, 707 distinct official-test engines. Test counts by subset: FD001 100, FD002 259, FD003 100, FD004 248. Repeated fits and architectures never multiply these engine counts. Calibration partitions and IDs are listed per fit in roster.json; original hybrid runs retain their own partitions. The extra scope includes four GPU-repeat architectures and the two additional CV-selected LSTM/hybrid controls, five fits per subset/architecture. No saved prediction pair was missing.

All score intervals and paired differences are 95% percentile CIs from 2000 synchronized engine-cluster bootstrap draws. Calibration maps are held fixed during the test bootstrap, so uncertainty from estimating calibration maps is excluded. Distinct engines receive equal pooled weight; within each engine, groups/fits receive equal weight. ECE pools group scores with engine-count weights across subsets; it is not ECE of averaged predictions. ECE5 uses fixed method/fit-specific quintile cuts; ECE10 uses fixed equal-width bins.

## A. Projection and calibrator comparison

All 14 probability paths are reported for every group and pooled in A_all_scores.csv (2520 rows). Each row includes score CI, paired method-minus-raw CI, test count, fit count, and calibration counts. Negative paired differences favor the method. TrainOff is the fixed recorded training-weight offset; its parameters are not estimated on calibration labels. All other maps are fitted separately on each fit’s calibration engines. No calibration optimization failed.

- Exploratory raw Brier (707 engines): 0.0367462; difference vs raw 0 [0, 0].
- Exploratory raw NLL (707 engines): 0.124702; difference vs raw 0 [0, 0].
- Exploratory projection Brier (707 engines): 0.0330409; difference vs raw -0.00370527 [-0.00560464, -0.00197747].
- Exploratory projection NLL (707 engines): 0.111594; difference vs raw -0.0131082 [-0.0197272, -0.00737003].
- Exploratory TrainOff Brier (707 engines): 0.0287274; difference vs raw -0.00801885 [-0.0139193, -0.00215972].
- Exploratory TrainOff NLL (707 engines): 0.097836; difference vs raw -0.0268664 [-0.046844, -0.00778431].
- Exploratory TrainOff+projection Brier (707 engines): 0.0280809; difference vs raw -0.00866534 [-0.0140422, -0.0033728].
- Exploratory TrainOff+projection NLL (707 engines): 0.0958305; difference vs raw -0.0288718 [-0.047089, -0.0115527].
- Exploratory Temp Brier (707 engines): 0.0413654; difference vs raw 0.00461919 [0.00271727, 0.00646978].
- Exploratory Temp NLL (707 engines): 0.284231; difference vs raw 0.159529 [0.0963635, 0.234061].
- Exploratory Temp+projection Brier (707 engines): 0.0335529; difference vs raw -0.0031933 [-0.0054862, -0.00099369].
- Exploratory Temp+projection NLL (707 engines): 0.134987; difference vs raw 0.0102849 [-0.00707988, 0.0309269].
- Exploratory TrainOff+Temp Brier (707 engines): 0.0326612; difference vs raw -0.004085 [-0.0101979, 0.00213945].
- Exploratory TrainOff+Temp NLL (707 engines): 0.293103; difference vs raw 0.168401 [0.0790287, 0.27186].
- Exploratory TrainOff+Temp+projection Brier (707 engines): 0.0293362; difference vs raw -0.00740996 [-0.0127652, -0.00203807].
- Exploratory TrainOff+Temp+projection NLL (707 engines): 0.143371; difference vs raw 0.0186689 [-0.0202273, 0.0693358].
- Exploratory Platt Brier (707 engines): 0.0446804; difference vs raw 0.00793417 [-0.00174551, 0.0174763].
- Exploratory Platt NLL (707 engines): 0.617151; difference vs raw 0.492449 [0.322844, 0.67808].
- Exploratory Platt+projection Brier (707 engines): 0.0318908; difference vs raw -0.00485537 [-0.0112041, 0.00146272].
- Exploratory Platt+projection NLL (707 engines): 0.163137; difference vs raw 0.0384346 [-0.00670813, 0.096953].
- Exploratory Isotonic Brier (707 engines): 0.0414539; difference vs raw 0.00470767 [-0.00340733, 0.0129168].
- Exploratory Isotonic NLL (707 engines): 0.912714; difference vs raw 0.788011 [0.532567, 1.06911].
- Exploratory Isotonic+projection Brier (707 engines): 0.03164; difference vs raw -0.0051062 [-0.0109214, 0.000621424].
- Exploratory Isotonic+projection NLL (707 engines): 0.196305; difference vs raw 0.0716023 [0.00930843, 0.149759].
- Exploratory Beta Brier (707 engines): 0.0500473; difference vs raw 0.0133011 [0.00400135, 0.0229942].
- Exploratory Beta NLL (707 engines): 0.783525; difference vs raw 0.658823 [0.486819, 0.838412].
- Exploratory Beta+projection Brier (707 engines): 0.0316004; difference vs raw -0.00514582 [-0.0112563, 0.00111318].
- Exploratory Beta+projection NLL (707 engines): 0.158672; difference vs raw 0.0339701 [-0.00858386, 0.0887281].

Projection lowers pooled Brier/NLL; TrainOff alone has lower pooled scores than projection alone. This descriptive comparison does not provide a paired CI for TrainOff versus projection. Temperature, Platt, Isotonic and Beta have adverse pooled NLL results; Isotonic followed by projection also has a positive NLL difference CI versus raw. There is no universally favored processing path.

## B. Consistency

- Exploratory Brier (44 groups; 707 distinct engines): helps 20, hurts 0, unresolved 24; 33 negative and 11 positive point differences.
- Exploratory NLL (44 groups; 707 distinct engines): helps 22, hurts 0, unresolved 22; 38 negative and 6 positive point differences.

B_consistency.csv contains the sign and CI for every group, including all unfavorable point estimates. Helps requires CI upper endpoint <0; hurts requires lower endpoint >0. All other results are unresolved.

## C. Distance dose response

C_dose_response.csv reports all four prespecified bins for all 44 groups (176 rows), with distinct engine counts, engine-fit row counts, Brier improvement and CI. Bins classify engine-fit pairs; an engine can appear in different bins across fits, so bin distinct-engine counts must not be summed. Positive improvement favors projection. The d=0 bin has zero improvement by construction. These are descriptive associations; projection magnitude and potential Brier change are mechanically related.

## D. Mechanism

- Exploratory above_U: group range 0.03 to 0.212903; 44 groups and 707 distinct test engines, group-specific counts/CIs in D_mechanism.csv.
- Exploratory below_L: group range 0 to 0.07; 44 groups and 707 distinct test engines, group-specific counts/CIs in D_mechanism.csv.
- Exploratory signed_probability_change: group range -0.0201868 to 0.000614735; 44 groups and 707 distinct test engines, group-specific counts/CIs in D_mechanism.csv.
- Exploratory gap_change: group range -0.0201868 to 0.0100389; 44 groups and 707 distinct test engines, group-specific counts/CIs in D_mechanism.csv.

Projection reduces the absolute gap between mean p and event base rate in 41/44 groups and increases it in 3/44 (707 distinct engines). This is a point-estimate classification, not a CI decision. D_mechanism.csv also gives base rates, raw/projected means and both absolute gaps, all with CIs.

## E. Adjusted flag associations

E_associations.csv retains all 264 exploratory outcome/adjustment rows: both outcomes, all 44 groups, RUL adjustment alone, RUL plus cubic raw p and the 20–40 indicator, and RUL-adjusted analysis restricted to the 20–40 band. Each row reports its actual regression engine count, flagged distinct engines, coefficient, CI, own mean, coefficient and CI divided by own mean, approximate MDE and MDE/mean. All point coefficients are identifiable; 44 rows have at least one undefined bootstrap draw (maximum 92/2000). Those draws are counted, not replaced with zero.

RUL adjustment uses the earlier cubic capped-RUL convention and fit-specific intercepts. The additional raw-p adjustment uses a cubic and the raw-RUL 20–40 indicator. Own-mean ratios use the same group and, for restricted analyses, the same band. MDE is approximately 2.801585 times bootstrap coefficient SD for 80% power at two-sided alpha .05, conditional on the observed design and fixed fits. It is not an exact power calculation. Associations are noncausal, with no multiplicity correction.

## Provenance and limits

Current session records configured model gpt-6.1-sol, runtime 0.166.0-alpha.5.1, and current desktop build 26.1027.3384.0 (OpenAI.Codex_26.1027.3384.0_x64__2p2nqsd0c76g0). Historical app/build and executable identifiers are retained in provenance.json, explicitly separated from current session identity. Exact served checkpoint/build identifier is unavailable. Software: Python 3.11.9, NumPy 2.3.4, SciPy 1.17.0, scikit-learn 1.9.0.

All calibration endpoints are retrospective and can differ in sampling policy from official-test final windows. The same official-test fleets have been examined before; the protocol lock does not make these fresh confirmatory tests. Pooling across original/equal-search/extra models describes this fixed roster rather than independent model replications. Independent human review is still missing.

The HTML companion contains every result in searchable tables. CSVs retain full numeric precision; displayed HTML numbers use six significant digits. Protocol, roster, fit parameters, bin edges, source code, input hashes, correction log and final manifest accompany the results.
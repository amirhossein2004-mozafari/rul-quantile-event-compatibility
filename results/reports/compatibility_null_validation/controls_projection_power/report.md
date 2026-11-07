# Frozen controls, direct projection, effect size and engine dependence

Protocol SHA256: `940943607cfd3cd971a17e9d5dcd3f94474a93724a717f391af1dda374a950ff`. Locked before these calculations; no outcome, threshold or criterion changed afterward. No training, forward inference or model selection ran. Earlier manuscript/claim artifacts remain unchanged.

All brackets are 95% engine-cluster percentile CIs from 2000 draws. Rates are percentages and rate differences are percentage points; Brier/NLL/ECE/distance use their original score units. Displayed non-rate estimates use three significant figures; CSVs retain full precision. Fit/test or fit/cal engine counts accompany every table row. Fixed-fit counts never multiply the engine count.

## Pooled estimates

Test: 707 engine clusters; calibration: 142 separate engine clusters. LSTM/hybrid are averaged equally within each subset, followed by engine-count weighting across subsets. There are 40 fixed models, not 40 independent fleets.

| Control | Fit/test engines | Fixed fits | Incompatibility % [CI] | Mean distance [CI] |
|---|---|---|---|---|
| Raw | 425/707 | 40 | 12.7 [11.1, 14.4] | 0.011 [0.00915, 0.0131] |
| Uniform, 100 draws | 425/707 | 40 | 88.3 [87.3, 89.3] | 0.397 [0.389, 0.405] |
| 1-p | 425/707 | 40 | 96.3 [95.4, 97.2] | 0.831 [0.813, 0.847] |
| logit +1 | 425/707 | 40 | 18.7 [16.5, 21.1] | 0.0257 [0.0217, 0.0301] |
| logit -1 | 425/707 | 40 | 8.0 [6.9, 9.2] | 0.00522 [0.00419, 0.00635] |

| Role/metric | Fit/evaluation engines | Raw [CI] | Projected [CI] | Projected minus raw [CI] |
|---|---|---|---|---|
| test Brier | 425/707 | 0.0368 [0.0276, 0.0467] | 0.0325 [0.0244, 0.0414] | -0.00424 [-0.00647, -0.00226] |
| test NLL | 425/707 | 0.123 [0.0917, 0.155] | 0.107 [0.0814, 0.135] | -0.0156 [-0.0236, -0.00874] |
| test ECE5 | 425/707 | 0.0393 [0.0301, 0.0535] | 0.0307 [0.0237, 0.0444] | -0.00855 [-0.0109, -0.00443] |
| test ECE10 | 425/707 | 0.0453 [0.0393, 0.0612] | 0.0363 [0.0319, 0.0507] | -0.00896 [-0.0118, -0.00584] |
| test incompatibility_rate | 425/707 | 12.7 [11.1, 14.4] | 0.0 [0.0, 0.0] | -12.7 [-14.4, -11.1] |
| calibration Brier | 425/142 | 0.0268 [0.0109, 0.0465] | 0.0216 [0.00792, 0.0387] | -0.00522 [-0.00964, -0.00163] |
| calibration NLL | 425/142 | 0.0886 [0.0387, 0.149] | 0.0728 [0.0304, 0.125] | -0.0158 [-0.0286, -0.00501] |
| calibration ECE5 | 425/142 | 0.0422 [0.0205, 0.0678] | 0.0341 [0.0159, 0.0578] | -0.00817 [-0.0119, -0.00358] |
| calibration ECE10 | 425/142 | 0.0449 [0.0238, 0.07] | 0.039 [0.0206, 0.062] | -0.00588 [-0.00992, -0.00192] |
| calibration incompatibility_rate | 425/142 | 9.5 [6.3, 13.0] | 0.0 [0.0, 0.0] | -9.5 [-13.0, -6.3] |

The -1 logit control lowers the pooled incompatibility rate. Direct projection produces zero incompatibility by construction. FD001 LSTM test Brier increases after projection; its paired interval includes zero. All group results, including these directions, are retained below.

## A. Every frozen group

| Group/control | Fit/test engines | Fixed fits | Incompatibility % [CI] | Mean distance [CI] |
|---|---|---|---|---|
| FD001 lstm Raw | 60/100 | 5 | 20.4 [14.2, 26.6] | 0.021 [0.0129, 0.0301] |
| FD001 lstm Uniform, 100 draws | 60/100 | 5 | 88.7 [85.9, 91.2] | 0.401 [0.378, 0.421] |
| FD001 lstm 1-p | 60/100 | 5 | 92.0 [87.0, 96.4] | 0.806 [0.75, 0.857] |
| FD001 lstm logit +1 | 60/100 | 5 | 20.8 [14.0, 28.4] | 0.0468 [0.0289, 0.0676] |
| FD001 lstm logit -1 | 60/100 | 5 | 20.2 [13.8, 27.2] | 0.0147 [0.00948, 0.0204] |
| FD001 hybrid Raw | 60/100 | 5 | 13.6 [8.4, 19.0] | 0.0138 [0.0079, 0.0206] |
| FD001 hybrid Uniform, 100 draws | 60/100 | 5 | 89.2 [86.4, 91.7] | 0.404 [0.382, 0.424] |
| FD001 hybrid 1-p | 60/100 | 5 | 97.2 [95.4, 98.8] | 0.836 [0.789, 0.879] |
| FD001 hybrid logit +1 | 60/100 | 5 | 18.6 [12.4, 25.2] | 0.0283 [0.017, 0.0413] |
| FD001 hybrid logit -1 | 60/100 | 5 | 12.0 [7.6, 16.6] | 0.0115 [0.0052, 0.0195] |
| FD002 lstm Raw | 156/259 | 5 | 9.6 [6.7, 12.5] | 0.00671 [0.00416, 0.00952] |
| FD002 lstm Uniform, 100 draws | 156/259 | 5 | 90.2 [88.5, 91.6] | 0.412 [0.399, 0.424] |
| FD002 lstm 1-p | 156/259 | 5 | 97.3 [95.8, 98.7] | 0.865 [0.839, 0.89] |
| FD002 lstm logit +1 | 156/259 | 5 | 15.4 [11.5, 19.4] | 0.0182 [0.0122, 0.0246] |
| FD002 lstm logit -1 | 156/259 | 5 | 3.5 [2.2, 4.9] | 0.0011 [0.000497, 0.00189] |
| FD002 hybrid Raw | 156/259 | 5 | 8.9 [6.6, 11.4] | 0.0072 [0.00431, 0.0104] |
| FD002 hybrid Uniform, 100 draws | 156/259 | 5 | 89.3 [87.7, 90.7] | 0.405 [0.392, 0.417] |
| FD002 hybrid 1-p | 156/259 | 5 | 97.1 [95.8, 98.3] | 0.845 [0.818, 0.871] |
| FD002 hybrid logit +1 | 156/259 | 5 | 14.9 [11.6, 18.3] | 0.0192 [0.0131, 0.0257] |
| FD002 hybrid logit -1 | 156/259 | 5 | 5.6 [3.9, 7.2] | 0.00407 [0.00236, 0.00593] |
| FD003 lstm Raw | 60/100 | 5 | 12.8 [8.2, 18.0] | 0.015 [0.00787, 0.0237] |
| FD003 lstm Uniform, 100 draws | 60/100 | 5 | 87.8 [84.8, 90.5] | 0.393 [0.367, 0.415] |
| FD003 lstm 1-p | 60/100 | 5 | 95.8 [92.8, 98.2] | 0.823 [0.771, 0.87] |
| FD003 lstm logit +1 | 60/100 | 5 | 22.6 [15.8, 30.2] | 0.0304 [0.0184, 0.0443] |
| FD003 lstm logit -1 | 60/100 | 5 | 5.8 [3.2, 9.0] | 0.00608 [0.0027, 0.0102] |
| FD003 hybrid Raw | 60/100 | 5 | 11.8 [7.6, 16.4] | 0.0149 [0.00814, 0.0223] |
| FD003 hybrid Uniform, 100 draws | 60/100 | 5 | 89.6 [87.4, 91.7] | 0.408 [0.389, 0.425] |
| FD003 hybrid 1-p | 60/100 | 5 | 96.6 [94.4, 98.4] | 0.846 [0.801, 0.886] |
| FD003 hybrid logit +1 | 60/100 | 5 | 17.4 [11.6, 23.6] | 0.0311 [0.019, 0.0449] |
| FD003 hybrid logit -1 | 60/100 | 5 | 8.2 [5.0, 11.8] | 0.00738 [0.00391, 0.0116] |
| FD004 lstm Raw | 149/248 | 5 | 16.6 [13.1, 20.3] | 0.0137 [0.00992, 0.018] |
| FD004 lstm Uniform, 100 draws | 149/248 | 5 | 86.7 [84.8, 88.5] | 0.385 [0.37, 0.4] |
| FD004 lstm 1-p | 149/248 | 5 | 95.2 [93.1, 96.9] | 0.81 [0.777, 0.841] |
| FD004 lstm logit +1 | 149/248 | 5 | 24.0 [19.4, 28.9] | 0.032 [0.0237, 0.041] |
| FD004 lstm logit -1 | 149/248 | 5 | 8.5 [6.0, 11.1] | 0.00383 [0.00245, 0.0054] |
| FD004 hybrid Raw | 149/248 | 5 | 12.7 [9.8, 15.6] | 0.00857 [0.00502, 0.0134] |
| FD004 hybrid Uniform, 100 draws | 149/248 | 5 | 86.2 [84.4, 88.1] | 0.38 [0.365, 0.394] |
| FD004 hybrid 1-p | 149/248 | 5 | 97.0 [95.3, 98.4] | 0.804 [0.772, 0.834] |
| FD004 hybrid logit +1 | 149/248 | 5 | 19.2 [15.5, 23.1] | 0.0205 [0.0141, 0.0283] |
| FD004 hybrid logit -1 | 149/248 | 5 | 9.0 [6.9, 11.3] | 0.00451 [0.00258, 0.00717] |

## A. Within-subset combined estimates

| Group/control | Fit/test engines | Fixed fits | Incompatibility % [CI] | Mean distance [CI] |
|---|---|---|---|---|
| FD001 combined Raw | 60/100 | 10 | 17.0 [11.8, 22.4] | 0.0174 [0.011, 0.0244] |
| FD001 combined Uniform, 100 draws | 60/100 | 10 | 88.9 [86.2, 91.4] | 0.402 [0.38, 0.422] |
| FD001 combined 1-p | 60/100 | 10 | 94.6 [91.3, 97.5] | 0.821 [0.77, 0.868] |
| FD001 combined logit +1 | 60/100 | 10 | 19.7 [13.3, 26.8] | 0.0376 [0.0237, 0.0536] |
| FD001 combined logit -1 | 60/100 | 10 | 16.1 [11.4, 20.8] | 0.0131 [0.00833, 0.0187] |
| FD002 combined Raw | 156/259 | 10 | 9.2 [6.9, 11.8] | 0.00695 [0.00469, 0.00944] |
| FD002 combined Uniform, 100 draws | 156/259 | 10 | 89.7 [88.2, 91.1] | 0.408 [0.396, 0.42] |
| FD002 combined 1-p | 156/259 | 10 | 97.2 [95.9, 98.4] | 0.855 [0.829, 0.88] |
| FD002 combined logit +1 | 156/259 | 10 | 15.1 [11.8, 18.5] | 0.0187 [0.0134, 0.0243] |
| FD002 combined logit -1 | 156/259 | 10 | 4.5 [3.3, 5.8] | 0.00259 [0.00158, 0.00371] |
| FD003 combined Raw | 60/100 | 10 | 12.3 [8.4, 16.6] | 0.015 [0.00894, 0.0219] |
| FD003 combined Uniform, 100 draws | 60/100 | 10 | 88.7 [86.1, 91.0] | 0.4 [0.379, 0.419] |
| FD003 combined 1-p | 60/100 | 10 | 96.2 [93.9, 98.1] | 0.834 [0.789, 0.877] |
| FD003 combined logit +1 | 60/100 | 10 | 20.0 [14.1, 26.4] | 0.0308 [0.0198, 0.0431] |
| FD003 combined logit -1 | 60/100 | 10 | 7.0 [4.5, 9.9] | 0.00673 [0.00363, 0.0103] |
| FD004 combined Raw | 149/248 | 10 | 14.6 [11.8, 17.8] | 0.0111 [0.008, 0.0151] |
| FD004 combined Uniform, 100 draws | 149/248 | 10 | 86.5 [84.6, 88.2] | 0.383 [0.367, 0.397] |
| FD004 combined 1-p | 149/248 | 10 | 96.1 [94.4, 97.5] | 0.807 [0.775, 0.837] |
| FD004 combined logit +1 | 149/248 | 10 | 21.6 [17.7, 25.7] | 0.0262 [0.0197, 0.0336] |
| FD004 combined logit -1 | 149/248 | 10 | 8.8 [6.7, 10.8] | 0.00417 [0.0028, 0.00593] |

The uniform-control group estimand averages 100 fixed probability draws per engine/run; CIs condition on those draws. A_per_seed.csv and A_uniform_per_draw.csv retain all seeds and all 4000 draw/seed rows. Saved uniform probability arrays preserve every generated control.

## B. test: Every frozen group

| Group/metric | Fit/evaluation engines | Fixed fits | Raw [CI] | Projected [CI] | Paired difference [CI] |
|---|---|---|---|---|---|
| FD001 lstm Brier | 60/100 | 5 | 0.0356 [0.0146, 0.0614] | 0.0371 [0.0176, 0.0619] | 0.00149 [-0.00668, 0.00964] |
| FD001 lstm NLL | 60/100 | 5 | 0.123 [0.0614, 0.201] | 0.122 [0.0627, 0.198] | -0.000982 [-0.0193, 0.0177] |
| FD001 lstm ECE5 | 60/100 | 5 | 0.0166 [0.0106, 0.0513] | 0.0153 [0.0108, 0.0501] | -0.00132 [-0.0226, 0.0226] |
| FD001 lstm ECE10 | 60/100 | 5 | 0.038 [0.032, 0.0757] | 0.027 [0.0195, 0.0628] | -0.011 [-0.0344, 0.00546] |
| FD001 lstm incompatibility_rate | 60/100 | 5 | 20.4 [14.2, 26.6] | 0.0 [0.0, 0.0] | -20.4 [-26.6, -14.2] |
| FD001 hybrid Brier | 60/100 | 5 | 0.0348 [0.0131, 0.0625] | 0.0326 [0.0122, 0.0591] | -0.00217 [-0.00689, 0.00197] |
| FD001 hybrid NLL | 60/100 | 5 | 0.121 [0.0484, 0.217] | 0.113 [0.0438, 0.205] | -0.00855 [-0.0231, 0.0037] |
| FD001 hybrid ECE5 | 60/100 | 5 | 0.0161 [0.00992, 0.0505] | 0.0113 [0.00882, 0.0457] | -0.00481 [-0.0146, 0.0112] |
| FD001 hybrid ECE10 | 60/100 | 5 | 0.0394 [0.0282, 0.0767] | 0.029 [0.0214, 0.0637] | -0.0103 [-0.0187, -0.000511] |
| FD001 hybrid incompatibility_rate | 60/100 | 5 | 13.6 [8.4, 19.0] | 0.0 [0.0, 0.0] | -13.6 [-19.0, -8.4] |
| FD002 lstm Brier | 156/259 | 5 | 0.0251 [0.0124, 0.0402] | 0.0212 [0.0105, 0.0344] | -0.00385 [-0.00698, -0.00112] |
| FD002 lstm NLL | 156/259 | 5 | 0.0816 [0.0425, 0.131] | 0.0709 [0.038, 0.112] | -0.0108 [-0.0199, -0.0033] |
| FD002 lstm ECE5 | 156/259 | 5 | 0.036 [0.0201, 0.0558] | 0.0302 [0.0148, 0.0477] | -0.0058 [-0.00966, -0.00346] |
| FD002 lstm ECE10 | 156/259 | 5 | 0.0364 [0.0226, 0.0563] | 0.0304 [0.0188, 0.0485] | -0.00597 [-0.00891, -0.00271] |
| FD002 lstm incompatibility_rate | 156/259 | 5 | 9.6 [6.7, 12.5] | 0.0 [0.0, 0.0] | -9.6 [-12.5, -6.7] |
| FD002 hybrid Brier | 156/259 | 5 | 0.0333 [0.0197, 0.0483] | 0.0283 [0.016, 0.0417] | -0.00504 [-0.00864, -0.00194] |
| FD002 hybrid NLL | 156/259 | 5 | 0.118 [0.0706, 0.173] | 0.0992 [0.0576, 0.15] | -0.019 [-0.033, -0.00723] |
| FD002 hybrid ECE5 | 156/259 | 5 | 0.0477 [0.0302, 0.0682] | 0.0411 [0.025, 0.0603] | -0.00665 [-0.00996, -0.00368] |
| FD002 hybrid ECE10 | 156/259 | 5 | 0.0472 [0.0335, 0.0687] | 0.0419 [0.0297, 0.0622] | -0.00527 [-0.009, -0.00178] |
| FD002 hybrid incompatibility_rate | 156/259 | 5 | 8.9 [6.6, 11.4] | 0.0 [0.0, 0.0] | -8.9 [-11.4, -6.6] |
| FD003 lstm Brier | 60/100 | 5 | 0.0267 [0.00832, 0.0519] | 0.026 [0.0104, 0.0469] | -0.000682 [-0.00803, 0.00643] |
| FD003 lstm NLL | 60/100 | 5 | 0.0935 [0.0361, 0.174] | 0.0879 [0.0402, 0.153] | -0.00563 [-0.0282, 0.0131] |
| FD003 lstm ECE5 | 60/100 | 5 | 0.0299 [0.0143, 0.0612] | 0.0163 [0.0105, 0.0458] | -0.0136 [-0.0194, 0.00167] |
| FD003 lstm ECE10 | 60/100 | 5 | 0.0382 [0.0231, 0.0704] | 0.0261 [0.0197, 0.0543] | -0.0122 [-0.0202, 0.00503] |
| FD003 lstm incompatibility_rate | 60/100 | 5 | 12.8 [8.2, 18.0] | 0.0 [0.0, 0.0] | -12.8 [-18.0, -8.2] |
| FD003 hybrid Brier | 60/100 | 5 | 0.0291 [0.0118, 0.0515] | 0.0227 [0.0095, 0.0409] | -0.00643 [-0.0129, -0.000557] |
| FD003 hybrid NLL | 60/100 | 5 | 0.0933 [0.0436, 0.159] | 0.0767 [0.0362, 0.132] | -0.0166 [-0.0326, -0.00188] |
| FD003 hybrid ECE5 | 60/100 | 5 | 0.0425 [0.0219, 0.0722] | 0.0284 [0.0181, 0.0543] | -0.0141 [-0.0214, -0.000427] |
| FD003 hybrid ECE10 | 60/100 | 5 | 0.047 [0.0283, 0.0777] | 0.0361 [0.0241, 0.0606] | -0.011 [-0.0205, 0.00123] |
| FD003 hybrid incompatibility_rate | 60/100 | 5 | 11.8 [7.6, 16.4] | 0.0 [0.0, 0.0] | -11.8 [-16.4, -7.6] |
| FD004 lstm Brier | 149/248 | 5 | 0.0529 [0.0339, 0.0746] | 0.0457 [0.0289, 0.0651] | -0.00721 [-0.0124, -0.00267] |
| FD004 lstm NLL | 149/248 | 5 | 0.173 [0.108, 0.249] | 0.146 [0.0939, 0.207] | -0.0267 [-0.0486, -0.00783] |
| FD004 lstm ECE5 | 149/248 | 5 | 0.0563 [0.0323, 0.0844] | 0.0426 [0.0198, 0.0689] | -0.0137 [-0.0179, -0.00919] |
| FD004 lstm ECE10 | 149/248 | 5 | 0.0593 [0.0405, 0.0886] | 0.0459 [0.0292, 0.073] | -0.0134 [-0.019, -0.00907] |
| FD004 lstm incompatibility_rate | 149/248 | 5 | 16.6 [13.1, 20.3] | 0.0 [0.0, 0.0] | -16.6 [-20.3, -13.1] |
| FD004 hybrid Brier | 149/248 | 5 | 0.0448 [0.0279, 0.0642] | 0.0403 [0.0248, 0.0576] | -0.00456 [-0.01, -0.000215] |
| FD004 hybrid NLL | 149/248 | 5 | 0.146 [0.0912, 0.208] | 0.128 [0.0823, 0.179] | -0.0186 [-0.0389, -0.00249] |
| FD004 hybrid ECE5 | 149/248 | 5 | 0.0379 [0.0177, 0.065] | 0.0295 [0.0114, 0.0546] | -0.0084 [-0.0128, -0.00201] |
| FD004 hybrid ECE10 | 149/248 | 5 | 0.0462 [0.0336, 0.0742] | 0.0381 [0.0285, 0.0643] | -0.00802 [-0.0144, -0.00162] |
| FD004 hybrid incompatibility_rate | 149/248 | 5 | 12.7 [9.8, 15.6] | 0.0 [0.0, 0.0] | -12.7 [-15.6, -9.8] |

## B. test: Within-subset combined

| Group/metric | Fit/evaluation engines | Fixed fits | Raw [CI] | Projected [CI] | Paired difference [CI] |
|---|---|---|---|---|---|
| FD001 combined Brier | 60/100 | 10 | 0.0352 [0.0143, 0.0617] | 0.0348 [0.0151, 0.0603] | -0.000343 [-0.00646, 0.00523] |
| FD001 combined NLL | 60/100 | 10 | 0.122 [0.0557, 0.208] | 0.117 [0.0536, 0.201] | -0.00477 [-0.0204, 0.00936] |
| FD001 combined ECE5 | 60/100 | 10 | 0.0163 [0.0121, 0.0504] | 0.0133 [0.0117, 0.0464] | -0.00307 [-0.0175, 0.0157] |
| FD001 combined ECE10 | 60/100 | 10 | 0.0387 [0.0312, 0.0745] | 0.028 [0.0224, 0.061] | -0.0106 [-0.025, 0.00149] |
| FD001 combined incompatibility_rate | 60/100 | 10 | 17.0 [11.8, 22.4] | 0.0 [0.0, 0.0] | -17.0 [-22.4, -11.8] |
| FD002 combined Brier | 156/259 | 10 | 0.0292 [0.0162, 0.044] | 0.0248 [0.0137, 0.0378] | -0.00444 [-0.0072, -0.00199] |
| FD002 combined NLL | 156/259 | 10 | 0.0999 [0.0572, 0.15] | 0.085 [0.049, 0.128] | -0.0149 [-0.024, -0.00663] |
| FD002 combined ECE5 | 156/259 | 10 | 0.0418 [0.0254, 0.0618] | 0.0356 [0.0201, 0.0535] | -0.00622 [-0.00913, -0.00415] |
| FD002 combined ECE10 | 156/259 | 10 | 0.0418 [0.0283, 0.0618] | 0.0362 [0.0245, 0.0549] | -0.00562 [-0.00809, -0.00299] |
| FD002 combined incompatibility_rate | 156/259 | 10 | 9.2 [6.9, 11.8] | 0.0 [0.0, 0.0] | -9.2 [-11.8, -6.9] |
| FD003 combined Brier | 60/100 | 10 | 0.0279 [0.0108, 0.0512] | 0.0243 [0.0103, 0.043] | -0.00356 [-0.00974, 0.00238] |
| FD003 combined NLL | 60/100 | 10 | 0.0934 [0.0411, 0.164] | 0.0823 [0.0387, 0.14] | -0.0111 [-0.0287, 0.00455] |
| FD003 combined ECE5 | 60/100 | 10 | 0.0362 [0.0196, 0.0662] | 0.0223 [0.0157, 0.049] | -0.0138 [-0.0193, -0.000698] |
| FD003 combined ECE10 | 60/100 | 10 | 0.0426 [0.0265, 0.0728] | 0.0311 [0.0225, 0.0567] | -0.0116 [-0.0189, 0.00223] |
| FD003 combined incompatibility_rate | 60/100 | 10 | 12.3 [8.4, 16.6] | 0.0 [0.0, 0.0] | -12.3 [-16.6, -8.4] |
| FD004 combined Brier | 149/248 | 10 | 0.0489 [0.0314, 0.0692] | 0.043 [0.0271, 0.0614] | -0.00588 [-0.0105, -0.00205] |
| FD004 combined NLL | 149/248 | 10 | 0.159 [0.1, 0.227] | 0.137 [0.0891, 0.194] | -0.0226 [-0.0407, -0.00728] |
| FD004 combined ECE5 | 149/248 | 10 | 0.0471 [0.0252, 0.0744] | 0.036 [0.0161, 0.0615] | -0.0111 [-0.0149, -0.00629] |
| FD004 combined ECE10 | 149/248 | 10 | 0.0527 [0.0378, 0.0812] | 0.042 [0.0298, 0.0683] | -0.0107 [-0.0158, -0.0062] |
| FD004 combined incompatibility_rate | 149/248 | 10 | 14.6 [11.8, 17.8] | 0.0 [0.0, 0.0] | -14.6 [-17.8, -11.8] |

## B. calibration: Every frozen group

| Group/metric | Fit/evaluation engines | Fixed fits | Raw [CI] | Projected [CI] | Paired difference [CI] |
|---|---|---|---|---|---|
| FD001 lstm Brier | 60/20 | 5 | 0.0425 [0.000184, 0.124] | 0.0408 [9.77e-05, 0.122] | -0.00172 [-0.00443, 0] |
| FD001 lstm NLL | 60/20 | 5 | 0.137 [0.00364, 0.386] | 0.128 [0.00248, 0.374] | -0.0087 [-0.022, 0] |
| FD001 lstm ECE5 | 60/20 | 5 | 0.0538 [0.00299, 0.151] | 0.047 [0.000601, 0.14] | -0.0068 [-0.0185, 0.000902] |
| FD001 lstm ECE10 | 60/20 | 5 | 0.0552 [0.00355, 0.151] | 0.048 [0.00242, 0.141] | -0.00718 [-0.0192, 0.000157] |
| FD001 lstm incompatibility_rate | 60/20 | 5 | 11.0 [0.0, 23.0] | 0.0 [0.0, 0.0] | -11.0 [-23.0, 0.0] |
| FD001 hybrid Brier | 60/20 | 5 | 0.0386 [3.44e-05, 0.114] | 0.037 [3.36e-05, 0.111] | -0.00151 [-0.00391, 0] |
| FD001 hybrid NLL | 60/20 | 5 | 0.116 [0.00146, 0.332] | 0.11 [0.00145, 0.322] | -0.00625 [-0.0158, 0] |
| FD001 hybrid ECE5 | 60/20 | 5 | 0.0511 [0.00144, 0.142] | 0.0458 [0.00137, 0.133] | -0.00529 [-0.0136, 1.62e-05] |
| FD001 hybrid ECE10 | 60/20 | 5 | 0.0516 [0.00144, 0.143] | 0.0463 [0.00144, 0.134] | -0.00529 [-0.0136, 1.62e-05] |
| FD001 hybrid incompatibility_rate | 60/20 | 5 | 6.0 [0.0, 13.0] | 0.0 [0.0, 0.0] | -6.0 [-13.0, 0.0] |
| FD002 lstm Brier | 156/52 | 5 | 0.00839 [0.000767, 0.0196] | 0.00721 [0.000414, 0.0174] | -0.00118 [-0.00242, -0.000209] |
| FD002 lstm NLL | 156/52 | 5 | 0.0329 [0.00823, 0.0668] | 0.0291 [0.00683, 0.0607] | -0.00374 [-0.00828, 9.41e-05] |
| FD002 lstm ECE5 | 156/52 | 5 | 0.0238 [0.00476, 0.0495] | 0.0191 [0.00524, 0.0444] | -0.0047 [-0.00823, 0.00109] |
| FD002 lstm ECE10 | 156/52 | 5 | 0.0267 [0.00779, 0.052] | 0.024 [0.00664, 0.0484] | -0.00273 [-0.00651, 0.000424] |
| FD002 lstm incompatibility_rate | 156/52 | 5 | 10.8 [4.6, 18.1] | 0.0 [0.0, 0.0] | -10.8 [-18.1, -4.6] |
| FD002 hybrid Brier | 156/52 | 5 | 0.0236 [0.00635, 0.0435] | 0.0176 [0.00452, 0.0348] | -0.00594 [-0.0142, 0.000826] |
| FD002 hybrid NLL | 156/52 | 5 | 0.0795 [0.026, 0.141] | 0.059 [0.0207, 0.108] | -0.0205 [-0.0493, 0.00259] |
| FD002 hybrid ECE5 | 156/52 | 5 | 0.0426 [0.0141, 0.0776] | 0.0333 [0.0131, 0.0664] | -0.00928 [-0.0169, 0.000671] |
| FD002 hybrid ECE10 | 156/52 | 5 | 0.0474 [0.0187, 0.0819] | 0.0431 [0.0173, 0.0761] | -0.00428 [-0.0125, 0.00321] |
| FD002 hybrid incompatibility_rate | 156/52 | 5 | 8.5 [3.8, 13.8] | 0.0 [0.0, 0.0] | -8.5 [-13.8, -3.8] |
| FD003 lstm Brier | 60/20 | 5 | 0.0503 [7.98e-08, 0.139] | 0.0403 [7.98e-08, 0.111] | -0.01 [-0.0284, 0.000173] |
| FD003 lstm NLL | 60/20 | 5 | 0.143 [7.74e-05, 0.393] | 0.119 [7.74e-05, 0.324] | -0.0234 [-0.0691, 0.00266] |
| FD003 lstm ECE5 | 60/20 | 5 | 0.0666 [7.74e-05, 0.178] | 0.0575 [7.74e-05, 0.154] | -0.00917 [-0.0233, 0.00257] |
| FD003 lstm ECE10 | 60/20 | 5 | 0.0671 [7.74e-05, 0.178] | 0.0586 [7.74e-05, 0.155] | -0.00844 [-0.0225, 0.00257] |
| FD003 lstm incompatibility_rate | 60/20 | 5 | 8.0 [0.0, 18.0] | 0.0 [0.0, 0.0] | -8.0 [-18.0, 0.0] |
| FD003 hybrid Brier | 60/20 | 5 | 0.0827 [5.85e-05, 0.208] | 0.066 [5.85e-05, 0.165] | -0.0167 [-0.0438, 0] |
| FD003 hybrid NLL | 60/20 | 5 | 0.295 [0.00212, 0.759] | 0.237 [0.00212, 0.607] | -0.0578 [-0.152, 0] |
| FD003 hybrid ECE5 | 60/20 | 5 | 0.0895 [0.00209, 0.226] | 0.0777 [0.00209, 0.195] | -0.0118 [-0.0311, 0] |
| FD003 hybrid ECE10 | 60/20 | 5 | 0.09 [0.00209, 0.226] | 0.0786 [0.00209, 0.196] | -0.0114 [-0.0307, 0] |
| FD003 hybrid incompatibility_rate | 60/20 | 5 | 5.0 [0.0, 14.0] | 0.0 [0.0, 0.0] | -5.0 [-14.0, 0.0] |
| FD004 lstm Brier | 149/50 | 5 | 0.0143 [0.00139, 0.033] | 0.00866 [0.00056, 0.0195] | -0.00569 [-0.0135, -0.000315] |
| FD004 lstm NLL | 149/50 | 5 | 0.0472 [0.011, 0.0985] | 0.0335 [0.00816, 0.0679] | -0.0137 [-0.0316, -0.000622] |
| FD004 lstm ECE5 | 149/50 | 5 | 0.0314 [0.00797, 0.0652] | 0.0218 [0.00483, 0.0481] | -0.00958 [-0.0173, -0.00217] |
| FD004 lstm ECE10 | 149/50 | 5 | 0.0337 [0.00995, 0.0666] | 0.0273 [0.00793, 0.0536] | -0.00637 [-0.0145, -2.57e-05] |
| FD004 lstm incompatibility_rate | 149/50 | 5 | 12.0 [5.2, 20.0] | 0.0 [0.0, 0.0] | -12.0 [-20.0, -5.2] |
| FD004 hybrid Brier | 149/50 | 5 | 0.0191 [0.00198, 0.048] | 0.0145 [0.00179, 0.0329] | -0.0046 [-0.0158, 0.00213] |
| FD004 hybrid NLL | 149/50 | 5 | 0.0625 [0.0129, 0.143] | 0.0504 [0.0129, 0.103] | -0.0122 [-0.0408, 0.00517] |
| FD004 hybrid ECE5 | 149/50 | 5 | 0.035 [0.00719, 0.0757] | 0.026 [0.00703, 0.0593] | -0.00901 [-0.0186, 0.00119] |
| FD004 hybrid ECE10 | 149/50 | 5 | 0.0387 [0.0119, 0.0782] | 0.0318 [0.0111, 0.0644] | -0.00682 [-0.0169, 0.00234] |
| FD004 hybrid incompatibility_rate | 149/50 | 5 | 10.0 [4.4, 16.4] | 0.0 [0.0, 0.0] | -10.0 [-16.4, -4.4] |

## B. calibration: Within-subset combined

| Group/metric | Fit/evaluation engines | Fixed fits | Raw [CI] | Projected [CI] | Paired difference [CI] |
|---|---|---|---|---|---|
| FD001 combined Brier | 60/20 | 10 | 0.0405 [0.000109, 0.119] | 0.0389 [7.96e-05, 0.116] | -0.00162 [-0.00406, 0] |
| FD001 combined NLL | 60/20 | 10 | 0.127 [0.00255, 0.359] | 0.119 [0.00205, 0.348] | -0.00747 [-0.019, 0] |
| FD001 combined ECE5 | 60/20 | 10 | 0.0524 [0.00249, 0.146] | 0.0464 [0.00107, 0.137] | -0.00605 [-0.0164, 0.000459] |
| FD001 combined ECE10 | 60/20 | 10 | 0.0534 [0.00249, 0.147] | 0.0472 [0.00201, 0.137] | -0.00623 [-0.0164, 8.65e-05] |
| FD001 combined incompatibility_rate | 60/20 | 10 | 8.5 [0.0, 18.0] | 0.0 [0.0, 0.0] | -8.5 [-18.0, 0.0] |
| FD002 combined Brier | 156/52 | 10 | 0.016 [0.00394, 0.0314] | 0.0124 [0.00244, 0.0261] | -0.00356 [-0.00786, 1.29e-05] |
| FD002 combined NLL | 156/52 | 10 | 0.0562 [0.0187, 0.102] | 0.0441 [0.0141, 0.0835] | -0.0121 [-0.0279, 0.000456] |
| FD002 combined ECE5 | 156/52 | 10 | 0.0332 [0.00998, 0.0634] | 0.0262 [0.00942, 0.0547] | -0.00699 [-0.012, -0.000139] |
| FD002 combined ECE10 | 156/52 | 10 | 0.0371 [0.0136, 0.0666] | 0.0336 [0.0122, 0.0615] | -0.0035 [-0.00917, 0.00148] |
| FD002 combined incompatibility_rate | 156/52 | 10 | 9.6 [4.4, 15.6] | 0.0 [0.0, 0.0] | -9.6 [-15.6, -4.4] |
| FD003 combined Brier | 60/20 | 10 | 0.0665 [2.92e-05, 0.174] | 0.0531 [2.92e-05, 0.138] | -0.0134 [-0.0361, 8.65e-05] |
| FD003 combined NLL | 60/20 | 10 | 0.219 [0.00108, 0.576] | 0.178 [0.00108, 0.464] | -0.0406 [-0.111, 0.00133] |
| FD003 combined ECE5 | 60/20 | 10 | 0.0781 [0.00106, 0.202] | 0.0676 [0.00106, 0.175] | -0.0105 [-0.0272, 0.00129] |
| FD003 combined ECE10 | 60/20 | 10 | 0.0785 [0.00106, 0.202] | 0.0686 [0.00106, 0.176] | -0.00991 [-0.0266, 0.00129] |
| FD003 combined incompatibility_rate | 60/20 | 10 | 6.5 [0.0, 14.0] | 0.0 [0.0, 0.0] | -6.5 [-14.0, 0.0] |
| FD004 combined Brier | 149/50 | 10 | 0.0167 [0.00221, 0.04] | 0.0116 [0.00181, 0.0257] | -0.00514 [-0.0141, 0.000347] |
| FD004 combined NLL | 149/50 | 10 | 0.0549 [0.0136, 0.118] | 0.042 [0.0118, 0.0835] | -0.0129 [-0.0351, 0.000975] |
| FD004 combined ECE5 | 149/50 | 10 | 0.0332 [0.0081, 0.0688] | 0.0239 [0.00643, 0.0535] | -0.0093 [-0.0173, -0.000832] |
| FD004 combined ECE10 | 149/50 | 10 | 0.0362 [0.012, 0.0718] | 0.0296 [0.0102, 0.0583] | -0.00659 [-0.0148, 0.000369] |
| FD004 combined incompatibility_rate | 149/50 | 10 | 11.0 [5.4, 17.4] | 0.0 [0.0, 0.0] | -11.0 [-17.4, -5.4] |

Brier uses unmodified probabilities; NLL alone clips to [1e-15,1-1e-15] and uses log1p for the non-event term. ECE5 uses label-free method-specific probability-quantile cuts, duplicates collapsed, fixed across bootstrap draws. ECE10 uses fixed equal-width bins. Both metrics average the fixed-model ECE values; they are not ECE of a model-averaged probability. ECE_bin_definitions.json records every edge set and occupied-bin count. Calibration endpoints are a separate recorded role, not independent validation of a fitted calibration map.

## C. Every frozen group: median_squared_error

| Group | Fit/test engines | Fits | Flag coefficient [CI] | Own mean MSE | Upper CI / mean | MDE 80% | MDE / mean | Undefined draws |
|---|---|---|---|---|---|---|---|---|
| FD001 lstm | 60/100 | 5 | 69.7 [-167, 405] | 217 | 187.0% | 429 | 198.1% | 0 |
| FD001 hybrid | 60/100 | 5 | -250 [-415, -95.3] | 259 | -36.8% | 227 | 87.6% | 0 |
| FD002 lstm | 156/259 | 5 | -138 [-240, -51] | 205 | -24.8% | 136 | 66.3% | 0 |
| FD002 hybrid | 156/259 | 5 | -149 [-311, -4.99] | 241 | -2.1% | 214 | 88.7% | 0 |
| FD003 lstm | 60/100 | 5 | -320 [-595, -71] | 323 | -22.0% | 380 | 117.6% | 0 |
| FD003 hybrid | 60/100 | 5 | -99.9 [-230, 29] | 234 | 12.4% | 186 | 79.3% | 0 |
| FD004 lstm | 149/248 | 5 | -36.3 [-276, 258] | 275 | 93.8% | 384 | 139.6% | 0 |
| FD004 hybrid | 149/248 | 5 | 90.2 [-147, 429] | 274 | 156.5% | 430 | 157.0% | 0 |

## C. Every frozen group: Brier

| Group | Fit/test engines | Fits | Flag coefficient [CI] | Own mean MSE | Upper CI / mean | MDE 80% | MDE / mean | Undefined draws |
|---|---|---|---|---|---|---|---|---|
| FD001 lstm | 60/100 | 5 | 0.0426 [-0.0369, 0.124] | 0.0356 | 348.9% | 0.115 | 324.3% | 0 |
| FD001 hybrid | 60/100 | 5 | -0.0143 [-0.0887, 0.055] | 0.0348 | 158.1% | 0.105 | 301.0% | 0 |
| FD002 lstm | 156/259 | 5 | 0.0908 [0.0332, 0.155] | 0.0251 | 615.7% | 0.0889 | 354.4% | 0 |
| FD002 hybrid | 156/259 | 5 | 0.103 [0.0365, 0.171] | 0.0333 | 513.2% | 0.0945 | 283.6% | 0 |
| FD003 lstm | 60/100 | 5 | 0.0822 [0.0155, 0.179] | 0.0267 | 672.7% | 0.12 | 450.5% | 0 |
| FD003 hybrid | 60/100 | 5 | 0.129 [0.0524, 0.209] | 0.0291 | 716.3% | 0.113 | 387.4% | 0 |
| FD004 lstm | 149/248 | 5 | 0.124 [0.0554, 0.202] | 0.0529 | 382.0% | 0.106 | 200.6% | 0 |
| FD004 hybrid | 149/248 | 5 | 0.103 [0.0247, 0.187] | 0.0448 | 416.7% | 0.117 | 260.6% | 0 |

## C. Within-subset combined: median_squared_error

| Group | Fit/test engines | Fits | Flag coefficient [CI] | Own mean MSE | Upper CI / mean | MDE 80% | MDE / mean | Undefined draws |
|---|---|---|---|---|---|---|---|---|
| FD001 combined | 60/100 | 10 | -90.2 [-271, 118] | 238 | 49.7% | 285 | 120.0% | 0 |
| FD002 combined | 156/259 | 10 | -144 [-270, -34.6] | 223 | -15.5% | 167 | 74.8% | 0 |
| FD003 combined | 60/100 | 10 | -210 [-390, -42.2] | 279 | -15.1% | 254 | 91.1% | 0 |
| FD004 combined | 149/248 | 10 | 27 [-204, 343] | 274 | 125.0% | 401 | 146.2% | 0 |

## C. Within-subset combined: Brier

| Group | Fit/test engines | Fits | Flag coefficient [CI] | Own mean MSE | Upper CI / mean | MDE 80% | MDE / mean | Undefined draws |
|---|---|---|---|---|---|---|---|---|
| FD001 combined | 60/100 | 10 | 0.0141 [-0.0532, 0.0796] | 0.0352 | 226.2% | 0.097 | 275.8% | 0 |
| FD002 combined | 156/259 | 10 | 0.0971 [0.0447, 0.148] | 0.0292 | 506.2% | 0.0745 | 254.9% | 0 |
| FD003 combined | 60/100 | 10 | 0.106 [0.0437, 0.18] | 0.0279 | 644.3% | 0.0967 | 346.6% | 0 |
| FD004 combined | 149/248 | 10 | 0.113 [0.049, 0.186] | 0.0489 | 381.0% | 0.0965 | 197.5% | 0 |

## C. Across-subset pooled: median_squared_error

| Group | Fit/test engines | Fits | Flag coefficient [CI] | Own mean MSE | Upper CI / mean | MDE 80% | MDE / mean | Undefined draws |
|---|---|---|---|---|---|---|---|---|
| FD001-FD004 combined | 425/707 | 40 | -85.6 [-191, 37.1] | 251 | 14.8% | 162 | 64.4% | 0 |

## C. Across-subset pooled: Brier

| Group | Fit/test engines | Fits | Flag coefficient [CI] | Own mean MSE | Upper CI / mean | MDE 80% | MDE / mean | Undefined draws |
|---|---|---|---|---|---|---|---|---|
| FD001-FD004 combined | 425/707 | 40 | 0.0922 [0.0589, 0.126] | 0.0368 | 343.7% | 0.0485 | 131.9% | 0 |

For point error, the mean is squared error of the saved unprojected median against true RUL capped at 125, in cycles squared. For Brier, the mean is the raw event-probability MSE. Upper-endpoint ratios are signed and use the observed group mean denominator; they are not explained-variance percentages.

The MDE is approximate: (Phi^-1(0.975)+Phi^-1(0.80)) times the saved engine-bootstrap coefficient SD (ddof=1), for a two-sided alpha=0.05 normal/Wald test. It is not an exact bounded-outcome power simulation or an observed-effect power calculation. Existing percentile CIs are unchanged. The pooled coefficient is an engine-count-weighted average of group-specific adjusted effects, not a common-slope pooled regression.

## D. Dependence and independent engine units

| Subset/role | Fitting engines | Evaluation engines | Architectures | Seeds/architecture | Fixed fits | Engine/run rows | Shared across architectures/seeds |
|---|---|---|---|---|---|---|---|
| FD001 test | 60 | 100 | 2 | 5 | 10 | 1000 | yes / yes |
| FD002 test | 156 | 259 | 2 | 5 | 10 | 2590 | yes / yes |
| FD003 test | 60 | 100 | 2 | 5 | 10 | 1000 | yes / yes |
| FD004 test | 149 | 248 | 2 | 5 | 10 | 2480 | yes / yes |
| FD001 calibration | 60 | 20 | 2 | 5 | 10 | 200 | yes / yes |
| FD002 calibration | 156 | 52 | 2 | 5 | 10 | 520 | yes / yes |
| FD003 calibration | 60 | 20 | 2 | 5 | 10 | 200 | yes / yes |
| FD004 calibration | 149 | 50 | 2 | 5 | 10 | 500 | yes / yes |

Both architectures and all five seeds share the same engines within a subset and role. IDs are namespaced by subset and role; calibration and official-test engines are never pooled. Across subsets, independent resampling streams are used. The pooled test estimate contains 707 engine clusters; the separately pooled calibration estimate contains 142. Engine IDs are saved in D_dependence.csv. Bootstrap indices/counts remain synchronized across methods and architectures within each subset.

## Files, checks and provenance

- A_controls.csv: all group, subset-combined and pooled control estimates/CIs.
- B_projection.csv: all raw/projected scores, marginal CIs and paired-difference CIs for both roles.
- C_effect_sizes_power.csv: every coefficient, CI, outcome mean, signed relative upper endpoint, bootstrap SE and approximate MDE.
- A_per_seed.csv, B_per_seed.csv, A_uniform_per_draw.csv: all fixed seeds and realizations.
- ECE_bin_definitions.json, bootstrap_*.npz, projection_*.npz, uniform_*.npz: fixed scoring and resampling records.
- checks.json: source reproduction, zero projection incompatibility, direct ECE checks and unchanged inputs.

All 89 experimental input files used by the analysis remained unchanged. Independent human review is still missing.

AI identifiers: configured model `gpt-6.1-sol`; runtime `0.166.0-alpha.5.1`; desktop build `26.1027.3384.0`. Exact served checkpoint remains unavailable. Saved source provenance and current session identity records are retained.

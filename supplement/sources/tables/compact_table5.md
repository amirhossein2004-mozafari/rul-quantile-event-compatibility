| Subset | Method | Brier | NLL | ECE5 [95% CI] | Skill |
| --- | --- | --- | --- | --- | --- |
| FD001 | Raw | 0.0339 | 0.1288 | 0.0259 [0.0077, 0.0635] | 0.828 |
| FD001 | TrainOff | 0.0470 | 0.1467 | 0.0431 [0.0153, 0.0865] | 0.762 |
| FD001 | CalPrior | 0.0493 | 0.1529 | 0.0443 [0.0172, 0.0910] | 0.750 |
| FD001 | Platt | 0.0422 | 0.1336 | 0.0365 [0.0123, 0.0779] | 0.786 |
| FD001 | Isotonic | 0.0417 | 0.3178 | 0.0313 [0.0118, 0.0732] | 0.789 |
| FD001 | Beta | 0.0421 | 0.1327 | 0.0358 [0.0125, 0.0778] | 0.787 |
| FD001 | FeatLR | 0.0629 | 0.2051 | 0.0602 [0.0192, 0.1093] | 0.681 |
| FD002 | Raw | 0.0302 | 0.1030 | 0.0448 [0.0258, 0.0663] | 0.839 |
| FD002 | TrainOff | 0.0158 | 0.0575 | 0.0155 [0.0040, 0.0318] | 0.916 |
| FD002 | CalPrior | 0.0151 | 0.0549 | 0.0123 [0.0036, 0.0273] | 0.920 |
| FD002 | Platt | 0.0156 | 0.0571 | 0.0148 [0.0049, 0.0301] | 0.917 |
| FD002 | Isotonic | 0.0156 | 0.0560 | 0.0143 [0.0049, 0.0298] | 0.917 |
| FD002 | Beta | 0.0159 | 0.0566 | 0.0147 [0.0050, 0.0304] | 0.915 |
| FD002 | FeatLR | 0.0291 | 0.1098 | 0.0228 [0.0096, 0.0432] | 0.845 |
| FD003 | Raw | 0.0269 | 0.0908 | 0.0314 [0.0116, 0.0675] | 0.837 |
| FD003 | TrainOff | 0.0223 | 0.0697 | 0.0137 [0.0087, 0.0419] | 0.864 |
| FD003 | CalPrior | 0.0226 | 0.0703 | 0.0132 [0.0090, 0.0434] | 0.863 |
| FD003 | Platt | 0.0219 | 0.0678 | 0.0128 [0.0072, 0.0417] | 0.867 |
| FD003 | Isotonic | 0.0232 | 0.0719 | 0.0121 [0.0064, 0.0424] | 0.859 |
| FD003 | Beta | 0.0219 | 0.0677 | 0.0130 [0.0072, 0.0418] | 0.867 |
| FD003 | FeatLR | 0.0415 | 0.1406 | 0.0227 [0.0097, 0.0664] | 0.748 |
| FD004 | Raw | 0.0395 | 0.1278 | 0.0320 [0.0123, 0.0578] | 0.774 |
| FD004 | TrainOff | 0.0329 | 0.1113 | 0.0157 [0.0085, 0.0406] | 0.812 |
| FD004 | CalPrior | 0.0331 | 0.1126 | 0.0176 [0.0080, 0.0426] | 0.810 |
| FD004 | Platt | 0.0317 | 0.1059 | 0.0100 [0.0072, 0.0308] | 0.818 |
| FD004 | Isotonic | 0.0327 | 0.1326 | 0.0101 [0.0073, 0.0307] | 0.813 |
| FD004 | Beta | 0.0319 | 0.1066 | 0.0091 [0.0072, 0.0301] | 0.818 |
| FD004 | FeatLR | 0.0476 | 0.1546 | 0.0206 [0.0076, 0.0495] | 0.728 |

: Fixed seven-method display for the original 20 hybrid models, mean over five runs per subset; all 14 methods and all 80 matched models remain in Supplement S32 and CSVs. TrainOff: training-weight offset; CalPrior: additional calibration-prefix prior adjustment; FeatLR: last-observation logistic regression. Skill is relative to the engine-balanced all-prefix calibration constant; endpoint-reference skill is retained separately. ECE5 uses probability-quantile bins, not the historical ten equal-width bins. Paired crossed run/engine percentile intervals use 1000 draws, conditional on fitted models/calibrators and fixed empirical bin edges; they exclude calibration-refit and population/split uncertainty.
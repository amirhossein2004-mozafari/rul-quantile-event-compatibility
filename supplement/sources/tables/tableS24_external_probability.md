| Model | Method | Brier | NLL | Incompatible (%) | Mean distance |
| --- | --- | --- | --- | --- | --- |
| LSTM | Raw | 0.04250 ± 0.00184 | 0.15944 ± 0.01028 | 10.24 ± 2.11 | 0.0056 ± 0.0023 |
| LSTM | Bayes | 0.04401 ± 0.00303 | 0.17587 ± 0.01579 | 10.80 ± 1.95 | 0.0049 ± 0.0014 |
| Hybrid | Raw | 0.04554 ± 0.00891 | 0.18238 ± 0.04944 | 11.05 ± 2.41 | 0.0082 ± 0.0052 |
| Hybrid | Bayes | 0.04634 ± 0.00946 | 0.19301 ± 0.05776 | 12.15 ± 1.06 | 0.0099 ± 0.0049 |

: DS01 probability and nominal-compatibility outcomes: engine-balanced metrics, five-seed mean ± sample SD. Bayes is the existing fixed training-weight logit offset; no temperature or other calibrator is fitted. Both methods retain identical nominal quantiles within a trained model. All per-engine and per-flight records, including unfavorable outcomes, are retained.

| Subset | Model | RMSE | MAE | Raw Brier |
| --- | --- | --- | --- | --- |
| FD001 | GRU | 14.3 ± 0.4 | 10.4 ± 0.2 | 0.0285 ± 0.0076 |
| FD001 | Hybrid | 15.9 ± 1.2 | 11.8 ± 0.7 | 0.0348 ± 0.0073 |
| FD001 | LSTM | 14.7 ± 0.6 | 10.9 ± 0.4 | 0.0356 ± 0.0043 |
| FD001 | TCN | 18.1 ± 2.9 | 13.7 ± 2.5 | 0.0314 ± 0.0071 |
| FD002 | GRU | 13.6 ± 0.5 | 9.8 ± 0.5 | 0.0258 ± 0.0065 |
| FD002 | Hybrid | 15.4 ± 1.4 | 10.8 ± 1.4 | 0.0333 ± 0.0142 |
| FD002 | LSTM | 14.3 ± 0.5 | 9.9 ± 0.4 | 0.0251 ± 0.0034 |
| FD002 | TCN | 18.5 ± 2.2 | 14.3 ± 1.9 | 0.0393 ± 0.0078 |
| FD003 | GRU | 14.7 ± 0.9 | 10.3 ± 0.5 | 0.0241 ± 0.0042 |
| FD003 | Hybrid | 15.2 ± 0.8 | 11.0 ± 1.0 | 0.0291 ± 0.0149 |
| FD003 | LSTM | 17.9 ± 1.1 | 12.5 ± 0.8 | 0.0267 ± 0.0086 |
| FD003 | TCN | 18.7 ± 1.9 | 14.5 ± 1.6 | 0.0283 ± 0.0042 |
| FD004 | GRU | 14.9 ± 0.4 | 10.2 ± 0.7 | 0.0334 ± 0.0038 |
| FD004 | Hybrid | 16.5 ± 0.3 | 11.6 ± 0.5 | 0.0448 ± 0.0038 |
| FD004 | LSTM | 16.6 ± 0.3 | 11.1 ± 0.4 | 0.0529 ± 0.0030 |
| FD004 | TCN | 19.3 ± 1.2 | 14.4 ± 1.4 | 0.0666 ± 0.0049 |

: Expanded equal-search comparison: five final initialization seeds per architecture on the same fitting/validation/calibration partition. Mean ± sample SD. Lower error/Brier is better. Forty frozen LSTM/hybrid fits are reused; forty TCN/GRU fits are new. Selection uses validation RMSE alone, with the same three learning rates and maximum 16 epochs for each architecture. Actual compute and parameter counts differ; these are not independent fleets or nested cross-validation results.
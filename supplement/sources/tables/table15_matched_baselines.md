| Subset | Model | RMSE | MAE | Raw Brier |
| --- | --- | --- | --- | --- |
| FD001 | gru | 14.3494 ± 0.4449 | 10.3823 ± 0.1771 | 0.0285 ± 0.0076 |
| FD001 | hybrid | 15.9108 ± 1.2489 | 11.7618 ± 0.7155 | 0.0348 ± 0.0073 |
| FD001 | lstm | 14.7117 ± 0.6390 | 10.9331 ± 0.4481 | 0.0356 ± 0.0043 |
| FD001 | tcn | 18.1294 ± 2.9193 | 13.6943 ± 2.4798 | 0.0314 ± 0.0071 |
| FD002 | gru | 13.6144 ± 0.4828 | 9.7550 ± 0.5010 | 0.0258 ± 0.0065 |
| FD002 | hybrid | 15.3935 ± 1.4420 | 10.8461 ± 1.4196 | 0.0333 ± 0.0142 |
| FD002 | lstm | 14.3200 ± 0.5281 | 9.8711 ± 0.4449 | 0.0251 ± 0.0034 |
| FD002 | tcn | 18.4807 ± 2.1678 | 14.3204 ± 1.9362 | 0.0393 ± 0.0078 |
| FD003 | gru | 14.7444 ± 0.8609 | 10.3128 ± 0.4978 | 0.0241 ± 0.0042 |
| FD003 | hybrid | 15.2379 ± 0.7841 | 11.0338 ± 0.9612 | 0.0291 ± 0.0149 |
| FD003 | lstm | 17.9138 ± 1.0708 | 12.5456 ± 0.8097 | 0.0267 ± 0.0086 |
| FD003 | tcn | 18.6511 ± 1.9062 | 14.4983 ± 1.5771 | 0.0283 ± 0.0042 |
| FD004 | gru | 14.9330 ± 0.3840 | 10.1701 ± 0.6750 | 0.0334 ± 0.0038 |
| FD004 | hybrid | 16.5418 ± 0.3357 | 11.5794 ± 0.5176 | 0.0448 ± 0.0038 |
| FD004 | lstm | 16.5609 ± 0.3404 | 11.1408 ± 0.4292 | 0.0529 ± 0.0030 |
| FD004 | tcn | 19.3297 ± 1.1805 | 14.4042 ± 1.4120 | 0.0666 ± 0.0049 |

: Expanded equal-search comparison: five final initialization seeds per architecture on the same fitting/validation/calibration partition. Mean ± sample SD. Lower error/Brier is better. Forty frozen LSTM/hybrid fits are reused; forty TCN/GRU fits are new. Selection uses validation RMSE alone, with the same three learning rates and maximum 16 epochs for each architecture. Actual compute and parameter counts differ; these are not independent fleets or nested cross-validation results.


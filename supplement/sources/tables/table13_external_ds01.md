| Model | RMSE | Brier | Raw Winkler | Incompatible (%) |
| --- | --- | --- | --- | --- |
| LSTM | 9.014 ± 0.946 | 0.04250 ± 0.00184 | 35.575 ± 4.194 | 10.24 ± 2.11 |
| Hybrid | 8.068 ± 0.496 | 0.04554 ± 0.00891 | 30.803 ± 2.423 | 11.05 ± 2.41 |

: Prospectively specified N-CMAPSS DS01 evaluation: five-seed mean ± sample SD after retraining each architecture on 6 official development engines. Every metric first averages within an engine, then across the same 4 official test engines (341 eligible flights), with RMSE obtained from engine-balanced MSE. RUL errors and Winkler use flight-cycle units. Compatibility uses nominal quantiles and the fixed 30-flight-cycle event. Raw intervals are uncalibrated. These are different targets, sampling and training budgets from the C-MAPSS experiments; scores must not be pooled across datasets. Seeds are repeated fits on the same test engines, not independent fleets.

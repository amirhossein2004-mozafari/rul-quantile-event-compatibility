| Subset | Arm | Runs | RMSE | MAE | Raw Brier |
| --- | --- | --- | --- | --- | --- |
| FD001 | lstm | 20 | 14.92915 ± 1.15000 | 10.83848 ± 0.85126 | 0.02455 ± 0.00379 |
| FD001 | hybrid | 20 | 15.57547 ± 1.20704 | 11.53303 ± 0.84575 | 0.03479 ± 0.00622 |
| FD001 | pcgrad | 20 | 14.89803 ± 0.69285 | 11.00736 ± 0.54287 | 0.02875 ± 0.00514 |
| FD002 | lstm | 20 | 14.99119 ± 0.63183 | 10.52083 ± 0.51167 | 0.02484 ± 0.00605 |
| FD002 | hybrid | 20 | 16.36660 ± 1.91614 | 11.91263 ± 1.63953 | 0.03241 ± 0.00963 |
| FD003 | lstm | 20 | 15.56755 ± 0.87404 | 10.82558 ± 0.69280 | 0.02480 ± 0.00712 |
| FD003 | hybrid | 20 | 15.17537 ± 1.01192 | 10.79386 ± 0.88561 | 0.02614 ± 0.00786 |
| FD004 | lstm | 20 | 15.00729 ± 0.60942 | 10.19022 ± 0.27975 | 0.03839 ± 0.00757 |
| FD004 | hybrid | 20 | 17.07295 ± 2.03736 | 12.67202 ± 1.84497 | 0.04712 ± 0.00872 |

: Expanded common-schedule cohort: mean ± sample SD across 20 observed paired seed/split replications. Five verified historical fits and fifteen additions contribute to each architecture/subset group and the FD001 PCGrad group. The same official-test engines recur across all runs. RMSE/MAE are in cycles; probability outputs use the unchanged raw event head. No model is selected by these new test results.

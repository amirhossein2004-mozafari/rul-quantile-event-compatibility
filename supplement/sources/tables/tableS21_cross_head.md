| Subset | Model | Method | Incompatible (%) | Mean distance | Brier |
| --- | --- | --- | --- | --- | --- |
| FD001 | LSTM | Raw | 20.40 ± 4.56 | 0.0210 ± 0.0061 | 0.03561 ± 0.00429 |
| FD001 | LSTM | Bayes | 18.00 ± 2.45 | 0.0228 ± 0.0042 | 0.05276 ± 0.00569 |
| FD001 | LSTM | Temp | 31.40 ± 2.30 | 0.0369 ± 0.0108 | 0.04191 ± 0.00368 |
| FD001 | LSTM | ShiftTemp | 19.20 ± 2.68 | 0.0260 ± 0.0089 | 0.05722 ± 0.00906 |
| FD001 | Hybrid | Raw | 13.60 ± 3.91 | 0.0138 ± 0.0075 | 0.03477 ± 0.00728 |
| FD001 | Hybrid | Bayes | 12.20 ± 4.66 | 0.0156 ± 0.0065 | 0.04555 ± 0.00874 |
| FD001 | Hybrid | Temp | 18.60 ± 4.98 | 0.0197 ± 0.0097 | 0.03656 ± 0.00793 |
| FD001 | Hybrid | ShiftTemp | 13.20 ± 3.90 | 0.0176 ± 0.0066 | 0.05030 ± 0.01049 |
| FD002 | LSTM | Raw | 9.58 ± 1.38 | 0.0067 ± 0.0021 | 0.02510 ± 0.00343 |
| FD002 | LSTM | Bayes | 3.47 ± 1.16 | 0.0008 ± 0.0003 | 0.01361 ± 0.00301 |
| FD002 | LSTM | Temp | 11.20 ± 0.91 | 0.0141 ± 0.0057 | 0.03357 ± 0.00673 |
| FD002 | LSTM | ShiftTemp | 11.35 ± 0.21 | 0.0079 ± 0.0010 | 0.01507 ± 0.00702 |
| FD002 | Hybrid | Raw | 8.88 ± 2.69 | 0.0072 ± 0.0040 | 0.03333 ± 0.01419 |
| FD002 | Hybrid | Bayes | 6.64 ± 2.61 | 0.0060 ± 0.0036 | 0.02090 ± 0.00967 |
| FD002 | Hybrid | Temp | 13.36 ± 6.94 | 0.0129 ± 0.0075 | 0.03598 ± 0.01190 |
| FD002 | Hybrid | ShiftTemp | 12.82 ± 1.00 | 0.0131 ± 0.0045 | 0.02314 ± 0.00930 |
| FD003 | LSTM | Raw | 12.80 ± 4.09 | 0.0150 ± 0.0081 | 0.02666 ± 0.00860 |
| FD003 | LSTM | Bayes | 7.00 ± 2.74 | 0.0024 ± 0.0016 | 0.02669 ± 0.00261 |
| FD003 | LSTM | Temp | 25.00 ± 5.79 | 0.0263 ± 0.0106 | 0.03403 ± 0.00747 |
| FD003 | LSTM | ShiftTemp | 11.00 ± 3.81 | 0.0053 ± 0.0033 | 0.02708 ± 0.00329 |
| FD003 | Hybrid | Raw | 11.80 ± 3.27 | 0.0149 ± 0.0113 | 0.02915 ± 0.01492 |
| FD003 | Hybrid | Bayes | 8.60 ± 4.34 | 0.0081 ± 0.0025 | 0.02207 ± 0.00476 |
| FD003 | Hybrid | Temp | 36.20 ± 12.40 | 0.0398 ± 0.0160 | 0.03750 ± 0.01141 |
| FD003 | Hybrid | ShiftTemp | 23.80 ± 10.18 | 0.0248 ± 0.0095 | 0.03268 ± 0.01069 |
| FD004 | LSTM | Raw | 16.61 ± 2.08 | 0.0137 ± 0.0029 | 0.05290 ± 0.00297 |
| FD004 | LSTM | Bayes | 5.89 ± 1.68 | 0.0013 ± 0.0005 | 0.03499 ± 0.00236 |
| FD004 | LSTM | Temp | 16.69 ± 2.76 | 0.0186 ± 0.0067 | 0.05904 ± 0.00580 |
| FD004 | LSTM | ShiftTemp | 19.60 ± 2.33 | 0.0124 ± 0.0028 | 0.04141 ± 0.00720 |
| FD004 | Hybrid | Raw | 12.66 ± 2.50 | 0.0086 ± 0.0031 | 0.04484 ± 0.00384 |
| FD004 | Hybrid | Bayes | 13.23 ± 3.55 | 0.0102 ± 0.0053 | 0.03787 ± 0.00415 |
| FD004 | Hybrid | Temp | 15.32 ± 6.64 | 0.0126 ± 0.0072 | 0.05017 ± 0.00972 |
| FD004 | Hybrid | ShiftTemp | 19.84 ± 3.41 | 0.0225 ± 0.0069 | 0.04513 ± 0.00622 |

: All four probability methods for nominal cross-head compatibility: mean ± sample SD across five final seeds. Percentage and distance use all engines; Brier is independently recomputed from official event labels and matches the previously retained probability-context results. A smaller incompatibility fraction or distance does not establish probability calibration or better prediction. Per-run CSVs retain counts, denominators and tolerance sensitivity.

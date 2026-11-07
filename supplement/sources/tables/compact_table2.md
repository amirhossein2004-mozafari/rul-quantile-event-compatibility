| Subset | Model | Engines/run | Raw incompatible (%) | Temp incompatible (%) | Raw mean distance |
| --- | --- | --- | --- | --- | --- |
| FD001 | LSTM | 100 | 20.40 ± 4.56 | 31.40 ± 2.30 | 0.0210 ± 0.0061 |
| FD001 | Hybrid | 100 | 13.60 ± 3.91 | 18.60 ± 4.98 | 0.0138 ± 0.0075 |
| FD002 | LSTM | 259 | 9.58 ± 1.38 | 11.20 ± 0.91 | 0.0067 ± 0.0021 |
| FD002 | Hybrid | 259 | 8.88 ± 2.69 | 13.36 ± 6.94 | 0.0072 ± 0.0040 |
| FD003 | LSTM | 100 | 12.80 ± 4.09 | 25.00 ± 5.79 | 0.0150 ± 0.0081 |
| FD003 | Hybrid | 100 | 11.80 ± 3.27 | 36.20 ± 12.40 | 0.0149 ± 0.0113 |
| FD004 | LSTM | 248 | 16.61 ± 2.08 | 16.69 ± 2.76 | 0.0137 ± 0.0029 |
| FD004 | Hybrid | 248 | 12.66 ± 2.50 | 15.32 ± 6.64 | 0.0086 ± 0.0031 |

: Nominal quantile/event compatibility at 30 cycles for the frozen equal-search models: five-seed mean ± sample SD. Incompatibility is distance beyond the necessary quantile-implied probability bounds greater than 1e-6. Distance is in probability units and averaged over every test engine, including zero distances. Temp changes only the probability output; nominal quantiles remain fixed. The same official-test engines recur across seeds. This is an exploratory internal-consistency diagnostic, not a calibration or population-coverage estimate. All four probability methods and individual run counts appear in Supplementary Tables S21-S22 and the attached CSVs.
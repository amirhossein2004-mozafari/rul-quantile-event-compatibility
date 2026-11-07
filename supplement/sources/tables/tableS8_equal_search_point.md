| Subset | Model | RMSE | MAE | NASA sum | Raw F1 |
| --- | --- | --- | --- | --- | --- |
| FD001 | LSTM | 14.712 ± 0.639 | 10.933 ± 0.448 | 364.6 ± 65.6 | 0.9213 ± 0.0160 |
| FD001 | Hybrid | 15.911 ± 1.249 | 11.762 ± 0.716 | 552.5 ± 223.7 | 0.9191 ± 0.0243 |
| FD002 | LSTM | 14.320 ± 0.528 | 9.871 ± 0.445 | 1171.1 ± 141.2 | 0.9244 ± 0.0141 |
| FD002 | Hybrid | 15.393 ± 1.442 | 10.846 ± 1.420 | 1481.9 ± 157.3 | 0.9109 ± 0.0271 |
| FD003 | LSTM | 17.914 ± 1.071 | 12.546 ± 0.810 | 1189.6 ± 409.8 | 0.9303 ± 0.0254 |
| FD003 | Hybrid | 15.238 ± 0.784 | 11.034 ± 0.961 | 404.7 ± 80.6 | 0.9057 ± 0.0384 |
| FD004 | LSTM | 16.561 ± 0.340 | 11.141 ± 0.429 | 1748.0 ± 282.1 | 0.8458 ± 0.0077 |
| FD004 | Hybrid | 16.542 ± 0.336 | 11.579 ± 0.518 | 1675.1 ± 359.4 | 0.8690 ± 0.0205 |

: Equal-search study point and discrimination outcomes: mean ± sample SD over five initialization seeds. RMSE and MAE use capped targets and projected medians; NASA is the within-run sum over engines. F1 uses raw probability at threshold 0.5. These engines and partitions are fixed across the five final seeds.

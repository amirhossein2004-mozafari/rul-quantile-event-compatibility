| Subset | Model | Raw Brier | Raw ECE | Exact coverage | Exact Winkler | Forward (ms) |
| --------- | --------- | ------------- | ------------- | ------------------- | ------------------ | ------------------- |
| FD001 | LSTM | 0.03561 | 0.03798 | 0.9480 | 56.623 | 0.545 |
| FD001 | Hybrid | 0.03477 | 0.03936 | 0.9280 | 59.930 | 3.044 |
| FD002 | LSTM | 0.02510 | 0.03638 | 0.9776 | 53.683 | 0.540 |
| FD002 | Hybrid | 0.03333 | 0.04720 | 0.9668 | 55.997 | 3.119 |
| FD003 | LSTM | 0.02666 | 0.03823 | 0.9400 | 69.179 | 0.573 |
| FD003 | Hybrid | 0.02915 | 0.04702 | 0.9460 | 59.152 | 3.158 |
| FD004 | LSTM | 0.05290 | 0.05931 | 0.9548 | 58.386 | 0.545 |
| FD004 | Hybrid | 0.04484 | 0.04617 | 0.9065 | 61.330 | 3.155 |

: Secondary outcomes in the equal-search study: seed means. Winkler is in cycles. Forward time is the mean across seeds of each model's 300-call batch-one median on the same CPU with one thread, after 50 warmup calls. Preprocessing and calibration are excluded. Hyperparameter selection optimized RMSE only; complete method summaries and sample SDs appear in Supplementary Tables S8-S11.

| Subset | Model | Learning rate | Best epoch | Validation RMSE | Delta |
| -------- | ---------- | -------------- | ------------ | ------------------ | -------------- |
| FD001 | LSTM | 0.0002 | 10 | 15.3324 | 0.0000 |
| FD001 | LSTM | 0.0005 | 9 | 16.3936 | 1.0612 |
| FD001 | LSTM | 0.001 | 8 | 15.3755 | 0.0431 |
| FD001 | Hybrid | 0.0002 | 16 | 15.2178 | 1.2515 |
| FD001 | Hybrid | 0.0005 | 7 | 15.0298 | 1.0635 |
| FD001 | Hybrid | 0.001 | 7 | 13.9663 | 0.0000 |
| FD002 | LSTM | 0.0002 | 9 | 16.8537 | 0.2712 |
| FD002 | LSTM | 0.0005 | 9 | 16.5825 | 0.0000 |
| FD002 | LSTM | 0.001 | 6 | 17.0225 | 0.4401 |
| FD002 | Hybrid | 0.0002 | 9 | 16.5779 | 0.0101 |
| FD002 | Hybrid | 0.0005 | 5 | 17.2831 | 0.7152 |
| FD002 | Hybrid | 0.001 | 5 | 16.5678 | 0.0000 |
| FD003 | LSTM | 0.0002 | 16 | 15.4238 | 1.4249 |
| FD003 | LSTM | 0.0005 | 11 | 13.9990 | 0.0000 |
| FD003 | LSTM | 0.001 | 8 | 14.4716 | 0.4726 |
| FD003 | Hybrid | 0.0002 | 16 | 15.9830 | 4.2155 |
| FD003 | Hybrid | 0.0005 | 11 | 13.6935 | 1.9260 |
| FD003 | Hybrid | 0.001 | 15 | 11.7675 | 0.0000 |
| FD004 | LSTM | 0.0002 | 6 | 20.5520 | 1.7638 |
| FD004 | LSTM | 0.0005 | 9 | 18.7882 | 0.0000 |
| FD004 | LSTM | 0.001 | 9 | 19.7845 | 0.9964 |
| FD004 | Hybrid | 0.0002 | 14 | 20.0506 | 0.0323 |
| FD004 | Hybrid | 0.0005 | 10 | 20.0182 | 0.0000 |
| FD004 | Hybrid | 0.001 | 8 | 20.2352 | 0.2170 |

: Validation-only configuration sensitivity. Each row is the minimum capped validation RMSE over 16 epochs for one learning rate and tuning seed 101. Delta is that rate's minimum minus the frozen selected minimum for the same subset/architecture; zero identifies the selected rate. Epoch ties use the earliest epoch; global ties use candidate order then epoch. No test metric enters these calculations or changes the selected configurations. Differences are descriptive on one fixed validation split, not confidence intervals or stability estimates over new splits/seeds.

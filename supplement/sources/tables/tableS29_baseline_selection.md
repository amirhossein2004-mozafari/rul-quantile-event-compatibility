| Subset/model | Learning rate | Epochs | Validation RMSE |
| --- | --- | --- | --- |
| FD001/gru | 0.001 | 6 | 13.7629 |
| FD001/hybrid | 0.001 | 7 | 13.9663 |
| FD001/lstm | 0.0002 | 10 | 15.3324 |
| FD001/tcn | 0.001 | 14 | 19.0577 |
| FD002/gru | 0.0002 | 16 | 15.5417 |
| FD002/hybrid | 0.001 | 5 | 16.5678 |
| FD002/lstm | 0.0005 | 9 | 16.5825 |
| FD002/tcn | 0.0005 | 12 | 18.9763 |
| FD003/gru | 0.0005 | 15 | 11.2421 |
| FD003/hybrid | 0.001 | 15 | 11.7675 |
| FD003/lstm | 0.0005 | 11 | 13.9990 |
| FD003/tcn | 0.001 | 16 | 17.2951 |
| FD004/gru | 0.001 | 11 | 17.1372 |
| FD004/hybrid | 0.0005 | 10 | 20.0182 |
| FD004/lstm | 0.0005 | 9 | 18.7882 |
| FD004/tcn | 0.0002 | 10 | 21.5608 |

: All selected configurations, including unchanged LSTM/hybrid selections. Each architecture has three candidates and 16 epochs per tuning candidate; final refits use the selected epoch budget. Validation results are selection statistics, not held-out generalization estimates.


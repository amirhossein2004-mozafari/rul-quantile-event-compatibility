| Subset | Model | RMSE | MAE | Raw F1 |
| --- | ---: | ---: | ---: | ---: |
| FD001 | LSTM | 14.944 ± 1.455 | 10.860 ± 1.187 | 0.9534 ± 0.0112 |
| FD001 | TCN | 16.763 ± 1.508 | 12.865 ± 1.274 | 0.9184 ± 0.0183 |
| FD001 | Hybrid | 16.228 ± 2.092 | 12.085 ± 1.480 | 0.9225 ± 0.0268 |
| FD002 | LSTM | 15.179 ± 0.374 | 10.588 ± 0.295 | 0.9258 ± 0.0143 |
| FD002 | TCN | 21.206 ± 1.784 | 16.743 ± 1.553 | 0.9078 ± 0.0112 |
| FD002 | Hybrid | 17.083 ± 1.923 | 12.773 ± 1.556 | 0.8973 ± 0.0168 |
| FD003 | LSTM | 15.397 ± 1.018 | 10.714 ± 0.706 | 0.9087 ± 0.0475 |
| FD003 | TCN | 16.897 ± 1.253 | 13.024 ± 1.312 | 0.9054 ± 0.0226 |
| FD003 | Hybrid | 14.677 ± 1.058 | 10.224 ± 0.730 | 0.9176 ± 0.0310 |
| FD004 | LSTM | 14.915 ± 0.708 | 10.122 ± 0.239 | 0.8882 ± 0.0229 |
| FD004 | TCN | 21.635 ± 1.776 | 17.185 ± 1.511 | 0.8512 ± 0.0175 |
| FD004 | Hybrid | 16.813 ± 1.615 | 12.281 ± 1.522 | 0.8584 ± 0.0171 |

: Separate matched architecture experiment: five seeds per model/subset, common fixed 16-epoch naive-MT schedule. Mean ± sample SD. Parameters: LSTM 34,116; TCN 69,668; Hybrid 115,095. These hybrid results are not the original Table 3 checkpoint results.

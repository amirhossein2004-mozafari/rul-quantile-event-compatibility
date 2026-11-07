| Subset | Backbone | Method | Engines | Coverage | Width | Winkler |
| --- | --- | --- | --- | --- | --- | --- |
| FD001 | LSTM | CV+-E | 60 | 0.970 | 52.8 | 57.3 |
| FD001 | LSTM | CV+-M | 60 | 1.000 | 84.1 | 84.1 |
| FD001 | LSTM | Split-3fit | 20 | 0.960 | 54.1 | 58.3 |
| FD001 | Hybrid | CV+-E | 60 | 0.970 | 55.7 | 60.9 |
| FD001 | Hybrid | CV+-M | 60 | 1.000 | 92.9 | 92.9 |
| FD001 | Hybrid | Split-3fit | 20 | 0.890 | 41.8 | 60.4 |
| FD002 | LSTM | CV+-E | 156 | 0.950 | 50.1 | 59.5 |
| FD002 | LSTM | CV+-M | 156 | 1.000 | 94.9 | 94.9 |
| FD002 | LSTM | Split-3fit | 52 | 0.981 | 62.1 | 66.5 |
| FD002 | Hybrid | CV+-E | 156 | 0.958 | 52.0 | 59.5 |
| FD002 | Hybrid | CV+-M | 156 | 1.000 | 92.4 | 92.4 |
| FD002 | Hybrid | Split-3fit | 52 | 0.973 | 62.0 | 64.6 |
| FD003 | LSTM | CV+-E | 60 | 0.910 | 50.2 | 73.0 |
| FD003 | LSTM | CV+-M | 60 | 0.990 | 83.4 | 85.5 |
| FD003 | LSTM | Split-3fit | 20 | 0.960 | 61.7 | 75.2 |
| FD003 | Hybrid | CV+-E | 60 | 0.940 | 56.9 | 67.7 |
| FD003 | Hybrid | CV+-M | 60 | 1.000 | 88.4 | 88.4 |
| FD003 | Hybrid | Split-3fit | 20 | 0.960 | 61.4 | 68.9 |
| FD004 | LSTM | CV+-E | 149 | 0.948 | 46.8 | 61.8 |
| FD004 | LSTM | CV+-M | 149 | 1.000 | 88.2 | 88.2 |
| FD004 | LSTM | Split-3fit | 50 | 0.960 | 52.1 | 62.8 |
| FD004 | Hybrid | CV+-E | 149 | 0.891 | 44.7 | 68.8 |
| FD004 | Hybrid | CV+-M | 149 | 1.000 | 96.4 | 96.4 |
| FD004 | Hybrid | Split-3fit | 50 | 0.935 | 54.0 | 68.9 |

: capped-target threefold CV+ comparison. CV+-E uses one fixed held-out endpoint per engine; CV+-M uses one maximum all-prefix absolute residual per held-out engine. Both reuse only fixed LR 0.0005/final-epoch 16 inner models, independently of the CV configuration winner. Split-3fit uses the same three fitted predictors averaged at the original calibration engines and official endpoints. The engine populations and their sizes differ between CV+ and split calibration and are stated, not pooled. CV+-M is an engine-path adaptation without a proved CV+ theorem for this statistic. Official truncation does not establish exchangeability with either calibration policy. Nominal.9 is not a claimed finite-sample lower bound. Results concern one fixed threefold fit per backbone/subset, not independent fold replications.


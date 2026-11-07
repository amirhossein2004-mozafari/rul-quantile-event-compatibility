| Subset | Backbone | Method | Engines | Coverage | Width | Winkler |
| --- | --- | --- | --- | --- | --- | --- |
| FD001 | LSTM | CV+-E | 60 | 1.000 | 86.4 | 86.4 |
| FD001 | LSTM | CV+-M | 60 | 1.000 | 217.5 | 217.5 |
| FD001 | LSTM | Split-3fit | 20 | 1.000 | 126.2 | 126.2 |
| FD001 | Hybrid | CV+-E | 60 | 1.000 | 99.7 | 99.7 |
| FD001 | Hybrid | CV+-M | 60 | 1.000 | 237.2 | 237.2 |
| FD001 | Hybrid | Split-3fit | 20 | 1.000 | 125.8 | 125.8 |
| FD002 | LSTM | CV+-E | 156 | 0.942 | 105.6 | 121.3 |
| FD002 | LSTM | CV+-M | 156 | 1.000 | 244.9 | 244.9 |
| FD002 | LSTM | Split-3fit | 52 | 0.996 | 160.1 | 160.4 |
| FD002 | Hybrid | CV+-E | 156 | 0.946 | 114.7 | 125.5 |
| FD002 | Hybrid | CV+-M | 156 | 1.000 | 249.7 | 249.7 |
| FD002 | Hybrid | Split-3fit | 52 | 1.000 | 159.8 | 159.8 |
| FD003 | LSTM | CV+-E | 60 | 1.000 | 137.5 | 137.5 |
| FD003 | LSTM | CV+-M | 60 | 1.000 | 300.9 | 300.9 |
| FD003 | LSTM | Split-3fit | 20 | 1.000 | 312.0 | 312.0 |
| FD003 | Hybrid | CV+-E | 60 | 1.000 | 114.7 | 114.7 |
| FD003 | Hybrid | CV+-M | 60 | 1.000 | 300.4 | 300.4 |
| FD003 | Hybrid | Split-3fit | 20 | 1.000 | 315.1 | 315.1 |
| FD004 | LSTM | CV+-E | 149 | 1.000 | 168.9 | 168.9 |
| FD004 | LSTM | CV+-M | 149 | 1.000 | 289.7 | 289.7 |
| FD004 | LSTM | Split-3fit | 50 | 1.000 | 224.9 | 224.9 |
| FD004 | Hybrid | CV+-E | 149 | 1.000 | 172.3 | 172.3 |
| FD004 | Hybrid | CV+-M | 149 | 1.000 | 293.4 | 293.4 |
| FD004 | Hybrid | Split-3fit | 50 | 1.000 | 222.2 | 222.2 |

: raw-target threefold CV+ comparison. CV+-E uses one fixed held-out endpoint per engine; CV+-M uses one maximum all-prefix absolute residual per held-out engine. Both reuse only fixed LR 0.0005/final-epoch 16 inner models, independently of the CV configuration winner. Split-3fit uses the same three fitted predictors averaged at the original calibration engines and official endpoints. The engine populations and their sizes differ between CV+ and split calibration and are stated, not pooled. CV+-M is an engine-path adaptation without a proved CV+ theorem for this statistic. Official truncation does not establish exchangeability with either calibration policy. Nominal.9 is not a claimed finite-sample lower bound. Results concern one fixed threefold fit per backbone/subset, not independent fold replications.


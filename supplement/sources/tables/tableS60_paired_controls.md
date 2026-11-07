| Subset | Control | Reference | Metric | Difference | 95% interval |
| --- | --- | --- | --- | --- | --- |
| FD001 | TCN-last | TCN-GPU | RMSE | -1.4035 | [-2.9916, 0.4165] |
| FD001 | TCN-last | TCN-GPU | Brier | -0.0028 | [-0.0118, 0.0054] |
| FD001 | Transformer | GRU-GPU | RMSE | 0.8800 | [-0.8103, 2.4843] |
| FD001 | Transformer | GRU-GPU | Brier | -0.0011 | [-0.0123, 0.0100] |
| FD001 | Gaussian-GRU | GRU-GPU | RMSE | -0.7519 | [-2.4207, 0.7155] |
| FD001 | Gaussian-GRU | GRU-GPU | Brier | -0.0051 | [-0.0206, 0.0074] |
| FD001 | LSTM-CV | LSTM-GPU | RMSE | -0.1295 | [-1.7354, 1.5142] |
| FD001 | LSTM-CV | LSTM-GPU | Brier | -0.0061 | [-0.0206, 0.0046] |
| FD001 | Hybrid-CV | Hybrid-GPU | RMSE | -1.6373 | [-3.9017, 0.4486] |
| FD001 | Hybrid-CV | Hybrid-GPU | Brier | -0.0041 | [-0.0166, 0.0076] |
| FD002 | TCN-last | TCN-GPU | RMSE | -0.6061 | [-3.0924, 1.7650] |
| FD002 | TCN-last | TCN-GPU | Brier | 0.0012 | [-0.0067, 0.0086] |
| FD002 | Transformer | GRU-GPU | RMSE | 0.8311 | [0.0014, 1.6827] |
| FD002 | Transformer | GRU-GPU | Brier | -0.0026 | [-0.0089, 0.0036] |
| FD002 | Gaussian-GRU | GRU-GPU | RMSE | 3.2176 | [1.3916, 5.5054] |
| FD002 | Gaussian-GRU | GRU-GPU | Brier | -0.0146 | [-0.0269, -0.0043] |
| FD002 | LSTM-CV | LSTM-GPU | RMSE | -0.0029 | [-0.9747, 1.0508] |
| FD002 | LSTM-CV | LSTM-GPU | Brier | -0.0088 | [-0.0166, -0.0026] |
| FD002 | Hybrid-CV | Hybrid-GPU | RMSE | 0.0000 | [0.0000, 0.0000] |
| FD002 | Hybrid-CV | Hybrid-GPU | Brier | 0.0000 | [0.0000, 0.0000] |
| FD003 | TCN-last | TCN-GPU | RMSE | -0.8272 | [-2.8942, 1.4229] |
| FD003 | TCN-last | TCN-GPU | Brier | -0.0029 | [-0.0220, 0.0158] |
| FD003 | Transformer | GRU-GPU | RMSE | 1.3633 | [-1.0058, 4.0718] |
| FD003 | Transformer | GRU-GPU | Brier | -0.0012 | [-0.0107, 0.0062] |
| FD003 | Gaussian-GRU | GRU-GPU | RMSE | 0.3255 | [-1.4977, 2.2559] |
| FD003 | Gaussian-GRU | GRU-GPU | Brier | -0.0057 | [-0.0290, 0.0150] |
| FD003 | LSTM-CV | LSTM-GPU | RMSE | 0.3359 | [-1.2330, 1.9831] |
| FD003 | LSTM-CV | LSTM-GPU | Brier | 0.0052 | [-0.0057, 0.0167] |
| FD003 | Hybrid-CV | Hybrid-GPU | RMSE | -0.0122 | [-1.1704, 1.1719] |
| FD003 | Hybrid-CV | Hybrid-GPU | Brier | 0.0017 | [-0.0102, 0.0156] |
| FD004 | TCN-last | TCN-GPU | RMSE | 0.0271 | [-1.1137, 1.3310] |
| FD004 | TCN-last | TCN-GPU | Brier | 0.0003 | [-0.0150, 0.0182] |
| FD004 | Transformer | GRU-GPU | RMSE | 0.9592 | [-0.4661, 2.4816] |
| FD004 | Transformer | GRU-GPU | Brier | -0.0026 | [-0.0138, 0.0081] |
| FD004 | Gaussian-GRU | GRU-GPU | RMSE | 0.1480 | [-0.8173, 1.1385] |
| FD004 | Gaussian-GRU | GRU-GPU | Brier | -0.0063 | [-0.0244, 0.0095] |
| FD004 | LSTM-CV | LSTM-GPU | RMSE | -0.9947 | [-2.1309, 0.1970] |
| FD004 | LSTM-CV | LSTM-GPU | Brier | -0.0066 | [-0.0173, 0.0027] |
| FD004 | Hybrid-CV | Hybrid-GPU | RMSE | 0.8098 | [-0.2893, 1.8375] |
| FD004 | Hybrid-CV | Hybrid-GPU | Brier | 0.0003 | [-0.0152, 0.0156] |

: Mean control-minus-reference differences and paired 1000-draw crossed fitted-run/engine percentile intervals, using same-device GPU-refitted references. The same engine and run draws are shared by methods in a subset. Configurations and fitted models remain fixed; tuning, calibration-refit, training-population and split uncertainty are excluded. No multiplicity-adjusted superiority decision is made. Every adverse and unresolved contrast remains. FD002 hybrid CV and its reference select the same configuration and give identical deterministic refits; their zero interval is a mechanical identity, not evidence of population equivalence.


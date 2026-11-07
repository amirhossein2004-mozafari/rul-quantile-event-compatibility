| Contrast | Engine-only 95% | Run-only 95% | Crossed 95% | Crossed 99% |
| --- | --- | --- | --- | --- |
| FD001 Hybrid-LSTM | [+0.015, +1.276] | [+0.061, +1.320] | [-0.299, +1.658] | [-0.603, +2.019] |
| FD002 Hybrid-LSTM | [+0.826, +1.946] | [+0.671, +2.184] | [+0.472, +2.444] | [+0.195, +2.809] |
| FD003 Hybrid-LSTM | [-1.287, +0.533] | [-0.870, +0.098] | [-1.539, +0.734] | [-1.898, +1.152] |
| FD004 Hybrid-LSTM | [+1.128, +2.969] | [+1.180, +3.030] | [+0.789, +3.442] | [+0.387, +3.957] |
| FD001 PCGrad-naive | [-1.026, -0.315] | [-1.416, -0.064] | [-1.585, +0.132] | [-1.885, +0.374] |

: Bootstrap decomposition of mean paired RMSE differences: 10,000 draws for each of five contrasts, in cycles. Engine draws are shared across both arms and every sampled run. Run-only resampling keeps the observed fleet fixed; engine-only keeps the fitted run collection fixed. Crossed resampling varies both factors, with seed/partition treated as one coupled factor. The 99% marginal intervals are an approximate Bonferroni sensitivity for the five-contrast family, not a guaranteed simultaneous population interval. No tuning or new training-pool sampling is modeled.

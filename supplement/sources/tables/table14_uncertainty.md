| Contrast | Mean difference ± paired SD | Crossed 95% interval | Conditional Holm p | First lower |
| --- | --- | --- | --- | --- |
| FD001 Hybrid-LSTM | +0.646 ± 1.505 | [-0.299, +1.658] | 0.269 | 8/20 |
| FD002 Hybrid-LSTM | +1.375 ± 1.776 | [+0.472, +2.444] | 0.00407 | 3/20 |
| FD003 Hybrid-LSTM | -0.392 ± 1.132 | [-1.539, +0.734] | 0.269 | 13/20 |
| FD004 Hybrid-LSTM | +2.066 ± 2.187 | [+0.789, +3.442] | 0.00161 | 4/20 |
| FD001 PCGrad-naive | -0.677 ± 1.647 | [-1.585, +0.132] | 0.269 | 10/20 |

: Expanded fixed-schedule comparisons: 20 paired seed/split replications per contrast. Differences are first arm minus second, in cycles; negative favors the first arm. Crossed empirical percentile intervals jointly resample paired fitted runs and the shared official-test engine IDs. They are approximate resampling sensitivities under the recorded benchmark/protocol. Exact signed-rank location sensitivities assume conditionally independent, symmetric run differences given fixed data; Holm adjusts the five listed contrasts only. These are not tests on 20 independent datasets. The RUL-only and TCN arms retain five historical fits; the equal-search study retains five separately selected fits per group.

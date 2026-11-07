| Subset | Control | RMSE | Brier | RUL NLL |
| --- | --- | --- | --- | --- |
| FD001 | GRU-GPU | 14.6 ± 0.8 | 0.0257 ± 0.0047 | — |
| FD001 | TCN-last | 16.7 ± 0.5 | 0.0294 ± 0.0041 | — |
| FD001 | Transformer | 15.5 ± 0.9 | 0.0246 ± 0.0034 | — |
| FD001 | Gaussian-GRU | 13.9 ± 0.5 | 0.0206 ± 0.0026 | 3.906 ± 0.056 |
| FD001 | Gaussian-Ens | 13.5 | 0.0198 | 3.859 |
| FD002 | GRU-GPU | 13.6 ± 0.2 | 0.0284 ± 0.0064 | — |
| FD002 | TCN-last | 17.1 ± 1.3 | 0.0385 ± 0.0061 | — |
| FD002 | Transformer | 14.4 ± 0.6 | 0.0258 ± 0.0042 | — |
| FD002 | Gaussian-GRU | 16.8 ± 2.2 | 0.0138 ± 0.0036 | 4.129 ± 0.273 |
| FD002 | Gaussian-Ens | 16.3 | 0.0121 | 3.941 |
| FD003 | GRU-GPU | 14.5 ± 1.2 | 0.0257 ± 0.0082 | — |
| FD003 | TCN-last | 17.9 ± 1.3 | 0.0279 ± 0.0183 | — |
| FD003 | Transformer | 15.9 ± 1.2 | 0.0245 ± 0.0039 | — |
| FD003 | Gaussian-GRU | 14.8 ± 0.6 | 0.0200 ± 0.0034 | 4.133 ± 0.135 |
| FD003 | Gaussian-Ens | 14.2 | 0.0191 | 3.950 |
| FD004 | GRU-GPU | 15.5 ± 0.4 | 0.0383 ± 0.0086 | — |
| FD004 | TCN-last | 19.8 ± 1.9 | 0.0681 ± 0.0122 | — |
| FD004 | Transformer | 16.5 ± 0.9 | 0.0357 ± 0.0045 | — |
| FD004 | Gaussian-GRU | 15.7 ± 0.3 | 0.0320 ± 0.0024 | 4.452 ± 0.397 |
| FD004 | Gaussian-Ens | 15.2 | 0.0304 | 4.049 |

: Additional fixed-role controls and the GPU-refitted GRU reference at its earlier validation-selected configuration. Neural single-model entries summarize five fresh CUDA fits; Gaussian-Ens is one equal-weight mixture of five Gaussian members per subset and has no independent seed SD. Earlier CPU results remain separately in Table 4. Every configuration is selected by capped validation RMSE, not independently optimized uncertainty quality. RMSE is in capped-RUL cycles; Brier scores the raw <=30 event. Continuous RUL NLL is a working Gaussian/mixture score on capped labels, not binary NLL or a correctly censored lifetime likelihood. A dash means no density was specified. Complete scores, CV-selected models and same-device paired empirical intervals appear in Supplement S34. No test outcome selects a method.


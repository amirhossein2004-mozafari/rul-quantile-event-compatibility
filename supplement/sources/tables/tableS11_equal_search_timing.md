| Subset | Model | Parameters | Training (s) | Median (ms) | p95 (ms) |
| --- | --- | --- | --- | --- | --- |
| FD001 | LSTM | 34116 | 34.6 ± 0.8 | 0.545 ± 0.015 | 0.753 ± 0.064 |
| FD001 | Hybrid | 115095 | 92.8 ± 1.6 | 3.044 ± 0.028 | 3.702 ± 0.120 |
| FD002 | LSTM | 34116 | 78.0 ± 0.6 | 0.540 ± 0.016 | 0.729 ± 0.080 |
| FD002 | Hybrid | 115095 | 167.5 ± 4.3 | 3.119 ± 0.038 | 3.866 ± 0.314 |
| FD003 | LSTM | 34116 | 43.5 ± 0.4 | 0.573 ± 0.015 | 0.913 ± 0.066 |
| FD003 | Hybrid | 115095 | 260.1 ± 2.2 | 3.158 ± 0.036 | 3.908 ± 0.096 |
| FD004 | LSTM | 34116 | 92.3 ± 3.6 | 0.545 ± 0.011 | 0.732 ± 0.058 |
| FD004 | Hybrid | 115095 | 399.9 ± 25.4 | 3.155 ± 0.073 | 3.895 ± 0.242 |

: Equal-search study parameter counts and host-specific timing: mean ± sample SD across five final models. Training is elapsed time for each selected-epoch refit under the recorded four-worker schedule, including checkpoint/history handling; it excludes the three-candidate tuning search. Median and p95 are within-model batch-one forward-call summaries, then aggregated over seeds. This is neither equal-FLOP budgeting nor end-to-end deployment timing.

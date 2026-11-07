| Subset | Method | Brier skill | NLL |
| --------- | --------------- | ------------------------ | ------------------------ |
| FD001 | Raw | 0.8226 ± 0.0279 | 0.1288 ± 0.0206 |
| FD001 | Bayes | 0.7537 ± 0.0404 | 0.1467 ± 0.0329 |
| FD001 | Temp | 0.8039 ± 0.0436 | 0.4686 ± 0.4587 |
| FD001 | ShiftTemp | 0.7395 ± 0.0630 | 0.3124 ± 0.3513 |
| FD002 | Raw | 0.8338 ± 0.0345 | 0.1030 ± 0.0200 |
| FD002 | Bayes | 0.9133 ± 0.0180 | 0.0575 ± 0.0103 |
| FD002 | Temp | 0.8375 ± 0.0270 | 0.1001 ± 0.0168 |
| FD002 | ShiftTemp | 0.9127 ± 0.0241 | 0.0598 ± 0.0129 |
| FD003 | Raw | 0.8395 ± 0.0668 | 0.0908 ± 0.0340 |
| FD003 | Bayes | 0.8679 ± 0.0402 | 0.0697 ± 0.0182 |
| FD003 | Temp | 0.8432 ± 0.0607 | 0.1916 ± 0.2137 |
| FD003 | ShiftTemp | 0.8471 ± 0.0460 | 0.2130 ± 0.1954 |
| FD004 | Raw | 0.7678 ± 0.0354 | 0.1278 ± 0.0191 |
| FD004 | Bayes | 0.8069 ± 0.0228 | 0.1113 ± 0.0073 |
| FD004 | Temp | 0.7678 ± 0.0348 | 0.1298 ± 0.0204 |
| FD004 | ShiftTemp | 0.8017 ± 0.0166 | 0.1291 ± 0.0185 |

: Original 20-checkpoint benchmark: all four probability methods. Skill and NLL are per-run values summarized as mean ± sample SD over five seeds. Skill uses each run's calibration-only constant; larger is better and zero matches that reference. NLL uses retained logits and fitted transforms; smaller is better. These outcomes do not isolate calibration or establish population reliability.

| Subset | Model | Method | Brier | ECE |
| --- | --- | --- | --- | --- |
| FD001 | LSTM | Raw | 0.03561 ± 0.00429 | 0.03798 ± 0.01332 |
| FD001 | LSTM | Bayes | 0.05276 ± 0.00569 | 0.07604 ± 0.00903 |
| FD001 | LSTM | Temp | 0.04191 ± 0.00368 | 0.06430 ± 0.01448 |
| FD001 | LSTM | ShiftTemp | 0.05722 ± 0.00906 | 0.08149 ± 0.00521 |
| FD001 | Hybrid | Raw | 0.03477 ± 0.00728 | 0.03936 ± 0.00381 |
| FD001 | Hybrid | Bayes | 0.04555 ± 0.00874 | 0.05140 ± 0.01278 |
| FD001 | Hybrid | Temp | 0.03656 ± 0.00793 | 0.04408 ± 0.00722 |
| FD001 | Hybrid | ShiftTemp | 0.05030 ± 0.01049 | 0.05612 ± 0.01363 |
| FD002 | LSTM | Raw | 0.02510 ± 0.00343 | 0.03638 ± 0.00250 |
| FD002 | LSTM | Bayes | 0.01361 ± 0.00301 | 0.02205 ± 0.00335 |
| FD002 | LSTM | Temp | 0.03357 ± 0.00673 | 0.03762 ± 0.00494 |
| FD002 | LSTM | ShiftTemp | 0.01507 ± 0.00702 | 0.01682 ± 0.00758 |
| FD002 | Hybrid | Raw | 0.03333 ± 0.01419 | 0.04720 ± 0.01868 |
| FD002 | Hybrid | Bayes | 0.02090 ± 0.00967 | 0.02919 ± 0.01016 |
| FD002 | Hybrid | Temp | 0.03598 ± 0.01190 | 0.04847 ± 0.02154 |
| FD002 | Hybrid | ShiftTemp | 0.02314 ± 0.00930 | 0.02583 ± 0.01111 |
| FD003 | LSTM | Raw | 0.02666 ± 0.00860 | 0.03823 ± 0.00937 |
| FD003 | LSTM | Bayes | 0.02669 ± 0.00261 | 0.04140 ± 0.00968 |
| FD003 | LSTM | Temp | 0.03403 ± 0.00747 | 0.06624 ± 0.01615 |
| FD003 | LSTM | ShiftTemp | 0.02708 ± 0.00329 | 0.03758 ± 0.00693 |
| FD003 | Hybrid | Raw | 0.02915 ± 0.01492 | 0.04702 ± 0.01659 |
| FD003 | Hybrid | Bayes | 0.02207 ± 0.00476 | 0.03571 ± 0.00992 |
| FD003 | Hybrid | Temp | 0.03750 ± 0.01141 | 0.08952 ± 0.03122 |
| FD003 | Hybrid | ShiftTemp | 0.03268 ± 0.01069 | 0.07065 ± 0.01861 |
| FD004 | LSTM | Raw | 0.05290 ± 0.00297 | 0.05931 ± 0.00620 |
| FD004 | LSTM | Bayes | 0.03499 ± 0.00236 | 0.02833 ± 0.00301 |
| FD004 | LSTM | Temp | 0.05904 ± 0.00580 | 0.06440 ± 0.00411 |
| FD004 | LSTM | ShiftTemp | 0.04141 ± 0.00720 | 0.04306 ± 0.00713 |
| FD004 | Hybrid | Raw | 0.04484 ± 0.00384 | 0.04617 ± 0.00306 |
| FD004 | Hybrid | Bayes | 0.03787 ± 0.00415 | 0.03410 ± 0.00422 |
| FD004 | Hybrid | Temp | 0.05017 ± 0.00972 | 0.05193 ± 0.00886 |
| FD004 | Hybrid | ShiftTemp | 0.04513 ± 0.00622 | 0.04606 ± 0.00746 |

: Equal-search study probability outcomes: mean ± sample SD for every prespecified method. Temperatures are fitted only on calibration engines. Raw/Bayes use no fitted temperature; ShiftTemp applies a fixed training-weight offset before temperature fitting. All 40 runs have both temperature fits available. No method is selected using official-test outcomes.

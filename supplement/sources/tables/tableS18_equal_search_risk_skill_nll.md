| Subset | Model | Method | Brier skill | NLL |
| --------- | ---------- | --------------- | ------------------------ | ------------------------ |
| FD001 | LSTM | Raw | 0.8435 ± 0.0189 | 0.1228 ± 0.0137 |
| FD001 | LSTM | Bayes | 0.7681 ± 0.0250 | 0.1608 ± 0.0147 |
| FD001 | LSTM | Temp | 0.8158 ± 0.0162 | 0.1481 ± 0.0127 |
| FD001 | LSTM | ShiftTemp | 0.7485 ± 0.0398 | 0.2601 ± 0.2101 |
| FD001 | Hybrid | Raw | 0.8472 ± 0.0320 | 0.1215 ± 0.0228 |
| FD001 | Hybrid | Bayes | 0.7998 ± 0.0384 | 0.1359 ± 0.0234 |
| FD001 | Hybrid | Temp | 0.8393 ± 0.0349 | 0.1253 ± 0.0253 |
| FD001 | Hybrid | ShiftTemp | 0.7789 ± 0.0461 | 0.2283 ± 0.1856 |
| FD002 | LSTM | Raw | 0.8709 ± 0.0176 | 0.0816 ± 0.0114 |
| FD002 | LSTM | Bayes | 0.9300 ± 0.0155 | 0.0496 ± 0.0086 |
| FD002 | LSTM | Temp | 0.8274 ± 0.0346 | 0.3282 ± 0.2270 |
| FD002 | LSTM | ShiftTemp | 0.9225 ± 0.0361 | 0.1668 ± 0.0577 |
| FD002 | Hybrid | Raw | 0.8286 ± 0.0729 | 0.1183 ± 0.0615 |
| FD002 | Hybrid | Bayes | 0.8926 ± 0.0497 | 0.0755 ± 0.0333 |
| FD002 | Hybrid | Temp | 0.8150 ± 0.0612 | 0.2367 ± 0.1346 |
| FD002 | Hybrid | ShiftTemp | 0.8810 ± 0.0478 | 0.1854 ± 0.0667 |
| FD003 | LSTM | Raw | 0.8539 ± 0.0471 | 0.0935 ± 0.0328 |
| FD003 | LSTM | Bayes | 0.8537 ± 0.0143 | 0.0861 ± 0.0079 |
| FD003 | LSTM | Temp | 0.8136 ± 0.0409 | 0.1262 ± 0.0263 |
| FD003 | LSTM | ShiftTemp | 0.8516 ± 0.0180 | 0.1387 ± 0.1185 |
| FD003 | Hybrid | Raw | 0.8403 ± 0.0818 | 0.0933 ± 0.0422 |
| FD003 | Hybrid | Bayes | 0.8791 ± 0.0261 | 0.0694 ± 0.0117 |
| FD003 | Hybrid | Temp | 0.7945 ± 0.0625 | 0.1428 ± 0.0371 |
| FD003 | Hybrid | ShiftTemp | 0.8210 ± 0.0586 | 0.1759 ± 0.1463 |
| FD004 | LSTM | Raw | 0.7077 ± 0.0164 | 0.1725 ± 0.0140 |
| FD004 | LSTM | Bayes | 0.8066 ± 0.0130 | 0.1168 ± 0.0082 |
| FD004 | LSTM | Temp | 0.6738 ± 0.0320 | 0.4125 ± 0.4128 |
| FD004 | LSTM | ShiftTemp | 0.7712 ± 0.0398 | 0.6846 ± 0.1130 |
| FD004 | Hybrid | Raw | 0.7522 ± 0.0212 | 0.1463 ± 0.0178 |
| FD004 | Hybrid | Bayes | 0.7907 ± 0.0229 | 0.1296 ± 0.0168 |
| FD004 | Hybrid | Temp | 0.7228 ± 0.0537 | 0.2751 ± 0.2574 |
| FD004 | Hybrid | ShiftTemp | 0.7506 ± 0.0344 | 0.5281 ± 0.3785 |

: Equal-search final models: all four probability methods, mean ± sample SD over five initialization seeds on fixed engine roles. Configurations were selected by validation RMSE. Skill is averaged after calculating each run's ratio, with a calibration-only constant. Stable NLL uses retained logits and full-calibration fits. No reference, method or model is selected using these test scores.

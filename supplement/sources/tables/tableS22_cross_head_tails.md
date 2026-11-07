| Subset | Model | Method | q95<30 conflict/eligible | q05>30 conflict/eligible |
| --- | --- | --- | --- | --- |
| FD001 | LSTM | Raw | 7.0/14.6 | 5.4/69.6 |
| FD001 | LSTM | Bayes | 14.6/14.6 | 2.0/69.6 |
| FD001 | LSTM | Temp | 14.6/14.6 | 8.8/69.6 |
| FD001 | LSTM | ShiftTemp | 11.4/14.6 | 3.6/69.6 |
| FD001 | Hybrid | Raw | 2.0/15.6 | 4.2/69.8 |
| FD001 | Hybrid | Bayes | 6.4/15.6 | 1.0/69.8 |
| FD001 | Hybrid | Temp | 7.4/15.6 | 8.0/69.8 |
| FD001 | Hybrid | ShiftTemp | 6.0/15.6 | 2.0/69.8 |
| FD002 | LSTM | Raw | 0.0/46.2 | 6.6/181.2 |
| FD002 | LSTM | Bayes | 3.0/46.2 | 0.2/181.2 |
| FD002 | LSTM | Temp | 0.0/46.2 | 0.2/181.2 |
| FD002 | LSTM | ShiftTemp | 0.0/46.2 | 0.0/181.2 |
| FD002 | Hybrid | Raw | 1.2/49.2 | 7.4/172.8 |
| FD002 | Hybrid | Bayes | 6.2/49.2 | 0.6/172.8 |
| FD002 | Hybrid | Temp | 3.6/49.2 | 6.8/172.8 |
| FD002 | Hybrid | ShiftTemp | 3.0/49.2 | 0.4/172.8 |
| FD003 | LSTM | Raw | 0.0/9.0 | 3.4/73.0 |
| FD003 | LSTM | Bayes | 2.4/9.0 | 0.2/73.0 |
| FD003 | LSTM | Temp | 7.2/9.0 | 13.4/73.0 |
| FD003 | LSTM | ShiftTemp | 2.0/9.0 | 0.6/73.0 |
| FD003 | Hybrid | Raw | 0.6/13.8 | 5.2/73.0 |
| FD003 | Hybrid | Bayes | 2.4/13.8 | 1.2/73.0 |
| FD003 | Hybrid | Temp | 8.8/13.8 | 24.0/73.0 |
| FD003 | Hybrid | ShiftTemp | 8.8/13.8 | 10.6/73.0 |
| FD004 | LSTM | Raw | 0.0/26.2 | 7.6/171.0 |
| FD004 | LSTM | Bayes | 4.6/26.2 | 0.0/171.0 |
| FD004 | LSTM | Temp | 0.0/26.2 | 2.6/171.0 |
| FD004 | LSTM | ShiftTemp | 0.0/26.2 | 0.0/171.0 |
| FD004 | Hybrid | Raw | 1.0/23.0 | 5.8/170.0 |
| FD004 | Hybrid | Bayes | 13.6/23.0 | 0.2/170.0 |
| FD004 | Hybrid | Temp | 1.0/23.0 | 3.4/170.0 |
| FD004 | Hybrid | ShiftTemp | 0.2/23.0 | 0.0/170.0 |

: Strict tail cases, displayed as five-seed mean conflict count / mean eligible count per run. The first column counts p<0.95-1e-6 when q95<30; the second counts p>0.05+1e-6 when q05>30. These ratios of displayed means are not estimates with independent pooled-engine denominators. The attached per-run CSV gives each integer numerator and denominator, including zero cases. These two tail cases are subsets of the general three-quantile diagnostic.

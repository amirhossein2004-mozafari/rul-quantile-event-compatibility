| Subset | Model | Method | Engines | Visits | Path coverage | Visit coverage |
| --------- | --------- | ------------------ | ---------- | ---------- | ---------------------- | ---------------------- |
| FD001 | LSTM | Raw | 10 | 73 | 0.5400 ± 0.0548 | 0.8930 ± 0.0313 |
| FD001 | LSTM | FirstVisitExact | 10 | 73 | 0.5400 ± 0.0548 | 0.8930 ± 0.0313 |
| FD001 | LSTM | BlockExact | 10 | 73 | 0.9600 ± 0.0894 | 0.9947 ± 0.0119 |
| FD001 | LSTM | BlockNormalized | 10 | 73 | 0.8600 ± 0.0548 | 0.9813 ± 0.0074 |
| FD001 | Hybrid | Raw | 10 | 73 | 0.3800 ± 0.1643 | 0.8007 ± 0.0800 |
| FD001 | Hybrid | FirstVisitExact | 10 | 73 | 0.4200 ± 0.1924 | 0.8306 ± 0.0493 |
| FD001 | Hybrid | BlockExact | 10 | 73 | 0.9200 ± 0.0837 | 0.9850 ± 0.0137 |
| FD001 | Hybrid | BlockNormalized | 10 | 73 | 0.8600 ± 0.0548 | 0.9780 ± 0.0100 |
| FD002 | LSTM | Raw | 26 | 165 | 0.4538 ± 0.0834 | 0.8769 ± 0.0166 |
| FD002 | LSTM | FirstVisitExact | 26 | 165 | 0.4538 ± 0.0834 | 0.8769 ± 0.0166 |
| FD002 | LSTM | BlockExact | 26 | 165 | 0.9308 ± 0.0172 | 0.9846 ± 0.0035 |
| FD002 | LSTM | BlockNormalized | 26 | 165 | 0.9538 ± 0.0322 | 0.9897 ± 0.0066 |
| FD002 | Hybrid | Raw | 26 | 165 | 0.4538 ± 0.0688 | 0.8709 ± 0.0188 |
| FD002 | Hybrid | FirstVisitExact | 26 | 165 | 0.4538 ± 0.0688 | 0.8709 ± 0.0188 |
| FD002 | Hybrid | BlockExact | 26 | 165 | 0.9538 ± 0.0172 | 0.9901 ± 0.0040 |
| FD002 | Hybrid | BlockNormalized | 26 | 165 | 0.9923 ± 0.0172 | 0.9981 ± 0.0043 |
| FD003 | LSTM | Raw | 10 | 76 | 0.5200 ± 0.0837 | 0.8651 ± 0.0602 |
| FD003 | LSTM | FirstVisitExact | 10 | 76 | 0.8600 ± 0.1140 | 0.9766 ± 0.0223 |
| FD003 | LSTM | BlockExact | 10 | 76 | 0.9200 ± 0.0837 | 0.9883 ± 0.0123 |
| FD003 | LSTM | BlockNormalized | 10 | 76 | 0.9200 ± 0.0837 | 0.9883 ± 0.0123 |
| FD003 | Hybrid | Raw | 10 | 76 | 0.2400 ± 0.1517 | 0.6456 ± 0.1256 |
| FD003 | Hybrid | FirstVisitExact | 10 | 76 | 0.7000 ± 0.2739 | 0.9137 ± 0.1101 |
| FD003 | Hybrid | BlockExact | 10 | 76 | 0.9600 ± 0.0548 | 0.9950 ± 0.0068 |
| FD003 | Hybrid | BlockNormalized | 10 | 76 | 0.8800 ± 0.1095 | 0.9817 ± 0.0215 |
| FD004 | LSTM | Raw | 25 | 191 | 0.4480 ± 0.0522 | 0.8280 ± 0.0292 |
| FD004 | LSTM | FirstVisitExact | 25 | 191 | 0.4640 ± 0.0727 | 0.8359 ± 0.0437 |
| FD004 | LSTM | BlockExact | 25 | 191 | 0.8800 ± 0.0748 | 0.9754 ± 0.0191 |
| FD004 | LSTM | BlockNormalized | 25 | 191 | 0.8640 ± 0.0727 | 0.9754 ± 0.0174 |
| FD004 | Hybrid | Raw | 25 | 191 | 0.3280 ± 0.0996 | 0.8315 ± 0.0144 |
| FD004 | Hybrid | FirstVisitExact | 25 | 191 | 0.5200 ± 0.1789 | 0.8893 ± 0.0565 |
| FD004 | Hybrid | BlockExact | 25 | 191 | 0.8000 ± 0.0566 | 0.9624 ± 0.0139 |
| FD004 | Hybrid | BlockNormalized | 25 | 191 | 0.8160 ± 0.0829 | 0.9653 ± 0.0165 |

: Scheduled monitoring coverage: mean ± sample SD across five initialization seeds. Visits are counted within each run, not independent samples. Visit coverage gives equal weight to each engine; path coverage requires every scheduled visit of an engine to be covered. Engine and visit counts are fixed across seeds. Data are previously examined simulated trajectories.

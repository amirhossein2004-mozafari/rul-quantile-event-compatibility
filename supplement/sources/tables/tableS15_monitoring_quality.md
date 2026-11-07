| Subset | Model | Method | Width | Winkler |
| --- | --- | --- | --- | --- |
| FD001 | LSTM | Raw | 43.197 ± 1.805 | 51.913 ± 5.956 |
| FD001 | LSTM | FirstVisitExact | 43.197 ± 1.805 | 51.913 ± 5.956 |
| FD001 | LSTM | BlockExact | 60.464 ± 9.404 | 61.183 ± 8.452 |
| FD001 | LSTM | BlockNormalized | 67.891 ± 5.852 | 68.521 ± 5.959 |
| FD001 | Hybrid | Raw | 38.501 ± 2.334 | 65.544 ± 14.427 |
| FD001 | Hybrid | FirstVisitExact | 40.533 ± 4.142 | 61.494 ± 8.899 |
| FD001 | Hybrid | BlockExact | 60.912 ± 7.365 | 62.768 ± 5.462 |
| FD001 | Hybrid | BlockNormalized | 64.380 ± 10.154 | 66.524 ± 10.161 |
| FD002 | LSTM | Raw | 41.096 ± 1.938 | 56.556 ± 2.224 |
| FD002 | LSTM | FirstVisitExact | 41.096 ± 1.938 | 56.556 ± 2.224 |
| FD002 | LSTM | BlockExact | 59.535 ± 3.392 | 61.552 ± 2.852 |
| FD002 | LSTM | BlockNormalized | 60.308 ± 10.031 | 61.679 ± 9.219 |
| FD002 | Hybrid | Raw | 42.203 ± 1.091 | 60.150 ± 5.034 |
| FD002 | Hybrid | FirstVisitExact | 42.203 ± 1.091 | 60.150 ± 5.034 |
| FD002 | Hybrid | BlockExact | 63.430 ± 3.975 | 64.374 ± 3.677 |
| FD002 | Hybrid | BlockNormalized | 79.602 ± 17.369 | 79.738 ± 17.183 |
| FD003 | LSTM | Raw | 35.334 ± 3.435 | 63.995 ± 20.359 |
| FD003 | LSTM | FirstVisitExact | 61.274 ± 13.177 | 64.886 ± 11.846 |
| FD003 | LSTM | BlockExact | 69.592 ± 8.849 | 71.489 ± 8.771 |
| FD003 | LSTM | BlockNormalized | 68.395 ± 9.535 | 70.358 ± 9.440 |
| FD003 | Hybrid | Raw | 27.654 ± 1.351 | 104.422 ± 50.437 |
| FD003 | Hybrid | FirstVisitExact | 54.990 ± 21.709 | 67.625 ± 14.575 |
| FD003 | Hybrid | BlockExact | 70.773 ± 8.987 | 72.011 ± 9.047 |
| FD003 | Hybrid | BlockNormalized | 69.686 ± 8.113 | 71.647 ± 9.147 |
| FD004 | LSTM | Raw | 37.366 ± 1.144 | 73.168 ± 9.644 |
| FD004 | LSTM | FirstVisitExact | 38.306 ± 3.218 | 72.570 ± 10.538 |
| FD004 | LSTM | BlockExact | 63.938 ± 2.913 | 66.111 ± 3.768 |
| FD004 | LSTM | BlockNormalized | 61.632 ± 3.593 | 63.379 ± 4.556 |
| FD004 | Hybrid | Raw | 39.275 ± 2.714 | 75.095 ± 3.390 |
| FD004 | Hybrid | FirstVisitExact | 47.773 ± 9.236 | 69.636 ± 5.514 |
| FD004 | Hybrid | BlockExact | 61.490 ± 1.754 | 64.980 ± 1.605 |
| FD004 | Hybrid | BlockNormalized | 60.366 ± 2.729 | 64.283 ± 2.439 |

: Scheduled monitoring interval quality, in cycles: engine-balanced mean width and Winkler, mean ± sample SD across five initialization seeds. All four prespecified methods are retained. Wider intervals can improve path coverage while worsening interval score; no universal winner or coverage guarantee is asserted.

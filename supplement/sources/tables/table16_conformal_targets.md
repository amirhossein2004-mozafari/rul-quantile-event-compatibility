| Subset | Method | Capped coverage | Capped width | Raw coverage | Raw width |
| --- | --- | --- | --- | --- | --- |
| FD001 | R-NN | 0.944 ± 0.027 | 45.6 ± 5.6 | 0.924 ± 0.032 | 53.2 ± 5.0 |
| FD001 | R-CQR | 0.944 ± 0.027 | 45.6 ± 5.6 | 0.924 ± 0.032 | 53.2 ± 5.0 |
| FD001 | U-CQR | 0.906 ± 0.071 | 44.0 ± 10.2 | 1.000 ± 0.000 | 148.1 ± 65.4 |
| FD001 | EB-CQR | 0.942 ± 0.026 | 47.5 ± 6.3 | 1.000 ± 0.000 | 174.8 ± 18.7 |
| FD001 | EM-CQR | 0.998 ± 0.004 | 78.9 ± 13.8 | 1.000 ± 0.000 | 258.5 ± 30.2 |
| FD001 | W-CQR | 0.924 ± 0.064 | 65.3 ± 17.7 | 0.984 ± 0.018 | ∞ (4/5 runs) |
| FD002 | R-NN | 0.941 ± 0.023 | 50.8 ± 5.1 | 0.776 ± 0.033 | 56.0 ± 5.1 |
| FD002 | R-CQR | 0.941 ± 0.023 | 50.8 ± 5.1 | 0.776 ± 0.033 | 56.0 ± 5.1 |
| FD002 | U-CQR | 0.934 ± 0.046 | 49.5 ± 12.9 | 0.983 ± 0.026 | 150.0 ± 30.8 |
| FD002 | EB-CQR | 0.955 ± 0.017 | 51.8 ± 8.1 | 0.995 ± 0.002 | 155.5 ± 7.9 |
| FD002 | EM-CQR | 1.000 ± 0.000 | 96.7 ± 5.8 | 1.000 ± 0.000 | 250.7 ± 12.8 |
| FD002 | W-CQR | 0.955 ± 0.021 | 52.5 ± 9.8 | 0.929 ± 0.059 | 118.9 ± 31.9 |
| FD003 | R-NN | 0.926 ± 0.055 | 43.3 ± 10.6 | 0.888 ± 0.089 | 49.1 ± 14.9 |
| FD003 | R-CQR | 0.926 ± 0.055 | 43.3 ± 10.7 | 0.888 ± 0.089 | 49.0 ± 15.0 |
| FD003 | U-CQR | 0.920 ± 0.031 | 39.9 ± 3.2 | 1.000 ± 0.000 | 196.6 ± 53.8 |
| FD003 | EB-CQR | 0.960 ± 0.012 | 46.3 ± 3.2 | 1.000 ± 0.000 | 247.3 ± 33.0 |
| FD003 | EM-CQR | 0.996 ± 0.009 | 75.2 ± 3.3 | 1.000 ± 0.000 | 354.7 ± 52.4 |
| FD003 | W-CQR | 0.966 ± 0.023 | 62.8 ± 10.3 | 1.000 ± 0.000 | ∞ (4/5 runs) |
| FD004 | R-NN | 0.879 ± 0.091 | 48.0 ± 8.1 | 0.709 ± 0.039 | 51.1 ± 6.8 |
| FD004 | R-CQR | 0.879 ± 0.091 | 48.0 ± 8.1 | 0.709 ± 0.039 | 51.1 ± 6.8 |
| FD004 | U-CQR | 0.928 ± 0.054 | 52.7 ± 16.3 | 1.000 ± 0.000 | 216.2 ± 20.2 |
| FD004 | EB-CQR | 0.931 ± 0.031 | 51.2 ± 10.3 | 1.000 ± 0.000 | 213.0 ± 6.1 |
| FD004 | EM-CQR | 0.994 ± 0.006 | 92.6 ± 8.3 | 1.000 ± 0.000 | 328.3 ± 4.5 |
| FD004 | W-CQR | 0.928 ± 0.049 | 54.2 ± 12.7 | 1.000 ± 0.000 | 207.4 ± 26.8 |

: Six fixed calibration constructions on the same20 original hybrid fits, five per subset. Mean ± seed SD; widths in cycles. R-NN: restricted nonnegative historical score; R-CQR: original signed CQR on restricted endpoints; U-CQR: signed CQR on unrestricted endpoints; EB-CQR: engine-balanced empirical all-prefix scores; EM-CQR: engine-max all-prefix scores; W-CQR: estimated cycle-density weights with test-point infinity mass. Capped intervals intersect [0,125]; raw intervals intersect [0,infinity), without upper capping. Infinity is retained, with number of affected runs. These are empirical official-test results, not established coverage guarantees.


| Study | Subset | Cal positive/n | Test positive/n | Constant Brier |
| ------------ | --------- | ------------------ | ------------------ | ------------------------ |
| Original | FD001 | 4-7/20 | 25/100 | 0.1910 ± 0.0038 |
| Original | FD002 | 10-15/52 | 61/259 | 0.1818 ± 0.0007 |
| Original | FD003 | 4-7/20 | 20/100 | 0.1690 ± 0.0088 |
| Original | FD004 | 9-14/50 | 53/248 | 0.1702 ± 0.0021 |
| EqualSearch | FD001 | 1/20 | 25/100 | 0.2275 ± 0.0000 |
| EqualSearch | FD002 | 6/52 | 61/259 | 0.1945 ± 0.0000 |
| EqualSearch | FD003 | 1/20 | 20/100 | 0.1825 ± 0.0000 |
| EqualSearch | FD004 | 5/50 | 53/248 | 0.1810 ± 0.0000 |

: Event support and calibration-only constant reference. Event is uncapped RUL at most 30 cycles. Calibration positives are a range across five original seeds; equal-search engine roles/endpoints are fixed across architectures and final seeds. Test counts are unique engines per subset, repeated across studies/seeds. Constant Brier is its test score, mean ± sample SD over seeds. Test event fractions never set the reference probability.

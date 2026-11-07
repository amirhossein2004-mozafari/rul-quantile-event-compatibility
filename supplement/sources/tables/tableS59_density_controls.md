| Subset | Density | RUL NLL | Coverage | Width | Winkler | Conflict |
| --- | --- | --- | --- | --- | --- | --- |
| FD001 | Gaussian-GRU | 3.906 ± 0.056 | 0.890 ± 0.020 | 38.5 ± 1.5 | 54.5 ± 2.8 | 0.000 ± 0.000 |
| FD001 | Gaussian-Ens | 3.859 | 0.930 | 39.8 | 52.9 | 0.000 |
| FD002 | Gaussian-GRU | 4.129 ± 0.273 | 0.822 ± 0.124 | 40.2 ± 2.9 | 63.6 ± 19.6 | 0.000 ± 0.000 |
| FD002 | Gaussian-Ens | 3.941 | 0.961 | 43.5 | 51.7 | 0.000 |
| FD003 | Gaussian-GRU | 4.133 ± 0.135 | 0.760 ± 0.054 | 34.9 ± 1.9 | 64.2 ± 9.9 | 0.000 ± 0.000 |
| FD003 | Gaussian-Ens | 3.950 | 0.830 | 37.5 | 56.5 | 0.000 |
| FD004 | Gaussian-GRU | 4.452 ± 0.397 | 0.791 ± 0.059 | 38.0 ± 2.2 | 63.1 ± 7.5 | 0.000 ± 0.000 |
| FD004 | Gaussian-Ens | 4.049 | 0.867 | 40.3 | 53.9 | 0.000 |

: Continuous working likelihood and induced quantile intervals. Uncalibrated interval scores use capped labels and the historical coordinate projection to [0,125]; nominal compatibility uses unprojected quantiles and the induced event CDF. The Gaussian working distribution can place mass below zero and does not model the cap atom; these are disclosed misspecifications, not an uncapped-lifetime likelihood. Mixture quantiles invert the average component CDF, rather than averaging component quantiles or matching one Gaussian variance. Conflict is the necessary-screen fraction at tolerance 1e-6, not proof of population calibration.


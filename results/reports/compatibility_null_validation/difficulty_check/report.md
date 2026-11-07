# Null distribution and per-fit difficulty

Protocol SHA256: `c5682eb82daac149437eaa71ac31f1c4eb171459cc4ab09aa75afba8c7957676`. Rates are fractions. Six-decimal display; full-precision CSVs retained.

## Null distribution

| subset | architecture | fitting_engines | synthetic_evaluation_engines | real_evaluation_engines | noncollapsed_synthetic_fits | real_raw_rate | null_min | null_p025 | null_p25 | null_median | null_p75 | null_p975 | null_max | real_location |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FD001 | lstm | 60 | 10000 | 100 | 22 | 0.204000 | 0.000000 | 0.000000 | 0.003175 | 0.997200 | 1.000000 | 1.000000 | 1.000000 | inside |
| FD001 | hybrid | 60 | 10000 | 100 | 5 | 0.136000 | 0.107400 | 0.143290 | 0.466300 | 0.498000 | 0.502600 | 0.552100 | 0.557600 | below |
| FD002 | lstm | 156 | 10000 | 259 | 30 | 0.095753 | 0.007000 | 0.009973 | 0.057825 | 0.255350 | 0.477525 | 0.574927 | 0.769300 | inside |
| FD002 | hybrid | 156 | 10000 | 259 | 10 | 0.088803 | 0.000000 | 0.007830 | 0.079150 | 0.183900 | 0.262425 | 0.887680 | 1.000000 | inside |
| FD003 | lstm | 60 | 10000 | 100 | 28 | 0.128000 | 0.000000 | 0.000000 | 0.064025 | 0.376050 | 0.586975 | 1.000000 | 1.000000 | inside |
| FD003 | hybrid | 60 | 10000 | 100 | 17 | 0.118000 | 0.013300 | 0.071220 | 0.220900 | 0.311900 | 0.421700 | 0.792820 | 0.969500 | inside |
| FD004 | lstm | 149 | 10000 | 248 | 30 | 0.166129 | 0.039300 | 0.043432 | 0.128150 | 0.301600 | 0.437800 | 0.602272 | 0.639900 | inside |
| FD004 | hybrid | 149 | 10000 | 248 | 18 | 0.126613 | 0.019600 | 0.036430 | 0.101100 | 0.228150 | 0.410325 | 0.944575 | 0.955200 | inside |

## FD001 — per-fit difficulty

| architecture | cohort | fit_identifier | fitting_engines | evaluation_engines | RMSE_capped | event_AUC | event_base_rate | median_q95_minus_q05_width |
|---|---|---|---|---|---|---|---|---|
| lstm | synthetic_noncollapsed | 1 | 60 | 10000 | 45.412643 | 0.651377 | 0.414900 | 36.835220 |
| lstm | synthetic_noncollapsed | 3 | 60 | 10000 | 47.654703 | 0.636140 | 0.414900 | 39.788654 |
| lstm | synthetic_noncollapsed | 4 | 60 | 10000 | 46.286657 | 0.575869 | 0.414900 | 67.636121 |
| lstm | synthetic_noncollapsed | 5 | 60 | 10000 | 46.043393 | 0.643054 | 0.414900 | 42.387239 |
| lstm | synthetic_noncollapsed | 6 | 60 | 10000 | 42.871293 | 0.629793 | 0.414900 | 89.421480 |
| lstm | synthetic_noncollapsed | 7 | 60 | 10000 | 45.334242 | 0.365872 | 0.414900 | 43.700908 |
| lstm | synthetic_noncollapsed | 8 | 60 | 10000 | 42.810533 | 0.645371 | 0.414900 | 83.389863 |
| lstm | synthetic_noncollapsed | 10 | 60 | 10000 | 47.974063 | 0.654428 | 0.414900 | 42.004503 |
| lstm | synthetic_noncollapsed | 11 | 60 | 10000 | 43.862162 | 0.653568 | 0.414900 | 62.420706 |
| lstm | synthetic_noncollapsed | 13 | 60 | 10000 | 43.463082 | 0.623041 | 0.414900 | 102.146741 |
| lstm | synthetic_noncollapsed | 14 | 60 | 10000 | 47.396707 | 0.634451 | 0.414900 | 39.265477 |
| lstm | synthetic_noncollapsed | 15 | 60 | 10000 | 42.797150 | 0.526458 | 0.414900 | 69.498586 |
| lstm | synthetic_noncollapsed | 16 | 60 | 10000 | 47.154370 | 0.649005 | 0.414900 | 42.959970 |
| lstm | synthetic_noncollapsed | 17 | 60 | 10000 | 48.142233 | 0.349689 | 0.414900 | 34.131361 |
| lstm | synthetic_noncollapsed | 19 | 60 | 10000 | 41.997347 | 0.653508 | 0.414900 | 89.595201 |
| lstm | synthetic_noncollapsed | 20 | 60 | 10000 | 43.033463 | 0.633582 | 0.414900 | 83.938249 |
| lstm | synthetic_noncollapsed | 21 | 60 | 10000 | 47.068131 | 0.620804 | 0.414900 | 46.928509 |
| lstm | synthetic_noncollapsed | 24 | 60 | 10000 | 49.470065 | 0.653424 | 0.414900 | 48.235093 |
| lstm | synthetic_noncollapsed | 25 | 60 | 10000 | 50.005352 | 0.588560 | 0.414900 | 24.562763 |
| lstm | synthetic_noncollapsed | 27 | 60 | 10000 | 42.461565 | 0.656526 | 0.414900 | 74.648420 |
| lstm | synthetic_noncollapsed | 28 | 60 | 10000 | 44.472228 | 0.554706 | 0.414900 | 48.620121 |
| lstm | synthetic_noncollapsed | 29 | 60 | 10000 | 41.608256 | 0.653305 | 0.414900 | 56.731440 |
| lstm | real | 1101 | 60 | 100 | 13.700791 | 0.986667 | 0.250000 | 66.325974 |
| lstm | real | 1202 | 60 | 100 | 14.594018 | 0.986667 | 0.250000 | 83.130524 |
| lstm | real | 1303 | 60 | 100 | 14.931852 | 0.985600 | 0.250000 | 77.396671 |
| lstm | real | 1404 | 60 | 100 | 15.426901 | 0.982400 | 0.250000 | 68.214354 |
| lstm | real | 1505 | 60 | 100 | 14.904965 | 0.989867 | 0.250000 | 68.695364 |
| hybrid | synthetic_noncollapsed | 9 | 60 | 10000 | 46.108336 | 0.353316 | 0.414900 | 119.324152 |
| hybrid | synthetic_noncollapsed | 14 | 60 | 10000 | 42.675738 | 0.643639 | 0.414900 | 73.363750 |
| hybrid | synthetic_noncollapsed | 16 | 60 | 10000 | 40.452431 | 0.651309 | 0.414900 | 122.492687 |
| hybrid | synthetic_noncollapsed | 17 | 60 | 10000 | 42.147343 | 0.654745 | 0.414900 | 107.250097 |
| hybrid | synthetic_noncollapsed | 25 | 60 | 10000 | 43.008273 | 0.651765 | 0.414900 | 111.641270 |
| hybrid | real | 1101 | 60 | 100 | 15.303755 | 0.993600 | 0.250000 | 51.933865 |
| hybrid | real | 1202 | 60 | 100 | 18.081000 | 0.988800 | 0.250000 | 54.536209 |
| hybrid | real | 1303 | 60 | 100 | 15.017688 | 0.989333 | 0.250000 | 46.111851 |
| hybrid | real | 1404 | 60 | 100 | 15.839083 | 0.985067 | 0.250000 | 50.341255 |
| hybrid | real | 1505 | 60 | 100 | 15.312313 | 0.988800 | 0.250000 | 47.359306 |

## FD002 — per-fit difficulty

| architecture | cohort | fit_identifier | fitting_engines | evaluation_engines | RMSE_capped | event_AUC | event_base_rate | median_q95_minus_q05_width |
|---|---|---|---|---|---|---|---|---|
| lstm | synthetic_noncollapsed | 0 | 156 | 10000 | 41.685854 | 0.596202 | 0.419600 | 131.461233 |
| lstm | synthetic_noncollapsed | 1 | 156 | 10000 | 40.976219 | 0.624169 | 0.419600 | 124.219778 |
| lstm | synthetic_noncollapsed | 2 | 156 | 10000 | 41.088632 | 0.649220 | 0.419600 | 104.765472 |
| lstm | synthetic_noncollapsed | 3 | 156 | 10000 | 40.071708 | 0.649437 | 0.419600 | 99.668400 |
| lstm | synthetic_noncollapsed | 4 | 156 | 10000 | 39.689957 | 0.647219 | 0.419600 | 126.987226 |
| lstm | synthetic_noncollapsed | 5 | 156 | 10000 | 39.974031 | 0.645868 | 0.419600 | 108.842739 |
| lstm | synthetic_noncollapsed | 6 | 156 | 10000 | 40.415111 | 0.649271 | 0.419600 | 87.557839 |
| lstm | synthetic_noncollapsed | 7 | 156 | 10000 | 43.955525 | 0.648324 | 0.419600 | 93.506794 |
| lstm | synthetic_noncollapsed | 8 | 156 | 10000 | 41.345016 | 0.651367 | 0.419600 | 92.354603 |
| lstm | synthetic_noncollapsed | 9 | 156 | 10000 | 40.248566 | 0.642646 | 0.419600 | 128.606440 |
| lstm | synthetic_noncollapsed | 10 | 156 | 10000 | 39.599987 | 0.647341 | 0.419600 | 102.210024 |
| lstm | synthetic_noncollapsed | 11 | 156 | 10000 | 45.877043 | 0.643299 | 0.419600 | 129.513924 |
| lstm | synthetic_noncollapsed | 12 | 156 | 10000 | 41.262852 | 0.647874 | 0.419600 | 129.509644 |
| lstm | synthetic_noncollapsed | 13 | 156 | 10000 | 41.465876 | 0.648776 | 0.419600 | 88.504889 |
| lstm | synthetic_noncollapsed | 14 | 156 | 10000 | 40.400482 | 0.649796 | 0.419600 | 97.006857 |
| lstm | synthetic_noncollapsed | 15 | 156 | 10000 | 40.923973 | 0.650887 | 0.419600 | 106.078278 |
| lstm | synthetic_noncollapsed | 16 | 156 | 10000 | 39.420266 | 0.647913 | 0.419600 | 100.366087 |
| lstm | synthetic_noncollapsed | 17 | 156 | 10000 | 39.671740 | 0.650548 | 0.419600 | 89.249475 |
| lstm | synthetic_noncollapsed | 18 | 156 | 10000 | 43.132402 | 0.648572 | 0.419600 | 129.517410 |
| lstm | synthetic_noncollapsed | 19 | 156 | 10000 | 41.117445 | 0.645755 | 0.419600 | 122.806131 |
| lstm | synthetic_noncollapsed | 20 | 156 | 10000 | 39.828457 | 0.647266 | 0.419600 | 102.969818 |
| lstm | synthetic_noncollapsed | 21 | 156 | 10000 | 41.365313 | 0.651885 | 0.419600 | 114.322227 |
| lstm | synthetic_noncollapsed | 22 | 156 | 10000 | 39.661440 | 0.648628 | 0.419600 | 125.573999 |
| lstm | synthetic_noncollapsed | 23 | 156 | 10000 | 40.405649 | 0.649780 | 0.419600 | 87.412193 |
| lstm | synthetic_noncollapsed | 24 | 156 | 10000 | 42.007013 | 0.620205 | 0.419600 | 128.417097 |
| lstm | synthetic_noncollapsed | 25 | 156 | 10000 | 43.873262 | 0.626810 | 0.419600 | 122.758265 |
| lstm | synthetic_noncollapsed | 26 | 156 | 10000 | 40.254801 | 0.649071 | 0.419600 | 90.482079 |
| lstm | synthetic_noncollapsed | 27 | 156 | 10000 | 39.487039 | 0.649668 | 0.419600 | 123.434885 |
| lstm | synthetic_noncollapsed | 28 | 156 | 10000 | 40.482176 | 0.649401 | 0.419600 | 111.008432 |
| lstm | synthetic_noncollapsed | 29 | 156 | 10000 | 39.364239 | 0.648729 | 0.419600 | 110.046083 |
| lstm | real | 1101 | 156 | 259 | 13.627393 | 0.997516 | 0.235521 | 53.721451 |
| lstm | real | 1202 | 156 | 259 | 14.177176 | 0.998013 | 0.235521 | 53.540771 |
| lstm | real | 1303 | 156 | 259 | 15.098157 | 0.998427 | 0.235521 | 56.584747 |
| lstm | real | 1404 | 156 | 259 | 14.412211 | 0.999089 | 0.235521 | 55.909576 |
| lstm | real | 1505 | 156 | 259 | 14.285130 | 0.999006 | 0.235521 | 54.541283 |
| hybrid | synthetic_noncollapsed | 3 | 156 | 10000 | 40.271379 | 0.647316 | 0.419600 | 88.399094 |
| hybrid | synthetic_noncollapsed | 7 | 156 | 10000 | 40.196260 | 0.647343 | 0.419600 | 60.320721 |
| hybrid | synthetic_noncollapsed | 18 | 156 | 10000 | 42.214931 | 0.645214 | 0.419600 | 119.056265 |
| hybrid | synthetic_noncollapsed | 22 | 156 | 10000 | 39.461854 | 0.648462 | 0.419600 | 84.268064 |
| hybrid | synthetic_noncollapsed | 23 | 156 | 10000 | 40.291186 | 0.650413 | 0.419600 | 62.245100 |
| hybrid | synthetic_noncollapsed | 24 | 156 | 10000 | 42.221395 | 0.603965 | 0.419600 | 114.182520 |
| hybrid | synthetic_noncollapsed | 25 | 156 | 10000 | 40.405137 | 0.649820 | 0.419600 | 110.088818 |
| hybrid | synthetic_noncollapsed | 26 | 156 | 10000 | 39.898756 | 0.649607 | 0.419600 | 105.259768 |
| hybrid | synthetic_noncollapsed | 28 | 156 | 10000 | 41.715864 | 0.648452 | 0.419600 | 91.140244 |
| hybrid | synthetic_noncollapsed | 29 | 156 | 10000 | 39.869457 | 0.646238 | 0.419600 | 95.707682 |
| hybrid | real | 1101 | 156 | 259 | 15.005641 | 0.998261 | 0.235521 | 56.566498 |
| hybrid | real | 1202 | 156 | 259 | 14.475730 | 0.997268 | 0.235521 | 51.197449 |
| hybrid | real | 1303 | 156 | 259 | 15.324973 | 0.998510 | 0.235521 | 54.327415 |
| hybrid | real | 1404 | 156 | 259 | 14.294998 | 0.997019 | 0.235521 | 56.149239 |
| hybrid | real | 1505 | 156 | 259 | 17.866014 | 0.991389 | 0.235521 | 53.025879 |

## FD003 — per-fit difficulty

| architecture | cohort | fit_identifier | fitting_engines | evaluation_engines | RMSE_capped | event_AUC | event_base_rate | median_q95_minus_q05_width |
|---|---|---|---|---|---|---|---|---|
| lstm | synthetic_noncollapsed | 0 | 60 | 10000 | 41.592689 | 0.653232 | 0.408000 | 123.912180 |
| lstm | synthetic_noncollapsed | 1 | 60 | 10000 | 42.732047 | 0.605508 | 0.408000 | 136.680647 |
| lstm | synthetic_noncollapsed | 2 | 60 | 10000 | 44.050121 | 0.367174 | 0.408000 | 124.414452 |
| lstm | synthetic_noncollapsed | 3 | 60 | 10000 | 39.934183 | 0.654099 | 0.408000 | 113.739254 |
| lstm | synthetic_noncollapsed | 4 | 60 | 10000 | 42.173878 | 0.653868 | 0.408000 | 130.451488 |
| lstm | synthetic_noncollapsed | 5 | 60 | 10000 | 42.252627 | 0.648748 | 0.408000 | 125.231462 |
| lstm | synthetic_noncollapsed | 6 | 60 | 10000 | 41.321769 | 0.651551 | 0.408000 | 116.522909 |
| lstm | synthetic_noncollapsed | 7 | 60 | 10000 | 40.699883 | 0.656477 | 0.408000 | 131.781786 |
| lstm | synthetic_noncollapsed | 8 | 60 | 10000 | 40.723947 | 0.640693 | 0.408000 | 129.206110 |
| lstm | synthetic_noncollapsed | 9 | 60 | 10000 | 39.667868 | 0.647266 | 0.408000 | 129.157394 |
| lstm | synthetic_noncollapsed | 10 | 60 | 10000 | 40.476265 | 0.654240 | 0.408000 | 111.019503 |
| lstm | synthetic_noncollapsed | 11 | 60 | 10000 | 39.938117 | 0.656205 | 0.408000 | 128.425636 |
| lstm | synthetic_noncollapsed | 12 | 60 | 10000 | 44.112659 | 0.373762 | 0.408000 | 126.281300 |
| lstm | synthetic_noncollapsed | 14 | 60 | 10000 | 39.309065 | 0.655992 | 0.408000 | 136.223759 |
| lstm | synthetic_noncollapsed | 15 | 60 | 10000 | 41.142735 | 0.654917 | 0.408000 | 132.916317 |
| lstm | synthetic_noncollapsed | 16 | 60 | 10000 | 40.626496 | 0.654715 | 0.408000 | 90.264816 |
| lstm | synthetic_noncollapsed | 17 | 60 | 10000 | 45.281393 | 0.654830 | 0.408000 | 114.797340 |
| lstm | synthetic_noncollapsed | 18 | 60 | 10000 | 39.931535 | 0.655229 | 0.408000 | 119.212824 |
| lstm | synthetic_noncollapsed | 19 | 60 | 10000 | 43.713521 | 0.622473 | 0.408000 | 129.489531 |
| lstm | synthetic_noncollapsed | 20 | 60 | 10000 | 40.302089 | 0.654709 | 0.408000 | 129.854401 |
| lstm | synthetic_noncollapsed | 21 | 60 | 10000 | 40.096616 | 0.655043 | 0.408000 | 108.306656 |
| lstm | synthetic_noncollapsed | 22 | 60 | 10000 | 40.524738 | 0.618995 | 0.408000 | 129.121868 |
| lstm | synthetic_noncollapsed | 23 | 60 | 10000 | 40.494107 | 0.655291 | 0.408000 | 116.509151 |
| lstm | synthetic_noncollapsed | 24 | 60 | 10000 | 40.927178 | 0.655598 | 0.408000 | 121.299770 |
| lstm | synthetic_noncollapsed | 26 | 60 | 10000 | 42.760312 | 0.629315 | 0.408000 | 131.634104 |
| lstm | synthetic_noncollapsed | 27 | 60 | 10000 | 42.189360 | 0.656059 | 0.408000 | 125.236139 |
| lstm | synthetic_noncollapsed | 28 | 60 | 10000 | 50.115709 | 0.379198 | 0.408000 | 128.959835 |
| lstm | synthetic_noncollapsed | 29 | 60 | 10000 | 41.505401 | 0.656169 | 0.408000 | 124.461651 |
| lstm | real | 1101 | 60 | 100 | 17.642417 | 0.990625 | 0.200000 | 49.317932 |
| lstm | real | 1202 | 60 | 100 | 16.341004 | 0.994375 | 0.200000 | 42.673800 |
| lstm | real | 1303 | 60 | 100 | 17.793121 | 0.997500 | 0.200000 | 46.021120 |
| lstm | real | 1404 | 60 | 100 | 18.678372 | 0.995000 | 0.200000 | 45.059902 |
| lstm | real | 1505 | 60 | 100 | 19.113883 | 0.990625 | 0.200000 | 50.890293 |
| hybrid | synthetic_noncollapsed | 2 | 60 | 10000 | 43.588024 | 0.631133 | 0.408000 | 102.060230 |
| hybrid | synthetic_noncollapsed | 3 | 60 | 10000 | 44.354092 | 0.643094 | 0.408000 | 96.672171 |
| hybrid | synthetic_noncollapsed | 4 | 60 | 10000 | 48.003408 | 0.627756 | 0.408000 | 67.229908 |
| hybrid | synthetic_noncollapsed | 7 | 60 | 10000 | 42.098214 | 0.650906 | 0.408000 | 63.985497 |
| hybrid | synthetic_noncollapsed | 10 | 60 | 10000 | 43.819763 | 0.654172 | 0.408000 | 54.522182 |
| hybrid | synthetic_noncollapsed | 15 | 60 | 10000 | 41.986836 | 0.656168 | 0.408000 | 81.820681 |
| hybrid | synthetic_noncollapsed | 16 | 60 | 10000 | 45.628813 | 0.656474 | 0.408000 | 100.921925 |
| hybrid | synthetic_noncollapsed | 17 | 60 | 10000 | 46.818569 | 0.635551 | 0.408000 | 54.020357 |
| hybrid | synthetic_noncollapsed | 19 | 60 | 10000 | 49.593758 | 0.547727 | 0.408000 | 112.352192 |
| hybrid | synthetic_noncollapsed | 20 | 60 | 10000 | 40.086215 | 0.653901 | 0.408000 | 128.809662 |
| hybrid | synthetic_noncollapsed | 21 | 60 | 10000 | 45.836689 | 0.653898 | 0.408000 | 83.007884 |
| hybrid | synthetic_noncollapsed | 22 | 60 | 10000 | 39.424755 | 0.656982 | 0.408000 | 128.478073 |
| hybrid | synthetic_noncollapsed | 23 | 60 | 10000 | 52.075056 | 0.650920 | 0.408000 | 38.926368 |
| hybrid | synthetic_noncollapsed | 24 | 60 | 10000 | 41.632681 | 0.654955 | 0.408000 | 67.493212 |
| hybrid | synthetic_noncollapsed | 26 | 60 | 10000 | 40.837435 | 0.654610 | 0.408000 | 105.342472 |
| hybrid | synthetic_noncollapsed | 27 | 60 | 10000 | 42.501710 | 0.639832 | 0.408000 | 90.893251 |
| hybrid | synthetic_noncollapsed | 29 | 60 | 10000 | 44.078657 | 0.654791 | 0.408000 | 58.891588 |
| hybrid | real | 1101 | 60 | 100 | 15.869642 | 1.000000 | 0.200000 | 34.851009 |
| hybrid | real | 1202 | 60 | 100 | 14.132515 | 0.997500 | 0.200000 | 31.730463 |
| hybrid | real | 1303 | 60 | 100 | 16.070807 | 0.996875 | 0.200000 | 30.370975 |
| hybrid | real | 1404 | 60 | 100 | 14.858080 | 0.996875 | 0.200000 | 29.292889 |
| hybrid | real | 1505 | 60 | 100 | 15.258486 | 0.993125 | 0.200000 | 29.989012 |

## FD004 — per-fit difficulty

| architecture | cohort | fit_identifier | fitting_engines | evaluation_engines | RMSE_capped | event_AUC | event_base_rate | median_q95_minus_q05_width |
|---|---|---|---|---|---|---|---|---|
| lstm | synthetic_noncollapsed | 0 | 149 | 10000 | 42.525828 | 0.654165 | 0.403000 | 102.856657 |
| lstm | synthetic_noncollapsed | 1 | 149 | 10000 | 39.174851 | 0.654963 | 0.403000 | 106.444201 |
| lstm | synthetic_noncollapsed | 2 | 149 | 10000 | 40.808560 | 0.648706 | 0.403000 | 97.161373 |
| lstm | synthetic_noncollapsed | 3 | 149 | 10000 | 40.330701 | 0.657896 | 0.403000 | 102.093081 |
| lstm | synthetic_noncollapsed | 4 | 149 | 10000 | 41.326465 | 0.648631 | 0.403000 | 85.892569 |
| lstm | synthetic_noncollapsed | 5 | 149 | 10000 | 40.094466 | 0.641142 | 0.403000 | 132.057686 |
| lstm | synthetic_noncollapsed | 6 | 149 | 10000 | 39.109800 | 0.657810 | 0.403000 | 109.785652 |
| lstm | synthetic_noncollapsed | 7 | 149 | 10000 | 40.799144 | 0.630992 | 0.403000 | 129.944939 |
| lstm | synthetic_noncollapsed | 8 | 149 | 10000 | 40.950998 | 0.659329 | 0.403000 | 100.613180 |
| lstm | synthetic_noncollapsed | 9 | 149 | 10000 | 39.775951 | 0.648891 | 0.403000 | 115.513977 |
| lstm | synthetic_noncollapsed | 10 | 149 | 10000 | 40.167769 | 0.651344 | 0.403000 | 127.682356 |
| lstm | synthetic_noncollapsed | 11 | 149 | 10000 | 40.789794 | 0.653304 | 0.403000 | 122.596010 |
| lstm | synthetic_noncollapsed | 12 | 149 | 10000 | 39.530508 | 0.657494 | 0.403000 | 115.503170 |
| lstm | synthetic_noncollapsed | 13 | 149 | 10000 | 42.929454 | 0.634775 | 0.403000 | 125.623167 |
| lstm | synthetic_noncollapsed | 14 | 149 | 10000 | 39.621849 | 0.656848 | 0.403000 | 110.440969 |
| lstm | synthetic_noncollapsed | 15 | 149 | 10000 | 41.849445 | 0.654296 | 0.403000 | 116.523849 |
| lstm | synthetic_noncollapsed | 16 | 149 | 10000 | 39.497463 | 0.647248 | 0.403000 | 93.618763 |
| lstm | synthetic_noncollapsed | 17 | 149 | 10000 | 42.077507 | 0.656949 | 0.403000 | 110.408846 |
| lstm | synthetic_noncollapsed | 18 | 149 | 10000 | 41.408357 | 0.632280 | 0.403000 | 127.677404 |
| lstm | synthetic_noncollapsed | 19 | 149 | 10000 | 40.747747 | 0.657172 | 0.403000 | 112.313286 |
| lstm | synthetic_noncollapsed | 20 | 149 | 10000 | 41.453242 | 0.637755 | 0.403000 | 129.409269 |
| lstm | synthetic_noncollapsed | 21 | 149 | 10000 | 41.102792 | 0.647240 | 0.403000 | 122.230541 |
| lstm | synthetic_noncollapsed | 22 | 149 | 10000 | 39.655083 | 0.651512 | 0.403000 | 120.157204 |
| lstm | synthetic_noncollapsed | 23 | 149 | 10000 | 39.937060 | 0.654650 | 0.403000 | 123.371010 |
| lstm | synthetic_noncollapsed | 24 | 149 | 10000 | 39.621273 | 0.653477 | 0.403000 | 110.612219 |
| lstm | synthetic_noncollapsed | 25 | 149 | 10000 | 42.707969 | 0.656256 | 0.403000 | 93.965851 |
| lstm | synthetic_noncollapsed | 26 | 149 | 10000 | 40.442200 | 0.658399 | 0.403000 | 98.419310 |
| lstm | synthetic_noncollapsed | 27 | 149 | 10000 | 40.580632 | 0.654655 | 0.403000 | 106.130686 |
| lstm | synthetic_noncollapsed | 28 | 149 | 10000 | 41.756577 | 0.657068 | 0.403000 | 101.699236 |
| lstm | synthetic_noncollapsed | 29 | 149 | 10000 | 45.412032 | 0.653490 | 0.403000 | 130.113747 |
| lstm | real | 1101 | 149 | 248 | 16.889086 | 0.989453 | 0.213710 | 47.079948 |
| lstm | real | 1202 | 149 | 248 | 16.182553 | 0.987325 | 0.213710 | 45.974827 |
| lstm | real | 1303 | 149 | 248 | 16.223456 | 0.990227 | 0.213710 | 44.117435 |
| lstm | real | 1404 | 149 | 248 | 16.863734 | 0.988582 | 0.213710 | 46.053093 |
| lstm | real | 1505 | 149 | 248 | 16.645615 | 0.987712 | 0.213710 | 48.869740 |
| hybrid | synthetic_noncollapsed | 0 | 149 | 10000 | 41.248222 | 0.655310 | 0.403000 | 78.573975 |
| hybrid | synthetic_noncollapsed | 1 | 149 | 10000 | 39.617485 | 0.651249 | 0.403000 | 104.087696 |
| hybrid | synthetic_noncollapsed | 2 | 149 | 10000 | 39.971271 | 0.654923 | 0.403000 | 91.320433 |
| hybrid | synthetic_noncollapsed | 3 | 149 | 10000 | 40.496472 | 0.398778 | 0.403000 | 102.596312 |
| hybrid | synthetic_noncollapsed | 5 | 149 | 10000 | 39.485384 | 0.655795 | 0.403000 | 113.908693 |
| hybrid | synthetic_noncollapsed | 9 | 149 | 10000 | 39.065285 | 0.649828 | 0.403000 | 87.037621 |
| hybrid | synthetic_noncollapsed | 10 | 149 | 10000 | 40.241549 | 0.497859 | 0.403000 | 105.301437 |
| hybrid | synthetic_noncollapsed | 14 | 149 | 10000 | 39.361042 | 0.650692 | 0.403000 | 97.197794 |
| hybrid | synthetic_noncollapsed | 16 | 149 | 10000 | 39.608442 | 0.370025 | 0.403000 | 103.170563 |
| hybrid | synthetic_noncollapsed | 17 | 149 | 10000 | 43.739385 | 0.657076 | 0.403000 | 77.896793 |
| hybrid | synthetic_noncollapsed | 18 | 149 | 10000 | 41.846749 | 0.653260 | 0.403000 | 93.057501 |
| hybrid | synthetic_noncollapsed | 19 | 149 | 10000 | 41.687435 | 0.656687 | 0.403000 | 98.790703 |
| hybrid | synthetic_noncollapsed | 20 | 149 | 10000 | 39.585049 | 0.650846 | 0.403000 | 112.171225 |
| hybrid | synthetic_noncollapsed | 21 | 149 | 10000 | 42.787375 | 0.653903 | 0.403000 | 109.392668 |
| hybrid | synthetic_noncollapsed | 22 | 149 | 10000 | 39.832369 | 0.462007 | 0.403000 | 108.152925 |
| hybrid | synthetic_noncollapsed | 23 | 149 | 10000 | 39.425169 | 0.654686 | 0.403000 | 83.190262 |
| hybrid | synthetic_noncollapsed | 25 | 149 | 10000 | 43.492838 | 0.654073 | 0.403000 | 90.973133 |
| hybrid | synthetic_noncollapsed | 29 | 149 | 10000 | 41.937243 | 0.471059 | 0.403000 | 115.774063 |
| hybrid | real | 1101 | 149 | 248 | 16.818576 | 0.991388 | 0.213710 | 44.955349 |
| hybrid | real | 1202 | 149 | 248 | 16.297869 | 0.983745 | 0.213710 | 38.905766 |
| hybrid | real | 1303 | 149 | 248 | 16.988267 | 0.989550 | 0.213710 | 47.926113 |
| hybrid | real | 1404 | 149 | 248 | 16.288625 | 0.982003 | 0.213710 | 43.809986 |
| hybrid | real | 1505 | 149 | 248 | 16.315449 | 0.982777 | 0.213710 | 42.521038 |


## Synthetic law (generator record)

- Weibull shape: 1 (exponential excess lifetime).
- Covariate: x in {-1, +1}; scale(x) = 60 exp(0.5 x).
- Training and uniform-endpoint lifetime: T = 30 + Exponential(scale(x)).
- Final-window generator: age sampled from saved empirical truncation ages; RUL = Exponential(scale(x)); lifetime = age + RUL.
- Final-window conditional RUL law: depends on x/features; independent of age given x. For 0 <= u < 125, F(u | x,age) = 1 - exp(-u/scale(x)). Capping places the remaining probability mass at 125.
- Uniform-endpoint conditional RUL law: depends on age and x/features. For 0 <= u < 125, F(u | x,age) = 1 - E1((age-30+u)/scale(x)) / E1((age-30)/scale(x)). Capping places the remaining probability mass at 125.
- Features: the first channel is x, the second is observed time/125; remaining channels combine x, time/scale(x), and independent Gaussian noise. They are not generated directly from realized RUL.
- Source: scripts/validate_compatibility_synthetic.py, oracle, endpoints, features, training_data; reports/compatibility_null_validation/report.md (Weibull shape 1 record).

Primary difficulty tables contain one row per fixed fit. Separate difficulty_summary.csv contains arithmetic means of fit-level metrics; its width column is a mean of fit-level medians. Per-fit values: difficulty_per_fit.csv and difficulty_per_fit_FD001–FD004.csv. No bootstrap, training or forward inference was run. Independent human review remains missing.

Source line ranges: oracle: 29–44; endpoints: 63–69; features: 71–75; training_data: 92–102.

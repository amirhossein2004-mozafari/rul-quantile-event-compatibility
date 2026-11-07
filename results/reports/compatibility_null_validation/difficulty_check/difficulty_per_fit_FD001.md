# FD001 — per-fit difficulty

`synthetic_noncollapsed`: retained temporal weighted_raw fits, final-window, 10000 engines. `real`: all five frozen real fits per architecture. RMSE uses capped truth and projected median; width uses raw quantiles. Rates/AUC are fractions.

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

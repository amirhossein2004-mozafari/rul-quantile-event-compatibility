# FD002 — per-fit difficulty

`synthetic_noncollapsed`: retained temporal weighted_raw fits, final-window, 10000 engines. `real`: all five frozen real fits per architecture. RMSE uses capped truth and projected median; width uses raw quantiles. Rates/AUC are fractions.

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

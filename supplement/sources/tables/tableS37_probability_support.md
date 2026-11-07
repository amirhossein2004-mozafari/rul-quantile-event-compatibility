| Split | Cal engines | Prefixes | Endpoint events | Prefix prior | Train prior |
| --- | --- | --- | --- | --- | --- |
| O-FD001-101 | 20 | 4426 | 6/20 | 0.1417 | 0.1789 |
| O-FD001-202 | 20 | 4209 | 5/20 | 0.1524 | 0.1761 |
| O-FD001-303 | 20 | 4204 | 7/20 | 0.1503 | 0.1760 |
| O-FD001-404 | 20 | 3939 | 4/20 | 0.1570 | 0.1728 |
| O-FD001-505 | 20 | 4210 | 6/20 | 0.1519 | 0.1761 |
| M-FD001-shared | 20 | 4290 | 1/20 | 0.1503 | 0.1794 |
| O-FD002-101 | 52 | 10663 | 14/52 | 0.1534 | 0.1742 |
| O-FD002-202 | 52 | 11294 | 10/52 | 0.1453 | 0.1772 |
| O-FD002-303 | 52 | 10851 | 14/52 | 0.1497 | 0.1751 |
| O-FD002-404 | 52 | 10820 | 10/52 | 0.1507 | 0.1750 |
| O-FD002-505 | 52 | 10729 | 15/52 | 0.1515 | 0.1745 |
| M-FD002-shared | 52 | 10861 | 6/52 | 0.1526 | 0.1745 |
| O-FD003-101 | 20 | 4582 | 6/20 | 0.1380 | 0.1393 |
| O-FD003-202 | 20 | 5298 | 5/20 | 0.1290 | 0.1452 |
| O-FD003-303 | 20 | 4965 | 7/20 | 0.1320 | 0.1424 |
| O-FD003-404 | 20 | 5274 | 4/20 | 0.1254 | 0.1450 |
| O-FD003-505 | 20 | 4956 | 6/20 | 0.1339 | 0.1423 |
| M-FD003-shared | 20 | 5274 | 1/20 | 0.1270 | 0.1464 |
| O-FD004-101 | 50 | 11951 | 12/50 | 0.1372 | 0.1419 |
| O-FD004-202 | 50 | 12525 | 10/50 | 0.1305 | 0.1438 |
| O-FD004-303 | 50 | 12491 | 14/50 | 0.1287 | 0.1437 |
| O-FD004-404 | 50 | 12480 | 9/50 | 0.1284 | 0.1436 |
| O-FD004-505 | 50 | 12195 | 14/50 | 0.1330 | 0.1427 |
| M-FD004-shared | 50 | 12324 | 5/50 | 0.1385 | 0.1453 |

: O: original split; M: one matched split shared across all four architectures and five seeds. Every calibration engine contains event and non-event prefixes. Prefix prior gives each engine total weight one; training prior uses complete fitting windows including RUL zero. The 24 unique feature-model fits must not be counted as100 independent baselines. Official-test event support is 25/100,61/259,20/100 and 53/248 for FD001-FD004; these labels only score frozen predictions. Prefixes are dependent, and neither calibration prior identifies the official truncation population.


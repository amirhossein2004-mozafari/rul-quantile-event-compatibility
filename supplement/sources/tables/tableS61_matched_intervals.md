| Subset | Predictor | Construction | RMSE | Coverage | Width | Winkler |
| --- | --- | --- | --- | --- | --- | --- |
| FD001 | LSTM | Point-CP | 14.7 ± 0.6 | 0.964 ± 0.015 | 55.2 ± 1.6 | 61.7 ± 2.6 |
| FD001 | LSTM | CQR | 14.7 ± 0.6 | 0.916 ± 0.092 | 43.5 ± 8.0 | infinity |
| FD001 | LSTM | Asym-CQR | 14.7 ± 0.6 | 0.944 ± 0.064 | 93.0 ± 2.6 | 104.9 ± 4.2 |
| FD001 | Hybrid | Point-CP | 15.9 ± 1.2 | 0.944 ± 0.044 | 51.4 ± 8.5 | 62.2 ± 2.7 |
| FD001 | Hybrid | CQR | 15.9 ± 1.2 | 0.928 ± 0.048 | 46.2 ± 7.3 | 59.9 ± 2.2 |
| FD001 | Hybrid | Asym-CQR | 15.9 ± 1.2 | 0.954 ± 0.028 | 93.2 ± 3.8 | 103.5 ± 2.7 |
| FD001 | TCN | Point-CP | 18.1 ± 2.9 | 0.954 ± 0.011 | 62.7 ± 13.4 | 71.4 ± 11.8 |
| FD001 | TCN | CQR | 18.1 ± 2.9 | 0.948 ± 0.015 | 62.9 ± 16.0 | 73.0 ± 14.9 |
| FD001 | TCN | Asym-CQR | 18.1 ± 2.9 | 0.970 ± 0.014 | 98.9 ± 2.2 | 105.6 ± 3.8 |
| FD001 | GRU | Point-CP | 14.3 ± 0.4 | 0.912 ± 0.004 | 41.5 ± 1.4 | 59.4 ± 2.2 |
| FD001 | GRU | CQR | 14.3 ± 0.4 | 0.882 ± 0.030 | 34.7 ± 3.2 | 54.8 ± 4.4 |
| FD001 | GRU | Asym-CQR | 14.3 ± 0.4 | 0.868 ± 0.049 | 87.5 ± 1.1 | 106.3 ± 4.2 |
| FD001 | TCN-last | Point-CP | 16.7 ± 0.5 | 0.950 ± 0.019 | 60.8 ± 5.9 | 67.9 ± 3.3 |
| FD001 | TCN-last | CQR | 16.7 ± 0.5 | 0.950 ± 0.007 | 56.0 ± 4.2 | 67.1 ± 3.8 |
| FD001 | TCN-last | Asym-CQR | 16.7 ± 0.5 | 0.960 ± 0.012 | 98.0 ± 2.0 | 104.9 ± 1.6 |
| FD001 | Transformer | Point-CP | 15.5 ± 0.9 | 0.964 ± 0.028 | 56.5 ± 10.4 | 63.7 ± 4.7 |
| FD001 | Transformer | CQR | 15.5 ± 0.9 | 0.962 ± 0.028 | 50.4 ± 11.0 | 58.2 ± 5.7 |
| FD001 | Transformer | Asym-CQR | 15.5 ± 0.9 | 0.904 ± 0.091 | 91.8 ± 8.0 | infinity |
| FD001 | Gaussian-GRU | Point-CP | 13.9 ± 0.5 | 0.932 ± 0.022 | 48.1 ± 4.4 | 58.6 ± 2.4 |
| FD001 | Gaussian-GRU | CQR | 13.9 ± 0.5 | 0.896 ± 0.058 | 40.3 ± 4.7 | 55.0 ± 2.8 |
| FD001 | Gaussian-GRU | Asym-CQR | 13.9 ± 0.5 | 0.958 ± 0.019 | 91.6 ± 0.9 | 98.1 ± 1.7 |
| FD001 | TCN-GPU | Point-CP | 18.1 ± 1.8 | 0.938 ± 0.024 | 60.6 ± 11.3 | 69.7 ± 6.5 |
| FD001 | TCN-GPU | CQR | 18.1 ± 1.8 | 0.938 ± 0.026 | 58.5 ± 14.5 | 70.4 ± 9.6 |
| FD001 | TCN-GPU | Asym-CQR | 18.1 ± 1.8 | 0.972 ± 0.013 | 99.2 ± 1.1 | 104.3 ± 2.0 |
| FD001 | LSTM-GPU | Point-CP | 14.9 ± 0.4 | 0.932 ± 0.047 | 51.6 ± 9.1 | 61.7 ± 2.4 |
| FD001 | LSTM-GPU | CQR | 14.9 ± 0.4 | 0.906 ± 0.073 | 44.5 ± 7.3 | 57.4 ± 2.3 |
| FD001 | LSTM-GPU | Asym-CQR | 14.9 ± 0.4 | 0.972 ± 0.011 | 93.6 ± 0.9 | 102.0 ± 2.1 |
| FD001 | Hybrid-GPU | Point-CP | 16.6 ± 1.9 | 0.926 ± 0.047 | 50.0 ± 7.1 | 62.8 ± 3.5 |
| FD001 | Hybrid-GPU | CQR | 16.6 ± 1.9 | 0.910 ± 0.063 | 44.1 ± 8.5 | 59.3 ± 4.4 |
| FD001 | Hybrid-GPU | Asym-CQR | 16.6 ± 1.9 | 0.940 ± 0.029 | 91.7 ± 3.2 | 102.7 ± 2.5 |
| FD001 | GRU-GPU | Point-CP | 14.6 ± 0.8 | 0.918 ± 0.016 | 45.3 ± 4.0 | 61.4 ± 2.5 |
| FD001 | GRU-GPU | CQR | 14.6 ± 0.8 | 0.872 ± 0.041 | 35.3 ± 4.9 | infinity |
| FD001 | GRU-GPU | Asym-CQR | 14.6 ± 0.8 | 0.918 ± 0.064 | 91.1 ± 3.5 | infinity |
| FD001 | Gaussian-Ens | Point-CP | 13.5 | 0.940 | 45.3 | 57.7 |
| FD001 | Gaussian-Ens | CQR | 13.5 | 0.900 | 38.1 | 53.1 |
| FD001 | Gaussian-Ens | Asym-CQR | 13.5 | 0.960 | 90.5 | 98.1 |
| FD001 | GBR | Point-CP | 17.3 | 0.980 | 68.9 | 72.9 |
| FD001 | GBR | CQR | 17.3 | 0.960 | 61.1 | 65.8 |
| FD001 | GBR | Asym-CQR | 17.3 | 1.000 | 107.2 | 107.2 |
| FD002 | LSTM | Point-CP | 14.3 ± 0.5 | 0.978 ± 0.010 | 60.4 ± 4.4 | 63.9 ± 3.4 |
| FD002 | LSTM | CQR | 14.3 ± 0.5 | 0.978 ± 0.009 | 50.2 ± 4.2 | 53.7 ± 3.3 |
| FD002 | LSTM | Asym-CQR | 14.3 ± 0.5 | 0.946 ± 0.059 | 60.4 ± 4.4 | 66.8 ± 2.4 |
| FD002 | Hybrid | Point-CP | 15.4 ± 1.4 | 0.969 ± 0.004 | 60.4 ± 2.8 | 65.5 ± 3.8 |
| FD002 | Hybrid | CQR | 15.4 ± 1.4 | 0.967 ± 0.008 | 50.3 ± 2.6 | 56.0 ± 3.6 |
| FD002 | Hybrid | Asym-CQR | 15.4 ± 1.4 | 0.958 ± 0.023 | 59.2 ± 1.1 | 65.7 ± 1.9 |
| FD002 | TCN | Point-CP | 18.5 ± 2.2 | 0.940 ± 0.013 | 58.2 ± 4.9 | 67.3 ± 5.8 |
| FD002 | TCN | CQR | 18.5 ± 2.2 | 0.958 ± 0.009 | 66.8 ± 11.3 | 72.1 ± 10.9 |
| FD002 | TCN | Asym-CQR | 18.5 ± 2.2 | 0.976 ± 0.011 | 60.3 ± 4.5 | 63.9 ± 3.6 |
| FD002 | GRU | Point-CP | 13.6 ± 0.5 | 0.985 ± 0.006 | 58.1 ± 2.8 | 61.6 ± 1.8 |
| FD002 | GRU | CQR | 13.6 ± 0.5 | 0.977 ± 0.013 | 48.4 ± 2.5 | 52.8 ± 1.7 |
| FD002 | GRU | Asym-CQR | 13.6 ± 0.5 | 0.939 ± 0.031 | 57.8 ± 1.6 | 65.2 ± 1.6 |
| FD002 | TCN-last | Point-CP | 17.1 ± 1.3 | 0.964 ± 0.013 | 59.6 ± 3.6 | 65.2 ± 2.7 |
| FD002 | TCN-last | CQR | 17.1 ± 1.3 | 0.965 ± 0.015 | 59.0 ± 7.4 | 63.2 ± 7.3 |
| FD002 | TCN-last | Asym-CQR | 17.1 ± 1.3 | 0.980 ± 0.008 | 58.6 ± 2.8 | 60.9 ± 1.8 |
| FD002 | Transformer | Point-CP | 14.4 ± 0.6 | 0.988 ± 0.006 | 67.1 ± 3.3 | 68.9 ± 3.2 |
| FD002 | Transformer | CQR | 14.4 ± 0.6 | 0.983 ± 0.010 | 54.3 ± 4.7 | 57.1 ± 4.5 |
| FD002 | Transformer | Asym-CQR | 14.4 ± 0.6 | 0.928 ± 0.033 | 56.7 ± 4.6 | 64.9 ± 3.7 |
| FD002 | Gaussian-GRU | Point-CP | 16.8 ± 2.2 | 0.960 ± 0.017 | 59.3 ± 5.3 | 66.5 ± 6.0 |
| FD002 | Gaussian-GRU | CQR | 16.8 ± 2.2 | 0.960 ± 0.024 | 50.6 ± 7.2 | 58.5 ± 7.3 |
| FD002 | Gaussian-GRU | Asym-CQR | 16.8 ± 2.2 | 0.972 ± 0.017 | 60.6 ± 5.6 | 67.0 ± 4.3 |
| FD002 | TCN-GPU | Point-CP | 17.7 ± 2.1 | 0.940 ± 0.003 | 56.2 ± 6.0 | 65.4 ± 5.9 |
| FD002 | TCN-GPU | CQR | 17.7 ± 2.1 | 0.946 ± 0.019 | 63.2 ± 10.1 | 69.4 ± 11.0 |
| FD002 | TCN-GPU | Asym-CQR | 17.7 ± 2.1 | 0.969 ± 0.011 | 60.7 ± 3.3 | 63.9 ± 3.5 |
| FD002 | LSTM-GPU | Point-CP | 14.5 ± 0.6 | 0.975 ± 0.011 | 59.5 ± 4.9 | 64.2 ± 3.3 |
| FD002 | LSTM-GPU | CQR | 14.5 ± 0.6 | 0.966 ± 0.016 | 46.8 ± 4.0 | 52.4 ± 3.4 |
| FD002 | LSTM-GPU | Asym-CQR | 14.5 ± 0.6 | 0.970 ± 0.019 | 60.3 ± 1.0 | 66.0 ± 2.3 |
| FD002 | Hybrid-GPU | Point-CP | 14.8 ± 0.5 | 0.969 ± 0.009 | 58.6 ± 3.0 | 63.9 ± 1.8 |
| FD002 | Hybrid-GPU | CQR | 14.8 ± 0.5 | 0.971 ± 0.008 | 50.0 ± 4.7 | 54.5 ± 3.1 |
| FD002 | Hybrid-GPU | Asym-CQR | 14.8 ± 0.5 | 0.948 ± 0.032 | 59.2 ± 2.7 | 65.0 ± 1.2 |
| FD002 | GRU-GPU | Point-CP | 13.6 ± 0.2 | 0.985 ± 0.004 | 58.6 ± 2.5 | 61.8 ± 2.0 |
| FD002 | GRU-GPU | CQR | 13.6 ± 0.2 | 0.981 ± 0.006 | 49.7 ± 3.1 | 53.5 ± 2.0 |
| FD002 | GRU-GPU | Asym-CQR | 13.6 ± 0.2 | 0.937 ± 0.036 | 56.4 ± 0.8 | 64.5 ± 2.9 |
| FD002 | Gaussian-Ens | Point-CP | 16.3 | 0.961 | 56.6 | 63.7 |
| FD002 | Gaussian-Ens | CQR | 16.3 | 0.961 | 44.0 | 51.9 |
| FD002 | Gaussian-Ens | Asym-CQR | 16.3 | 0.961 | 58.7 | 65.5 |
| FD002 | GBR | Point-CP | 17.6 | 0.985 | 68.8 | 71.6 |
| FD002 | GBR | CQR | 17.6 | 0.954 | 60.1 | 66.0 |
| FD002 | GBR | Asym-CQR | 17.6 | 0.988 | 76.1 | 77.0 |
| FD003 | LSTM | Point-CP | 17.9 ± 1.1 | 0.940 ± 0.016 | 58.9 ± 4.9 | 73.8 ± 0.8 |
| FD003 | LSTM | CQR | 17.9 ± 1.1 | 0.940 ± 0.016 | 56.1 ± 5.6 | 69.2 ± 1.7 |
| FD003 | LSTM | Asym-CQR | 17.9 ± 1.1 | 0.982 ± 0.008 | 99.5 ± 2.8 | 104.2 ± 2.0 |
| FD003 | Hybrid | Point-CP | 15.2 ± 0.8 | 0.958 ± 0.036 | 57.1 ± 11.4 | 64.4 ± 7.6 |
| FD003 | Hybrid | CQR | 15.2 ± 0.8 | 0.946 ± 0.043 | 49.9 ± 13.5 | 59.2 ± 9.1 |
| FD003 | Hybrid | Asym-CQR | 15.2 ± 0.8 | 0.988 ± 0.022 | 99.5 ± 6.8 | 102.2 ± 5.0 |
| FD003 | TCN | Point-CP | 18.7 ± 1.9 | 0.942 ± 0.037 | 61.1 ± 13.9 | 73.1 ± 8.3 |
| FD003 | TCN | CQR | 18.7 ± 1.9 | 0.946 ± 0.046 | 63.9 ± 17.3 | 73.1 ± 12.0 |
| FD003 | TCN | Asym-CQR | 18.7 ± 1.9 | 0.988 ± 0.022 | 104.5 ± 7.3 | 106.8 ± 4.4 |
| FD003 | GRU | Point-CP | 14.7 ± 0.9 | 0.906 ± 0.035 | 44.6 ± 7.2 | 61.2 ± 2.7 |
| FD003 | GRU | CQR | 14.7 ± 0.9 | 0.916 ± 0.034 | 39.1 ± 6.7 | 53.1 ± 3.2 |
| FD003 | GRU | Asym-CQR | 14.7 ± 0.9 | 0.972 ± 0.036 | 90.0 ± 2.4 | 94.6 ± 4.3 |
| FD003 | TCN-last | Point-CP | 17.9 ± 1.3 | 0.942 ± 0.036 | 60.6 ± 9.1 | 69.8 ± 5.3 |
| FD003 | TCN-last | CQR | 17.9 ± 1.3 | 0.948 ± 0.044 | 59.1 ± 12.4 | 67.0 ± 8.2 |
| FD003 | TCN-last | Asym-CQR | 17.9 ± 1.3 | 0.988 ± 0.008 | 102.4 ± 3.5 | 104.1 ± 2.4 |
| FD003 | Transformer | Point-CP | 15.9 ± 1.2 | 0.894 ± 0.048 | 44.1 ± 6.6 | 65.1 ± 5.4 |
| FD003 | Transformer | CQR | 15.9 ± 1.2 | 0.888 ± 0.067 | 38.0 ± 6.6 | 56.1 ± 3.1 |
| FD003 | Transformer | Asym-CQR | 15.9 ± 1.2 | 0.956 ± 0.040 | 90.8 ± 4.1 | 95.0 ± 1.4 |
| FD003 | Gaussian-GRU | Point-CP | 14.8 ± 0.6 | 0.940 ± 0.042 | 53.3 ± 7.8 | 61.3 ± 2.7 |
| FD003 | Gaussian-GRU | CQR | 14.8 ± 0.6 | 0.960 ± 0.020 | 51.5 ± 5.0 | 54.9 ± 3.0 |
| FD003 | Gaussian-GRU | Asym-CQR | 14.8 ± 0.6 | 0.986 ± 0.011 | 97.4 ± 3.3 | 98.4 ± 2.7 |
| FD003 | TCN-GPU | Point-CP | 18.7 ± 1.9 | 0.956 ± 0.029 | 63.0 ± 12.7 | 70.3 ± 7.4 |
| FD003 | TCN-GPU | CQR | 18.7 ± 1.9 | 0.964 ± 0.009 | 67.6 ± 11.6 | 72.1 ± 9.6 |
| FD003 | TCN-GPU | Asym-CQR | 18.7 ± 1.9 | 0.990 ± 0.012 | 105.7 ± 2.7 | 106.3 ± 2.2 |
| FD003 | LSTM-GPU | Point-CP | 18.5 ± 1.0 | 0.922 ± 0.026 | 55.2 ± 8.6 | 78.2 ± 3.4 |
| FD003 | LSTM-GPU | CQR | 18.5 ± 1.0 | 0.932 ± 0.024 | 51.8 ± 7.4 | 71.5 ± 4.0 |
| FD003 | LSTM-GPU | Asym-CQR | 18.5 ± 1.0 | 0.982 ± 0.011 | 99.4 ± 5.4 | 104.1 ± 4.9 |
| FD003 | Hybrid-GPU | Point-CP | 15.0 ± 1.0 | 0.922 ± 0.074 | 50.0 ± 11.6 | 64.8 ± 5.1 |
| FD003 | Hybrid-GPU | CQR | 15.0 ± 1.0 | 0.884 ± 0.151 | 44.6 ± 14.7 | 62.9 ± 10.9 |
| FD003 | Hybrid-GPU | Asym-CQR | 15.0 ± 1.0 | 0.970 ± 0.031 | 95.5 ± 5.0 | 99.2 ± 2.6 |
| FD003 | GRU-GPU | Point-CP | 14.5 ± 1.2 | 0.922 ± 0.052 | 48.8 ± 10.8 | 60.4 ± 5.6 |
| FD003 | GRU-GPU | CQR | 14.5 ± 1.2 | 0.930 ± 0.063 | 43.4 ± 9.8 | 53.0 ± 5.5 |
| FD003 | GRU-GPU | Asym-CQR | 14.5 ± 1.2 | 0.966 ± 0.039 | 90.9 ± 3.4 | 95.7 ± 3.8 |
| FD003 | Gaussian-Ens | Point-CP | 14.2 | 0.960 | 55.8 | 59.1 |
| FD003 | Gaussian-Ens | CQR | 14.2 | 0.940 | 47.7 | 51.9 |
| FD003 | Gaussian-Ens | Asym-CQR | 14.2 | 0.970 | 94.9 | 96.1 |
| FD003 | GBR | Point-CP | 20.2 | 0.930 | 61.7 | 74.7 |
| FD003 | GBR | CQR | 20.2 | 0.910 | 58.1 | 68.4 |
| FD003 | GBR | Asym-CQR | 20.2 | 0.970 | 105.8 | 106.7 |
| FD004 | LSTM | Point-CP | 16.6 ± 0.3 | 0.945 ± 0.023 | 54.2 ± 7.4 | 66.5 ± 2.2 |
| FD004 | LSTM | CQR | 16.6 ± 0.3 | 0.955 ± 0.032 | 48.7 ± 5.9 | 58.4 ± 2.3 |
| FD004 | LSTM | Asym-CQR | 16.6 ± 0.3 | 0.973 ± 0.024 | 62.4 ± 3.6 | 68.5 ± 3.6 |
| FD004 | Hybrid | Point-CP | 16.5 ± 0.3 | 0.932 ± 0.027 | 51.5 ± 7.6 | 67.2 ± 2.2 |
| FD004 | Hybrid | CQR | 16.5 ± 0.3 | 0.906 ± 0.041 | 44.1 ± 7.0 | 61.4 ± 3.1 |
| FD004 | Hybrid | Asym-CQR | 16.5 ± 0.3 | 0.931 ± 0.029 | 58.6 ± 4.3 | 71.4 ± 3.7 |
| FD004 | TCN | Point-CP | 19.3 ± 1.2 | 0.931 ± 0.016 | 56.9 ± 0.9 | 71.5 ± 4.2 |
| FD004 | TCN | CQR | 19.3 ± 1.2 | 0.931 ± 0.018 | 59.1 ± 8.1 | 69.8 ± 5.4 |
| FD004 | TCN | Asym-CQR | 19.3 ± 1.2 | 0.952 ± 0.008 | 71.9 ± 1.6 | 80.0 ± 1.4 |
| FD004 | GRU | Point-CP | 14.9 ± 0.4 | 0.923 ± 0.019 | 45.1 ± 3.6 | 62.2 ± 1.7 |
| FD004 | GRU | CQR | 14.9 ± 0.4 | 0.902 ± 0.047 | 38.7 ± 4.2 | 54.4 ± 3.2 |
| FD004 | GRU | Asym-CQR | 14.9 ± 0.4 | 0.911 ± 0.035 | 49.9 ± 5.0 | 63.6 ± 8.2 |
| FD004 | TCN-last | Point-CP | 19.8 ± 1.9 | 0.904 ± 0.013 | 55.8 ± 6.4 | 76.6 ± 4.9 |
| FD004 | TCN-last | CQR | 19.8 ± 1.9 | 0.926 ± 0.035 | 60.9 ± 14.2 | 73.3 ± 8.6 |
| FD004 | TCN-last | Asym-CQR | 19.8 ± 1.9 | 0.941 ± 0.026 | 68.7 ± 4.6 | 79.2 ± 2.3 |
| FD004 | Transformer | Point-CP | 16.5 ± 0.9 | 0.918 ± 0.039 | 48.9 ± 5.5 | 65.5 ± 3.4 |
| FD004 | Transformer | CQR | 16.5 ± 0.9 | 0.915 ± 0.021 | 41.3 ± 3.7 | 58.3 ± 2.8 |
| FD004 | Transformer | Asym-CQR | 16.5 ± 0.9 | 0.899 ± 0.027 | 44.2 ± 2.0 | 65.8 ± 5.2 |
| FD004 | Gaussian-GRU | Point-CP | 15.7 ± 0.3 | 0.889 ± 0.022 | 41.4 ± 3.7 | 64.2 ± 2.8 |
| FD004 | Gaussian-GRU | CQR | 15.7 ± 0.3 | 0.936 ± 0.026 | 45.9 ± 5.0 | 56.3 ± 2.4 |
| FD004 | Gaussian-GRU | Asym-CQR | 15.7 ± 0.3 | 0.960 ± 0.014 | 51.1 ± 5.2 | 58.9 ± 2.3 |
| FD004 | TCN-GPU | Point-CP | 19.8 ± 1.1 | 0.934 ± 0.019 | 59.0 ± 3.6 | 72.7 ± 3.8 |
| FD004 | TCN-GPU | CQR | 19.8 ± 1.1 | 0.935 ± 0.023 | 62.5 ± 7.7 | 74.0 ± 4.5 |
| FD004 | TCN-GPU | Asym-CQR | 19.8 ± 1.1 | 0.947 ± 0.014 | 71.6 ± 2.5 | 81.1 ± 1.1 |
| FD004 | LSTM-GPU | Point-CP | 16.6 ± 0.4 | 0.935 ± 0.020 | 50.9 ± 4.3 | 65.3 ± 2.3 |
| FD004 | LSTM-GPU | CQR | 16.6 ± 0.4 | 0.908 ± 0.046 | 41.9 ± 6.3 | 58.8 ± 2.5 |
| FD004 | LSTM-GPU | Asym-CQR | 16.6 ± 0.4 | 0.942 ± 0.027 | 57.9 ± 5.4 | 69.9 ± 5.1 |
| FD004 | Hybrid-GPU | Point-CP | 16.6 ± 0.3 | 0.938 ± 0.017 | 52.7 ± 4.5 | 67.0 ± 2.6 |
| FD004 | Hybrid-GPU | CQR | 16.6 ± 0.3 | 0.912 ± 0.040 | 45.6 ± 7.4 | 61.5 ± 3.1 |
| FD004 | Hybrid-GPU | Asym-CQR | 16.6 ± 0.3 | 0.923 ± 0.038 | 58.8 ± 6.0 | 72.6 ± 3.9 |
| FD004 | GRU-GPU | Point-CP | 15.5 ± 0.4 | 0.916 ± 0.037 | 46.7 ± 7.1 | 64.5 ± 1.9 |
| FD004 | GRU-GPU | CQR | 15.5 ± 0.4 | 0.913 ± 0.050 | 39.7 ± 3.9 | 54.6 ± 3.1 |
| FD004 | GRU-GPU | Asym-CQR | 15.5 ± 0.4 | 0.934 ± 0.029 | 52.5 ± 6.8 | 64.2 ± 5.3 |
| FD004 | Gaussian-Ens | Point-CP | 15.2 | 0.883 | 40.8 | 61.5 |
| FD004 | Gaussian-Ens | CQR | 15.2 | 0.931 | 44.0 | 52.6 |
| FD004 | Gaussian-Ens | Asym-CQR | 15.2 | 0.952 | 49.7 | 56.2 |
| FD004 | GBR | Point-CP | 20.0 | 0.875 | 50.7 | 79.4 |
| FD004 | GBR | CQR | 20.0 | 0.927 | 59.9 | 69.9 |
| FD004 | GBR | Asym-CQR | 20.0 | 0.992 | 89.7 | 91.4 |

: capped-target interval comparison under the same saved calibration endpoints and official-test engines. Point-CP uses absolute point residuals; CQR uses the original signed two-tail maximum; Asym-CQR uses separate lower/upper residuals with fixed 0.025/0.075 tail allocations. Gaussian-Ens and GBR are one fixed model construction per subset; other entries summarize five fits. GBR uses three fixed 200-tree, depth 3, rate 0.05 models on fitting-window last-observation features. RMSE uses the capped point predictor against the stated target and is unchanged by interval calibration. These are matched algorithm-family controls inspired by Javanmardi and Robinson, not full reproductions of their feature pipelines or published systems. Models remain capped-trained even for raw residual calibration. Untagged LSTM/Hybrid/TCN/GRU entries are earlier CPU fits; GPU-tagged references and the new arms are CUDA refits. New calibrated sets intersect the target domain; empty sets retain infinite Winkler scores. Infinite cutoffs and repeated-engine counts appear in Table S66. No coverage guarantee is established.


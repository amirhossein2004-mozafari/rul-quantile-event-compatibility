
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

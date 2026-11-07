| Study | Predictor/output | Published C-MAPSS result | Comparison boundary |
| --- | --- | --- | --- |
| [@mfsscinet2024] | MFSSCINet; RUL point prediction | RMSE 10.93 / 13.55 / 11.26 / 13.67 (FD001-FD004) | Their Table 5; windows and tuning differ from this study |
| [@robinson2026riskaware] | Gradient boosting; asymmetric CQR | RMSE 13.26-16.85 across subsets; coverage 88-92% at 90% nominal | Published aggregate ranges; not a matched reimplementation |
| Present evaluation | Ordered quantiles and a separate event probability | Matched architecture and probability results in Tables 2-5 | Within-study controls share the recorded protocol |

: Published results provide context, not a pooled leaderboard. The Cen values are copied at their published precision; the Robinson values are the publisher abstract ranges. Different windows, targets, preprocessing and selection rules prevent a causal performance ranking against the present runs.


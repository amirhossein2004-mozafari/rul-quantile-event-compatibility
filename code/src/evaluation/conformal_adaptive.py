"""Exact nonnegative conformal evaluation on capped RUL, with reproducible diagnostics.

Width normalization is evaluated empirically. It neither establishes exchangeability
between the endpoint sampling schemes nor guarantees 90% coverage in every test run.
Run: python -m src.evaluation.conformal_adaptive
"""
from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_CEILING
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

RESULTS_EXACT = PROJECT_ROOT/"results/final_evaluation_v3_exact_conformal"
CALIBRATION = RESULTS_EXACT/"calibration"
OUT_DIR = PROJECT_ROOT/"results/implement_stage"
ALL_SUBSETS = ["FD001", "FD002", "FD003", "FD004"]
ALL_SEEDS = [101, 202, 303, 404, 505]
ALPHA = 0.10
EPS_W = 1e-6
RUL_CAP = 125.0


def _validate_alpha(alpha):
    if not np.isscalar(alpha) or not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be finite and strictly between zero and one")


def _validate_vectors(lower, upper, y=None):
    lower, upper = np.asarray(lower, dtype=float), np.asarray(upper, dtype=float)
    arrays = [lower, upper] if y is None else [lower, upper, np.asarray(y, dtype=float)]
    if (lower.ndim != 1 or not len(lower)
            or any(a.shape != lower.shape or not np.isfinite(a).all() for a in arrays)
            or np.any(lower > upper)):
        raise ValueError("Require nonempty paired finite vectors with lower <= upper")
    return arrays


def _standard_scores(q05, q95, y):
    """Nonnegative max-margin variant; unlike signed CQR, it cannot shrink base intervals."""
    lower, upper, target = _validate_vectors(q05, q95, y)
    return np.maximum(np.maximum(lower-target, target-upper), 0.0)


def _scale(q05, q95, alpha_norm):
    _validate_vectors(q05, q95)
    if not np.isfinite(alpha_norm) or alpha_norm < 0:
        raise ValueError("Normalization power must be finite and nonnegative")
    with np.errstate(over="raise", invalid="raise"):
        scale = np.maximum(np.asarray(q95)-np.asarray(q05), EPS_W)**alpha_norm
    if not np.isfinite(scale).all() or np.any(scale <= 0):
        raise ValueError("Normalization scale must be finite and positive")
    return scale


def _normalized_scores(q05, q95, y, alpha_norm=1.0):
    return _standard_scores(q05, q95, y)/_scale(q05, q95, alpha_norm)


def conformal_rank(n, alpha):
    _validate_alpha(alpha)
    if not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError("Calibration set must be nonempty")
    # Decimal arithmetic avoids ceil(3.0000000000000004) for nominal decimal alpha.
    return int((Decimal(int(n)+1)*(Decimal(1)-Decimal(str(alpha)))).to_integral_value(rounding=ROUND_CEILING))


def _exact_conformal_quantile(scores, alpha):
    values = np.asarray(scores, dtype=float)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all() or np.any(values < 0):
        raise ValueError("Require nonempty finite nonnegative conformal scores")
    k = conformal_rank(len(values), alpha)
    return float("inf") if k > len(values) else float(np.partition(values, k-1)[k-1])


def build_intervals(q05, q95, q_hat, alpha_norm=0.0):
    scale = _scale(q05, q95, alpha_norm)
    if not np.isscalar(q_hat) or np.isnan(q_hat) or q_hat < 0:
        raise ValueError("q_hat must be nonnegative, allowing positive infinity")
    lower = np.asarray(q05, dtype=float)-q_hat*scale
    upper = np.asarray(q95, dtype=float)+q_hat*scale
    return lower, upper, np.clip(lower, 0, RUL_CAP), np.clip(upper, 0, RUL_CAP)


def interval_components(y_true, lower, upper, alpha=ALPHA):
    _validate_alpha(alpha)
    lower, upper, y = _validate_vectors(lower, upper, y_true)
    width = upper-lower
    lower_penalty = (2/alpha)*np.maximum(lower-y, 0)
    upper_penalty = (2/alpha)*np.maximum(y-upper, 0)
    return {"covered": (lower <= y) & (y <= upper), "width": width,
            "lower_miss": y < lower, "upper_miss": y > upper,
            "lower_penalty": lower_penalty, "upper_penalty": upper_penalty,
            "winkler": width+lower_penalty+upper_penalty}


def compute_winkler_score(y_true, lower, upper, alpha=ALPHA):
    return float(interval_components(y_true, lower, upper, alpha)["winkler"].mean())


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _validated_inputs(subset, seed):
    """Reconstruct sampling, ground truth and regime labels independently of predictions."""
    import joblib
    from src.data.preprocessing import SELECTED_SENSOR_COLUMNS, SETTING_COLUMNS, load_raw_cmapss
    from src.evaluation.verify_benchmark import notebook_definitions

    train, test, rul = load_raw_cmapss(PROJECT_ROOT/"data/raw/cmapss", subset)
    train["RUL_raw"] = train.RUL
    checkpoint_dir = PROJECT_ROOT/"results/final_evaluation_v3/checkpoints"
    pre_path = checkpoint_dir/f"{subset}_seed_{seed}_preprocessing.joblib"
    saved = joblib.load(pre_path)
    if (saved["subset"], saved["seed"]) != (subset, seed):
        raise ValueError("Saved split identity mismatch")
    if saved["config"]["window_size"] != 30 or saved["config"]["rul_cap"] != 125:
        raise ValueError("Unexpected saved benchmark configuration")
    # Require the successful complete replay from step 1 and unchanged artifacts.
    stage1 = PROJECT_ROOT/"results/verification_stage1"
    summary = json.loads((stage1/"summary.json").read_text())
    if not summary["pass"] or summary["runs_completed"] != 20:
        raise ValueError("Full 20-run prediction replay prerequisite is not satisfied")
    parity = pd.read_csv(stage1/"prediction_parity.csv")
    prior = json.loads((stage1/f"{subset}_seed_{seed}_training.json").read_text())
    for path, key in [(pre_path, "preprocessing_sha256"),
                      (checkpoint_dir/f"{subset}_seed_{seed}_model.pt", "checkpoint_sha256"),
                      (PROJECT_ROOT/f"data/raw/cmapss/train_{subset}.txt", "training_data_sha256")]:
        if sha256(path) != prior[key]:
            raise ValueError(f"Artifact changed since step-1 replay: {path}")
    np.testing.assert_array_equal(saved["model_engines"], prior["model_engines"])
    np.testing.assert_array_equal(saved["calibration_engines"], prior["calibration_engines"])
    model_ids, cal_ids = set(saved["model_engines"]), set(saved["calibration_engines"])
    if model_ids & cal_ids or model_ids | cal_ids != set(train.engine_id.unique()):
        raise ValueError("Invalid saved engine partition")
    cal = pd.read_csv(CALIBRATION/f"{subset}_seed_{seed}_calibration.csv")
    pred = pd.read_csv(RESULTS_EXACT/f"{subset}_seed_{seed}_predictions.csv")
    for split, path in [("calibration", CALIBRATION/f"{subset}_seed_{seed}_calibration.csv"),
                        ("test", RESULTS_EXACT/f"{subset}_seed_{seed}_predictions.csv")]:
        checks = parity[(parity.Subset == subset) & (parity.Seed == seed)
                        & (parity.Source == "final_evaluation_v3_exact_conformal") & (parity.Split == split)]
        if len(checks) != 4 or not checks.Pass.all() or not (checks.PredictionFileSHA256 == sha256(path)).all():
            raise ValueError("Prediction file differs from the verified replay")
    historical, _ = notebook_definitions()
    cal_train = train[train.engine_id.isin(cal_ids)]
    reference = historical["create_calibration_sequences"](cal_train, SELECTED_SENSOR_COLUMNS, 30, 125, seed)
    test_reference = historical["create_official_test_sequences"](test, rul, SELECTED_SENSOR_COLUMNS, 30, 125)
    for rows, reference in [(cal, reference), (pred, test_reference)]:
        if not rows.engine_id.is_unique:
            raise ValueError("Each engine must contribute exactly one endpoint")
        for column, key in [("engine_id", "engine_id"), ("cycle", "cycle"),
                            ("true_RUL_raw", "raw_rul"), ("true_RUL_clipped", "clipped_rul")]:
            np.testing.assert_array_equal(rows[column], reference[key])
        _validate_vectors(rows.q05_raw, rows.q95_raw, rows.true_RUL_clipped)
        if not rows.true_RUL_clipped.between(0, RUL_CAP).all():
            raise ValueError("Primary target is outside the capped domain")
    np.testing.assert_array_equal(pred.padded_cycles, test_reference["padded_cycles"])
    if set(cal.engine_id) != cal_ids:
        raise ValueError("Calibration membership does not match saved engine split")
    pre = saved["preprocessor"]
    sampling = []
    for split, raw, rows in [("calibration", cal_train, cal), ("test", test, pred)]:
        lookup = raw.set_index(["engine_id", "cycle"])
        last = lookup.loc[list(zip(rows.engine_id, rows.cycle))]
        settings = pre["setting_scaler"].transform(last[SETTING_COLUMNS].astype("float64"))
        regimes = np.zeros(len(rows), dtype=int) if pre["n_regimes"] == 1 else pre["kmeans"].predict(settings)
        for i, row in enumerate(rows.itertuples()):
            sampling.append({"Subset": subset, "Seed": seed, "Split": split,
                             "engine_id": row.engine_id, "cycle": row.cycle,
                             "true_RUL_raw": row.true_RUL_raw, "true_RUL_clipped": row.true_RUL_clipped,
                             "raw_above_cap": row.true_RUL_raw > RUL_CAP, "near_failure": row.true_RUL_raw <= 30,
                             "padded_cycles": int(max(30-row.cycle, 0)), "last_regime": int(regimes[i])})
    return cal, pred, pd.DataFrame(sampling)


def evaluate_run(subset, seed, alpha_norm=1.0, artifact_dir=None):
    cal, pred, sampling = _validated_inputs(subset, seed)
    q05, q95, y = pred.q05_raw.to_numpy(), pred.q95_raw.to_numpy(), pred.true_RUL_clipped.to_numpy()
    cal_scores = _standard_scores(cal.q05_raw, cal.q95_raw, cal.true_RUL_clipped)
    cal_normalized = _normalized_scores(cal.q05_raw, cal.q95_raw, cal.true_RUL_clipped, alpha_norm)
    cutoffs = {"exact": _exact_conformal_quantile(cal_scores, ALPHA),
               "adaptive": _exact_conformal_quantile(cal_normalized, ALPHA)}
    row = {"Subset": subset, "Seed": seed, "N_cal": len(cal), "N_test": len(pred),
           "K_exact": conformal_rank(len(cal), ALPHA), "Alpha": ALPHA, "Normalization_power": alpha_norm,
           "Q_hat_exact": cutoffs["exact"], "Q_hat_adaptive": cutoffs["adaptive"],
           "Test_raw_above_cap": int((pred.true_RUL_raw > RUL_CAP).sum()),
           "Calibration_raw_above_cap": int((cal.true_RUL_raw > RUL_CAP).sum())}
    per_engine = pred[["engine_id", "cycle", "true_RUL_raw", "true_RUL_clipped", "q05_raw", "q50_raw", "q95_raw"]].copy()
    strata = []
    test_sampling = sampling[sampling.Split == "test"].reset_index(drop=True)
    for method, power in [("exact", 0.0), ("adaptive", alpha_norm)]:
        lower_raw, upper_raw, lower, upper = build_intervals(q05, q95, cutoffs[method], power)
        components = interval_components(y, lower, upper)
        # Projection to the target domain must not lose any previously covered bounded target.
        before_covered = (lower_raw <= y) & (y <= upper_raw)
        if np.any(before_covered & ~components["covered"]):
            raise RuntimeError("Clipping lost coverage of a capped target")
        for name, value in [("lower_unclipped", lower_raw), ("upper_unclipped", upper_raw),
                            ("lower", lower), ("upper", upper), *components.items()]:
            per_engine[f"{name}_{method}"] = value
        covered_count = int(components["covered"].sum())
        row.update({f"Coverage_{method}": covered_count/len(y),
                    f"Covered_{method}": covered_count, f"Width_{method}": float(components["width"].mean()),
                    f"Winkler_{method}": float(components["winkler"].mean()),
                    f"Lower_misses_{method}": int(components["lower_miss"].sum()),
                    f"Upper_misses_{method}": int(components["upper_miss"].sum()),
                    f"Achieves_90_{method}": bool(covered_count*10 >= len(y)*9),
                    f"Uncapped_diagnostic_coverage_{method}": float(((lower <= pred.true_RUL_raw) & (pred.true_RUL_raw <= upper)).mean())})
        for family, labels in [
            ("raw_RUL_domain", {"within_cap": ~test_sampling.raw_above_cap, "above_cap": test_sampling.raw_above_cap}),
            ("near_failure", {"RUL_le_30": test_sampling.near_failure, "RUL_gt_30": ~test_sampling.near_failure}),
            ("padding", {"padded": test_sampling.padded_cycles > 0, "not_padded": test_sampling.padded_cycles == 0}),
            ("last_regime", {str(i): test_sampling.last_regime == i for i in range(1 if subset in ("FD001", "FD003") else 6)})]:
            for label, mask in labels.items():
                mask = mask.to_numpy()
                n = int(mask.sum())
                strata.append({"Subset": subset, "Seed": seed, "Method": method, "Stratum": family, "Level": label, "N": n,
                               "Covered": int(components["covered"][mask].sum()),
                               "Coverage": float(components["covered"][mask].mean()) if n else np.nan,
                               "Width": float(components["width"][mask].mean()) if n else np.nan,
                               "Winkler": float(components["winkler"][mask].mean()) if n else np.nan})
    for metric in ("Coverage", "Width", "Winkler"):
        delta = row[f"{metric}_adaptive"]-row[f"{metric}_exact"]
        row[f"Delta_{metric}_adaptive_minus_exact"] = delta
    row["Delta_coverage_percentage_points"] = 100*row["Delta_Coverage_adaptive_minus_exact"]
    row["Delta_coverage_relative_percent"] = (100*row["Delta_Coverage_adaptive_minus_exact"]/row["Coverage_exact"]
                                              if row["Coverage_exact"] else np.nan)
    if artifact_dir is not None:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        prefix = f"{subset}_seed_{seed}"
        per_engine.to_csv(artifact_dir/f"{prefix}_intervals.csv", index=False)
        diagnostics = cal[["engine_id", "cycle", "true_RUL_raw", "true_RUL_clipped", "q05_raw", "q95_raw"]].copy()
        diagnostics["score_exact"] = cal_scores
        diagnostics["scale_adaptive"] = _scale(cal.q05_raw, cal.q95_raw, alpha_norm)
        diagnostics["score_adaptive"] = cal_normalized
        diagnostics.to_csv(artifact_dir/f"{prefix}_calibration_scores.csv", index=False)
        sampling.to_csv(artifact_dir/f"{prefix}_sampling.csv", index=False)
        pd.DataFrame(strata).to_csv(artifact_dir/f"{prefix}_strata.csv", index=False)
    return row


def select_output_dir(subset, seed, power):
    if (subset is None) != (seed is None):
        raise ValueError("Specify both subset and seed or neither")
    if subset is not None and (subset not in ALL_SUBSETS or seed not in ALL_SEEDS):
        raise ValueError("Unknown benchmark subset/seed")
    if not np.isfinite(power) or power < 0:
        raise ValueError("Normalization power must be finite and nonnegative")
    root = PROJECT_ROOT/"results/conformal_stage56"
    canonical = subset is None and power == 1.0
    return (root if canonical else root/"diagnostics"/f"{subset or 'all'}_{seed or 'all'}_power_{power:g}"), canonical


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subset", choices=ALL_SUBSETS)
    parser.add_argument("--seed", type=int, choices=ALL_SEEDS)
    parser.add_argument("--alpha-norm", type=float, default=1.0)
    args = parser.parse_args()
    output, canonical = select_output_dir(args.subset, args.seed, args.alpha_norm)
    output.mkdir(parents=True, exist_ok=True)
    protocol = PROJECT_ROOT/"reports/conformal_protocol_stage56.json"
    manifest = {"status": "running", "canonical": canonical, "protocol_sha256": sha256(protocol),
                "normalization_power": args.alpha_norm, "target": "min(raw_RUL,125)",
                "coverage_guarantee_established": False,
                "sampling_limitation": "different calibration eligibility and official-test truncation schemes",
                "source_sha256": {str(p.relative_to(PROJECT_ROOT)): sha256(p) for p in [
                    Path(__file__), PROJECT_ROOT/"src/evaluation/verify_benchmark.py",
                    PROJECT_ROOT/"src/data/preprocessing.py"]},
                "input_sha256": {},
                "external_review": "not performed; deterministic verification is separate"}
    manifest_path = output/"run_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    if canonical:
        for name in ("f2_conformal_adaptive_fixed.csv", "f2_conformal_adaptive.csv",
                     "f0_baseline_full.json", "f0_baseline_smoke.json"):
            original = OUT_DIR/name
            backup = output/f"before_stage56_{name}"
            if original.exists() and not backup.exists():
                shutil.copy2(original, backup)
    runs = [(args.subset, args.seed)] if args.subset else [(s, seed) for s in ALL_SUBSETS for seed in ALL_SEEDS]
    try:
        rows = []
        for subset, seed in runs:
            row = evaluate_run(subset, seed, args.alpha_norm, output)
            rows.append(row)
            paths = [CALIBRATION/f"{subset}_seed_{seed}_calibration.csv",
                     RESULTS_EXACT/f"{subset}_seed_{seed}_predictions.csv",
                     PROJECT_ROOT/f"results/final_evaluation_v3/checkpoints/{subset}_seed_{seed}_preprocessing.joblib"]
            paths.extend(PROJECT_ROOT/f"data/raw/cmapss/{kind}_{subset}.txt" for kind in ("train", "test", "RUL"))
            manifest["input_sha256"].update({str(p.relative_to(PROJECT_ROOT)): sha256(p) for p in paths})
            print(f"{subset} {seed}: coverage {row['Coverage_exact']:.4f} -> {row['Coverage_adaptive']:.4f}; "
                  f"Winkler {row['Winkler_exact']:.4f} -> {row['Winkler_adaptive']:.4f}", flush=True)
        df = pd.DataFrame(rows)
        df.to_csv(output/"per_run.csv", index=False)
        summaries = []
        for subset, group in df.groupby("Subset"):
            entry = {"Subset": subset, "N_runs": len(group)}
            for method in ("exact", "adaptive"):
                entry[f"Runs_ge90_{method}"] = int(group[f"Achieves_90_{method}"].sum())
                for metric in ("Coverage", "Width", "Winkler"):
                    entry[f"{metric}_{method}_mean"] = group[f"{metric}_{method}"].mean()
                    entry[f"{metric}_{method}_std"] = group[f"{metric}_{method}"].std(ddof=1)
            for metric in ("Coverage", "Width", "Winkler"):
                values = group[f"Delta_{metric}_adaptive_minus_exact"]
                entry[f"Delta_{metric}_mean"] = values.mean()
                entry[f"Delta_{metric}_std"] = values.std(ddof=1)
            entry["Adaptive_Winkler_better_runs"] = int((group.Winkler_adaptive < group.Winkler_exact).sum())
            entry["Adaptive_Winkler_worse_runs"] = int((group.Winkler_adaptive > group.Winkler_exact).sum())
            summaries.append(entry)
        pd.DataFrame(summaries).to_csv(output/"summary.csv", index=False)
        sampling = pd.concat([pd.read_csv(output/f"{s}_seed_{seed}_sampling.csv") for s, seed in runs], ignore_index=True)
        sampling_summary = sampling.groupby(["Subset", "Seed", "Split"]).agg(
            N=("engine_id", "size"), Raw_RUL_min=("true_RUL_raw", "min"), Raw_RUL_max=("true_RUL_raw", "max"),
            N_raw_above_cap=("raw_above_cap", "sum"), N_near_failure=("near_failure", "sum"),
            N_padded=("padded_cycles", lambda x: int((x > 0).sum()))).reset_index()
        sampling_summary.to_csv(output/"sampling_summary.csv", index=False)
        if canonical:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            df.to_csv(OUT_DIR/"f2_conformal_adaptive_fixed.csv", index=False)
            df.to_csv(OUT_DIR/"f2_conformal_adaptive.csv", index=False)
        manifest.update({"status": "complete", "runs": len(df),
                         "runs_ge90_exact": int(df.Achieves_90_exact.sum()),
                         "runs_ge90_adaptive": int(df.Achieves_90_adaptive.sum()),
                         "output_sha256": {p.name: sha256(p) for p in sorted(output.glob("*.csv"))}})
    except Exception as exc:
        manifest.update({"status": "failed", "error": repr(exc)})
        raise
    finally:
        manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Saved {len(df)} runs to {output}")


if __name__ == "__main__":
    main()

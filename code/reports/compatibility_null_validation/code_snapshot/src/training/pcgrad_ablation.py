"""Controlled FD001 single-task / naive multi-task / PCGrad campaign.

Run: python -m src.training.pcgrad_ablation
Smoke: python -m src.training.pcgrad_ablation --smoke
The final official-test evaluation runs only after all 15 models finish training.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import random
import time
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.metrics import f1_score, roc_auc_score, average_precision_score

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.data.preprocessing import (
    RegimeAwarePreprocessor, SELECTED_SENSOR_COLUMNS, SETTING_COLUMNS,
    get_cmapss_column_names, create_sliding_windows, load_raw_cmapss)
from src.models.hybrid_lstm_tcn import HybridLSTMTCNPrognostic
from src.training.pcgrad import PCGradOptimizer
from src.utils.metrics import rmse, mae, r2_score, nasa_score, brier_score

PROTOCOL = ROOT/"reports/pcgrad_protocol_stage78.json"
OUTPUT = ROOT/"results/pcgrad_stage78"
ARMS = ("single_task", "naive_mt", "pcgrad")
SEEDS = (101, 202, 303, 404, 505)
FEATURES = SELECTED_SENSOR_COLUMNS+[f"{c}_scaled" for c in SETTING_COLUMNS]
SHARED_PREFIXES = ("sensor_attention.", "lstm.", "temporal_attention.", "tcn.", "fusion.")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tensor_hash(tensor):
    array = tensor.detach().cpu().contiguous().numpy()
    return hashlib.sha256(str(array.shape).encode()+str(array.dtype).encode()+array.tobytes()).hexdigest()


def state_hash(state):
    digest = hashlib.sha256()
    for name, value in state.items():
        digest.update(name.encode())
        digest.update(tensor_hash(value).encode())
    return digest.hexdigest()


def reset_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def load_preprocessor(saved):
    pre = saved["preprocessor"]
    obj = RegimeAwarePreprocessor(n_regimes=pre["n_regimes"])
    obj.setting_scaler = pre["setting_scaler"]
    obj.kmeans = pre["kmeans"]
    obj.sensor_scalers = pre["sensor_scalers"]
    obj.is_fitted = True
    return obj


def prepare_training(seed, output):
    """Read training data only. No official test inputs/labels are loaded here."""
    checkpoint_dir = ROOT/"results/final_evaluation_v3/checkpoints"
    pre_path = checkpoint_dir/f"FD001_seed_{seed}_preprocessing.joblib"
    saved = joblib.load(pre_path)
    prior_path = ROOT/f"results/verification_stage1/FD001_seed_{seed}_training.json"
    prior = json.loads(prior_path.read_text())
    train_path = ROOT/"data/raw/cmapss/train_FD001.txt"
    assert sha256(train_path) == prior["training_data_sha256"]
    assert sha256(pre_path) == prior["preprocessing_sha256"]
    assert saved["subset"] == "FD001" and saved["seed"] == seed
    np.testing.assert_array_equal(saved["model_engines"], prior["model_engines"])
    np.testing.assert_array_equal(saved["calibration_engines"], prior["calibration_engines"])
    full = pd.read_csv(train_path, sep=r"\s+", header=None, names=get_cmapss_column_names())
    full["RUL"] = full.groupby("engine_id").cycle.transform("max")-full.cycle
    training = full[full.engine_id.isin(saved["model_engines"])].copy()
    assert not set(training.engine_id) & set(saved["calibration_engines"])
    # Historical benchmark excludes incomplete training windows.
    training = training[training.groupby("engine_id").cycle.transform("size") >= 30]
    scaled = load_preprocessor(saved).transform(training)
    X, y, risk = create_sliding_windows(scaled, FEATURES, window_size=30, rul_cap=125, risk_threshold=30)
    positive, negative = int(risk.sum()), int(len(risk)-risk.sum())
    assert (positive, negative) == (prior["n_positive"], prior["n_negative"])
    weight = float(np.float32(negative/positive))
    assert weight == prior["w_pos_train_float32"]
    tensors = (torch.from_numpy(X), torch.from_numpy(y).unsqueeze(1), torch.from_numpy(risk).unsqueeze(1))
    endpoints = []
    for engine_id, frame in training.groupby("engine_id", sort=False):
        for row in frame.sort_values("cycle").iloc[29:].itertuples():
            endpoints.append((engine_id, row.cycle))
    metadata = {"seed": seed, "subset": "FD001", "model_engines": saved["model_engines"].tolist(),
                "calibration_engines": saved["calibration_engines"].tolist(),
                "N_train": len(y), "N_positive": positive, "N_negative": negative,
                "pos_weight": weight, "train_data_sha256": sha256(train_path),
                "preprocessing_sha256": sha256(pre_path),
                "X_sha256": tensor_hash(tensors[0]), "y_sha256": tensor_hash(tensors[1]),
                "risk_sha256": tensor_hash(tensors[2])}
    output.mkdir(parents=True, exist_ok=True)
    (output/f"seed_{seed}_data.json").write_text(json.dumps(metadata, indent=2))
    pd.DataFrame(endpoints, columns=["engine_id", "cycle"]).to_csv(output/f"seed_{seed}_training_endpoints.csv", index=False)
    return tensors, metadata


def task_losses(outputs, target, risk, pos_weight):
    q05, q50, q95, logit = outputs
    rul_loss = sum(torch.maximum(tau*(target-q), (tau-1)*(target-q)).mean()
                   for tau, q in zip((.05, .5, .95), (q05, q50, q95)))
    risk_loss = .5*F.binary_cross_entropy_with_logits(logit, risk, pos_weight=pos_weight)
    return rul_loss, risk_loss


def permutation_for_epoch(n, seed, epoch):
    return torch.randperm(n, generator=torch.Generator().manual_seed(seed*1000+epoch))


def train_arm(seed, arm, tensors, data_meta, output, protocol, smoke=False):
    arm_dir = output/f"seed_{seed}"/arm
    arm_dir.mkdir(parents=True, exist_ok=True)
    final_path = arm_dir/"final.pt"
    if final_path.exists():
        completed = torch.load(final_path, weights_only=True)
        if completed["protocol_sha256"] != sha256(PROTOCOL):
            raise ValueError("Completed checkpoint protocol differs")
        print(f"{seed} {arm}: final checkpoint already saved", flush=True)
        return final_path
    reset_seed(seed)
    training_started_utc = datetime.now(timezone.utc).isoformat()
    model = HybridLSTMTCNPrognostic().train()
    initial = {k: v.detach().clone() for k, v in model.state_dict().items()}
    initial_hash = state_hash(initial)
    initial_path = output/f"seed_{seed}_initial.pt"
    if initial_path.exists():
        assert state_hash(torch.load(initial_path, weights_only=True)["model_state_dict"]) == initial_hash
    else:
        torch.save({"model_state_dict": initial, "seed": seed, "state_sha256": initial_hash}, initial_path)
    assert sum(p.numel() for p in model.parameters()) == 115095
    optimizer = torch.optim.AdamW(model.parameters(), lr=protocol["optimizer"]["lr"],
                                 weight_decay=protocol["optimizer"]["weight_decay"],
                                 betas=tuple(protocol["optimizer"]["betas"]), eps=protocol["optimizer"]["eps"])
    shared = [p for name, p in model.named_parameters() if name.startswith(SHARED_PREFIXES)]
    wrapper = PCGradOptimizer(optimizer, shared_params=shared, reduction="sum", seed=seed)
    x, y, risk = tensors
    if smoke:
        x, y, risk = x[:256], y[:256], risk[:256]
    pos_weight = torch.tensor([data_meta["pos_weight"]], dtype=torch.float32)
    epochs = 1 if smoke else protocol["epochs"]
    history, start_epoch, total_steps = [], 0, 0
    progress_path = arm_dir/"progress.pt"
    if progress_path.exists():
        progress = torch.load(progress_path, weights_only=True)
        assert progress["protocol_sha256"] == sha256(PROTOCOL)
        model.load_state_dict(progress["model_state_dict"], strict=True)
        optimizer.load_state_dict(progress["optimizer_state_dict"])
        history = progress["history"]
        start_epoch = progress["epochs_completed"]
        total_steps = progress["total_steps"]
        torch.set_rng_state(progress["torch_rng_state"])
    parameters = list(model.parameters())
    names = [name for name, _ in model.named_parameters()]
    for epoch in range(start_epoch, epochs):
        started = time.perf_counter()
        order = permutation_for_epoch(len(x), seed, epoch)
        rng_digest = hashlib.sha256()
        losses_rul, losses_risk, batch_sizes = [], [], []
        stats, clipped_norms = [], []
        for begin in range(0, len(order), protocol["batch_size"]):
            indices = order[begin:begin+protocol["batch_size"]]
            rng_state = torch.get_rng_state()
            rng_digest.update(rng_state.numpy().tobytes())
            optimizer.zero_grad(set_to_none=True)
            outputs = model(x[indices])
            rul_loss, risk_loss = task_losses(outputs, y[indices], risk[indices], pos_weight)
            if arm == "single_task":
                rul_loss.backward()
            else:
                first_witness = total_steps == 0
                wrapper.pc_backward([rul_loss, risk_loss], project=arm == "pcgrad", capture=first_witness)
                stats.append(wrapper.last_stats.copy())
                if first_witness:
                    witness = wrapper.last_witness
                    witness.update({"seed": seed, "arm": arm, "parameter_names": names,
                                    "batch_indices": indices.clone(), "torch_rng_before_forward": rng_state.clone(),
                                    "rul_loss": float(rul_loss.detach()), "risk_loss": float(risk_loss.detach()),
                                    "initial_state_sha256": initial_hash})
                    torch.save(witness, arm_dir/"first_step_gradients.pt")
            norm = torch.nn.utils.clip_grad_norm_(parameters, protocol["gradient_clip_global_norm"],
                                                  error_if_nonfinite=True)
            clipped_norms.append(float(norm))
            optimizer.step()
            losses_rul.append(float(rul_loss.detach()))
            losses_risk.append(float(risk_loss.detach()) if arm != "single_task" else float("nan"))
            batch_sizes.append(len(indices))
            total_steps += 1
        record = {"Epoch": epoch+1, "Steps": len(batch_sizes), "Samples": sum(batch_sizes),
                  "RUL_loss": float(np.average(losses_rul, weights=batch_sizes)),
                  "Weighted_risk_loss": (float(np.average(losses_risk, weights=batch_sizes))
                                         if arm != "single_task" else None),
                  "Conflict_steps": sum(s["conflict"] for s in stats) if stats else None,
                  "Conflict_rate": float(np.mean([s["conflict"] for s in stats])) if stats else None,
                  "Mean_task_cosine": float(np.mean([s["cosine"] for s in stats])) if stats else None,
                  "Mean_rul_gradient_norm": float(np.mean([s["task1_norm"] for s in stats])) if stats else None,
                  "Mean_weighted_risk_gradient_norm": float(np.mean([s["task2_norm"] for s in stats])) if stats else None,
                  "Mean_preclip_gradient_norm": float(np.mean(clipped_norms)),
                  "Clipped_steps": sum(n > protocol["gradient_clip_global_norm"] for n in clipped_norms),
                  "Permutation_sha256": tensor_hash(order), "Torch_rng_stream_sha256": rng_digest.hexdigest(),
                  "State_sha256": state_hash(model.state_dict()), "Seconds": time.perf_counter()-started}
        history.append(record)
        pd.DataFrame(history).to_csv(arm_dir/"history.csv", index=False)
        torch.save({"model_state_dict": model.state_dict(), "optimizer_state_dict": optimizer.state_dict(),
                    "history": history, "epochs_completed": epoch+1, "total_steps": total_steps,
                    "torch_rng_state": torch.get_rng_state(), "protocol_sha256": sha256(PROTOCOL)}, progress_path)
        print(f"{seed} {arm} epoch {epoch+1:02d}/{epochs}: rul={record['RUL_loss']:.4f}, "
              f"conflict={record['Conflict_rate']}, {record['Seconds']:.1f}s", flush=True)
    if arm == "single_task":
        for name, value in model.state_dict().items():
            if name.startswith("risk_head."):
                assert torch.equal(value, initial[name]), "Unused risk head unexpectedly updated"
    torch.save({"model_state_dict": model.state_dict(), "seed": seed, "arm": arm,
                "subset": "FD001", "protocol_sha256": sha256(PROTOCOL),
                "initial_state_sha256": initial_hash, "final_state_sha256": state_hash(model.state_dict()),
                "epochs": epochs, "steps": total_steps, "N_train": len(x), "pos_weight": data_meta["pos_weight"],
                "data_sha256": data_meta["X_sha256"], "smoke": smoke,
                "train_seconds": sum(h["Seconds"] for h in history)}, final_path)
    timing = {"started_utc": training_started_utc, "finished_utc": datetime.now(timezone.utc).isoformat()}
    (arm_dir/"timing.json").write_text(json.dumps(timing, indent=2))
    return final_path


def paired_control_checks(output, seeds, smoke=False):
    checks = []
    for seed in seeds:
        states = [torch.load(output/f"seed_{seed}"/arm/"final.pt", weights_only=True) for arm in ARMS]
        for key in ("initial_state_sha256", "epochs", "steps", "N_train", "data_sha256", "pos_weight"):
            assert len({s[key] for s in states}) == 1, f"Pairing mismatch: {seed}/{key}"
        histories = [pd.read_csv(output/f"seed_{seed}"/arm/"history.csv") for arm in ARMS]
        for column in ("Permutation_sha256", "Torch_rng_stream_sha256", "Steps", "Samples"):
            for other in histories[1:]:
                np.testing.assert_array_equal(histories[0][column], other[column])
        assert len(histories[0]) == (1 if smoke else 16)
        checks.append({"Seed": seed, "Initial_state_equal": True, "Data_equal": True,
                       "Minibatch_order_equal": True, "Dropout_rng_equal": True,
                       "Epochs": len(histories[0]), "Steps": states[0]["steps"]})
    pd.DataFrame(checks).to_csv(output/"paired_controls.csv", index=False)


def train_seed(seed, output, protocol, smoke=False):
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    tensors, data_meta = prepare_training(seed, output)
    for arm in ARMS:
        train_arm(seed, arm, tensors, data_meta, output, protocol, smoke)
    return seed


def configure_worker():
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)


def evaluate_campaign(output, seeds):
    """This is the only campaign function that reads official-test labels."""
    _, test, true_rul = load_raw_cmapss(ROOT/"data/raw/cmapss", "FD001")
    rows = []
    for seed in seeds:
        saved = joblib.load(ROOT/f"results/final_evaluation_v3/checkpoints/FD001_seed_{seed}_preprocessing.joblib")
        scaled = load_preprocessor(saved).transform(test)
        x, target, risk = create_sliding_windows(scaled, FEATURES, is_test=True, test_rul_df=true_rul)
        engine_ids = test.engine_id.unique()
        endpoints = test.groupby("engine_id", sort=False).cycle.max().to_numpy()
        for arm in ARMS:
            final_path = output/f"seed_{seed}"/arm/"final.pt"
            ckpt = torch.load(final_path, weights_only=True)
            assert ckpt["epochs"] == 16 and not ckpt["smoke"]
            model = HybridLSTMTCNPrognostic().eval()
            model.load_state_dict(ckpt["model_state_dict"], strict=True)
            with torch.no_grad():
                q05, q50, q95, logits = model(torch.from_numpy(x))
            quantiles = np.column_stack([q.numpy().ravel() for q in (q05, q50, q95)])
            prediction = np.clip(quantiles[:, 1], 0, 125)
            probs = torch.sigmoid(logits).numpy().ravel() if arm != "single_task" else np.full(len(target), np.nan)
            raw_target = true_rul.RUL.to_numpy()
            frame = pd.DataFrame({"engine_id": engine_ids, "cycle": endpoints, "true_RUL_raw": raw_target,
                                  "true_RUL_clipped": target, "risk_target": risk.astype(int),
                                  "q05": quantiles[:, 0], "q50": quantiles[:, 1], "q95": quantiles[:, 2],
                                  "predicted_RUL": prediction, "risk_probability": probs})
            frame.to_csv(output/f"FD001_seed_{seed}_{arm}_predictions.csv", index=False)
            y64 = target.astype(np.float64)
            p64 = prediction.astype(np.float64)
            pinball = sum(np.maximum(tau*(y64-quantiles[:, j]), (tau-1)*(y64-quantiles[:, j])).mean()
                          for j, tau in enumerate((.05, .5, .95)))
            row = {"Subset": "FD001", "Seed": seed, "Arm": arm, "N_test": len(target),
                   "RMSE": rmse(y64, p64), "MAE": mae(y64, p64), "R2": r2_score(y64, p64),
                   "NASA_total": nasa_score(y64, p64), "NASA_mean": nasa_score(y64, p64)/len(target),
                   "Pinball_sum": float(pinball), "Risk_F1": (float(f1_score(risk, probs >= .5, zero_division=0))
                                                            if arm != "single_task" else None),
                   "Risk_AUC": float(roc_auc_score(risk, probs)) if arm != "single_task" else None,
                   "Risk_AP": float(average_precision_score(risk, probs)) if arm != "single_task" else None,
                   "Risk_Brier": brier_score(risk, probs) if arm != "single_task" else None,
                   "Train_seconds": ckpt["train_seconds"], "Epochs": ckpt["epochs"], "Steps": ckpt["steps"],
                   "Checkpoint_sha256": sha256(final_path)}
            rows.append(row)
    frame = pd.DataFrame(rows)
    frame.to_csv(output/"per_run.csv", index=False)
    metrics = ["RMSE", "MAE", "R2", "NASA_total", "NASA_mean", "Pinball_sum", "Risk_F1", "Risk_AUC", "Risk_AP", "Risk_Brier", "Train_seconds"]
    summary = []
    for arm, group in frame.groupby("Arm"):
        for metric in metrics:
            summary.append({"Arm": arm, "Metric": metric, "N": int(group[metric].notna().sum()),
                            "Mean": group[metric].mean(), "Std": group[metric].std(ddof=1)})
    pd.DataFrame(summary).to_csv(output/"summary.csv", index=False)
    differences = []
    for seed in seeds:
        block = frame[frame.Seed == seed].set_index("Arm")
        for a, b in [("pcgrad", "naive_mt"), ("naive_mt", "single_task"), ("pcgrad", "single_task")]:
            for metric in metrics:
                first, second = block.loc[a, metric], block.loc[b, metric]
                if pd.notna(first) and pd.notna(second):
                    differences.append({"Seed": seed, "Comparison": f"{a}_minus_{b}", "Metric": metric,
                                        "Difference": float(first-second)})
    differences = pd.DataFrame(differences)
    differences.to_csv(output/"paired_differences.csv", index=False)
    differences.groupby(["Comparison", "Metric"]).Difference.agg(["mean", "std", "count"]).reset_index().to_csv(
        output/"paired_summary.csv", index=False)
    return frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    protocol = json.loads(PROTOCOL.read_text())
    assert protocol["epochs"] == 16 and protocol["batch_size"] == 128
    output = OUTPUT/"diagnostics"/"spine" if args.smoke else OUTPUT
    output.mkdir(parents=True, exist_ok=True)
    sources = [Path(__file__), ROOT/"src/training/pcgrad.py", ROOT/"src/models/hybrid_lstm_tcn.py",
               ROOT/"src/data/preprocessing.py", ROOT/"src/utils/metrics.py"]
    provenance = {"protocol_sha256": sha256(PROTOCOL),
                  "source_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in sources}}
    manifest_path = output/"run_manifest.json"
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text())
        if any(old.get(k) != v for k, v in provenance.items()):
            raise ValueError("Existing campaign source/protocol differs; preserve it and use a new campaign directory")
        if old["status"] in ("complete", "smoke_complete"):
            print("Campaign already complete; use the verification script to check saved results.")
            return
    manifest = {**provenance, "status": "training", "smoke": args.smoke,
                "python": platform.python_version(), "pytorch": str(torch.__version__),
                "device": "cpu", "threads": 1, "interop_threads": 1, "platform": platform.platform(),
                "seed_workers": 1 if args.smoke else 3,
                "started_utc": datetime.now(timezone.utc).isoformat(),
                "evaluation_started_after_all_training": False, "external_review": "not performed"}
    manifest_path.write_text(json.dumps(manifest, indent=2))
    seeds = SEEDS[:1] if args.smoke else SEEDS
    try:
        if args.smoke:
            train_seed(seeds[0], output, protocol, smoke=True)
        else:
            with ProcessPoolExecutor(max_workers=3, initializer=configure_worker) as workers:
                pending = [workers.submit(train_seed, seed, output, protocol) for seed in seeds]
                for result in as_completed(pending):
                    print(f"Completed training for seed {result.result()}", flush=True)
        paired_control_checks(output, seeds, args.smoke)
        manifest["training_checkpoints_complete"] = len(seeds)*len(ARMS)
        manifest_path.write_text(json.dumps(manifest, indent=2))
        if args.smoke:
            manifest["status"] = "smoke_complete"
        else:
            manifest.update({"status": "evaluating", "evaluation_started_after_all_training": True})
            manifest["evaluation_started_utc"] = datetime.now(timezone.utc).isoformat()
            manifest_path.write_text(json.dumps(manifest, indent=2))
            results = evaluate_campaign(output, seeds)
            manifest.update({"status": "complete", "runs": len(results),
                             "input_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in [
                                 ROOT/"data/raw/cmapss/train_FD001.txt", ROOT/"data/raw/cmapss/test_FD001.txt",
                                 ROOT/"data/raw/cmapss/RUL_FD001.txt"]}})
        manifest["output_sha256"] = {str(p.relative_to(output)): sha256(p)
                                     for p in sorted(output.rglob("*")) if p.is_file()
                                     and p.suffix in (".csv", ".pt", ".json")
                                     and p != manifest_path and "smoke" not in p.relative_to(output).parts
                                     and "diagnostics" not in p.relative_to(output).parts}
    except Exception as exc:
        manifest.update({"status": "failed", "error": repr(exc)})
        raise
    finally:
        manifest["last_updated_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Campaign status: {manifest['status']}; output: {output}", flush=True)


if __name__ == "__main__":
    main()

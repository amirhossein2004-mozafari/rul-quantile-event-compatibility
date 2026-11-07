"""
src/evaluation/risk_calibration.py
====================================
F1 — Near-Failure Risk Calibration via Exact Training-Prior Shift and
     Held-Out Temperature Scaling.

Exact Training Weight Formulation
---------------------------------
The risk classification head is trained using BCEWithLogitsLoss with positive-class
loss weight:
    w_pos,train = N_neg,train / N_pos,train
computed over all sliding windows of length 30 on the 80% model-training engines
for that specific subset and random seed.

At the population optimum of weighted BCE, this weighting produces a logit
shift of +ln(w_pos,train). A finite fitted network need not satisfy that identity:
    r_cal = r_t - ln(w_pos,train)

Four Evaluated Calibration Modes:
  (a) Raw Uncalibrated:                p_raw   = sigmoid(r_t)
  (b) Analytic Training-Prior Shift:   p_bayes = sigmoid(r_t - ln(w_pos,train))
  (c) Held-Out Temperature Scaling:    p_temp  = sigmoid(r_t / T)  [T fitted on held-out cal]
  (d) Prior-Shift + Temperature: p_shift_temp = sigmoid((r_t - ln(w_pos,train)) / T_shift)
                                [T_shift fitted on held-out cal after prior shift]

The fourth method has one fitted parameter, not the two free parameters of
affine Platt scaling. Stratified engine folds provide calibration-only OOF
diagnostics. Official-test predictions use a final refit on all calibration
engines. Neither test scores nor OOF scores select the reported methods.

Outputs:
  - results/implement_stage/f1_risk_calibration_fixed.csv
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from scipy.optimize import minimize_scalar
from scipy.special import expit
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import StratifiedKFold, train_test_split

PROJECT_ROOT  = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.preprocessing import load_raw_cmapss

RESULTS_EXACT = PROJECT_ROOT / "results" / "final_evaluation_v3_exact_conformal"
CALIBRATION   = RESULTS_EXACT / "calibration"
CHECKPOINTS   = PROJECT_ROOT / "results" / "final_evaluation_v3" / "checkpoints"
OUT_DIR       = PROJECT_ROOT / "results" / "implement_stage"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ALL_SUBSETS = ["FD001", "FD002", "FD003", "FD004"]
ALL_SEEDS   = [101, 202, 303, 404, 505]
METHODS = ('Raw', 'Bayes', 'Temp', 'ShiftTemp')
TEMPERATURE_BOUNDS = (0.1, 10.0)


def compute_exact_training_w_pos(data_dir: Path, subset: str, seed: int) -> tuple[float, float, int, int]:
    """
    Compute the exact w_pos,train = N_neg / N_pos from 30-cycle sliding windows
    on the 80% model-training engines for the specified subset and random seed.
    """
    saved_path = CHECKPOINTS / f"{subset}_seed_{seed}_preprocessing.joblib"
    saved = joblib.load(saved_path)
    if saved['subset'] != subset or saved['seed'] != seed:
        raise ValueError(f"Preprocessing metadata mismatch: {saved_path}")
    config = saved['config']
    if config['window_size'] != 30 or config['risk_threshold'] != 30:
        raise ValueError('This benchmark requires window_size=30 and risk_threshold=30')
    train_df, _, _ = load_raw_cmapss(data_dir, subset)
    max_cycles = train_df.groupby("engine_id")["cycle"].max().to_dict()
    train_df["RUL_raw"] = train_df["engine_id"].map(max_cycles) - train_df["cycle"]

    all_engines = train_df["engine_id"].unique()
    model_eng, cal_eng = train_test_split(all_engines, test_size=0.20, random_state=seed)
    if not (np.array_equal(model_eng, saved['model_engines'])
            and np.array_equal(cal_eng, saved['calibration_engines'])):
        raise ValueError(f"Reconstructed split differs from saved training split: {subset}/{seed}")
    m_df = train_df[train_df["engine_id"].isin(saved['model_engines'])]

    n_pos = 0
    n_neg = 0
    for _, edf in m_df.groupby("engine_id"):
        rul_vals = edf.sort_values('cycle')["RUL_raw"].values
        n_cycles = len(rul_vals)
        if n_cycles >= 30:
            for end_idx in range(29, n_cycles):
                if rul_vals[end_idx] <= 30:
                    n_pos += 1
                else:
                    n_neg += 1

    if n_pos == 0 or n_neg == 0:
        raise ValueError(f"Training split must contain both classes: {subset}/{seed}")
    # Original notebook constructs BCE pos_weight as float32.
    w_pos_train = float(np.float32(n_neg / n_pos))
    ln_w_pos = float(np.log(w_pos_train))
    return w_pos_train, ln_w_pos, n_pos, n_neg


def compute_ece(y_true: np.ndarray, probabilities: np.ndarray, n_bins: int = 10) -> float:
    """Expected Calibration Error with 10 equal-width bins."""
    y_true = np.asarray(y_true, dtype=np.float64)
    probabilities = np.asarray(probabilities, dtype=np.float64)
    if (y_true.ndim != 1 or probabilities.shape != y_true.shape or not len(y_true)
            or not np.isfinite(probabilities).all() or not np.isin(y_true, [0, 1]).all()
            or np.any((probabilities < 0) | (probabilities > 1)) or n_bins < 1):
        raise ValueError('ECE requires paired finite probabilities and binary labels')
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        if i == n_bins - 1:
            mask = (probabilities >= edges[i]) & (probabilities <= edges[i + 1])
        else:
            mask = (probabilities >= edges[i]) & (probabilities < edges[i + 1])
        if mask.sum() == 0:
            continue
        observed = y_true[mask].mean()
        confidence = probabilities[mask].mean()
        ece += mask.mean() * abs(observed - confidence)
    return float(ece)


def _validate_logits(logits, labels):
    logits = np.asarray(logits, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.float64)
    if (logits.ndim != 1 or labels.shape != logits.shape or not len(labels)
            or not np.isfinite(logits).all() or not np.isin(labels, [0, 1]).all()):
        raise ValueError('Expected nonempty paired finite logits and binary labels')
    return logits, labels


def binary_nll(logits, labels):
    logits, labels = _validate_logits(logits, labels)
    return float(np.mean(np.logaddexp(0, (1-2*labels)*logits)))


def fit_temperature_details(logits, y_true):
    """Minimize convex NLL in inverse temperature on the predeclared bounds."""
    logits, labels = _validate_logits(logits, y_true)
    if len(np.unique(labels)) != 2:
        raise ValueError('Temperature fitting requires both calibration classes')
    if np.all(logits == 0):
        return {'T': 1.0, 'NLL': binary_nll(logits, labels),
                'at_boundary': False, 'status': 'flat_logits_identity'}
    lower, upper = 1/TEMPERATURE_BOUNDS[1], 1/TEMPERATURE_BOUNDS[0]
    objective = lambda inverse: binary_nll(logits*inverse, labels)
    result = minimize_scalar(objective, bounds=(lower, upper), method='bounded', options={'xatol': 1e-10})
    if not result.success or not np.isfinite(result.fun):
        raise RuntimeError(f'Temperature optimization failed: {result.message}')
    # Explicitly include endpoints and the identity; do not silently miss a boundary optimum.
    inverse = min([lower, upper, 1.0, float(result.x)], key=objective)
    return {'T': float(1/inverse), 'NLL': objective(inverse),
            'at_boundary': bool(inverse in (lower, upper)), 'status': 'bounded_nll_optimum'}


def fit_temperature(logits: np.ndarray, y_true: np.ndarray) -> float:
    return fit_temperature_details(logits, y_true)['T']


def fit_calibrators(cal_logits, y_cal, engine_ids, ln_w_pos, seed):
    """Calibration-only API: official-test inputs/labels cannot enter fitting."""
    logits, labels = _validate_logits(cal_logits, y_cal)
    engines = np.asarray(engine_ids)
    if engines.shape != labels.shape or len(np.unique(engines)) != len(engines):
        raise ValueError('Require one calibration endpoint per engine')
    if not np.isfinite(ln_w_pos):
        raise ValueError('Training-prior offset must be finite')
    shifted = logits-ln_w_pos
    fits = {'Temp': fit_temperature_details(logits, labels),
            'ShiftTemp': fit_temperature_details(shifted, labels)}
    minority = int(np.bincount(labels.astype(int), minlength=2).min())
    n_splits = min(5, minority) if minority >= 2 else 0
    oof = {'Temp': np.full(len(labels), np.nan), 'ShiftTemp': np.full(len(labels), np.nan)}
    assignment = np.full(len(labels), -1, dtype=int)
    folds = []
    if n_splits:
        splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        for fold, (train_idx, valid_idx) in enumerate(splitter.split(logits, labels)):
            assignment[valid_idx] = fold
            record = {'fold': fold, 'train_engine_ids': engines[train_idx].tolist(),
                      'validation_engine_ids': engines[valid_idx].tolist(),
                      'train_positive': int(labels[train_idx].sum()),
                      'train_negative': int(len(train_idx)-labels[train_idx].sum()),
                      'validation_positive': int(labels[valid_idx].sum()),
                      'validation_negative': int(len(valid_idx)-labels[valid_idx].sum())}
            for name, values in [('Temp', logits), ('ShiftTemp', shifted)]:
                fit = fit_temperature_details(values[train_idx], labels[train_idx])
                record[name] = fit
                oof[name][valid_idx] = expit(values[valid_idx]/fit['T'])
            folds.append(record)
        if np.any(assignment < 0) or any(not np.isfinite(v).all() for v in oof.values()):
            raise RuntimeError('Incomplete OOF predictions')
    status = ('five_fold' if n_splits == 5 else 'reduced_folds_minority_count'
              if n_splits else 'unavailable_minority_count_below_two')
    return {'fits': fits, 'n_splits': n_splits, 'cv_status': status,
            'folds': folds, 'assignment': assignment, 'oof': oof,
            'test_rule': 'final refit on all calibration engines; no fold ensemble'}


def apply_calibrators(logits, raw_probabilities, ln_w_pos, fitted):
    logits = np.asarray(logits, dtype=np.float64)
    return {'Raw': np.asarray(raw_probabilities, dtype=np.float64),
            'Bayes': expit(logits-ln_w_pos),
            'Temp': expit(logits/fitted['fits']['Temp']['T']),
            'ShiftTemp': expit((logits-ln_w_pos)/fitted['fits']['ShiftTemp']['T'])}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def evaluate_run(subset: str, seed: int, data_dir: Path, artifact_dir: Path | None = None) -> dict:
    from src.evaluation.risk_inputs import replay_risk_inputs
    pred_path = RESULTS_EXACT/f'{subset}_seed_{seed}_predictions.csv'
    cal_path = CALIBRATION/f'{subset}_seed_{seed}_calibration.csv'
    pred_df, cal_df = pd.read_csv(pred_path), pd.read_csv(cal_path)
    logits = replay_risk_inputs(subset, seed, data_dir, cal_df, pred_df)
    weight, offset, n_pos, n_neg = compute_exact_training_w_pos(data_dir, subset, seed)
    y_cal = (cal_df.true_RUL_raw.to_numpy() <= 30).astype(int)
    # Finish every fit before using the official-test labels for scoring.
    fitted = fit_calibrators(logits['calibration'], y_cal, cal_df.engine_id.to_numpy(), offset, seed)
    probabilities = apply_calibrators(logits['test'], pred_df.risk_probability, offset, fitted)
    y_test = (pred_df.true_RUL_raw.to_numpy() <= 30).astype(int)
    row = {'Subset': subset, 'Seed': seed, 'N_pos_train': n_pos, 'N_neg_train': n_neg,
           'w_pos_train': weight, 'ln_w_pos': offset, 'N_cal': len(y_cal),
           'N_pos_cal': int(y_cal.sum()), 'N_neg_cal': int(len(y_cal)-y_cal.sum()),
           'N_test': len(y_test), 'CV_folds': fitted['n_splits'], 'CV_status': fitted['cv_status'],
           'T_raw': fitted['fits']['Temp']['T'], 'T_shift': fitted['fits']['ShiftTemp']['T'],
           'T_raw_at_boundary': fitted['fits']['Temp']['at_boundary'],
           'T_shift_at_boundary': fitted['fits']['ShiftTemp']['at_boundary']}
    for name, p in probabilities.items():
        row[f'Brier_{name}'] = float(brier_score_loss(y_test, p))
        row[f'ECE_{name}'] = compute_ece(y_test, p)
    for name in ('Temp', 'ShiftTemp'):
        row[f'OOF_Brier_{name}'] = (float(brier_score_loss(y_cal, fitted['oof'][name]))
                                   if fitted['n_splits'] else None)
        row[f'OOF_ECE_{name}'] = (compute_ece(y_cal, fitted['oof'][name])
                                 if fitted['n_splits'] else None)
    if artifact_dir is not None:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        test_out = pred_df[['engine_id', 'cycle', 'true_RUL_raw']].copy()
        test_out['target'] = y_test
        test_out['raw_logit'] = logits['test']
        for name, p in probabilities.items():
            test_out[f'p_{name}'] = p
        test_out.to_csv(artifact_dir/f'{subset}_seed_{seed}_test.csv', index=False)
        cal_out = cal_df[['engine_id', 'cycle', 'true_RUL_raw']].copy()
        cal_out['target'] = y_cal
        cal_out['raw_logit'] = logits['calibration']
        cal_out['p_Raw'] = cal_df.risk_probability
        cal_out['p_Bayes'] = expit(logits['calibration']-offset)
        cal_out['fold'] = fitted['assignment']
        for name, p in fitted['oof'].items():
            cal_out[f'p_OOF_{name}'] = p
        cal_out.to_csv(artifact_dir/f'{subset}_seed_{seed}_calibration_oof.csv', index=False)
        metadata = {key: value for key, value in fitted.items() if key not in ('assignment', 'oof')}
        metadata.update({'subset': subset, 'seed': seed, 'training_weight': weight,
                         'ln_training_weight': offset, 'temperature_bounds': TEMPERATURE_BOUNDS,
                         'fourth_formula': 'sigmoid((raw_logit - ln_training_weight) / T_shift)',
                         'input_sha256': {str(p.relative_to(PROJECT_ROOT)): sha256(p) for p in [
                             pred_path, cal_path, CHECKPOINTS/f'{subset}_seed_{seed}_model.pt',
                             CHECKPOINTS/f'{subset}_seed_{seed}_preprocessing.joblib',
                             data_dir/f'train_{subset}.txt', data_dir/f'test_{subset}.txt',
                             data_dir/f'RUL_{subset}.txt']}})
        (artifact_dir/f'{subset}_seed_{seed}_fits.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return row


def main():
    import torch
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', default='data/raw/cmapss')
    args = parser.parse_args()
    torch.set_num_threads(1)
    output = PROJECT_ROOT/'results/calibration_stage3'
    output.mkdir(parents=True, exist_ok=True)
    protocol = PROJECT_ROOT/'reports/calibration_protocol_stage3.json'
    manifest = {'status': 'running', 'protocol_sha256': sha256(protocol),
                'source_sha256': {str(p.relative_to(PROJECT_ROOT)): sha256(p) for p in [
                    Path(__file__), PROJECT_ROOT/'src/evaluation/risk_inputs.py',
                    PROJECT_ROOT/'src/models/hybrid_lstm_tcn.py', PROJECT_ROOT/'src/data/preprocessing.py']},
                'python': platform.python_version(), 'torch': str(torch.__version__), 'threads': 1,
                'independent_external_review': 'not performed',
                'test_exposure': 'retrospective remediation; previous test results were already inspected'}
    manifest_path = output/'run_manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    legacy = OUT_DIR/'f1_risk_calibration_fixed.csv'
    backup = output/'before_stage3_f1_risk_calibration_fixed.csv'
    if legacy.exists() and not backup.exists():
        shutil.copy2(legacy, backup)
    try:
        rows = []
        for subset in ALL_SUBSETS:
            for seed in ALL_SEEDS:
                row = evaluate_run(subset, seed, PROJECT_ROOT/args.data_dir, output)
                rows.append(row)
                print(f'{subset} {seed}: {row["CV_folds"]} folds, T_raw={row["T_raw"]:.4f}, T_shift={row["T_shift"]:.4f}', flush=True)
        df = pd.DataFrame(rows)
        df.to_csv(output/'per_run.csv', index=False)
        summary = []
        for subset, group in df.groupby('Subset'):
            for method in METHODS:
                summary.append({'Subset': subset, 'Method': method, 'N_runs': len(group),
                                'Brier_mean': group[f'Brier_{method}'].mean(),
                                'Brier_std': group[f'Brier_{method}'].std(ddof=1),
                                'ECE_mean': group[f'ECE_{method}'].mean(),
                                'ECE_std': group[f'ECE_{method}'].std(ddof=1),
                                'Brier_improved_vs_raw': int((group[f'Brier_{method}'] < group.Brier_Raw).sum()),
                                'ECE_improved_vs_raw': int((group[f'ECE_{method}'] < group.ECE_Raw).sum())})
        pd.DataFrame(summary).to_csv(output/'summary.csv', index=False)
        df.to_csv(legacy, index=False)
        manifest.update({'status': 'complete', 'runs': len(df),
                         'output_sha256': {p.name: sha256(p) for p in sorted(output.glob('*.csv'))},
                         'fit_metadata_sha256': {p.name: sha256(p) for p in sorted(output.glob('*_fits.json'))}})
    except Exception as exc:
        manifest.update({'status': 'failed', 'error': repr(exc)})
        raise
    finally:
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f'Saved all 20 runs and summary to {output}')


if __name__ == "__main__":
    main()

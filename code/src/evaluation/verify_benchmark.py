"""Replay the saved 20-run benchmark without fitting or changing original artifacts.

Run: python -m src.evaluation.verify_benchmark
Tolerances are fixed before replay: quantiles atol=1e-3, rtol=1e-5;
risk probabilities atol=1e-5, rtol=1e-5 (float32 CPU/runtime drift).
Notebook evidence uses zero-based cell indices.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split

from src.data.preprocessing import (
    RegimeAwarePreprocessor, SELECTED_SENSOR_COLUMNS, SETTING_COLUMNS,
    load_raw_cmapss,
)
from src.models.hybrid_lstm_tcn import HybridLSTMTCNPrognostic
from src.evaluation.risk_calibration import compute_exact_training_w_pos

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINTS = ROOT / 'results/final_evaluation_v3/checkpoints'
NOTEBOOK = ROOT / 'notebooks/22_final_model_evaluation_v4_exact_conformal.ipynb'
SUBSETS = ('FD001', 'FD002', 'FD003', 'FD004')
SEEDS = (101, 202, 303, 404, 505)
FEATURES = SELECTED_SENSOR_COLUMNS + [f'{c}_scaled' for c in SETTING_COLUMNS]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def notebook_definitions():
    """Read only named historical definitions; never execute notebook top-level runs."""
    wanted = {'transform_regime_aware', 'create_training_sequences',
              'create_calibration_sequences', 'create_official_test_sequences'}
    namespace = {'np': np, 'pd': pd, 'setting_cols': SETTING_COLUMNS}
    evidence = []
    for i, cell in enumerate(json.loads(NOTEBOOK.read_text(encoding='utf-8'))['cells']):
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell['source'])
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if node.name in wanted:
                    exec(compile(ast.Module(body=[node], type_ignores=[]), str(NOTEBOOK), 'exec'), namespace)
                    evidence.append({'cell': i, 'definition': node.name,
                                     'source': ast.get_source_segment(source, node)})
                elif node.name in {'FinalRULModel', 'train_final_model', 'prepare_final_split'}:
                    evidence.append({'cell': i, 'definition': node.name,
                                     'source': ast.get_source_segment(source, node)})
    if not wanted.issubset(namespace):
        raise ValueError('Missing historical notebook definitions')
    return namespace, evidence


def restore_preprocessor(saved):
    obj = RegimeAwarePreprocessor(n_regimes=saved['n_regimes'])
    obj.setting_scaler = saved['setting_scaler']
    obj.kmeans = saved['kmeans']
    obj.sensor_scalers = saved['sensor_scalers']
    obj.is_fitted = True
    return obj


def windows_at_rows(scaled, rows, window_size):
    """Reconstruct each saved endpoint, checking cycle identity and edge padding."""
    groups = {int(k): v.sort_values('cycle') for k, v in scaled.groupby('engine_id')}
    windows = []
    for row in rows.itertuples():
        engine = groups[int(row.engine_id)]
        history = engine[engine['cycle'] <= row.cycle]
        if history.empty or history['cycle'].iloc[-1] != row.cycle:
            raise ValueError(f'Invalid endpoint {row.engine_id}/{row.cycle}')
        values = history[FEATURES].to_numpy(dtype=np.float32)[-window_size:]
        if len(values) < window_size:
            values = np.pad(values, ((window_size-len(values), 0), (0, 0)), mode='edge')
        windows.append(values)
    return np.asarray(windows, dtype=np.float32)


def replay(subset, seed, historical, out_dir):
    checkpoint_path = CHECKPOINTS / f'{subset}_seed_{seed}_model.pt'
    preprocessing_path = CHECKPOINTS / f'{subset}_seed_{seed}_preprocessing.joblib'
    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
    saved = joblib.load(preprocessing_path)
    assert ckpt['subset'] == saved['subset'] == subset
    assert ckpt['seed'] == saved['seed'] == seed
    assert ckpt['config'] == saved['config']
    config = saved['config']
    window = config['window_size']
    cap = config['rul_cap']
    threshold = config['risk_threshold']
    train, test, rul = load_raw_cmapss(ROOT/'data/raw/cmapss', subset)
    train['RUL_raw'] = train['RUL']
    model_ids, cal_ids = train_test_split(train.engine_id.unique(), test_size=.2, random_state=seed)
    np.testing.assert_array_equal(model_ids, saved['model_engines'])
    np.testing.assert_array_equal(cal_ids, saved['calibration_engines'])
    assert not set(model_ids).intersection(cal_ids)
    model_train = train[train.engine_id.isin(model_ids)]
    cal_train = train[train.engine_id.isin(cal_ids)]
    # Count exact eligible endpoints directly, independent of window materialization.
    per_engine = []
    for engine_id, frame in model_train.groupby('engine_id'):
        eligible = frame.sort_values('cycle').iloc[window-1:]
        n_pos = int((eligible.RUL_raw <= threshold).sum())
        per_engine.append({'engine_id': int(engine_id), 'n_positive': n_pos,
                           'n_negative': int(len(eligible)-n_pos)})
    n_pos = sum(e['n_positive'] for e in per_engine)
    n_neg = sum(e['n_negative'] for e in per_engine)
    assert n_pos > 0 and n_neg > 0
    # Use the actual historical sequence generator as a separate reference.
    _, _, original_risk = historical['create_training_sequences'](
        model_train, SELECTED_SENSOR_COLUMNS, window, cap, threshold)
    assert int(original_risk.sum()) == n_pos
    assert len(original_risk) == n_pos+n_neg
    counts = pd.read_csv(ROOT/'results/final_evaluation_v3/all_runs_final_v3.csv')
    run = counts[(counts.Subset == subset) & (counts.Seed == seed)].iloc[0]
    assert int(run.TrainSequences) == n_pos+n_neg
    weight, _, checked_pos, checked_neg = compute_exact_training_w_pos(
        ROOT/'data/raw/cmapss', subset, seed)
    assert (checked_pos, checked_neg) == (n_pos, n_neg)
    assert weight == float(np.float32(n_neg/n_pos))
    manifest = {'subset': subset, 'seed': seed, 'model_engines': model_ids.tolist(),
                'calibration_engines': cal_ids.tolist(), 'window_size': window,
                'risk_threshold': threshold, 'n_positive': n_pos, 'n_negative': n_neg,
                'w_pos_train': n_neg/n_pos,
                'w_pos_train_float32': float(np.float32(n_neg/n_pos)),
                'per_engine': per_engine, 'checkpoint_sha256': sha256(checkpoint_path),
                'preprocessing_sha256': sha256(preprocessing_path),
                'training_data_sha256': sha256(ROOT/f'data/raw/cmapss/train_{subset}.txt'),
                'weight_provenance': 'reconstructed from saved split/config and historical notebook loss; not stored in checkpoint'}
    (out_dir/f'{subset}_seed_{seed}_training.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    pre = restore_preprocessor(saved['preprocessor'])
    model = HybridLSTMTCNPrognostic(input_size=config['features']).eval()
    model.load_state_dict(ckpt['model_state_dict'], strict=True)
    assert sum(p.numel() for p in model.parameters()) == 115095
    rows = []
    for split, raw in [('test', test), ('calibration', cal_train)]:
        scaled = pre.transform(raw)
        reference_scaled = historical['transform_regime_aware'](raw, SELECTED_SENSOR_COLUMNS, saved['preprocessor'])
        np.testing.assert_array_equal(scaled[FEATURES].to_numpy(), reference_scaled[FEATURES].to_numpy())
        if split == 'test':
            ref = historical['create_official_test_sequences'](scaled, rul, FEATURES, window, cap)
        else:
            ref = historical['create_calibration_sequences'](scaled, FEATURES, window, cap, seed)
        for directory in ['final_evaluation_v3', 'final_evaluation_v3_exact_conformal']:
            source = ROOT/'results'/directory
            source = (source/f'{subset}_seed_{seed}_predictions.csv' if split == 'test'
                      else source/'calibration'/f'{subset}_seed_{seed}_calibration.csv')
            stored = pd.read_csv(source)
            np.testing.assert_array_equal(stored.engine_id.to_numpy(), ref['engine_id'])
            np.testing.assert_array_equal(stored.cycle.to_numpy(), ref['cycle'])
            np.testing.assert_array_equal(stored.true_RUL_raw.to_numpy(), ref['raw_rul'])
            np.testing.assert_array_equal(stored.true_RUL_clipped.to_numpy(), ref['clipped_rul'])
            x = windows_at_rows(scaled, stored, window)
            np.testing.assert_array_equal(x, ref['X'])
            with torch.no_grad():
                q05, q50, q95, logits = model(torch.from_numpy(x))
            outputs = {'q05_raw': q05.numpy().ravel(), 'q50_raw': q50.numpy().ravel(),
                       'q95_raw': q95.numpy().ravel(), 'risk_probability': torch.sigmoid(logits).numpy().ravel()}
            for name, predicted in outputs.items():
                target = stored[name].to_numpy()
                atol = 1e-5 if name == 'risk_probability' else 1e-3
                passed = bool(np.allclose(predicted, target, atol=atol, rtol=1e-5))
                rows.append({'Subset': subset, 'Seed': seed, 'Split': split, 'Source': directory,
                             'Output': name, 'N': len(target), 'MaxAbsoluteError': float(np.max(np.abs(predicted-target))),
                             'atol': atol, 'rtol': 1e-5, 'Pass': passed,
                             'PredictionFileSHA256': sha256(source)})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    torch.set_num_threads(1)
    out = ROOT/'results/verification_stage1'
    out.mkdir(parents=True, exist_ok=True)
    historical, evidence = notebook_definitions()
    (out/'notebook_evidence.json').write_text(json.dumps({'notebook_sha256': sha256(NOTEBOOK), 'definitions': evidence}, indent=2), encoding='utf-8')
    rows, failures = [], []
    runs = [(s, seed) for s in SUBSETS for seed in SEEDS]
    if args.smoke:
        runs = runs[:1]
    for subset, seed in runs:
        try:
            result = replay(subset, seed, historical, out)
            rows.extend(result)
            print(f'{subset} {seed}: {sum(r["Pass"] for r in result)}/{len(result)} output checks passed', flush=True)
        except Exception as exc:
            failures.append({'Subset': subset, 'Seed': seed, 'error': repr(exc)})
            print(f'{subset} {seed}: ERROR {exc}', flush=True)
    suffix = '_smoke' if args.smoke else ''
    pd.DataFrame(rows).to_csv(out/f'prediction_parity{suffix}.csv', index=False)
    priors = []
    for subset, seed in runs:
        if any(f['Subset'] == subset and f['Seed'] == seed for f in failures):
            continue
        manifest = json.loads((out/f'{subset}_seed_{seed}_training.json').read_text(encoding='utf-8'))
        priors.append({'Subset': subset, 'Seed': seed, 'N_pos_train': manifest['n_positive'],
                       'N_neg_train': manifest['n_negative'],
                       'w_pos_train': manifest['w_pos_train_float32'],
                       'ln_w_pos': float(np.log(manifest['w_pos_train_float32'])), 'Pass': True})
    pd.DataFrame(priors).to_csv(out/f'training_prior_verification{suffix}.csv', index=False)
    success = bool(rows) and all(r['Pass'] for r in rows) and not failures
    summary = {'pass': success, 'runs_requested': len(runs), 'runs_completed': len(rows)//16,
               'checks': len(rows), 'failures': failures, 'python': platform.python_version(),
               'pytorch': str(torch.__version__), 'threads': torch.get_num_threads(),
               'scope': 'prediction replay and reconstructed weight provenance; no retraining'}
    (out/f'summary{suffix}.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if success else 1)


if __name__ == '__main__':
    main()

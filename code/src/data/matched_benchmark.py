"""Saved-split benchmark reconstruction shared by the stage-9 train/eval entry points."""
import json
from pathlib import Path
import os

import joblib
import numpy as np
import pandas as pd
import torch

from src.data.preprocessing import (
    RegimeAwarePreprocessor, SELECTED_SENSOR_COLUMNS, SETTING_COLUMNS,
    get_cmapss_column_names, create_sliding_windows,
)
from src.training.pcgrad_ablation import sha256, tensor_hash

ROOT = Path(__file__).resolve().parents[2]
FEATURES = SELECTED_SENSOR_COLUMNS+[f'{c}_scaled' for c in SETTING_COLUMNS]


def atomic_json(value, path):
    path = Path(path)
    temporary = path.with_name(path.name+f'.{os.getpid()}.tmp')
    temporary.write_text(json.dumps(value, indent=2), encoding='utf-8')
    os.replace(temporary, path)


def atomic_csv(frame, path):
    path = Path(path)
    temporary = path.with_name(path.name+f'.{os.getpid()}.tmp')
    frame.to_csv(temporary, index=False)
    os.replace(temporary, path)


def atomic_torch(value, path):
    path = Path(path)
    temporary = path.with_name(path.name+f'.{os.getpid()}.tmp')
    torch.save(value, temporary)
    os.replace(temporary, path)


def saved_preprocessing(subset, seed):
    path = ROOT/f'results/final_evaluation_v3/checkpoints/{subset}_seed_{seed}_preprocessing.joblib'
    saved = joblib.load(path)
    prior = json.loads((ROOT/f'results/verification_stage1/{subset}_seed_{seed}_training.json').read_text())
    if sha256(path) != prior['preprocessing_sha256'] or (saved['subset'], saved['seed']) != (subset, seed):
        raise ValueError('Saved preprocessing identity/provenance mismatch')
    np.testing.assert_array_equal(saved['model_engines'], prior['model_engines'])
    np.testing.assert_array_equal(saved['calibration_engines'], prior['calibration_engines'])
    return saved, prior


def restore_preprocessor(saved):
    pre = saved['preprocessor']
    obj = RegimeAwarePreprocessor(n_regimes=pre['n_regimes'])
    obj.setting_scaler, obj.kmeans = pre['setting_scaler'], pre['kmeans']
    obj.sensor_scalers, obj.is_fitted = pre['sensor_scalers'], True
    return obj


def training_data(subset, seed, output):
    """No official-test data or labels are read while constructing training windows."""
    saved, prior = saved_preprocessing(subset, seed)
    path = ROOT/f'data/raw/cmapss/train_{subset}.txt'
    if sha256(path) != prior['training_data_sha256']:
        raise ValueError('Raw training file changed since benchmark verification')
    full = pd.read_csv(path, sep=r'\s+', header=None, names=get_cmapss_column_names())
    full['RUL'] = full.groupby('engine_id').cycle.transform('max')-full.cycle
    frame = full[full.engine_id.isin(saved['model_engines'])].copy()
    frame = frame[frame.groupby('engine_id').cycle.transform('size') >= 30]
    scaled = restore_preprocessor(saved).transform(frame)
    x, y, risk = create_sliding_windows(scaled, FEATURES, 30, 125, 30)
    positive, negative = int(risk.sum()), int(len(risk)-risk.sum())
    assert (positive, negative) == (prior['n_positive'], prior['n_negative'])
    tensors = (torch.from_numpy(x), torch.from_numpy(y).unsqueeze(1), torch.from_numpy(risk).unsqueeze(1))
    metadata = {'subset': subset, 'seed': seed, 'N_train': len(y), 'N_positive': positive,
                'N_negative': negative, 'pos_weight': float(np.float32(negative/positive)),
                'model_engines': saved['model_engines'].tolist(),
                'calibration_engines': saved['calibration_engines'].tolist(),
                'X_sha256': tensor_hash(tensors[0]), 'y_sha256': tensor_hash(tensors[1]),
                'risk_sha256': tensor_hash(tensors[2]),
                'input_sha256': {str(path.relative_to(ROOT)): sha256(path),
                    f'results/final_evaluation_v3/checkpoints/{subset}_seed_{seed}_preprocessing.joblib': prior['preprocessing_sha256']}}
    assert metadata['pos_weight'] == prior['w_pos_train_float32']
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    atomic_json(metadata, output/f'{subset}_seed_{seed}_data.json')
    return tensors, metadata


def calibration_and_test(subset, seed):
    """Reconstruct original held-out endpoints and official final windows after training."""
    saved, _ = saved_preprocessing(subset, seed)
    columns = get_cmapss_column_names()
    train = pd.read_csv(ROOT/f'data/raw/cmapss/train_{subset}.txt', sep=r'\s+', header=None, names=columns)
    test = pd.read_csv(ROOT/f'data/raw/cmapss/test_{subset}.txt', sep=r'\s+', header=None, names=columns)
    rul = pd.read_csv(ROOT/f'data/raw/cmapss/RUL_{subset}.txt', header=None, names=['RUL'])
    train['RUL'] = train.groupby('engine_id').cycle.transform('max')-train.cycle
    cal_rows = pd.read_csv(ROOT/f'results/final_evaluation_v3_exact_conformal/calibration/{subset}_seed_{seed}_calibration.csv')
    if not cal_rows.engine_id.is_unique or set(cal_rows.engine_id) != set(saved['calibration_engines']):
        raise ValueError('Invalid original calibration membership')
    pre = restore_preprocessor(saved)
    cal_scaled = pre.transform(train[train.engine_id.isin(saved['calibration_engines'])])
    groups = {i: g.sort_values('cycle') for i, g in cal_scaled.groupby('engine_id')}
    xs, ys = [], []
    for row in cal_rows.itertuples():
        engine = groups[row.engine_id]
        history = engine[engine.cycle <= row.cycle]
        true = float(engine.cycle.max()-row.cycle)
        if len(history) < 30 or history.cycle.iloc[-1] != row.cycle or not 1 <= true <= 125:
            raise ValueError('Ineligible calibration endpoint')
        if true != row.true_RUL_raw or min(true, 125) != row.true_RUL_clipped:
            raise ValueError('Calibration target mismatch')
        xs.append(history[FEATURES].to_numpy(dtype=np.float32)[-30:])
        ys.append(true)
    cal = {'X': np.asarray(xs, dtype=np.float32), 'raw_y': np.asarray(ys, dtype=np.float32),
           'y': np.minimum(ys, 125).astype(np.float32), 'engine_id': cal_rows.engine_id.to_numpy(),
           'cycle': cal_rows.cycle.to_numpy()}
    test_scaled = pre.transform(test)
    x_test, y_test, _ = create_sliding_windows(test_scaled, FEATURES, 30, 125, 30, is_test=True, test_rul_df=rul)
    official = {'X': x_test, 'raw_y': rul.RUL.to_numpy(dtype=np.float32), 'y': y_test,
                'engine_id': test.engine_id.unique(),
                'cycle': test.groupby('engine_id', sort=False).cycle.max().to_numpy()}
    return cal, official

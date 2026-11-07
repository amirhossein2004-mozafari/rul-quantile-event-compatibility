"""Recover raw risk logits from the verified benchmark, never from clipped probabilities."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import torch

from src.data.preprocessing import (
    RegimeAwarePreprocessor, SELECTED_SENSOR_COLUMNS, SETTING_COLUMNS, load_raw_cmapss,
)
from src.models.hybrid_lstm_tcn import HybridLSTMTCNPrognostic

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINTS = ROOT/'results/final_evaluation_v3/checkpoints'
FEATURES = SELECTED_SENSOR_COLUMNS + [f'{c}_scaled' for c in SETTING_COLUMNS]


def replay_risk_inputs(subset: str, seed: int, data_dir: Path,
                       calibration: pd.DataFrame, test: pd.DataFrame):
    saved = joblib.load(CHECKPOINTS/f'{subset}_seed_{seed}_preprocessing.joblib')
    checkpoint = torch.load(CHECKPOINTS/f'{subset}_seed_{seed}_model.pt', map_location='cpu', weights_only=True)
    if (saved['subset'], saved['seed']) != (subset, seed):
        raise ValueError('Saved preprocessing identity mismatch')
    if (checkpoint['subset'], checkpoint['seed']) != (subset, seed) or checkpoint['config'] != saved['config']:
        raise ValueError('Checkpoint identity/configuration mismatch')
    config = saved['config']
    if config['risk_threshold'] != 30 or config['window_size'] != 30:
        raise ValueError('Unexpected benchmark threshold or window length')
    train, official_test, rul = load_raw_cmapss(data_dir, subset)
    model_ids, cal_ids = set(saved['model_engines']), set(saved['calibration_engines'])
    if model_ids & cal_ids or model_ids | cal_ids != set(train.engine_id.unique()):
        raise ValueError('Invalid saved engine partition')
    if not calibration.engine_id.is_unique or set(calibration.engine_id) != cal_ids:
        raise ValueError('Calibration must contain one endpoint per saved calibration engine')
    if not test.engine_id.is_unique or set(test.engine_id) != set(official_test.engine_id.unique()):
        raise ValueError('Test endpoints do not match official test engines')
    pre = RegimeAwarePreprocessor(n_regimes=saved['preprocessor']['n_regimes'])
    pre.setting_scaler = saved['preprocessor']['setting_scaler']
    pre.kmeans = saved['preprocessor']['kmeans']
    pre.sensor_scalers = saved['preprocessor']['sensor_scalers']
    pre.is_fitted = True
    model = HybridLSTMTCNPrognostic(input_size=config['features']).eval()
    model.load_state_dict(checkpoint['model_state_dict'], strict=True)
    result = {}
    for name, raw, rows in [('calibration', train[train.engine_id.isin(cal_ids)], calibration),
                            ('test', official_test, test)]:
        scaled = pre.transform(raw)
        groups = {int(i): f.sort_values('cycle') for i, f in scaled.groupby('engine_id')}
        windows = []
        for row in rows.itertuples():
            engine = groups[int(row.engine_id)]
            history = engine[engine.cycle <= row.cycle]
            if history.empty or history.cycle.iloc[-1] != row.cycle:
                raise ValueError(f'Unknown endpoint: {name}/{row.engine_id}/{row.cycle}')
            if name == 'test':
                if row.cycle != engine.cycle.iloc[-1]:
                    raise ValueError('Test endpoint is not the last observed cycle')
                true_rul = float(rul.RUL.iloc[int(row.engine_id)-1])
            else:
                true_rul = float(engine.cycle.max()-row.cycle)
                if len(history) < config['window_size'] or not 1 <= true_rul <= config['rul_cap']:
                    raise ValueError('Ineligible calibration endpoint')
            if row.true_RUL_raw != true_rul or row.true_RUL_clipped != min(true_rul, config['rul_cap']):
                raise ValueError('Stored target differs from raw dataset ground truth')
            values = history[FEATURES].to_numpy(dtype=np.float32)[-config['window_size']:]
            if len(values) < config['window_size']:
                values = np.pad(values, ((config['window_size']-len(values), 0), (0, 0)), mode='edge')
            windows.append(values)
        with torch.no_grad():
            q05, q50, q95, logits = model(torch.from_numpy(np.asarray(windows, dtype=np.float32)))
        for col, predicted in [('q05_raw', q05), ('q50_raw', q50), ('q95_raw', q95)]:
            np.testing.assert_allclose(predicted.numpy().ravel(), rows[col], atol=1e-3, rtol=1e-5)
        np.testing.assert_allclose(torch.sigmoid(logits).numpy().ravel(), rows.risk_probability, atol=1e-5, rtol=1e-5)
        result[name] = logits.numpy().ravel().astype(np.float64)
    return result

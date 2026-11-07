"""
src/data/preprocessing.py
=========================
Reusable C-MAPSS data loading, operating-regime clustering,
and sliding-window sequence preparation pipeline.
Matches Sections 3.2 and 3.3 of the turbofan RUL prognostic framework.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Canonical column definitions
SETTING_COLUMNS = ["setting_1", "setting_2", "setting_3"]
ALL_SENSOR_COLUMNS = [f"sensor_{i}" for i in range(1, 22)]

# 15 informative sensors selected after removing invariant/flat sensors (Section 3.2)
SELECTED_SENSOR_COLUMNS = [
    "sensor_2", "sensor_3", "sensor_4", "sensor_6", "sensor_7",
    "sensor_8", "sensor_9", "sensor_11", "sensor_12", "sensor_13",
    "sensor_14", "sensor_15", "sensor_17", "sensor_20", "sensor_21"
]

ALL_FEATURE_COLUMNS = SELECTED_SENSOR_COLUMNS + SETTING_COLUMNS

# Operating regimes per C-MAPSS sub-dataset
N_REGIMES = {
    "FD001": 1,
    "FD002": 6,
    "FD003": 1,
    "FD004": 6,
}

RUL_CAP_DEFAULT = 125
RISK_THRESHOLD_DEFAULT = 30
WINDOW_SIZE_DEFAULT = 30


def get_cmapss_column_names() -> List[str]:
    """Return standard C-MAPSS text file column names."""
    return ["engine_id", "cycle"] + SETTING_COLUMNS + ALL_SENSOR_COLUMNS


def load_raw_cmapss(
    data_dir: Union[str, Path],
    subset: str = "FD001",
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load raw C-MAPSS train, test, and true test RUL files.

    Parameters
    ----------
    data_dir : Path or str
        Directory containing train_{subset}.txt, test_{subset}.txt, RUL_{subset}.txt.
    subset : str
        One of 'FD001', 'FD002', 'FD003', 'FD004'.

    Returns
    -------
    train_df, test_df, test_rul_df
    """
    data_dir = Path(data_dir)
    cols = get_cmapss_column_names()

    train_file = data_dir / f"train_{subset}.txt"
    test_file = data_dir / f"test_{subset}.txt"
    rul_file = data_dir / f"RUL_{subset}.txt"

    if not train_file.exists():
        raise FileNotFoundError(f"Training file not found: {train_file}")
    if not test_file.exists():
        raise FileNotFoundError(f"Test file not found: {test_file}")
    if not rul_file.exists():
        raise FileNotFoundError(f"RUL file not found: {rul_file}")

    train_df = pd.read_csv(train_file, sep=r"\s+", header=None, names=cols)
    test_df = pd.read_csv(test_file, sep=r"\s+", header=None, names=cols)
    test_rul = pd.read_csv(rul_file, sep=r"\s+", header=None, names=["RUL"])

    # Compute ground-truth RUL for training trajectories
    train_df["max_cycle"] = train_df.groupby("engine_id")["cycle"].transform("max")
    train_df["RUL"] = train_df["max_cycle"] - train_df["cycle"]
    train_df["RUL_clipped"] = train_df["RUL"].clip(upper=RUL_CAP_DEFAULT)

    return train_df, test_df, test_rul


class RegimeAwarePreprocessor:
    """
    Operating-regime-aware sensor normalizer matching Section 3.3.

    - Fits StandardScaler on setting variables (only on training engines).
    - Partitions setting space using K-Means (k=6 for FD002/FD004, k=1 for FD001/FD003).
    - Normalizes sensors with regime-specific StandardScaler instances.
    - Prevents data leakage: fit() is strictly executed on training engines only.
    """

    def __init__(
        self,
        n_regimes: int = 1,
        sensor_cols: Optional[List[str]] = None,
        setting_cols: Optional[List[str]] = None,
        seed: int = 42,
    ) -> None:
        self.n_regimes = n_regimes
        self.sensor_cols = sensor_cols or SELECTED_SENSOR_COLUMNS
        self.setting_cols = setting_cols or SETTING_COLUMNS
        self.seed = seed

        self.setting_scaler = StandardScaler()
        self.kmeans: Optional[KMeans] = None
        self.sensor_scalers: Dict[int, StandardScaler] = {}
        self.is_fitted = False

    def fit(self, df: pd.DataFrame) -> "RegimeAwarePreprocessor":
        """Fit setting scaler, K-means clustering, and regime sensor scalers."""
        settings_raw = df[self.setting_cols].astype("float64")
        settings_scaled = self.setting_scaler.fit_transform(settings_raw)

        if self.n_regimes == 1:
            self.kmeans = None
            regime_labels = np.zeros(len(df), dtype=int)
        else:
            self.kmeans = KMeans(
                n_clusters=self.n_regimes,
                random_state=self.seed,
                n_init=20,
            )
            regime_labels = self.kmeans.fit_predict(settings_scaled)

        self.sensor_scalers = {}
        for regime in range(self.n_regimes):
            mask = regime_labels == regime
            scaler = StandardScaler()
            if mask.sum() > 0:
                scaler.fit(df.loc[mask, self.sensor_cols].astype("float64"))
            else:
                scaler.fit(df[self.sensor_cols].astype("float64"))
            self.sensor_scalers[regime] = scaler

        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply regime assignment and normalized sensor scaling."""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before calling transform().")

        out = df.copy()
        for col in self.sensor_cols:
            out[col] = out[col].astype("float64")

        settings_scaled = self.setting_scaler.transform(out[self.setting_cols].astype("float64"))

        if self.n_regimes == 1 or self.kmeans is None:
            regime_labels = np.zeros(len(out), dtype=int)
        else:
            regime_labels = self.kmeans.predict(settings_scaled)

        out["operating_regime"] = regime_labels

        for regime in range(self.n_regimes):
            mask = regime_labels == regime
            if mask.sum() == 0:
                continue
            scaled_sensors = self.sensor_scalers[regime].transform(
                out.loc[mask, self.sensor_cols].astype("float64")
            )
            for j, col in enumerate(self.sensor_cols):
                out.loc[mask, col] = scaled_sensors[:, j]

        for idx, col in enumerate(self.setting_cols):
            out[f"{col}_scaled"] = settings_scaled[:, idx]

        return out

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)


def create_sliding_windows(
    df: pd.DataFrame,
    feature_cols: Optional[List[str]] = None,
    window_size: int = WINDOW_SIZE_DEFAULT,
    rul_cap: int = RUL_CAP_DEFAULT,
    risk_threshold: int = RISK_THRESHOLD_DEFAULT,
    is_test: bool = False,
    test_rul_df: Optional[pd.DataFrame] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate fixed-length sliding windows of multivariate observations matching Section 3.2.

    If an engine sequence contains fewer than `window_size` (30) cycles, left-padding
    is applied by repeating the earliest available observation (`np.pad` with `mode='edge'`
    along the temporal axis) to preserve temporal ordering and causal dynamics without
    introducing artificial zeros.

    Parameters
    ----------
    df : pd.DataFrame
        Preprocessed DataFrame containing 'engine_id', 'cycle', and feature columns.
    feature_cols : list of str, optional
        List of 18 feature columns (15 sensors + 3 settings).
    window_size : int
        Sequence length W (default: 30 cycles).
    rul_cap : int
        Maximum operational target RUL (default: 125).
    risk_threshold : int
        Near-failure horizon in cycles (default: 30).
    is_test : bool
        If True, only extracts the final window per test engine with edge left-padding if needed.
    test_rul_df : pd.DataFrame, optional
        True RUL values for test engines.

    Returns
    -------
    X : np.ndarray, shape (N_samples, window_size, len(feature_cols))
    y : np.ndarray, shape (N_samples,) - Capped operational RUL target
    risk : np.ndarray, shape (N_samples,) - Binary near-failure target (1 if uncapped RUL <= risk_threshold)
    """
    if feature_cols is None:
        feature_cols = SELECTED_SENSOR_COLUMNS + [f"{c}_scaled" for c in SETTING_COLUMNS]

    X_list, y_list, risk_list = [], [], []

    engine_ids = df["engine_id"].unique()

    if is_test:
        if test_rul_df is None:
            raise ValueError("test_rul_df is required when is_test=True.")
        true_ruls = test_rul_df["RUL"].values

        for idx, eng_id in enumerate(engine_ids):
            eng_data = df[df["engine_id"] == eng_id][feature_cols].values
            L = len(eng_data)
            if L >= window_size:
                window = eng_data[-window_size:]
            else:
                pad_len = window_size - L
                # Replicate/edge left-padding on time axis: repeats earliest observation eng_data[0]
                window = np.pad(eng_data, ((pad_len, 0), (0, 0)), mode="edge")

            true_rul = float(true_ruls[idx])
            capped_rul = min(true_rul, float(rul_cap))
            risk_label = 1.0 if true_rul <= float(risk_threshold) else 0.0

            X_list.append(window)
            y_list.append(capped_rul)
            risk_list.append(risk_label)
    else:
        for eng_id in engine_ids:
            sub = df[df["engine_id"] == eng_id].sort_values("cycle")
            feats = sub[feature_cols].values
            raw_ruls = sub["RUL"].values

            L = len(feats)
            if L < window_size:
                pad_len = window_size - L
                window = np.pad(feats, ((pad_len, 0), (0, 0)), mode="edge")
                true_rul = float(raw_ruls[-1])
                capped_rul = min(true_rul, float(rul_cap))
                risk_label = 1.0 if true_rul <= float(risk_threshold) else 0.0

                X_list.append(window)
                y_list.append(capped_rul)
                risk_list.append(risk_label)
                continue

            for start in range(L - window_size + 1):
                end = start + window_size
                window = feats[start:end]
                true_rul = float(raw_ruls[end - 1])
                capped_rul = min(true_rul, float(rul_cap))
                risk_label = 1.0 if true_rul <= float(risk_threshold) else 0.0

                X_list.append(window)
                y_list.append(capped_rul)
                risk_list.append(risk_label)

    return (
        np.array(X_list, dtype=np.float32),
        np.array(y_list, dtype=np.float32),
        np.array(risk_list, dtype=np.float32),
    )

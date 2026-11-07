"""
src/utils/metrics.py
====================
Mathematical evaluation metrics for prognostic remaining useful life (RUL) estimation,
uncertainty quantification, and near-failure hazard calibration.
Matches Section 3.9, 3.10, and 4.6 of the manuscript.
"""

from __future__ import annotations

from typing import Sequence, Union

import numpy as np


def rmse(y_true: Union[np.ndarray, Sequence[float]], y_pred: Union[np.ndarray, Sequence[float]]) -> float:
    """Root Mean Squared Error (RMSE) in cycles."""
    y_t = np.asarray(y_true, dtype=np.float64)
    y_p = np.asarray(y_pred, dtype=np.float64)
    return float(np.sqrt(np.mean((y_t - y_p) ** 2)))


def mae(y_true: Union[np.ndarray, Sequence[float]], y_pred: Union[np.ndarray, Sequence[float]]) -> float:
    """Mean Absolute Error (MAE) in cycles."""
    y_t = np.asarray(y_true, dtype=np.float64)
    y_p = np.asarray(y_pred, dtype=np.float64)
    return float(np.mean(np.abs(y_t - y_p)))


def r2_score(y_true: Union[np.ndarray, Sequence[float]], y_pred: Union[np.ndarray, Sequence[float]]) -> float:
    """Coefficient of Determination (R^2)."""
    y_t = np.asarray(y_true, dtype=np.float64)
    y_p = np.asarray(y_pred, dtype=np.float64)
    ss_res = np.sum((y_t - y_p) ** 2)
    ss_tot = np.sum((y_t - np.mean(y_t)) ** 2)
    if ss_tot == 0:
        return 0.0
    return float(1.0 - (ss_res / ss_tot))


def nasa_score(y_true: Union[np.ndarray, Sequence[float]], y_pred: Union[np.ndarray, Sequence[float]]) -> float:
    """
    NASA C-MAPSS asymmetric scoring function.

    Error d = y_pred - y_true:
      - Late predictions (d >= 0) penalize heavily: exp(d / 10) - 1
      - Early predictions (d < 0) penalize moderately: exp(-d / 13) - 1
    """
    y_t = np.asarray(y_true, dtype=np.float64)
    y_p = np.asarray(y_pred, dtype=np.float64)
    d = y_p - y_t
    penalty = np.where(d < 0, np.exp(-d / 13.0) - 1.0, np.exp(d / 10.0) - 1.0)
    return float(np.sum(penalty))


def pinball_loss(
    y_true: Union[np.ndarray, Sequence[float]],
    q_pred: Union[np.ndarray, Sequence[float]],
    tau: float = 0.50,
) -> float:
    """
    Quantile (Pinball) loss for a single quantile level tau in (0, 1).
    L_tau(y, q) = max(tau * (y - q), (tau - 1) * (y - q))
    """
    y_t = np.asarray(y_true, dtype=np.float64)
    q_p = np.asarray(q_pred, dtype=np.float64)
    diff = y_t - q_p
    loss = np.maximum(tau * diff, (tau - 1.0) * diff)
    return float(np.mean(loss))


def multi_quantile_pinball_loss(
    y_true: Union[np.ndarray, Sequence[float]],
    quantiles_pred: np.ndarray,
    taus: Sequence[float] = (0.05, 0.50, 0.95),
) -> float:
    """
    Average pinball loss across multiple quantile levels.

    Parameters
    ----------
    y_true : 1D array of shape (N,)
    quantiles_pred : 2D array of shape (N, len(taus))
    taus : sequence of quantile levels
    """
    total_loss = 0.0
    for idx, tau in enumerate(taus):
        total_loss += pinball_loss(y_true, quantiles_pred[:, idx], tau=tau)
    return float(total_loss / len(taus))


def brier_score(
    y_true: Union[np.ndarray, Sequence[int]],
    y_prob: Union[np.ndarray, Sequence[float]],
) -> float:
    """
    Brier score for binary probabilistic predictions.
    BS = (1 / N) * sum((p_i - z_i)^2)
    """
    y_t = np.asarray(y_true, dtype=np.float64)
    p = np.asarray(y_prob, dtype=np.float64)
    return float(np.mean((p - y_t) ** 2))


def expected_calibration_error(
    y_true: Union[np.ndarray, Sequence[int]],
    y_prob: Union[np.ndarray, Sequence[float]],
    n_bins: int = 10,
) -> float:
    """
    Expected Calibration Error (ECE) with equal-width probability bins on [0, 1].

    ECE = sum_{b=1}^B (n_b / N) * |freq(b) - conf(b)|
    """
    y_t = np.asarray(y_true, dtype=np.float64)
    p = np.asarray(y_prob, dtype=np.float64)
    N = len(y_t)
    if N == 0:
        return 0.0

    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        bin_lower = bins[i]
        bin_upper = bins[i + 1]

        if i == n_bins - 1:
            in_bin = (p >= bin_lower) & (p <= bin_upper)
        else:
            in_bin = (p >= bin_lower) & (p < bin_upper)

        n_b = np.sum(in_bin)
        if n_b > 0:
            freq_b = np.mean(y_t[in_bin])
            conf_b = np.mean(p[in_bin])
            ece += (n_b / N) * np.abs(freq_b - conf_b)

    return float(ece)

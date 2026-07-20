"""One-dimensional Kalman filter for latent retrieval bias."""

from __future__ import annotations

import numpy as np
import pandas as pd


def kalman_filter_1d(
    observations: pd.Series | np.ndarray,
    process_var: float = 0.015,
    measurement_var: float = 1.0,
) -> pd.DataFrame:
    """Estimate a time-varying residual-bias state from scalar observations."""
    obs = np.asarray(observations, dtype=float)
    state = 0.0
    covariance = 1.0
    states = []
    covariances = []
    innovations = []
    for value in obs:
        pred_state = state
        pred_cov = covariance + process_var
        innovation = value - pred_state
        gain = pred_cov / (pred_cov + measurement_var)
        state = pred_state + gain * innovation
        covariance = (1.0 - gain) * pred_cov
        states.append(state)
        covariances.append(covariance)
        innovations.append(innovation)
    return pd.DataFrame(
        {
            "observation_k": obs,
            "latent_bias_k": states,
            "state_std_k": np.sqrt(covariances),
            "innovation_k": innovations,
        }
    )

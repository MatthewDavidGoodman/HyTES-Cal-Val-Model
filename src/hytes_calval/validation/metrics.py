"""Cal/Val residual metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd


def validation_metrics(residual_k: pd.Series | np.ndarray, label: str = "raw") -> pd.Series:
    """Return standard LST validation metrics in Kelvin."""
    residual = np.asarray(residual_k, dtype=float)
    return pd.Series(
        {
            "label": label,
            "n": int(residual.size),
            "bias_k": float(np.mean(residual)),
            "mae_k": float(np.mean(np.abs(residual))),
            "rmse_k": float(np.sqrt(np.mean(residual**2))),
            "std_k": float(np.std(residual, ddof=1)),
            "p05_k": float(np.quantile(residual, 0.05)),
            "p50_k": float(np.quantile(residual, 0.50)),
            "p95_k": float(np.quantile(residual, 0.95)),
        }
    )

"""Interpretable residual correction for thermal Cal/Val."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "emissivity",
    "transmittance",
    "view_zenith_deg",
    "precipitable_water_proxy",
    "ndvi",
]


@dataclass(frozen=True)
class RidgeResidualCorrector:
    """Small ridge model for bias correction without a heavy ML dependency."""

    columns: list[str]
    mean: np.ndarray
    scale: np.ndarray
    beta: np.ndarray

    def predict_residual(self, frame: pd.DataFrame) -> np.ndarray:
        matrix = _design_matrix(frame, self.columns)
        matrix = (matrix - self.mean) / self.scale
        matrix = np.column_stack([np.ones(len(matrix)), matrix])
        return matrix @ self.beta

    def correct(self, frame: pd.DataFrame) -> pd.DataFrame:
        out = frame.copy()
        predicted_bias = self.predict_residual(out)
        out["predicted_bias_k"] = predicted_bias
        out["corrected_lst_k"] = out["retrieved_lst_k"] - predicted_bias
        out["corrected_residual_k"] = out["corrected_lst_k"] - out["reference_lst_k"]
        return out


def _design_matrix(frame: pd.DataFrame, columns: list[str] | None = None) -> np.ndarray:
    numeric = frame[FEATURE_COLUMNS].copy()
    land_dummies = pd.get_dummies(frame["land_cover"], prefix="land", dtype=float)
    matrix_frame = pd.concat([numeric, land_dummies], axis=1)
    if columns is None:
        return matrix_frame.to_numpy(dtype=float)
    for col in columns:
        if col not in matrix_frame:
            matrix_frame[col] = 0.0
    return matrix_frame[columns].to_numpy(dtype=float)


def fit_ridge_residual_corrector(
    frame: pd.DataFrame,
    alpha: float = 5.0,
) -> RidgeResidualCorrector:
    """Fit a ridge model to predict retrieval residuals from Cal/Val covariates."""
    matrix_frame = pd.concat(
        [frame[FEATURE_COLUMNS], pd.get_dummies(frame["land_cover"], prefix="land", dtype=float)],
        axis=1,
    )
    columns = list(matrix_frame.columns)
    x = matrix_frame.to_numpy(dtype=float)
    mean = x.mean(axis=0)
    scale = x.std(axis=0, ddof=1)
    scale[scale == 0.0] = 1.0
    x_scaled = (x - mean) / scale
    x_design = np.column_stack([np.ones(len(x_scaled)), x_scaled])
    y = frame["residual_k"].to_numpy(dtype=float)
    penalty = alpha * np.eye(x_design.shape[1])
    penalty[0, 0] = 0.0
    beta = np.linalg.solve(x_design.T @ x_design + penalty, x_design.T @ y)
    return RidgeResidualCorrector(columns=columns, mean=mean, scale=scale, beta=beta)

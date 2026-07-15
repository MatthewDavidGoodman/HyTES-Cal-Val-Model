"""Explicit unit conversions used by the physics implementation."""

from __future__ import annotations

import numpy as np

ArrayLike = float | list[float] | np.ndarray


def celsius_to_kelvin(value_c: ArrayLike) -> np.ndarray:
    """Convert degrees Celsius to Kelvin."""
    return np.asarray(value_c, dtype=float) + 273.15


def kelvin_to_celsius(value_k: ArrayLike) -> np.ndarray:
    """Convert Kelvin to degrees Celsius."""
    value = np.asarray(value_k, dtype=float)
    if np.any(value < 0.0):
        raise ValueError("Kelvin temperature cannot be negative.")
    return value - 273.15


def hectopascal_to_pascal(value_hpa: ArrayLike) -> np.ndarray:
    """Convert hPa (equivalent to mbar) to Pa."""
    return np.asarray(value_hpa, dtype=float) * 100.0


def relative_humidity_percent_to_fraction(value_pct: ArrayLike) -> np.ndarray:
    """Convert relative humidity expressed as percent to a unit fraction."""
    value = np.asarray(value_pct, dtype=float)
    if np.any((value < 0.0) | (value > 100.0)):
        raise ValueError("Relative humidity percent must be between 0 and 100.")
    return value / 100.0

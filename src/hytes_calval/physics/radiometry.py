"""Thermal-infrared radiometry for skin-temperature Cal/Val.

The module uses spectral radiance in W m^-2 sr^-1 um^-1. That keeps
10-12 um thermal radiance values around 7-13 rather than millions in
per-meter SI units, which makes debug tables easier to read.
"""

from __future__ import annotations

import numpy as np

ArrayLike = float | list[float] | np.ndarray

PLANCK_H = 6.62607015e-34  # J s
LIGHT_C = 299_792_458.0  # m s^-1
BOLTZMANN_K = 1.380649e-23  # J K^-1
DEFAULT_WAVELENGTH_M = 10.8e-6
_PER_METER_TO_PER_MICRON = 1e-6


def _as_array(value: ArrayLike) -> np.ndarray:
    return np.asarray(value, dtype=float)


def planck_radiance(
    temperature_k: ArrayLike,
    wavelength_m: float = DEFAULT_WAVELENGTH_M,
) -> np.ndarray:
    """Return blackbody spectral radiance in W m^-2 sr^-1 um^-1."""
    temperature = _as_array(temperature_k)
    if np.any(temperature <= 0.0):
        raise ValueError("temperature_k must be positive.")
    wavelength = float(wavelength_m)
    exponent = (PLANCK_H * LIGHT_C) / (wavelength * BOLTZMANN_K * temperature)
    radiance_per_meter = (2.0 * PLANCK_H * LIGHT_C**2) / (wavelength**5 * np.expm1(exponent))
    return radiance_per_meter * _PER_METER_TO_PER_MICRON


def brightness_temperature_from_radiance(
    radiance: ArrayLike,
    wavelength_m: float = DEFAULT_WAVELENGTH_M,
) -> np.ndarray:
    """Invert Planck radiance to brightness temperature in Kelvin."""
    rad = _as_array(radiance)
    if np.any(rad <= 0.0):
        raise ValueError("radiance must be positive.")
    wavelength = float(wavelength_m)
    rad_per_meter = rad / _PER_METER_TO_PER_MICRON
    numerator = PLANCK_H * LIGHT_C
    denominator = wavelength * BOLTZMANN_K * np.log1p(
        (2.0 * PLANCK_H * LIGHT_C**2) / (wavelength**5 * rad_per_meter)
    )
    return numerator / denominator


def toa_radiance(
    surface_temperature_k: ArrayLike,
    emissivity: ArrayLike,
    transmittance: ArrayLike,
    downwelling_radiance: ArrayLike,
    upwelling_radiance: ArrayLike,
    wavelength_m: float = DEFAULT_WAVELENGTH_M,
) -> np.ndarray:
    """Forward single-band top-of-atmosphere radiance model.

    L_toa = tau * [epsilon * B(Ts) + (1 - epsilon) * L_down] + L_up
    """
    eps = _as_array(emissivity)
    tau = _as_array(transmittance)
    if np.any((eps <= 0.0) | (eps > 1.0)):
        raise ValueError("emissivity must be in (0, 1].")
    if np.any((tau <= 0.0) | (tau > 1.0)):
        raise ValueError("transmittance must be in (0, 1].")
    blackbody = planck_radiance(surface_temperature_k, wavelength_m=wavelength_m)
    return tau * (eps * blackbody + (1.0 - eps) * _as_array(downwelling_radiance)) + _as_array(
        upwelling_radiance
    )


def invert_surface_temperature(
    l_toa: ArrayLike,
    emissivity: ArrayLike,
    transmittance: ArrayLike,
    downwelling_radiance: ArrayLike,
    upwelling_radiance: ArrayLike,
    wavelength_m: float = DEFAULT_WAVELENGTH_M,
) -> np.ndarray:
    """Retrieve skin temperature from TOA radiance with emissivity/atmosphere terms."""
    eps = _as_array(emissivity)
    tau = _as_array(transmittance)
    corrected_blackbody = (
        _as_array(l_toa)
        - _as_array(upwelling_radiance)
        - tau * (1.0 - eps) * _as_array(downwelling_radiance)
    ) / (tau * eps)
    return brightness_temperature_from_radiance(corrected_blackbody, wavelength_m=wavelength_m)

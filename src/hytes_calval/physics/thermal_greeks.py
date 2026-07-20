"""Greek-style retrieval sensitivities for thermal Cal/Val model risk."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd

from .radiometry import DEFAULT_WAVELENGTH_M, invert_surface_temperature

BASE_KEYS = ("l_toa", "emissivity", "transmittance", "downwelling_radiance", "upwelling_radiance")
DEFAULT_STEPS = {
    "l_toa": 0.01,
    "emissivity": 1e-4,
    "transmittance": 1e-4,
    "downwelling_radiance": 0.01,
    "upwelling_radiance": 0.01,
}


def _temperature(params: Mapping[str, float], wavelength_m: float = DEFAULT_WAVELENGTH_M) -> float:
    return float(
        invert_surface_temperature(
            l_toa=params["l_toa"],
            emissivity=params["emissivity"],
            transmittance=params["transmittance"],
            downwelling_radiance=params["downwelling_radiance"],
            upwelling_radiance=params["upwelling_radiance"],
            wavelength_m=wavelength_m,
        )
    )


def thermal_greeks(
    l_toa: float,
    emissivity: float,
    transmittance: float,
    downwelling_radiance: float,
    upwelling_radiance: float,
    wavelength_m: float = DEFAULT_WAVELENGTH_M,
    steps: Mapping[str, float] | None = None,
) -> pd.Series:
    """Compute first-order temperature sensitivity to retrieval inputs."""
    params = {
        "l_toa": float(l_toa),
        "emissivity": float(emissivity),
        "transmittance": float(transmittance),
        "downwelling_radiance": float(downwelling_radiance),
        "upwelling_radiance": float(upwelling_radiance),
    }
    step_map = DEFAULT_STEPS | dict(steps or {})
    out = {"temperature_k": _temperature(params, wavelength_m=wavelength_m)}
    name_map = {
        "l_toa": "delta_l_toa",
        "emissivity": "epsilon_vega",
        "transmittance": "tau_rho",
        "downwelling_radiance": "delta_l_down",
        "upwelling_radiance": "delta_l_up",
    }
    for key in BASE_KEYS:
        h = step_map[key]
        plus = dict(params)
        minus = dict(params)
        plus[key] += h
        minus[key] -= h
        if key in {"emissivity", "transmittance"}:
            minus[key] = max(1e-5, minus[key])
            plus[key] = min(0.999999, plus[key])
        out[name_map[key]] = (_temperature(plus, wavelength_m) - _temperature(minus, wavelength_m)) / (
            plus[key] - minus[key]
        )
    return pd.Series(out)


def convexity_hessian(
    params: Mapping[str, float],
    wavelength_m: float = DEFAULT_WAVELENGTH_M,
    steps: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """Finite-difference Hessian of retrieved temperature against input factors."""
    base = {key: float(params[key]) for key in BASE_KEYS}
    step_map = DEFAULT_STEPS | dict(steps or {})
    rows: list[list[float]] = []
    for i_key in BASE_KEYS:
        row = []
        hi = step_map[i_key]
        for j_key in BASE_KEYS:
            hj = step_map[j_key]
            pp = dict(base)
            pm = dict(base)
            mp = dict(base)
            mm = dict(base)
            pp[i_key] += hi
            pp[j_key] += hj
            pm[i_key] += hi
            pm[j_key] -= hj
            mp[i_key] -= hi
            mp[j_key] += hj
            mm[i_key] -= hi
            mm[j_key] -= hj
            for candidate in (pp, pm, mp, mm):
                candidate["emissivity"] = float(np.clip(candidate["emissivity"], 1e-5, 0.999999))
                candidate["transmittance"] = float(np.clip(candidate["transmittance"], 1e-5, 0.999999))
            value = (
                _temperature(pp, wavelength_m)
                - _temperature(pm, wavelength_m)
                - _temperature(mp, wavelength_m)
                + _temperature(mm, wavelength_m)
            ) / (4.0 * hi * hj)
            row.append(value)
        rows.append(row)
    return pd.DataFrame(rows, index=BASE_KEYS, columns=BASE_KEYS)


def monte_carlo_temperature_uncertainty(
    params: Mapping[str, float],
    sigmas: Mapping[str, float],
    n: int = 5_000,
    seed: int = 7,
    wavelength_m: float = DEFAULT_WAVELENGTH_M,
) -> pd.Series:
    """Propagate input-factor uncertainty into a temperature distribution."""
    rng = np.random.default_rng(seed)
    draws = {key: np.full(n, float(params[key])) for key in BASE_KEYS}
    for key, sigma in sigmas.items():
        draws[key] = draws[key] + rng.normal(0.0, float(sigma), size=n)
    draws["emissivity"] = np.clip(draws["emissivity"], 0.80, 0.999)
    draws["transmittance"] = np.clip(draws["transmittance"], 0.40, 0.999)
    temps = invert_surface_temperature(
        l_toa=draws["l_toa"],
        emissivity=draws["emissivity"],
        transmittance=draws["transmittance"],
        downwelling_radiance=draws["downwelling_radiance"],
        upwelling_radiance=draws["upwelling_radiance"],
        wavelength_m=wavelength_m,
    )
    return pd.Series(
        {
            "n_used": int(n),
            "mean_k": float(np.mean(temps)),
            "std_k": float(np.std(temps, ddof=1)),
            "p05_k": float(np.quantile(temps, 0.05)),
            "p50_k": float(np.quantile(temps, 0.50)),
            "p95_k": float(np.quantile(temps, 0.95)),
        }
    )

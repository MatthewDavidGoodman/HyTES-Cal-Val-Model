"""Synthetic HyTES/ECOSTRESS-like matchup table for runnable demos.

This file intentionally does not pretend to be NASA data. It creates a
controlled diagnostic dataset with known error sources so the package can be
installed, tested, and demonstrated before project credentials and real
Lake Tahoe files are available.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from hytes_calval.physics.radiometry import toa_radiance, invert_surface_temperature

LAND_COVERS = np.array(["water", "vegetation", "bare_soil", "urban"])


def generate_skin_temperature_matchups(n: int = 2_500, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic retrieval/reference matchups with realistic covariates."""
    rng = np.random.default_rng(seed)
    land_cover = rng.choice(LAND_COVERS, size=n, p=[0.25, 0.35, 0.20, 0.20])
    land_offset = np.select(
        [land_cover == "water", land_cover == "vegetation", land_cover == "bare_soil", land_cover == "urban"],
        [-2.2, -0.8, 4.0, 3.0],
        default=0.0,
    )
    ndvi_center = np.select(
        [land_cover == "water", land_cover == "vegetation", land_cover == "bare_soil", land_cover == "urban"],
        [-0.05, 0.72, 0.14, 0.26],
        default=0.3,
    )
    ndvi = np.clip(rng.normal(ndvi_center, 0.08), -0.2, 0.95)
    view_zenith_deg = rng.uniform(0.0, 40.0, size=n)
    precipitable_water_proxy = rng.gamma(shape=2.0, scale=0.8, size=n)
    true_lst_k = 300.0 + land_offset + 1.3 * np.sin(view_zenith_deg / 40.0 * np.pi) + rng.normal(
        0.0, 2.4, size=n
    )
    true_emissivity = np.select(
        [land_cover == "water", land_cover == "vegetation", land_cover == "bare_soil", land_cover == "urban"],
        [0.990, 0.982, 0.935, 0.955],
        default=0.96,
    ) + rng.normal(0.0, 0.006, size=n)
    true_emissivity = np.clip(true_emissivity, 0.88, 0.995)
    true_transmittance = np.clip(
        0.91 - 0.045 * precipitable_water_proxy - 0.0012 * view_zenith_deg + rng.normal(0, 0.010, n),
        0.62,
        0.95,
    )
    downwelling_radiance = 1.15 + 0.48 * precipitable_water_proxy + rng.normal(0.0, 0.05, n)
    upwelling_radiance = 0.42 + 0.32 * precipitable_water_proxy + 0.006 * view_zenith_deg + rng.normal(
        0.0, 0.04, n
    )
    l_toa_true = toa_radiance(
        true_lst_k,
        true_emissivity,
        true_transmittance,
        downwelling_radiance,
        upwelling_radiance,
    )
    l_toa_observed = l_toa_true * (1.0 + rng.normal(0.0, 0.0025, size=n)) + rng.normal(0.0, 0.025, n)
    assumed_emissivity = np.clip(true_emissivity + rng.normal(0.0, 0.012, size=n), 0.86, 0.999)
    assumed_transmittance = np.clip(true_transmittance + rng.normal(0.0, 0.020, size=n), 0.55, 0.98)
    retrieved_lst_k = invert_surface_temperature(
        l_toa=l_toa_observed,
        emissivity=assumed_emissivity,
        transmittance=assumed_transmittance,
        downwelling_radiance=downwelling_radiance,
        upwelling_radiance=upwelling_radiance,
    )
    reference_lst_k = true_lst_k + rng.normal(0.0, 0.20, size=n)
    df = pd.DataFrame(
        {
            "retrieved_lst_k": retrieved_lst_k,
            "reference_lst_k": reference_lst_k,
            "residual_k": retrieved_lst_k - reference_lst_k,
            "l_toa_w_m2_sr_um": l_toa_observed,
            "emissivity": assumed_emissivity,
            "transmittance": assumed_transmittance,
            "downwelling_radiance_w_m2_sr_um": downwelling_radiance,
            "upwelling_radiance_w_m2_sr_um": upwelling_radiance,
            "view_zenith_deg": view_zenith_deg,
            "precipitable_water_proxy": precipitable_water_proxy,
            "ndvi": ndvi,
            "land_cover": land_cover,
            "true_lst_k": true_lst_k,
            "true_emissivity": true_emissivity,
            "true_transmittance": true_transmittance,
        }
    )
    return df

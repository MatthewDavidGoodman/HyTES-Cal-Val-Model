from __future__ import annotations

import numpy as np

from hytes_calval.physics.radiometry import (
    brightness_temperature_from_radiance,
    invert_surface_temperature,
    planck_radiance,
    toa_radiance,
)


def test_planck_round_trip() -> None:
    temperatures = np.array([285.0, 300.0, 315.0])
    radiance = planck_radiance(temperatures)
    recovered = brightness_temperature_from_radiance(radiance)
    assert np.allclose(recovered, temperatures, atol=1e-8)


def test_surface_temperature_inversion_round_trip() -> None:
    surface_temperature = 303.2
    l_toa = toa_radiance(
        surface_temperature_k=surface_temperature,
        emissivity=0.96,
        transmittance=0.82,
        downwelling_radiance=1.7,
        upwelling_radiance=1.1,
    )
    recovered = invert_surface_temperature(
        l_toa=l_toa,
        emissivity=0.96,
        transmittance=0.82,
        downwelling_radiance=1.7,
        upwelling_radiance=1.1,
    )
    assert np.isclose(float(recovered), surface_temperature, atol=1e-8)

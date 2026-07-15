import numpy as np
import pytest

from hytes_calval.physics.units import (
    celsius_to_kelvin,
    hectopascal_to_pascal,
    kelvin_to_celsius,
    relative_humidity_percent_to_fraction,
)


def test_temperature_round_trip() -> None:
    values = np.array([-5.0, 0.0, 20.0])
    assert np.allclose(kelvin_to_celsius(celsius_to_kelvin(values)), values)


def test_pressure_conversion() -> None:
    assert np.isclose(hectopascal_to_pascal(1013.25), 101325.0)


def test_relative_humidity_conversion() -> None:
    assert np.isclose(relative_humidity_percent_to_fraction(55.0), 0.55)


def test_invalid_relative_humidity_fails() -> None:
    with pytest.raises(ValueError):
        relative_humidity_percent_to_fraction(110.0)

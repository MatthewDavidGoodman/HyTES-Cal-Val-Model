from __future__ import annotations

from hytes_calval.physics.thermal_greeks import thermal_greeks
from hytes_calval.synthetic import generate_skin_temperature_matchups
from hytes_calval.validation import fit_ridge_residual_corrector, validation_metrics


def test_greeks_have_expected_signs() -> None:
    row = generate_skin_temperature_matchups(n=10, seed=1).iloc[0]
    greeks = thermal_greeks(
        l_toa=float(row["l_toa_w_m2_sr_um"]),
        emissivity=float(row["emissivity"]),
        transmittance=float(row["transmittance"]),
        downwelling_radiance=float(row["downwelling_radiance_w_m2_sr_um"]),
        upwelling_radiance=float(row["upwelling_radiance_w_m2_sr_um"]),
    )
    assert greeks["delta_l_toa"] > 0.0
    assert greeks["delta_l_up"] < 0.0
    assert greeks["epsilon_vega"] < 0.0


def test_bias_correction_improves_synthetic_rmse() -> None:
    frame = generate_skin_temperature_matchups(n=1200, seed=42)
    corrector = fit_ridge_residual_corrector(frame)
    corrected = corrector.correct(frame)
    raw = validation_metrics(frame["residual_k"], label="raw")
    adjusted = validation_metrics(corrected["corrected_residual_k"], label="bias_corrected")
    assert adjusted["rmse_k"] < raw["rmse_k"]

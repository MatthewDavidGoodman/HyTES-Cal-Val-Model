"""Command line demo for the HyTES Cal/Val thermal-Greeks bridge."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from hytes_calval.physics.thermal_greeks import (
    convexity_hessian,
    monte_carlo_temperature_uncertainty,
    thermal_greeks,
)
from hytes_calval.stochastic import kalman_filter_1d
from hytes_calval.synthetic import generate_skin_temperature_matchups
from hytes_calval.validation import fit_ridge_residual_corrector, validation_metrics


def run_demo(out: Path, n: int, seed: int) -> pd.DataFrame:
    out.mkdir(parents=True, exist_ok=True)
    matchups = generate_skin_temperature_matchups(n=n, seed=seed)
    corrector = fit_ridge_residual_corrector(matchups)
    corrected = corrector.correct(matchups)
    metrics = pd.DataFrame(
        [
            validation_metrics(matchups["residual_k"], label="raw"),
            validation_metrics(corrected["corrected_residual_k"], label="bias_corrected"),
        ]
    )
    median = matchups.iloc[len(matchups) // 2]
    greek_input = {
        "l_toa": float(median["l_toa_w_m2_sr_um"]),
        "emissivity": float(median["emissivity"]),
        "transmittance": float(median["transmittance"]),
        "downwelling_radiance": float(median["downwelling_radiance_w_m2_sr_um"]),
        "upwelling_radiance": float(median["upwelling_radiance_w_m2_sr_um"]),
    }
    greeks = thermal_greeks(**greek_input)
    hessian = convexity_hessian(greek_input)
    uncertainty = monte_carlo_temperature_uncertainty(
        greek_input,
        sigmas={
            "l_toa": 0.04,
            "emissivity": 0.01,
            "transmittance": 0.02,
            "downwelling_radiance": 0.10,
            "upwelling_radiance": 0.08,
        },
        seed=seed,
    )
    kalman = kalman_filter_1d(matchups["residual_k"].head(300))
    matchups.to_csv(out / "synthetic_matchups.csv", index=False)
    corrected.to_csv(out / "synthetic_matchups_corrected.csv", index=False)
    metrics.to_csv(out / "validation_metrics.csv", index=False)
    greeks.to_csv(out / "thermal_greeks.csv")
    hessian.to_csv(out / "thermal_convexity_hessian.csv")
    uncertainty.to_csv(out / "monte_carlo_uncertainty.csv")
    kalman.to_csv(out / "kalman_bias_state.csv", index=False)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Run synthetic HyTES/ECOSTRESS-like Cal/Val demo.")
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    parser.add_argument("--n", type=int, default=2500)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    metrics = run_demo(out=args.out, n=args.n, seed=args.seed)
    print("Synthetic data source: generated HyTES/ECOSTRESS-like matchup table, not NASA data.")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()

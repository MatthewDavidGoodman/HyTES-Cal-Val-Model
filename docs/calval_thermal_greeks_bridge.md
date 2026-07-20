# Cal/Val Thermal-Greeks Bridge

This extension connects the HyTES Lake Tahoe Cal/Val project to the stochastic/Greeks modeling thread.

## Data currently used

The runnable demo uses a synthetic HyTES-like matchup table generated in `src/hytes_calval/synthetic/skin_temperature.py`.
It is **not** real HyTES, buoy, or meteorology data. It is a controlled dataset for package validation and demonstration.

## Data-level guardrail

This project is **not** an L3/gridded-product workflow.

For the NASA workstation version, treat the real-data source as local HyTES/Lake Tahoe Cal/Val material, such as:

- HyTES L2-style product exports or local tables derived from them
- geolocated HyTES retrieved surface temperature, brightness temperature, or radiance fields
- Lake Tahoe buoy temperature profiles
- Wilson-style skin/bulk correction outputs
- meteorology and heat-flux variables
- view geometry and quality-control flags
- Copilot-generated matchup or prediction outputs built from the same local source files

Do not frame the project as using Level-3 products unless the underlying workflow actually switches to a Level-3 gridded dataset.

## Why synthetic first

The synthetic dataset makes the repo immediately runnable and testable while preserving the real scientific architecture:

1. radiance forward model
2. radiance-to-skin-temperature inversion
3. matchup residual computation
4. bias correction
5. thermal Greeks and convexity
6. stochastic latent-bias filtering

The real-data bridge should replace the synthetic generator with Lake Tahoe project tables:

- HyTES geolocated LST, brightness-temperature, or radiance outputs
- buoy temperature profiles at 1-5 m
- Wilson-style skin/bulk correction variables
- meteorology and heat-flux variables
- view geometry and quality-control flags

## Quant analogy

| Quant object | Thermal Cal/Val object |
|---|---|
| Option price | observed thermal radiance |
| Underlying state | surface skin temperature |
| Implied inversion | radiance-to-temperature inversion |
| Greeks | sensitivities to radiance, emissivity, transmittance, atmospheric path radiance |
| Gamma/convexity | nonlinear retrieval curvature |
| Model risk | residual bias and uncertainty budget |
| Stochastic process | time-varying calibration/retrieval residual |

## MVP result

The demo should show raw validation metrics and a bias-corrected metric table. The bias-corrector is intentionally simple: ridge regression over emissivity, transmittance, view angle, water-vapor proxy, NDVI, and land-cover dummies. The scientific rule remains that ML comes after the physical baseline and must be tested out-of-sample by flight, year, or site once real data are connected.

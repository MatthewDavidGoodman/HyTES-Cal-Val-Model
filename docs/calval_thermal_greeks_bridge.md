# Cal/Val Thermal-Greeks Bridge

This extension connects the HyTES Lake Tahoe Cal/Val project to the stochastic/Greeks modeling thread.

## Data currently used

The runnable demo uses a synthetic HyTES/ECOSTRESS-like matchup table generated in `src/hytes_calval/synthetic/skin_temperature.py`.
It is **not** real HyTES, ECOSTRESS, buoy, or meteorology data. It is a controlled dataset for package validation and demonstration.

Each synthetic row contains:

- retrieved LST in Kelvin
- reference LST in Kelvin
- residual in Kelvin
- observed top-of-atmosphere spectral radiance in `W m^-2 sr^-1 um^-1`
- assumed emissivity
- assumed atmospheric transmittance
- downwelling and upwelling atmospheric radiance
- view zenith angle
- precipitable-water proxy
- NDVI
- land-cover class
- hidden true LST/emissivity/transmittance used only to generate the benchmark

## Why synthetic first

The synthetic dataset makes the repo immediately runnable and testable while preserving the real scientific architecture:

1. radiance forward model
2. radiance-to-skin-temperature inversion
3. matchup residual computation
4. bias correction
5. thermal Greeks and convexity
6. stochastic latent-bias filtering

The real-data bridge should replace the synthetic generator with Lake Tahoe project tables:

- HyTES geolocated LST or radiance products
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

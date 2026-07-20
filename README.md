# HyTES Cal/Val Model

Physics-first calibration and validation of HyTES thermal observations over Lake Tahoe using buoy temperature profiles, meteorological measurements, and explicit surface-skin-temperature retrieval diagnostics.

## Project priority

1. Reproduce the Wilson (2013) skin/bulk temperature method exactly.
2. Verify equations, variables, units, constants, sign conventions, and correction terms.
3. Build 2016-2023 HyTES-to-buoy matchups.
4. Validate HyTES against both raw depth measurements and a physics-derived skin-temperature reference.
5. Add machine learning only after the physical baseline is correct.

## Data-level guardrail

This repository is **not** assuming an L3/gridded-product workflow.

For the NASA-computer version, the real-data path should be the local HyTES/Lake Tahoe Cal/Val material actually being used on the workstation: HyTES L2-style product exports or HyTES-derived local matchup tables, buoy profiles, meteorology, Wilson skin/bulk outputs, and Copilot outputs built from the same source material.

If the HyTES file is already a matchup table, point `configs/real_data.local.yml` at that table. If the HyTES files are earlier-stage product exports, first build a local observation/pixel/site matchup table and keep it out of git.

## New runnable extension: Cal/Val Thermal Greeks

This branch adds a runnable Python bridge from the Lake Tahoe HyTES Cal/Val project to the stochastic/Greeks modeling thread.

The analogy is direct:

| Quant finance object | Thermal remote-sensing object |
|---|---|
| Option price | observed top-of-atmosphere thermal radiance |
| Latent state / underlying | surface skin temperature |
| Implied-volatility inversion | radiance-to-temperature inversion |
| Greeks | sensitivity of retrieved temperature to radiance, emissivity, atmosphere, and view geometry |
| Gamma / convexity | second-order retrieval curvature and nonlinear error propagation |
| Model risk | Cal/Val residual bias and uncertainty budget |
| Stochastic process | time-varying retrieval bias, calibration drift, or atmospheric residual |

The demo currently uses **synthetic HyTES-like matchup data**, not real NASA data. That is deliberate: it gives us a testable package before plugging in HyTES local products/matchups, Lake Tahoe buoy profiles, Wilson skin/bulk corrections, and meteorology.

## NASA-computer real-data mode

This branch now includes a local-only real-data workflow. Raw HyTES, buoy, meteorology, Copilot, and intermediate files should stay on the NASA/JPL workstation and must not be committed.

Start from the example config:

```bash
cp configs/real_data.example.yml configs/real_data.local.yml
```

Then edit `configs/real_data.local.yml` so the paths and column mappings match the files on the workstation. The local config is ignored by git.

Build local matchups:

```bash
python examples/build_real_matchups.py
```

Compare this repo's output against the Copilot-built workflow:

```bash
python examples/compare_with_copilot.py
```

The first real-data target remains:

```text
HyTES retrieved surface temperature - Wilson-estimated skin temperature
```

Use direct buoy temperatures at 1-5 m as diagnostics, not as automatic skin-temperature truth.

## What the package does now

- Implements a single-band thermal radiance forward model.
- Inverts observed radiance to retrieved surface skin temperature.
- Computes first-order thermal Greeks:
  - `delta_l_toa`: sensitivity to observed radiance / calibration
  - `epsilon_vega`: sensitivity to emissivity error
  - `tau_rho`: sensitivity to atmospheric transmittance
  - `delta_l_down` and `delta_l_up`: path-radiance sensitivities
- Computes second-order convexity / cross-Greek terms.
- Generates synthetic Cal/Val matchup tables.
- Loads local real-data tables using machine-specific YAML column mappings.
- Builds nearest-time HyTES/buoy/met matchups without committing raw data.
- Compares repository outputs against a Copilot-built output table.
- Computes bias, MAE, RMSE, standard deviation, and residual quantiles.
- Fits a lightweight ridge residual model for interpretable bias correction.
- Runs a one-dimensional Kalman filter for latent residual-bias tracking.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Optional geospatial tools for later raster work:

```bash
pip install -e '.[geospatial]'
```

## Run synthetic demo

```bash
hytes-calval-demo --out outputs --n 2500 --seed 42
```

or:

```bash
python examples/demo_thermal_greeks.py
```

Expected generated files:

```text
outputs/synthetic_matchups.csv
outputs/synthetic_matchups_corrected.csv
outputs/validation_metrics.csv
outputs/thermal_greeks.csv
outputs/thermal_convexity_hessian.csv
outputs/monte_carlo_uncertainty.csv
outputs/kalman_bias_state.csv
```

## Run real-data workflow locally

```bash
python examples/build_real_matchups.py
python examples/compare_with_copilot.py
```

Expected local-only generated files:

```text
outputs/real_data/real_matchups.csv
outputs/real_data/copilot_joined_comparison.csv
outputs/real_data/copilot_comparison_stats.csv
```

## Core comparison

The key physics-based residual remains:

```text
HyTES surface temperature - Wilson-estimated skin temperature
```

Direct comparisons against buoy temperatures at 1-5 m remain important diagnostics, but subsurface buoy temperature is not automatically a direct skin-temperature truth measurement.

## Planned repository structure

```text
configs/                 experiment and data-path configuration
configs/*.local.yml      local workstation configs, ignored by git
docs/                    paper specification, equations, variables, decisions
src/hytes_calval/
  physics/               Wilson (2013), radiometry, heat-flux, skin/bulk corrections, uncertainty
  synthetic/             runnable synthetic matchup data for package testing
  ingestion/             local HyTES, buoy, meteorology, and report readers
  compare/               Copilot-vs-repository output reconciliation
  matchups/              temporal, spatial, and quality-control matching
  validation/            metrics, plots, diagnostics, residual correction, uncertainty budget
  stochastic/            latent residual-bias and drift models
  ml/                    downstream residual models only
tests/                   equation, units, limits, and pipeline tests
```

## Immediate tasks

- Add the exact Wilson (2013) paper and create an equation-by-equation specification.
- Inventory the three folder types present for each year from 2016 through 2023.
- Document the PDF report means, charts, exclusions, and processing assumptions.
- Confirm whether the HyTES variable is radiance, brightness temperature, or retrieved surface temperature.
- Confirm which HyTES local product/export/matchup is being used; do not assume L3.
- Confirm buoy sensor depths, sensor accuracy, time zone, and meteorological provenance.
- Replace the synthetic matchup generator with real Lake Tahoe HyTES/buoy/meteorology matchups.
- Compare repository output against the Copilot-built output table and explain every material discrepancy.
- Split model evaluation by year, flight, site, or held-out overpass before trusting any correction model.

## Scientific rules

- Preserve spatial and temporal mismatch for every matchup.
- Keep units explicit in variable names.
- Never hide quality-control exclusions.
- Never train and test on random rows from the same flight or overpass.
- Report raw HyTES performance before any correction.
- Evaluate any correction out of sample by year, flight, or site.
- Do not push raw NASA, JPL, buoy, meteorology, or Copilot data files to GitHub.
- Do not silently mix HyTES data levels/products between this workflow and the Copilot workflow.

This repository is currently a structured foundation. Wilson implementation and real-data validation should be completed only from the actual paper and project data, not from memory or guessed formulas.

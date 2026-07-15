# HyTES Cal/Val Model

Physics-first calibration and validation of HyTES thermal observations over Lake Tahoe using buoy temperature profiles and meteorological measurements.

## Project priority

1. Reproduce the Wilson (2013) skin/bulk temperature method exactly.
2. Verify equations, variables, units, constants, sign conventions, and correction terms.
3. Build 2016-2023 HyTES-to-buoy matchups.
4. Validate HyTES against both raw depth measurements and a physics-derived skin-temperature reference.
5. Add machine learning only after the physical baseline is correct.

## Core comparison

The key physics-based residual will be

```text
HyTES surface temperature - Wilson-estimated skin temperature
```

Direct comparisons against buoy temperatures at 1-5 m remain important diagnostics, but subsurface buoy temperature is not automatically a direct skin-temperature truth measurement.

## Planned repository structure

```text
configs/                 experiment and data-path configuration
docs/                    paper specification, equations, variables, decisions
src/hytes_calval/
  physics/               Wilson (2013), heat-flux, skin/bulk corrections, uncertainty
  ingestion/             2016-2023 HyTES, buoy, meteorology, and report readers
  matchups/              temporal, spatial, and quality-control matching
  validation/            metrics, plots, diagnostics, uncertainty budget
  ml/                    downstream residual models only
tests/                   equation, units, limits, and pipeline tests
```

## Immediate tasks

- Add the exact Wilson (2013) paper and create an equation-by-equation specification.
- Inventory the three folder types present for each year from 2016 through 2023.
- Document the PDF report means, charts, exclusions, and processing assumptions.
- Confirm whether the HyTES variable is radiance, brightness temperature, or retrieved surface temperature.
- Confirm buoy sensor depths, sensor accuracy, time zone, and meteorological provenance.

## Scientific rules

- Preserve spatial and temporal mismatch for every matchup.
- Keep units explicit in variable names.
- Never hide quality-control exclusions.
- Never train and test on random rows from the same flight or overpass.
- Report raw HyTES performance before any correction.
- Evaluate any correction out of sample by year, flight, or site.

This repository is currently a structured foundation. The Wilson implementation will be completed only from the actual paper and project data, not from memory or guessed formulas.

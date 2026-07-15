# AGENTS.md

## Mission

Build a transparent, reproducible, physics-first HyTES Lake Tahoe Cal/Val pipeline.

## Non-negotiable rules

1. Do not invent or reconstruct Wilson (2013) equations from memory. Use the paper as the controlling source.
2. Record every equation, symbol, unit, constant, correction, assumption, and validity range before implementation.
3. Do not describe 1-5 m buoy measurements as direct thermal skin-temperature truth.
4. Preserve time offset, spatial offset, QC status, site, flight, year, and buoy depth in every matchup.
5. Never overwrite raw data.
6. Never use random-row validation when observations share a year, flight, date, or site.
7. Report raw HyTES metrics before physics correction and before ML correction.
8. Fit all preprocessing inside training folds.
9. Add unit, dimensional, limiting-case, and paper-reproduction tests for physics functions.
10. Keep machine learning downstream of the Wilson physical baseline.

## Development order

1. Paper specification and variable dictionary.
2. Unit and sign-convention utilities.
3. Scalar Wilson reference implementation.
4. Tests against paper examples and limiting cases.
5. Vectorized implementation.
6. 2016-2023 data inventory and readers.
7. Matchup and QC audit tables.
8. Raw depth and Wilson-reference validation.
9. Uncertainty budget.
10. Residual ML models and grouped out-of-sample evaluation.

## Definition of done for physics code

- Source equation and page recorded in documentation.
- Inputs and outputs have explicit units.
- Sign convention is stated.
- Constants cite their source.
- Missing and invalid inputs fail clearly.
- Scalar tests pass.
- Vectorized results match scalar results.
- Intermediate terms can be exported for audit.

## Definition of done for ML code

- Beats or is honestly compared with raw and Wilson baselines.
- Uses leave-one-year, flight, or site-out evaluation.
- Contains no leakage.
- Reports performance by year, site, depth, and environmental regime.
- Documents limitations and scientific interpretation.

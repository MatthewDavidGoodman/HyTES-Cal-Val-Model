# Wilson (2013) Paper Specification

> Status: template awaiting the actual paper from the project computer.

No formula should be implemented until it is entered here with its exact source.

## Bibliographic record

- Full title:
- Authors:
- Journal/report:
- Year: 2013
- DOI or report number:
- Version used:

## Scientific target

- Quantity estimated:
- Definition of skin temperature:
- Definition of bulk temperature:
- Positive correction convention:
- Intended spatial and temporal scales:

## Equation register

For every equation, copy the mathematical expression in original notation and then map it to repository notation.

| ID | Paper page/equation | Purpose | Inputs | Output | Units | Assumptions | Implemented |
|---|---|---|---|---|---|---|---|
| W01 | TBD | TBD | TBD | TBD | TBD | TBD | No |

## Variable dictionary

| Paper symbol | Repository name | Meaning | Required unit | Measurement height/depth | Source |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | Wilson (2013) |

## Constants and parameterizations

| Symbol | Value | Unit | Source | Fixed or fitted | Notes |
|---|---:|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

## Corrections to audit

The paper will determine which are present. Do not assume all apply.

- cool-skin correction;
- warm-layer correction;
- wind-height conversion;
- humidity or vapor-pressure conversion;
- pressure correction;
- shortwave and longwave radiation terms;
- sensible heat flux;
- latent heat flux;
- conductive or molecular sublayer term;
- stability correction;
- time interpolation or averaging.

## Sign and unit checks

- Is the primary difference `skin - bulk` or `bulk - skin`?
- Which temperatures must be Kelvin internally?
- Is pressure expressed in Pa, hPa, or mbar?
- Is humidity relative humidity, specific humidity, mixing ratio, or vapor pressure?
- What wind reference height is required?
- Are radiative fluxes positive downward or upward?

## Validity domain

- Wind-speed range:
- Temperature range:
- Humidity range:
- Stability assumptions:
- Freshwater or seawater assumptions:
- Day/night restrictions:
- Geographic or seasonal limitations:

## Reproduction tests

| Test | Paper location | Expected result | Tolerance | Status |
|---|---|---:|---:|---|
| Example 1 | TBD | TBD | TBD | Pending |

## Uncertainty sources

- HyTES retrieval uncertainty;
- buoy sensor uncertainty;
- representativeness error between skin and subsurface temperature;
- temporal mismatch;
- spatial mismatch;
- meteorological measurement uncertainty;
- parameter uncertainty;
- structural model uncertainty.

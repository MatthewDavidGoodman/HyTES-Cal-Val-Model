# Real-data and Copilot comparison workflow

This note is for running the repository on the NASA/JPL workstation with local HyTES, buoy, meteorology, and Copilot-generated files.

## Rule zero: do not commit raw data

Raw mission files, internal reports, intermediate matchups, Copilot exports, and local path configs should stay on the workstation. This branch ignores:

```text
data/raw/
data/interim/
data/processed/
data/copilot/
configs/*.local.yml
outputs/*.csv
outputs/*.png
outputs/*.parquet
```

Only commit code, tests, docs, and sanitized examples.

## Data-level guardrail: not L3

This workflow should not assume Level-3 gridded products.

The expected real-data inputs are local HyTES/Lake Tahoe Cal/Val files on the workstation: HyTES L2-style product exports or already-built local matchup tables, buoy profiles, meteorology, Wilson skin/bulk outputs, and Copilot outputs derived from the same source material.

If a file is already a matchup table, use it directly as `hytes_table`. If a file is an earlier-stage HyTES product export, first create a local table with one row per observation/pixel/site matchup and keep that table out of git.

## Step 1: create a local config

```bash
cp configs/real_data.example.yml configs/real_data.local.yml
```

Edit the local file so each path points to the real files on the NASA computer:

```yaml
paths:
  hytes_table: /local/path/to/hytes_l2_or_matchups.csv
  buoy_table: /local/path/to/lake_tahoe_buoy.csv
  meteorology_table: /local/path/to/met.csv
  copilot_output: /local/path/to/copilot_output.csv
```

Then map whatever column names exist in those files into the canonical names used by this repo. The current minimal real-data columns are:

```text
time_utc
site_id
retrieved_lst_k
wilson_skin_temp_k OR buoy_temp_1m_k
```

Optional but scientifically important columns:

```text
latitude
longitude
radiance
brightness_temperature_k
emissivity
transmittance
upwelling_radiance
downwelling_radiance
view_zenith_deg
quality_flag
wind_speed_m_s
relative_humidity_fraction
shortwave_w_m2
longwave_w_m2
```

## Step 2: build local real-data matchups

```bash
python examples/build_real_matchups.py
```

This writes:

```text
outputs/real_data/real_matchups.csv
```

The first version performs nearest-time matching, optionally by `site_id`, using the tolerance in `configs/real_data.local.yml`. Spatial matching should be tightened after confirming the exact HyTES pixel geometry and buoy-site coordinates.

## Step 3: compare against the Copilot-built workflow

Place or point the local config to the Copilot output table. The comparison script expects both outputs to share keys such as:

```text
time_utc, site_id
```

and comparable numeric columns such as:

```text
retrieved_lst_k, reference_lst_k, residual_k
```

Run:

```bash
python examples/compare_with_copilot.py
```

It writes:

```text
outputs/real_data/copilot_joined_comparison.csv
outputs/real_data/copilot_comparison_stats.csv
```

Use the stats table to answer:

1. Are we matching the same observations?
2. Are our temperature units identical?
3. Is Wilson skin temperature being used consistently, or is one workflow using 1 m buoy temperature directly?
4. Are quality-control exclusions identical?
5. Are time zones and overpass times aligned?
6. Are both outputs based on the same HyTES data level/export, rather than one silently using a gridded product?

## Step 4: decision tree for mismatches

Large constant offset
: Check Celsius vs Kelvin, or skin-vs-depth reference mixup.

Time-dependent drift
: Check calibration drift, meteorology alignment, or overpass-time parsing.

Site-specific offset
: Check buoy coordinate/site mapping, spatial footprint, bathymetry, or local wind exposure.

Only cloudy/low-quality rows differ
: Check cloud/QC masking and exclusion logic.

Data-level mismatch
: Check whether one workflow used the local HyTES L2-style export/matchup and the other used a gridded or already-aggregated product.

Copilot lower RMSE but random split
: Do not trust it yet. Re-evaluate by held-out year, flight, site, or overpass.

## Scientific guardrail

The real target is not merely lower RMSE. The target is a traceable physical residual:

```text
HyTES retrieved surface temperature - Wilson-estimated skin temperature
```

Then residual ML should be used as a diagnostic/correction layer, not as a replacement for the physics baseline.

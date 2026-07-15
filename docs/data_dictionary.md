# Initial Data Dictionary

This is the target standardized schema. Actual source names must be mapped after inventorying the 2016-2023 folders.

## HyTES observations

| Standard name | Unit | Description |
|---|---|---|
| `observation_id` | none | Unique pixel or observation identifier |
| `overpass_id` | none | Flight/overpass grouping identifier |
| `year` | year | Campaign year |
| `timestamp_utc` | UTC | Observation timestamp |
| `latitude_deg` | degrees north | Observation latitude |
| `longitude_deg` | degrees east | Observation longitude |
| `hytes_surface_temp_c` | deg C | Retrieved thermal surface temperature, only after product type is confirmed |
| `view_zenith_deg` | degrees | Sensor view zenith angle |
| `retrieval_uncertainty_c` | deg C | Product-provided uncertainty, if available |
| `qc_good` | boolean | Decoded overall quality status |
| `qc_reason` | text | Human-readable QC explanation |

## Buoy profile

| Standard name | Unit | Description |
|---|---|---|
| `site_id` | none | Test-site or buoy identifier |
| `timestamp_utc` | UTC | Buoy observation timestamp |
| `water_temp_1m_c` | deg C | Water temperature at nominal 1 m depth |
| `water_temp_2m_c` | deg C | Water temperature at nominal 2 m depth |
| `water_temp_3m_c` | deg C | Water temperature at nominal 3 m depth |
| `water_temp_4m_c` | deg C | Water temperature at nominal 4 m depth |
| `water_temp_5m_c` | deg C | Water temperature at nominal 5 m depth |
| `sensor_depth_actual_m` | m | Actual depth when available |
| `buoy_temp_uncertainty_c` | deg C | Sensor calibration uncertainty |

## Meteorology

| Standard name | Unit | Description |
|---|---|---|
| `wind_speed_mps` | m/s | Wind speed at documented measurement height |
| `wind_height_m` | m | Wind sensor height |
| `wind_direction_deg` | degrees | Meteorological wind direction |
| `air_temp_c` | deg C | Air temperature at documented height |
| `air_temp_height_m` | m | Air-temperature sensor height |
| `relative_humidity_pct` | percent | Relative humidity, not unit fraction |
| `specific_humidity_kgkg` | kg/kg | Specific humidity if calculated or supplied |
| `pressure_pa` | Pa | Atmospheric pressure in SI units |
| `shortwave_down_wm2` | W/m2 | Downwelling shortwave radiation |
| `longwave_down_wm2` | W/m2 | Downwelling longwave radiation |

## Matchup and physics output

| Standard name | Unit | Description |
|---|---|---|
| `distance_m` | m | Spatial distance from HyTES observation to buoy |
| `time_delta_minutes` | min | Absolute temporal mismatch |
| `bulk_reference_depth_m` | m | Depth selected as bulk-temperature input |
| `bulk_temp_c` | deg C | Selected buoy bulk temperature |
| `skin_bulk_correction_c` | deg C | Wilson correction using explicit sign convention |
| `wilson_skin_temp_c` | deg C | Physics-derived skin-temperature estimate |
| `raw_residual_1m_c` | deg C | HyTES minus 1 m buoy temperature |
| `physics_residual_c` | deg C | HyTES minus Wilson skin-temperature estimate |

## Unit rules

- Pressure is standardized to Pa: `1 hPa = 100 Pa`.
- Temperature may be stored in Celsius but thermodynamic equations must convert to Kelvin when required.
- Relative humidity percentages must never be confused with fractions.
- Wind speed must retain its measurement height until any height adjustment is explicitly applied.

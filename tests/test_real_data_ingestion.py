from __future__ import annotations

import pandas as pd

from hytes_calval.ingestion.real_data import DataCatalog, build_real_matchups, normalize_columns


def test_normalize_columns_renames_and_parses_time() -> None:
    frame = pd.DataFrame({"t": ["2023-07-01T00:00:00Z"], "lst": [300.0]})
    normalized = normalize_columns(frame, {"time_utc": "t", "retrieved_lst_k": "lst"})

    assert "time_utc" in normalized.columns
    assert "retrieved_lst_k" in normalized.columns
    assert str(normalized["time_utc"].dtype).startswith("datetime64")


def test_build_real_matchups_from_local_tables(tmp_path) -> None:
    hytes_path = tmp_path / "hytes.csv"
    buoy_path = tmp_path / "buoy.csv"

    pd.DataFrame(
        {
            "overpass_time_utc": ["2023-07-01T00:10:00Z"],
            "site": ["A"],
            "hytes_lst": [301.0],
        }
    ).to_csv(hytes_path, index=False)
    pd.DataFrame(
        {
            "time": ["2023-07-01T00:00:00Z"],
            "site": ["A"],
            "wilson_skin": [299.5],
        }
    ).to_csv(buoy_path, index=False)

    catalog = DataCatalog(
        paths={"hytes_table": str(hytes_path), "buoy_table": str(buoy_path)},
        columns={
            "hytes": {
                "time_utc": "overpass_time_utc",
                "site_id": "site",
                "retrieved_lst_k": "hytes_lst",
            },
            "buoy": {"time_utc": "time", "site_id": "site", "wilson_skin_temp_k": "wilson_skin"},
        },
        matchup={"time_tolerance_minutes": 30},
    )

    matchups = build_real_matchups(catalog)
    assert matchups.loc[0, "reference_lst_k"] == 299.5
    assert matchups.loc[0, "residual_k"] == 1.5

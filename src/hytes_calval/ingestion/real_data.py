"""Real-data ingestion utilities for local HyTES / buoy / meteorology workflows.

These helpers intentionally read local files only. They are designed for the NASA/JPL
workstation workflow where raw data should not be committed to GitHub.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


@dataclass(frozen=True)
class DataCatalog:
    """Parsed real-data configuration."""

    paths: dict[str, str]
    columns: dict[str, dict[str, str]]
    matchup: dict[str, Any]


SUPPORTED_TABLE_EXTENSIONS = {".csv", ".parquet", ".json", ".jsonl"}


def load_catalog(path: str | Path) -> DataCatalog:
    """Load a local YAML data catalog.

    The expected starting point is ``configs/real_data.local.yml``, copied from
    ``configs/real_data.example.yml``.
    """

    catalog_path = Path(path)
    with catalog_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}

    return DataCatalog(
        paths=dict(payload.get("paths", {})),
        columns=dict(payload.get("columns", {})),
        matchup=dict(payload.get("matchup", {})),
    )


def load_table(path: str | Path) -> pd.DataFrame:
    """Load a local table from CSV, Parquet, JSON, or JSONL."""

    table_path = Path(path).expanduser()
    if not table_path.exists():
        raise FileNotFoundError(f"Could not find local table: {table_path}")

    suffix = table_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(table_path)
    if suffix == ".parquet":
        return pd.read_parquet(table_path)
    if suffix == ".json":
        return pd.read_json(table_path)
    if suffix == ".jsonl":
        return pd.read_json(table_path, lines=True)

    supported = ", ".join(sorted(SUPPORTED_TABLE_EXTENSIONS))
    raise ValueError(f"Unsupported table format {suffix!r}. Supported: {supported}")


def normalize_columns(frame: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """Rename project-specific columns into canonical repository column names.

    The mapping is written as ``canonical_name: source_column_name`` in YAML.
    Missing source columns are ignored so partial real-data runs can still proceed.
    """

    reverse_mapping = {source: canonical for canonical, source in mapping.items() if source in frame.columns}
    normalized = frame.rename(columns=reverse_mapping).copy()

    if "time_utc" in normalized.columns:
        normalized["time_utc"] = pd.to_datetime(normalized["time_utc"], utc=True, errors="coerce")

    return normalized


def _asof_join_by_site(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    tolerance_minutes: float,
    suffix: str,
) -> pd.DataFrame:
    """Nearest-time join, optionally grouped by site_id when both frames have it."""

    if right.empty:
        return left
    if "time_utc" not in left.columns or "time_utc" not in right.columns:
        raise ValueError("Both frames need a canonical time_utc column for real-data matchups.")

    left_sorted = left.sort_values("time_utc").copy()
    right_sorted = right.sort_values("time_utc").copy()
    tolerance = pd.Timedelta(minutes=float(tolerance_minutes))

    by = "site_id" if "site_id" in left_sorted.columns and "site_id" in right_sorted.columns else None
    return pd.merge_asof(
        left_sorted,
        right_sorted,
        on="time_utc",
        by=by,
        direction="nearest",
        tolerance=tolerance,
        suffixes=("", suffix),
    )


def build_real_matchups(catalog: DataCatalog) -> pd.DataFrame:
    """Build a canonical matchup table from local HyTES, buoy, and met files.

    The output is intentionally simple: one row per HyTES observation matched to
    nearest buoy/met records within a configured time tolerance. Spatial matching
    should be made stricter once exact pixel/site geometry is confirmed.
    """

    hytes = normalize_columns(load_table(catalog.paths["hytes_table"]), catalog.columns.get("hytes", {}))
    buoy_path = catalog.paths.get("buoy_table")
    met_path = catalog.paths.get("meteorology_table")

    tolerance_minutes = float(catalog.matchup.get("time_tolerance_minutes", 30))
    matchups = hytes

    if buoy_path:
        buoy = normalize_columns(load_table(buoy_path), catalog.columns.get("buoy", {}))
        matchups = _asof_join_by_site(
            matchups,
            buoy,
            tolerance_minutes=tolerance_minutes,
            suffix="_buoy",
        )

    if met_path:
        met = normalize_columns(load_table(met_path), catalog.columns.get("meteorology", {}))
        matchups = _asof_join_by_site(
            matchups,
            met,
            tolerance_minutes=tolerance_minutes,
            suffix="_met",
        )

    preferred_ref = str(catalog.matchup.get("preferred_reference_column", "wilson_skin_temp_k"))
    fallback_ref = str(catalog.matchup.get("fallback_reference_column", "buoy_temp_1m_k"))

    if preferred_ref in matchups.columns:
        matchups["reference_lst_k"] = matchups[preferred_ref]
    elif fallback_ref in matchups.columns:
        matchups["reference_lst_k"] = matchups[fallback_ref]

    if "retrieved_lst_k" in matchups.columns and "reference_lst_k" in matchups.columns:
        matchups["residual_k"] = matchups["retrieved_lst_k"] - matchups["reference_lst_k"]

    return matchups

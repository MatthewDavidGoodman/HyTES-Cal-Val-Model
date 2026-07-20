"""Compare this repository's outputs against a Copilot-built workflow output."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from hytes_calval.ingestion.real_data import load_table


@dataclass(frozen=True)
class ComparisonResult:
    """Tables produced by an output-to-output comparison."""

    joined: pd.DataFrame
    stats: pd.DataFrame


def _coerce_key_columns(frame: pd.DataFrame, key_columns: list[str]) -> pd.DataFrame:
    normalized = frame.copy()
    for column in key_columns:
        if column not in normalized.columns:
            raise ValueError(f"Missing key column {column!r}")
        if "time" in column.lower():
            normalized[column] = pd.to_datetime(normalized[column], utc=True, errors="coerce")
    return normalized


def compare_outputs(
    ours: pd.DataFrame,
    copilot: pd.DataFrame,
    *,
    key_columns: list[str],
    value_columns: list[str],
) -> ComparisonResult:
    """Align two workflow outputs and summarize numeric differences.

    ``value_columns`` should name canonical columns present in both frames, such as
    ``retrieved_lst_k``, ``reference_lst_k``, ``corrected_lst_k``, or ``residual_k``.
    """

    ours_norm = _coerce_key_columns(ours, key_columns)
    copilot_norm = _coerce_key_columns(copilot, key_columns)

    missing_ours = [column for column in value_columns if column not in ours_norm.columns]
    missing_copilot = [column for column in value_columns if column not in copilot_norm.columns]
    if missing_ours or missing_copilot:
        raise ValueError(
            "Missing comparison columns. "
            f"ours_missing={missing_ours}; copilot_missing={missing_copilot}"
        )

    joined = ours_norm.merge(
        copilot_norm,
        on=key_columns,
        how="inner",
        suffixes=("_ours", "_copilot"),
    )

    rows: list[dict[str, float | int | str]] = []
    for column in value_columns:
        ours_col = f"{column}_ours"
        copilot_col = f"{column}_copilot"
        diff = joined[ours_col].astype(float) - joined[copilot_col].astype(float)
        rows.append(
            {
                "column": column,
                "n_matched": int(diff.notna().sum()),
                "mean_diff_ours_minus_copilot": float(diff.mean()),
                "mae_diff": float(diff.abs().mean()),
                "rmse_diff": float((diff.pow(2).mean()) ** 0.5),
                "max_abs_diff": float(diff.abs().max()),
            }
        )
        joined[f"{column}_diff_ours_minus_copilot"] = diff

    return ComparisonResult(joined=joined, stats=pd.DataFrame(rows))


def load_and_compare(
    ours_path: str | Path,
    copilot_path: str | Path,
    *,
    key_columns: list[str],
    value_columns: list[str],
) -> ComparisonResult:
    """Load two local output files and compare them."""

    return compare_outputs(
        load_table(ours_path),
        load_table(copilot_path),
        key_columns=key_columns,
        value_columns=value_columns,
    )

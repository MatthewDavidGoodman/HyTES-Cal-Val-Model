from __future__ import annotations

import pandas as pd

from hytes_calval.compare import compare_outputs


def test_compare_outputs_summarizes_differences() -> None:
    ours = pd.DataFrame(
        {
            "time_utc": ["2023-07-01T00:00:00Z", "2023-07-01T00:30:00Z"],
            "site_id": ["A", "A"],
            "retrieved_lst_k": [300.0, 302.0],
            "residual_k": [1.0, 2.0],
        }
    )
    copilot = pd.DataFrame(
        {
            "time_utc": ["2023-07-01T00:00:00Z", "2023-07-01T00:30:00Z"],
            "site_id": ["A", "A"],
            "retrieved_lst_k": [299.5, 301.0],
            "residual_k": [0.5, 1.0],
        }
    )

    result = compare_outputs(
        ours,
        copilot,
        key_columns=["time_utc", "site_id"],
        value_columns=["retrieved_lst_k", "residual_k"],
    )

    assert len(result.joined) == 2
    assert set(result.stats["column"]) == {"retrieved_lst_k", "residual_k"}
    residual_row = result.stats.loc[result.stats["column"] == "residual_k"].iloc[0]
    assert residual_row["mean_diff_ours_minus_copilot"] == 0.75

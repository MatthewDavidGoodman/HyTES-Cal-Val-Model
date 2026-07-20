"""Compare repository outputs with the current Copilot-built output table."""

from __future__ import annotations

from pathlib import Path

from hytes_calval.compare import load_and_compare


def main() -> None:
    result = load_and_compare(
        ours_path="outputs/real_data/real_matchups.csv",
        copilot_path="data/copilot/copilot_matchups_or_predictions.csv",
        key_columns=["time_utc", "site_id"],
        value_columns=["retrieved_lst_k", "reference_lst_k", "residual_k"],
    )

    output_dir = Path("outputs/real_data")
    output_dir.mkdir(parents=True, exist_ok=True)
    result.joined.to_csv(output_dir / "copilot_joined_comparison.csv", index=False)
    result.stats.to_csv(output_dir / "copilot_comparison_stats.csv", index=False)
    print(result.stats.to_string(index=False))


if __name__ == "__main__":
    main()

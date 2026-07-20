"""Build local real-data matchups from a machine-specific catalog."""

from __future__ import annotations

from pathlib import Path

from hytes_calval.ingestion import build_real_matchups, load_catalog


def main() -> None:
    catalog = load_catalog("configs/real_data.local.yml")
    output_dir = Path(catalog.paths.get("output_dir", "outputs/real_data"))
    output_dir.mkdir(parents=True, exist_ok=True)

    matchups = build_real_matchups(catalog)
    output_path = output_dir / "real_matchups.csv"
    matchups.to_csv(output_path, index=False)
    print(f"wrote {len(matchups):,} rows to {output_path}")


if __name__ == "__main__":
    main()

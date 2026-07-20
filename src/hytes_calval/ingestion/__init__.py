"""Local real-data ingestion helpers."""

from .real_data import DataCatalog, build_real_matchups, load_catalog, load_table, normalize_columns

__all__ = [
    "DataCatalog",
    "build_real_matchups",
    "load_catalog",
    "load_table",
    "normalize_columns",
]

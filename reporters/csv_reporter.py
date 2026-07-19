"""CSV timeline reporter."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _serialize_complex_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with complex event fields encoded as stable JSON strings."""

    export_df = df.copy()
    for column in ("raw_evidence", "provenance"):
        if column in export_df.columns:
            export_df[column] = export_df[column].apply(
                lambda value: json.dumps(value, ensure_ascii=False, default=str)
            )
    return export_df


def export_timeline_csv(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Export a timeline DataFrame to CSV."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    _serialize_complex_columns(df).to_csv(path, index=False)
    return path

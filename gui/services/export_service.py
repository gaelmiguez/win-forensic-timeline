"""In-memory exports of filtered canonical CommonEvent records."""

from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from gui.config import CANONICAL_EVENT_FIELDS
from gui.models import ExportPayload, FilterCriteria


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def canonical_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Return only the 16 canonical fields, preserving original values."""
    records: list[dict[str, Any]] = []
    for row in frame.to_dict(orient="records"):
        records.append(
            {field: _json_safe(row.get(field)) for field in CANONICAL_EVENT_FIELDS}
        )
    return records


def build_export(frame: pd.DataFrame, format_name: str) -> ExportPayload:
    """Build CSV, JSON or JSONL bytes without touching the filesystem."""
    normalized_format = format_name.casefold()
    records = canonical_records(frame)
    if normalized_format == "csv":
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=CANONICAL_EVENT_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False, default=str)
                    if isinstance(value, (dict, list))
                    else value
                    for key, value in record.items()
                }
            )
        return ExportPayload(
            output.getvalue().encode("utf-8-sig"),
            "text/csv",
            "filtered_events.csv",
            len(records),
        )
    if normalized_format == "json":
        content = json.dumps(records, ensure_ascii=False, indent=2, default=str)
        return ExportPayload(
            content.encode("utf-8"),
            "application/json",
            "filtered_events.json",
            len(records),
        )
    if normalized_format == "jsonl":
        content = "\n".join(
            json.dumps(record, ensure_ascii=False, default=str) for record in records
        )
        if records:
            content += "\n"
        return ExportPayload(
            content.encode("utf-8"),
            "application/x-ndjson",
            "filtered_events.jsonl",
            len(records),
        )
    raise ValueError(f"Unsupported export format: {format_name}")


def build_filter_manifest(
    criteria: FilterCriteria,
    source_output_root: str | Path | None,
    total_source_events: int,
    exported_events: int,
    generated_at: datetime | None = None,
) -> ExportPayload:
    """Build a privacy-aware JSON manifest for one filtered export."""
    source_name = Path(source_output_root).name if source_output_root else None
    filters = {
        key: _json_safe(value)
        for key, value in asdict(criteria).items()
        if value not in (None, "", (), [])
    }
    manifest = {
        "generated_at_utc": (generated_at or datetime.now(timezone.utc)).isoformat(),
        "source_output_root": source_name,
        "filters": filters,
        "total_source_events": total_source_events,
        "exported_events": exported_events,
    }
    return ExportPayload(
        json.dumps(manifest, ensure_ascii=False, indent=2, default=str).encode("utf-8"),
        "application/json",
        "filtered_events_manifest.json",
        1,
    )

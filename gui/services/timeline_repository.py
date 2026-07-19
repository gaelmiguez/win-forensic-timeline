"""Read-only loader for timeline.csv outputs."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path

import pandas as pd

from gui.config import CANONICAL_EVENT_FIELDS, TIMELINE_JSON_FIELDS
from gui.models import FileFingerprint, IssueSeverity, LoadIssue, LoadResult, LoadStatus
from gui.services.event_repository import parse_aware_utc


def load_timeline(path: Path) -> LoadResult:
    """Load a timeline CSV while preserving its original cell strings."""
    resolved = path.expanduser().resolve(strict=False)
    if not resolved.is_file():
        return LoadResult(
            data=pd.DataFrame(),
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "timeline_file_not_found",
                    "No se encontró timeline.csv.",
                    resolved,
                )
            ],
            status=LoadStatus.ERROR,
        )

    try:
        fingerprint = FileFingerprint.from_path(resolved)
        frame = pd.read_csv(resolved, encoding="utf-8", dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        return LoadResult(
            data=pd.DataFrame(),
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "timeline_empty_file",
                    "timeline.csv está vacío y no contiene cabecera.",
                    resolved,
                )
            ],
            fingerprint=FileFingerprint.from_path(resolved),
            status=LoadStatus.ERROR,
        )
    except (OSError, UnicodeError, pd.errors.ParserError) as exc:
        return LoadResult(
            data=pd.DataFrame(),
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "timeline_read_error",
                    f"No se pudo leer timeline.csv: {exc}",
                    resolved,
                )
            ],
            status=LoadStatus.ERROR,
        )

    missing = [field for field in CANONICAL_EVENT_FIELDS if field not in frame.columns]
    if missing:
        return LoadResult(
            data=frame,
            records_read=len(frame),
            records_rejected=len(frame),
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "timeline_missing_columns",
                    f"Faltan columnas canónicas: {', '.join(missing)}.",
                    resolved,
                )
            ],
            fingerprint=fingerprint,
            status=LoadStatus.ERROR,
        )

    issues: list[LoadIssue] = []
    extra = sorted(set(frame.columns) - set(CANONICAL_EVENT_FIELDS))
    if extra:
        issues.append(
            LoadIssue(
                IssueSeverity.WARNING,
                "timeline_extra_columns",
                f"Se conservaron columnas adicionales: {', '.join(extra)}.",
                resolved,
            )
        )

    parsed_timestamps: list[pd.Timestamp | pd.NaT] = []
    parsed_json: dict[str, list[object | None]] = {
        field: [] for field in TIMELINE_JSON_FIELDS
    }
    for row_index, row in frame.iterrows():
        parsed = parse_aware_utc(row["timestamp_utc"])
        if parsed is None:
            parsed_timestamps.append(pd.NaT)
            issues.append(
                LoadIssue(
                    IssueSeverity.WARNING,
                    "timeline_invalid_timestamp",
                    "La marca temporal no se podrá usar en filtros temporales.",
                    resolved,
                    int(row_index),
                    "timestamp_utc",
                )
            )
        else:
            parsed_timestamps.append(pd.Timestamp(parsed))

        for field in TIMELINE_JSON_FIELDS:
            value = row[field]
            if not value:
                parsed_json[field].append(None)
                continue
            try:
                parsed_json[field].append(json.loads(value))
            except (JSONDecodeError, TypeError):
                parsed_json[field].append(None)
                issues.append(
                    LoadIssue(
                        IssueSeverity.WARNING,
                        "timeline_invalid_serialized_json",
                        "La celda no contiene JSON serializado válido; se conservó el texto original.",
                        resolved,
                        int(row_index),
                        field,
                    )
                )

    loaded = frame.copy(deep=True)
    loaded["_ui_timestamp_utc"] = pd.Series(parsed_timestamps, dtype="datetime64[ns, UTC]")
    for field, values in parsed_json.items():
        loaded[f"_ui_{field}"] = values

    status = LoadStatus.EMPTY if loaded.empty else LoadStatus.SUCCESS
    return LoadResult(
        data=loaded,
        records_read=len(frame),
        records_accepted=len(frame),
        records_rejected=0,
        issues=issues,
        fingerprint=fingerprint,
        status=status,
    )

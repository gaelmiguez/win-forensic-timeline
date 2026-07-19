"""Read-only loader for normalized events.json outputs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import pandas as pd

from gui.config import CANONICAL_EVENT_FIELDS, REQUIRED_TEXT_EVENT_FIELDS
from gui.models import FileFingerprint, IssueSeverity, LoadIssue, LoadResult, LoadStatus


def parse_aware_utc(value: Any) -> datetime | None:
    """Parse an ISO timestamp only when it contains timezone information."""
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def _row_issue(
    severity: IssueSeverity,
    code: str,
    message: str,
    path: Path,
    row_index: int,
    field: str | None = None,
) -> LoadIssue:
    return LoadIssue(severity, code, message, path, row_index, field)


def _validate_event_record(
    record: Any, path: Path, row_index: int
) -> tuple[dict[str, Any] | None, list[LoadIssue]]:
    issues: list[LoadIssue] = []
    if not isinstance(record, dict):
        return None, [
            _row_issue(
                IssueSeverity.ERROR,
                "event_not_object",
                "El evento debe ser un objeto JSON.",
                path,
                row_index,
            )
        ]

    missing = [field for field in CANONICAL_EVENT_FIELDS if field not in record]
    if missing:
        return None, [
            _row_issue(
                IssueSeverity.ERROR,
                "event_missing_fields",
                f"Faltan claves canónicas: {', '.join(missing)}.",
                path,
                row_index,
            )
        ]

    unknown = sorted(set(record) - set(CANONICAL_EVENT_FIELDS))
    if unknown:
        issues.append(
            _row_issue(
                IssueSeverity.WARNING,
                "event_unknown_fields",
                f"Se conservaron claves no canónicas: {', '.join(unknown)}.",
                path,
                row_index,
            )
        )

    for field in REQUIRED_TEXT_EVENT_FIELDS:
        if not isinstance(record[field], str) or not record[field].strip():
            issues.append(
                _row_issue(
                    IssueSeverity.ERROR,
                    "event_invalid_required_text",
                    "El campo debe ser texto no vacío.",
                    path,
                    row_index,
                    field,
                )
            )

    timestamp_utc = parse_aware_utc(record["timestamp_utc"])
    if timestamp_utc is None:
        issues.append(
            _row_issue(
                IssueSeverity.ERROR,
                "event_invalid_timestamp_utc",
                "timestamp_utc debe ser una fecha ISO timezone-aware.",
                path,
                row_index,
                "timestamp_utc",
            )
        )

    timestamp_local = record["timestamp_local"]
    if timestamp_local is not None and parse_aware_utc(timestamp_local) is None:
        issues.append(
            _row_issue(
                IssueSeverity.ERROR,
                "event_invalid_timestamp_local",
                "timestamp_local debe ser nulo o una fecha ISO timezone-aware.",
                path,
                row_index,
                "timestamp_local",
            )
        )

    for field in ("object", "scenario_id"):
        value = record[field]
        if value is not None and not isinstance(value, str):
            issues.append(
                _row_issue(
                    IssueSeverity.ERROR,
                    "event_invalid_optional_text",
                    "El campo debe ser texto o nulo.",
                    path,
                    row_index,
                    field,
                )
            )

    confidence = record["confidence"]
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not 0.0 <= float(confidence) <= 1.0
    ):
        issues.append(
            _row_issue(
                IssueSeverity.ERROR,
                "event_invalid_confidence",
                "confidence debe ser numérico y estar entre 0 y 1.",
                path,
                row_index,
                "confidence",
            )
        )

    provenance = record["provenance"]
    if not isinstance(provenance, dict):
        issues.append(
            _row_issue(
                IssueSeverity.ERROR,
                "event_invalid_provenance",
                "provenance debe ser un objeto JSON.",
                path,
                row_index,
                "provenance",
            )
        )
    elif not provenance:
        issues.append(
            _row_issue(
                IssueSeverity.WARNING,
                "event_empty_provenance",
                "El evento no contiene detalles de procedencia.",
                path,
                row_index,
                "provenance",
            )
        )

    if any(issue.severity is IssueSeverity.ERROR for issue in issues):
        return None, issues

    accepted = dict(record)
    accepted["_ui_timestamp_utc"] = pd.Timestamp(timestamp_utc)
    return accepted, issues


def load_events(path: Path) -> LoadResult:
    """Load events.json, preserving valid rows and accounting for rejections."""
    resolved = path.expanduser().resolve(strict=False)
    if not resolved.is_file():
        return LoadResult(
            data=pd.DataFrame(),
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "events_file_not_found",
                    "No se encontró events.json.",
                    resolved,
                )
            ],
            status=LoadStatus.ERROR,
        )

    try:
        fingerprint = FileFingerprint.from_path(resolved)
        with resolved.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, UnicodeError) as exc:
        return LoadResult(
            data=pd.DataFrame(),
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "events_read_error",
                    f"No se pudo leer events.json: {exc}",
                    resolved,
                )
            ],
            status=LoadStatus.ERROR,
        )
    except JSONDecodeError as exc:
        return LoadResult(
            data=pd.DataFrame(),
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "events_invalid_json",
                    f"events.json no contiene JSON válido (línea {exc.lineno}).",
                    resolved,
                )
            ],
            fingerprint=fingerprint,
            status=LoadStatus.ERROR,
        )

    if not isinstance(payload, list):
        return LoadResult(
            data=pd.DataFrame(),
            records_read=1,
            records_rejected=1,
            issues=[
                LoadIssue(
                    IssueSeverity.ERROR,
                    "events_invalid_root",
                    "La raíz de events.json debe ser una lista.",
                    resolved,
                )
            ],
            fingerprint=fingerprint,
            status=LoadStatus.ERROR,
        )

    accepted: list[dict[str, Any]] = []
    issues: list[LoadIssue] = []
    seen_ids: set[str] = set()
    rejected = 0
    for row_index, record in enumerate(payload):
        validated, row_issues = _validate_event_record(record, resolved, row_index)
        issues.extend(row_issues)
        if validated is None:
            rejected += 1
            continue
        event_id = validated["event_id"]
        if event_id in seen_ids:
            rejected += 1
            issues.append(
                _row_issue(
                    IssueSeverity.ERROR,
                    "event_duplicate_id",
                    f"event_id duplicado: {event_id}.",
                    resolved,
                    row_index,
                    "event_id",
                )
            )
            continue
        seen_ids.add(event_id)
        accepted.append(validated)

    if not payload:
        status = LoadStatus.EMPTY
    elif not accepted:
        status = LoadStatus.ERROR
    elif rejected:
        status = LoadStatus.PARTIAL
    else:
        status = LoadStatus.SUCCESS

    return LoadResult(
        data=pd.DataFrame(accepted),
        records_read=len(payload),
        records_accepted=len(accepted),
        records_rejected=rejected,
        issues=issues,
        fingerprint=fingerprint,
        status=status,
    )

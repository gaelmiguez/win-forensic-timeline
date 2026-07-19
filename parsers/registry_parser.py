"""Windows Registry metadata parser.

This phase intentionally does not read live Registry keys or binary hives. It
normalizes controlled JSON metadata, such as autorun entries, into CommonEvent
objects while preserving traceability.
"""

from __future__ import annotations

import json
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any

from core.event_model import CommonEvent
from core.time_utils import ensure_utc, parse_iso_to_utc


def parse(input_path: str | Path, max_files: int | None = None) -> list[CommonEvent]:
    """Parse Registry metadata JSON files and return normalized events."""

    if max_files is not None and max_files <= 0:
        return []

    events: list[CommonEvent] = []
    files = _discover_registry_metadata_files(Path(input_path))
    if max_files is not None:
        files = files[:max_files]

    for file_path in files:
        metadata = _load_registry_metadata(file_path)
        if metadata is None:
            continue

        for entry in _iter_registry_entries(metadata, file_path):
            try:
                event = _event_from_registry_entry(entry, file_path, metadata)
            except Exception as exc:
                _warn(f"Skipping Registry entry from {file_path}: {exc}")
                continue

            if event is not None:
                events.append(event)

    return events


def _discover_registry_metadata_files(input_path: Path) -> list[Path]:
    """Return Registry metadata JSON files from a file or directory input."""

    if not input_path.exists():
        return []

    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() == ".json" else []

    return sorted(path for path in input_path.rglob("*.json") if path.is_file())


def _load_registry_metadata(file_path: Path) -> dict[str, Any] | None:
    """Load a Registry metadata JSON document."""

    try:
        loaded = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _warn(f"Ignoring invalid Registry metadata {file_path}: {exc}")
        return None

    if not isinstance(loaded, dict):
        _warn(f"Ignoring invalid Registry metadata {file_path}: expected a JSON object.")
        return None

    return loaded


def _iter_registry_entries(metadata: dict[str, Any], source_path: Path) -> list[dict[str, Any]]:
    """Return normalized entry dictionaries from a Registry metadata document."""

    entries = metadata.get("entries", [])
    if not isinstance(entries, list):
        _warn(f"Ignoring Registry metadata {source_path}: entries must be a list.")
        return []

    normalized_entries: list[dict[str, Any]] = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            _warn(f"Skipping Registry entry {index} from {source_path}: expected a JSON object.")
            continue

        normalized = dict(entry)
        normalized.setdefault("source_type", metadata.get("source_type"))
        normalized.setdefault("parser_backend", metadata.get("parser_backend") or "external_registry_json")
        normalized.setdefault("artifact", metadata.get("artifact") or "Registry")
        if "scenario_id" not in normalized and metadata.get("scenario_id") is not None:
            normalized["scenario_id"] = metadata.get("scenario_id")
        normalized_entries.append(normalized)

    return normalized_entries


def _event_from_registry_entry(
    entry: dict[str, Any], source_path: Path, metadata: dict[str, Any]
) -> CommonEvent | None:
    """Map a Registry metadata entry to a CommonEvent."""

    timestamp_utc = _select_registry_timestamp(entry)
    if timestamp_utc is None:
        _warn(f"Skipping Registry entry from {source_path}: missing forensic timestamp.")
        return None

    timestamp_field = "last_write_time_utc" if _has_value(entry.get("last_write_time_utc")) else "timestamp_utc"
    original_timestamp = entry.get(timestamp_field)
    hive = _clean_text(entry.get("hive")) or "UNKNOWN"
    key_path = _clean_registry_path(entry.get("key_path"))
    value_name = _clean_text(entry.get("value_name")) or "(default)"
    source_type = _clean_text(entry.get("source_type")) or _clean_text(metadata.get("source_type")) or "registry"
    parser_backend = (
        _clean_text(entry.get("parser_backend"))
        or _clean_text(metadata.get("parser_backend"))
        or "external_registry_json"
    )
    registry_object = _build_registry_object(hive, key_path, value_name)

    raw_evidence = {
        "hive": hive,
        "key_path": key_path,
        "value_name": value_name,
        "value_type": entry.get("value_type"),
        "value_data": entry.get("value_data"),
        "last_write_time_utc": entry.get("last_write_time_utc"),
        "source_type": source_type,
        "parser_backend": parser_backend,
    }
    provenance = {
        "artifact": "Registry",
        "source_path": str(source_path),
        "parser": "registry_parser",
        "parser_backend": parser_backend,
        "timestamp_field": timestamp_field,
        "original_timestamp": str(original_timestamp),
        "timestamp_format": "Registry timestamp UTC",
        "normalization_method": "parse_iso_to_utc",
        "registry_hive": hive,
        "registry_key_path": key_path,
        "registry_value_name": value_name,
    }

    return CommonEvent.create(
        timestamp_utc=timestamp_utc,
        timestamp_local=None,
        timestamp_type="registry_last_write_time",
        source_artifact="Registry",
        source_location=str(source_path),
        event_category="persistence",
        event_action="registry_autorun_configured",
        object=registry_object,
        description=f"Entrada de autorun detectada en Registry: {value_name}",
        raw_evidence=raw_evidence,
        parser_module="registry_parser",
        traceability_ref=f"{source_path.name}:{registry_object}",
        confidence=0.75,
        provenance=provenance,
        scenario_id=_clean_text(entry.get("scenario_id")) or _clean_text(metadata.get("scenario_id")),
    )


def _select_registry_timestamp(entry: dict[str, Any]) -> datetime | None:
    """Select the explicit Registry forensic timestamp as UTC."""

    for key in ("last_write_time_utc", "timestamp_utc"):
        value = entry.get(key)
        if not _has_value(value):
            continue

        if isinstance(value, datetime):
            try:
                return ensure_utc(value)
            except Exception:
                return None

        if isinstance(value, str):
            try:
                return parse_iso_to_utc(value)
            except Exception:
                return None

    return None


def _build_registry_object(hive: str, key_path: str, value_name: str) -> str:
    parts = [hive]
    if key_path:
        parts.append(key_path.strip("\\"))
    parts.append(value_name)
    return "\\".join(part for part in parts if part)


def _clean_registry_path(value: Any) -> str:
    text = _clean_text(value)
    if text is None:
        return ""
    return "\\".join(part for part in text.replace("/", "\\").split("\\") if part)


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _has_value(value: Any) -> bool:
    return value is not None and value != ""


def _warn(message: str) -> None:
    warnings.warn(message, RuntimeWarning, stacklevel=2)

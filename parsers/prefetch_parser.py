"""Windows Prefetch parser.

This module implements the first defensive Prefetch parsing layer. It discovers
``.pf`` files and maps normalized Prefetch metadata to ``CommonEvent`` objects.
If no usable Prefetch backend is available, parsing fails closed: no execution
event is fabricated from filesystem metadata.
"""

from __future__ import annotations

import warnings
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from core.event_model import CommonEvent
from core.time_utils import ensure_utc, filetime_to_utc, parse_iso_to_utc

MAX_REFERENCED_FILES = 50

_BACKEND_CHECKED = False
_PREFETCH2JSON: Callable[[str], dict[str, Any]] | None = None
_BACKEND_IMPORT_ERROR: str | None = None


def parse(input_path: str | Path, max_files: int | None = None) -> list[CommonEvent]:
    """Parse Prefetch files from a path and return normalized events.

    The parser accepts either a single ``.pf`` file or a directory. If the
    optional parsing backend is unavailable, this function returns an empty list
    after controlled warnings instead of inventing execution events.
    """

    if max_files is not None and max_files <= 0:
        return []

    events: list[CommonEvent] = []
    files = _discover_prefetch_files(Path(input_path))
    if max_files is not None:
        files = files[:max_files]

    for file_path in files:
        try:
            metadata = _parse_prefetch_file(file_path)
        except Exception as exc:
            _warn(f"Ignoring Prefetch file {file_path}: {exc}")
            continue

        if metadata is None:
            continue

        try:
            event = _event_from_prefetch_metadata(metadata, file_path)
        except Exception as exc:
            _warn(f"Skipping Prefetch metadata from {file_path}: {exc}")
            continue

        if event is not None:
            events.append(event)

    return events


def _discover_prefetch_files(input_path: Path) -> list[Path]:
    """Return Prefetch ``.pf`` files from a file or directory input."""

    if not input_path.exists():
        return []

    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() == ".pf" else []

    return sorted(path for path in input_path.rglob("*") if path.is_file() and path.suffix.lower() == ".pf")


def _parse_prefetch_file(file_path: Path) -> dict[str, Any] | None:
    """Parse a Prefetch file using a backend or external JSON metadata."""

    backend = _load_prefetch2json_backend()
    if backend is not None:
        try:
            raw_metadata = backend(str(file_path))
        except Exception as exc:
            _warn(f"Cannot parse Prefetch file {file_path} with backend: {exc}")
        else:
            if isinstance(raw_metadata, dict):
                raw_metadata.setdefault("parser_backend", "prefetch-parser")
            metadata = _normalize_prefetch_metadata(raw_metadata, file_path)
            metadata.setdefault("prefetch_file_name", file_path.name)
            metadata.setdefault("source_path", str(file_path))
            return metadata

    sidecar_path = _find_sidecar_metadata(file_path)
    if sidecar_path is not None:
        metadata = _load_sidecar_metadata(sidecar_path)
        if metadata is None:
            return None
        metadata.setdefault("parser_backend", "external_metadata_json")
        metadata.setdefault("prefetch_file_name", file_path.name)
        metadata.setdefault("source_path", str(file_path))
        return _normalize_prefetch_metadata(metadata, file_path)

    if backend is None:
        reason = _BACKEND_IMPORT_ERROR or "prefetch-parser backend is not available."
        _warn(f"Cannot parse Prefetch file {file_path}: {reason}; no JSON sidecar found.")

    return None


def _find_sidecar_metadata(file_path: Path) -> Path | None:
    """Return the JSON sidecar path for a Prefetch file if it exists."""

    sidecar_path = file_path.with_suffix(".json")
    return sidecar_path if sidecar_path.exists() and sidecar_path.is_file() else None


def _load_sidecar_metadata(sidecar_path: Path) -> dict[str, Any] | None:
    """Load external Prefetch metadata from a JSON sidecar."""

    try:
        loaded = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _warn(f"Ignoring invalid Prefetch sidecar {sidecar_path}: {exc}")
        return None

    if not isinstance(loaded, dict):
        _warn(f"Ignoring invalid Prefetch sidecar {sidecar_path}: expected a JSON object.")
        return None

    return loaded


def _event_from_prefetch_metadata(metadata: dict[str, Any], source_path: Path) -> CommonEvent | None:
    """Map normalized Prefetch metadata to a CommonEvent."""

    normalized = _normalize_prefetch_metadata(metadata, source_path)
    timestamp_utc = _select_primary_last_run_time(normalized)
    if timestamp_utc is None:
        _warn(f"Skipping Prefetch metadata from {source_path}: missing execution timestamp.")
        return None

    executable_name = _clean_text(normalized.get("executable_name")) or _infer_executable_from_filename(source_path)
    parser_backend = _clean_text(normalized.get("parser_backend")) or "metadata"
    raw_evidence = {
        "executable_name": executable_name,
        "prefetch_hash": normalized.get("prefetch_hash"),
        "run_count": normalized.get("run_count"),
        "last_run_time_utc": _datetime_to_iso(normalized.get("last_run_time_utc")),
        "last_run_times_utc": [
            _datetime_to_iso(value)
            for value in _as_list(normalized.get("last_run_times_utc"))
            if _coerce_datetime_to_utc(value) is not None
        ],
        "volume_information": normalized.get("volume_information") or [],
        "referenced_files": _limit_referenced_files(normalized.get("referenced_files")),
        "parser_backend": parser_backend,
        "prefetch_version": normalized.get("prefetch_version"),
    }
    referenced_files = _as_list(normalized.get("referenced_files"))
    if len(referenced_files) > MAX_REFERENCED_FILES:
        raw_evidence["referenced_files_truncated"] = True
        raw_evidence["referenced_files_total"] = len(referenced_files)

    original_timestamp = _select_original_timestamp(normalized, timestamp_utc)
    provenance = {
        "artifact": "Prefetch",
        "source_path": normalized.get("source_path") or str(source_path),
        "parser": "prefetch_parser",
        "parser_backend": parser_backend,
        "timestamp_field": "last_run_time",
        "original_timestamp": original_timestamp,
        "timestamp_format": normalized.get("timestamp_format") or "Prefetch execution timestamp UTC",
        "normalization_method": normalized.get("normalization_method") or "ensure_utc",
        "prefetch_file_name": normalized.get("prefetch_file_name") or source_path.name,
    }

    return CommonEvent.create(
        timestamp_utc=timestamp_utc,
        timestamp_local=None,
        timestamp_type="prefetch_last_run_time",
        source_artifact="Prefetch",
        source_location=str(source_path),
        event_category="program_execution",
        event_action="program_executed",
        object=executable_name,
        description=f"Ejecución de programa detectada por Prefetch: {executable_name}",
        raw_evidence=raw_evidence,
        parser_module="prefetch_parser",
        traceability_ref=source_path.name,
        confidence=0.85,
        provenance=provenance,
    )


def _select_primary_last_run_time(metadata: dict[str, Any]) -> datetime | None:
    """Select the primary Prefetch execution timestamp as UTC."""

    direct_value = _coerce_datetime_to_utc(metadata.get("last_run_time_utc"))
    if direct_value is not None:
        return direct_value

    run_times = [
        value
        for value in (_coerce_datetime_to_utc(item) for item in _as_list(metadata.get("last_run_times_utc")))
        if value is not None
    ]
    if not run_times:
        return None

    return max(run_times)


def _normalize_prefetch_metadata(raw: object, source_path: Path) -> dict[str, Any]:
    """Normalize backend-specific Prefetch metadata into a stable dictionary."""

    if not isinstance(raw, dict):
        return {
            "executable_name": _infer_executable_from_filename(source_path),
            "parser_backend": "unknown",
        }

    metadata: dict[str, Any] = dict(raw)
    normalized = {
        "executable_name": _first_present(metadata, "executable_name", "executable_filename", "name")
        or _infer_executable_from_filename(source_path),
        "prefetch_hash": _first_present(metadata, "prefetch_hash", "hash"),
        "run_count": _first_present(metadata, "run_count", "exec_count", "execution_count"),
        "last_run_time_utc": _first_present(
            metadata,
            "last_run_time_utc",
            "last_run_time",
            "last_exec_time",
        ),
        "last_run_times_utc": _first_present(
            metadata,
            "last_run_times_utc",
            "last_run_times",
            "run_times",
        )
        or [],
        "volume_information": _first_present(metadata, "volume_information", "volumes") or [],
        "referenced_files": _first_present(metadata, "referenced_files", "filenames") or [],
        "parser_backend": _first_present(metadata, "parser_backend", "backend") or "metadata",
        "prefetch_version": _first_present(metadata, "prefetch_version", "format_version"),
        "timestamp_format": metadata.get("timestamp_format"),
        "normalization_method": metadata.get("normalization_method"),
        "prefetch_file_name": metadata.get("prefetch_file_name") or source_path.name,
        "source_path": metadata.get("source_path") or str(source_path),
    }
    return normalized


def _load_prefetch2json_backend() -> Callable[[str], dict[str, Any]] | None:
    """Return prefetch-parser's prefetch2json function if it is importable."""

    global _BACKEND_CHECKED, _PREFETCH2JSON, _BACKEND_IMPORT_ERROR

    if _BACKEND_CHECKED:
        return _PREFETCH2JSON

    _BACKEND_CHECKED = True
    try:
        from prefetch_parser import prefetch2json  # type: ignore
    except Exception as exc:
        _BACKEND_IMPORT_ERROR = f"prefetch-parser is not usable: {exc}"
        _PREFETCH2JSON = None
    else:
        _PREFETCH2JSON = prefetch2json
        _BACKEND_IMPORT_ERROR = None

    return _PREFETCH2JSON


def _coerce_datetime_to_utc(value: Any) -> datetime | None:
    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        return ensure_utc(value)

    if isinstance(value, int) and not isinstance(value, bool):
        try:
            return filetime_to_utc(value)
        except Exception:
            return None

    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            if "T" in stripped or stripped.endswith("Z") or "+" in stripped:
                return parse_iso_to_utc(stripped)
            return ensure_utc(datetime.fromisoformat(stripped))
        except Exception:
            return None

    return None


def _datetime_to_iso(value: Any) -> str | None:
    dt = _coerce_datetime_to_utc(value)
    return dt.isoformat() if dt is not None else None


def _select_original_timestamp(metadata: dict[str, Any], selected: datetime) -> str:
    direct_value = metadata.get("last_run_time_utc")
    direct_dt = _coerce_datetime_to_utc(direct_value)
    if direct_dt is not None and direct_dt == selected:
        return str(direct_value)

    for value in _as_list(metadata.get("last_run_times_utc")):
        dt = _coerce_datetime_to_utc(value)
        if dt is not None and dt == selected:
            return str(value)

    return selected.isoformat()


def _limit_referenced_files(value: Any) -> list[Any]:
    return _as_list(value)[:MAX_REFERENCED_FILES]


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _first_present(metadata: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = metadata.get(key)
        if value is not None:
            return value
    return None


def _infer_executable_from_filename(source_path: Path) -> str:
    stem = source_path.name
    if stem.lower().endswith(".pf"):
        stem = stem[:-3]
    if "-" in stem:
        stem = stem.rsplit("-", 1)[0]
    return stem.lower() if stem else "unknown.exe"


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _warn(message: str) -> None:
    warnings.warn(message, RuntimeWarning, stacklevel=2)

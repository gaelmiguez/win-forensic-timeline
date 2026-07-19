"""Windows Event Log parser.

This module provides the first functional EVTX parsing layer for the prototype.
It reads Windows Event Log records with python-evtx when available, extracts a
small and traceable subset of XML fields, and maps each event to CommonEvent.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from core.event_model import CommonEvent
from core.time_utils import parse_iso_to_utc


def parse(input_path: str | Path, max_records: int | None = None) -> list[CommonEvent]:
    """Parse EVTX files from a path and return normalized CommonEvent objects."""

    if max_records is not None and max_records <= 0:
        return []

    events: list[CommonEvent] = []
    for file_path in _discover_evtx_files(Path(input_path)):
        remaining = None if max_records is None else max_records - len(events)
        if remaining is not None and remaining <= 0:
            break

        try:
            events.extend(_parse_evtx_file(file_path, max_records=remaining))
        except Exception as exc:
            _warn(f"Ignoring EVTX file {file_path}: {exc}")

    return events


def _discover_evtx_files(input_path: Path) -> list[Path]:
    """Return EVTX files from input_path, accepting either a file or folder."""

    if not input_path.exists():
        return []

    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() == ".evtx" else []

    return sorted(path for path in input_path.rglob("*.evtx") if path.is_file())


def _parse_evtx_file(file_path: Path, max_records: int | None = None) -> list[CommonEvent]:
    """Read an EVTX file with python-evtx and map records to CommonEvent."""

    evtx_class = _load_evtx_class()
    if evtx_class is None:
        return []

    events: list[CommonEvent] = []
    processed_records = 0

    try:
        with evtx_class(str(file_path)) as log:
            for record in log.records():
                if max_records is not None and processed_records >= max_records:
                    break

                processed_records += 1
                record_number = _get_record_number(record, processed_records)
                try:
                    event = _event_from_xml(record.xml(), file_path, record_number)
                except Exception as exc:
                    _warn(f"Skipping EVTX record {record_number} in {file_path}: {exc}")
                    continue

                if event is not None:
                    events.append(event)
    except Exception as exc:
        _warn(f"Ignoring unreadable EVTX file {file_path}: {exc}")

    return events


def _event_from_xml(
    xml_text: str,
    source_path: Path,
    record_number: int | None = None,
) -> CommonEvent | None:
    """Map a single EVTX XML record to CommonEvent.

    The full XML is intentionally not stored in raw_evidence to avoid large or
    sensitive payloads leaking into the normalized event stream.
    """

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        _warn(f"Skipping EVTX XML record from {source_path}: invalid XML: {exc}")
        return None

    system_fields = _extract_system_fields(root)
    original_timestamp = system_fields.get("time_created")
    if not original_timestamp:
        _warn(f"Skipping EVTX record in {source_path}: missing System/TimeCreated/@SystemTime")
        return None

    try:
        timestamp_utc = parse_iso_to_utc(original_timestamp)
    except Exception as exc:
        _warn(
            f"Skipping EVTX record in {source_path}: invalid TimeCreated value "
            f"{original_timestamp!r}: {exc}"
        )
        return None

    event_data = _extract_event_data(root)
    user_data = _extract_user_data(root)
    event_id = system_fields.get("event_id")
    channel = system_fields.get("channel")
    provider_name = system_fields.get("provider_name")
    event_record_id = system_fields.get("event_record_id")

    if channel and event_id:
        event_object = f"{channel}:{event_id}"
    elif event_id:
        event_object = f"event_id_{event_id}"
    else:
        event_object = "windows_event"

    event_id_text = event_id or "desconocido"
    provider_text = provider_name or "proveedor desconocido"
    channel_text = channel or "canal desconocido"
    record_ref = event_record_id or record_number or "unknown"

    raw_evidence = {
        "provider_name": provider_name,
        "event_id": event_id,
        "version": system_fields.get("version"),
        "level": system_fields.get("level"),
        "task": system_fields.get("task"),
        "opcode": system_fields.get("opcode"),
        "keywords": system_fields.get("keywords"),
        "channel": channel,
        "computer": system_fields.get("computer"),
        "event_record_id": event_record_id,
        "event_data": event_data,
        "user_data": user_data,
    }
    provenance = {
        "artifact": "EVTX",
        "source_path": str(source_path),
        "record_number": record_number,
        "event_record_id": event_record_id,
        "provider_name": provider_name,
        "event_id": event_id,
        "channel": channel,
        "timestamp_field": "System.TimeCreated.SystemTime",
        "original_timestamp": original_timestamp,
        "timestamp_format": "EVTX SystemTime UTC",
        "normalization_method": "parse_iso_to_utc",
        "parser": "evtx_parser",
    }

    return CommonEvent.create(
        timestamp_utc=timestamp_utc,
        timestamp_local=None,
        timestamp_type="evtx_time_created",
        source_artifact="EVTX",
        source_location=str(source_path),
        event_category="system_event",
        event_action="windows_event",
        object=event_object,
        description=(
            f"Evento Windows {event_id_text} registrado por "
            f"{provider_text} en {channel_text}"
        ),
        raw_evidence=raw_evidence,
        parser_module="evtx_parser",
        traceability_ref=f"{source_path.name}:{record_ref}",
        confidence=0.9,
        provenance=provenance,
    )


def _extract_system_fields(root: ET.Element) -> dict[str, Any]:
    """Extract commonly used fields from the EVTX System node."""

    system = _find_child(root, "System")
    if system is None:
        return {}

    fields: dict[str, Any] = {}
    for child in list(system):
        name = _strip_namespace(child.tag)
        text = _clean_text(child.text)

        if name == "Provider":
            fields["provider_name"] = child.attrib.get("Name")
        elif name == "EventID":
            fields["event_id"] = text
        elif name == "Version":
            fields["version"] = text
        elif name == "Level":
            fields["level"] = text
        elif name == "Task":
            fields["task"] = text
        elif name == "Opcode":
            fields["opcode"] = text
        elif name == "Keywords":
            fields["keywords"] = text
        elif name == "TimeCreated":
            fields["time_created"] = child.attrib.get("SystemTime")
        elif name == "EventRecordID":
            fields["event_record_id"] = text
        elif name == "Correlation":
            fields["correlation_activity_id"] = child.attrib.get("ActivityID")
        elif name == "Execution":
            fields["execution_process_id"] = child.attrib.get("ProcessID")
            fields["execution_thread_id"] = child.attrib.get("ThreadID")
        elif name == "Channel":
            fields["channel"] = text
        elif name == "Computer":
            fields["computer"] = text
        elif name == "Security":
            fields["security_user_id"] = child.attrib.get("UserID")

    return fields


def _extract_event_data(root: ET.Element) -> dict[str, Any]:
    """Extract simple EventData/Data values from an EVTX XML record."""

    event_data = _find_child(root, "EventData")
    if event_data is None:
        return {}

    values: dict[str, Any] = {}
    unnamed_index = 1
    for child in list(event_data):
        if _strip_namespace(child.tag) != "Data":
            continue

        key = child.attrib.get("Name")
        if not key:
            key = f"Data_{unnamed_index}"
            unnamed_index += 1

        _store_value(values, key, _clean_text(child.text))

    return values


def _extract_user_data(root: ET.Element) -> dict[str, Any]:
    """Extract simple UserData values without preserving full XML."""

    user_data = _find_child(root, "UserData")
    if user_data is None:
        return {}

    values: dict[str, Any] = {}
    for child in list(user_data):
        key = _strip_namespace(child.tag)
        values[key] = _element_to_simple_value(child)

    return values


def _strip_namespace(tag: str) -> str:
    """Return a tag name without XML namespace."""

    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _load_evtx_class():
    try:
        from Evtx.Evtx import Evtx
    except Exception as exc:
        _warn(f"python-evtx is not available; EVTX parsing skipped: {exc}")
        return None

    return Evtx


def _get_record_number(record: Any, fallback: int) -> int:
    for attribute in ("record_num", "record_number"):
        value = getattr(record, attribute, None)
        if callable(value):
            try:
                return int(value())
            except Exception:
                continue
        if value is not None:
            try:
                return int(value)
            except Exception:
                continue

    return fallback


def _find_child(parent: ET.Element, name: str) -> ET.Element | None:
    for child in list(parent):
        if _strip_namespace(child.tag) == name:
            return child
    return None


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned if cleaned else None


def _store_value(values: dict[str, Any], key: str, value: Any) -> None:
    if key not in values:
        values[key] = value
        return

    current = values[key]
    if isinstance(current, list):
        current.append(value)
    else:
        values[key] = [current, value]


def _element_to_simple_value(element: ET.Element) -> Any:
    children = list(element)
    attributes = dict(element.attrib)
    text = _clean_text(element.text)

    if not children:
        if attributes:
            data: dict[str, Any] = dict(attributes)
            if text is not None:
                data["text"] = text
            return data
        return text

    data = dict(attributes)
    if text is not None:
        data["text"] = text
    for child in children:
        key = child.attrib.get("Name") or _strip_namespace(child.tag)
        _store_value(data, key, _element_to_simple_value(child))
    return data


def _warn(message: str) -> None:
    warnings.warn(message, RuntimeWarning, stacklevel=2)

import json
from datetime import datetime, timezone

import pytest

from core.event_model import CommonEvent
from main import run_pipeline
from parsers.registry_parser import (
    _discover_registry_metadata_files,
    _event_from_registry_entry,
    _select_registry_timestamp,
    parse,
)
from scripts.generate_sample_registry_metadata import generate_sample_registry_metadata


def _write_registry_metadata(path, entries, **overrides):
    metadata = {
        "parser_backend": "external_registry_json",
        "artifact": "Registry",
        "source_type": "autoruns",
        "entries": entries,
    }
    metadata.update(overrides)
    path.write_text(json.dumps(metadata), encoding="utf-8")
    return metadata


def _sample_entry(**overrides):
    entry = {
        "hive": "HKCU",
        "key_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "value_name": "ExampleApp",
        "value_type": "REG_SZ",
        "value_data": "C:\\Tools\\ExampleApp.exe",
        "last_write_time_utc": "2024-01-10T09:25:00Z",
        "scenario_id": "S_REGISTRY_SYNTH",
    }
    entry.update(overrides)
    return entry


def test_discover_registry_metadata_files_finds_json_recursively(tmp_path):
    root = tmp_path / "registry"
    nested = root / "sample"
    nested.mkdir(parents=True)
    first = root / "autoruns.json"
    second = nested / "more.json"
    ignored = nested / "notes.txt"
    first.write_text("{}", encoding="utf-8")
    second.write_text("{}", encoding="utf-8")
    ignored.write_text("ignore", encoding="utf-8")

    assert set(_discover_registry_metadata_files(root)) == {first, second}


def test_discover_registry_metadata_files_empty_folder_returns_empty_list(tmp_path):
    assert _discover_registry_metadata_files(tmp_path) == []


def test_discover_registry_metadata_files_ignores_non_json_file(tmp_path):
    path = tmp_path / "artifact.txt"
    path.write_text("not json", encoding="utf-8")

    assert _discover_registry_metadata_files(path) == []


def test_parse_invalid_json_does_not_break(tmp_path):
    path = tmp_path / "autoruns.json"
    path.write_text("{invalid json", encoding="utf-8")

    with pytest.warns(RuntimeWarning, match="invalid Registry metadata"):
        assert parse(tmp_path) == []


def test_parse_valid_metadata_generates_registry_event(tmp_path):
    source_path = tmp_path / "autoruns.json"
    _write_registry_metadata(source_path, [_sample_entry()])

    events = parse(tmp_path)

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CommonEvent)
    assert event.source_artifact == "Registry"
    assert event.event_category == "persistence"
    assert event.event_action == "registry_autorun_configured"
    assert "HKCU" in event.object
    assert "Software\\Microsoft\\Windows\\CurrentVersion\\Run" in event.object
    assert "ExampleApp" in event.object
    assert event.timestamp_utc.tzinfo is not None
    assert event.timestamp_utc.utcoffset() is not None
    assert event.raw_evidence["value_name"] == "ExampleApp"
    assert event.raw_evidence["value_data"] == "C:\\Tools\\ExampleApp.exe"
    assert event.raw_evidence["key_path"] == "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    assert event.provenance["registry_hive"] == "HKCU"
    assert event.provenance["registry_key_path"] == "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    assert event.provenance["registry_value_name"] == "ExampleApp"
    assert event.provenance["timestamp_field"] == "last_write_time_utc"
    assert event.scenario_id == "S_REGISTRY_SYNTH"


def test_event_from_registry_entry_without_timestamp_returns_none(tmp_path):
    entry = _sample_entry(last_write_time_utc=None)

    with pytest.warns(RuntimeWarning, match="missing forensic timestamp"):
        assert _event_from_registry_entry(entry, tmp_path / "autoruns.json", {}) is None


def test_select_registry_timestamp_uses_timestamp_utc_fallback():
    timestamp = _select_registry_timestamp({"timestamp_utc": "2024-01-10T09:30:00Z"})

    assert timestamp == datetime(2024, 1, 10, 9, 30, tzinfo=timezone.utc)


def test_parse_uses_timestamp_utc_when_last_write_time_missing(tmp_path):
    source_path = tmp_path / "autoruns.json"
    entry = _sample_entry(last_write_time_utc=None, timestamp_utc="2024-01-10T09:30:00Z")
    _write_registry_metadata(source_path, [entry])

    events = parse(source_path)

    assert len(events) == 1
    assert events[0].provenance["timestamp_field"] == "timestamp_utc"
    assert events[0].timestamp_utc == datetime(2024, 1, 10, 9, 30, tzinfo=timezone.utc)


def test_parse_propagates_metadata_scenario_id(tmp_path):
    source_path = tmp_path / "autoruns.json"
    entry = _sample_entry(scenario_id=None)
    _write_registry_metadata(source_path, [entry], scenario_id="S_METADATA")

    events = parse(source_path)

    assert events[0].scenario_id == "S_METADATA"


def test_parse_respects_max_files(tmp_path):
    first = tmp_path / "a.json"
    second = tmp_path / "b.json"
    _write_registry_metadata(first, [_sample_entry(value_name="FirstApp")])
    _write_registry_metadata(second, [_sample_entry(value_name="SecondApp")])

    assert len(parse(tmp_path, max_files=1)) == 1


def test_generate_sample_registry_metadata_creates_autoruns_json(tmp_path):
    output_dir = tmp_path / "registry" / "sample"

    output_path = generate_sample_registry_metadata(output_dir=output_dir, overwrite=True)

    assert output_path == output_dir / "autoruns.json"
    assert output_path.exists()
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["parser_backend"] == "external_registry_json"
    assert len(loaded["entries"]) == 2


def test_pipeline_processes_synthetic_registry_metadata(tmp_path):
    evidence_root = tmp_path / "evidence"
    output_root = tmp_path / "output"
    generate_sample_registry_metadata(output_dir=evidence_root / "registry" / "sample", overwrite=True)

    result = run_pipeline(evidence_root, output_root)

    registry_events = [event for event in result["events"] if event.source_artifact == "Registry"]
    assert len(registry_events) == 2
    assert {event.raw_evidence["value_name"] for event in registry_events} == {"ExampleApp", "UpdaterTask"}
    assert (output_root / "events.json").exists()

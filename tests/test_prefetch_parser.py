import json
from datetime import datetime, timezone

import pytest

from core.event_model import CommonEvent
from main import run_pipeline
from parsers import prefetch_parser
from parsers.prefetch_parser import (
    _discover_prefetch_files,
    _event_from_prefetch_metadata,
    _select_primary_last_run_time,
    parse,
)
from scripts.generate_sample_prefetch_metadata import generate_sample_prefetch_metadata


def test_discover_prefetch_files_finds_pf_recursively(tmp_path):
    root = tmp_path / "prefetch"
    nested = root / "nested"
    nested.mkdir(parents=True)
    first = root / "NOTEPAD.EXE-11111111.pf"
    second = nested / "CALC.EXE-22222222.PF"
    ignored = nested / "not_prefetch.txt"
    first.write_bytes(b"PF")
    second.write_bytes(b"PF")
    ignored.write_text("ignore", encoding="utf-8")

    assert set(_discover_prefetch_files(root)) == {first, second}


def test_discover_prefetch_files_empty_folder_returns_empty_list(tmp_path):
    assert _discover_prefetch_files(tmp_path) == []


def test_discover_prefetch_files_ignores_non_pf_file(tmp_path):
    path = tmp_path / "artifact.txt"
    path.write_text("not pf", encoding="utf-8")

    assert _discover_prefetch_files(path) == []


def test_event_from_prefetch_metadata_generates_common_event(tmp_path):
    source_path = tmp_path / "NOTEPAD.EXE-12345678.pf"
    metadata = {
        "executable_name": "notepad.exe",
        "prefetch_hash": "12345678",
        "run_count": 4,
        "last_run_time_utc": datetime(2026, 6, 20, 10, 0, tzinfo=timezone.utc),
        "last_run_times_utc": [
            datetime(2026, 6, 19, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 6, 20, 10, 0, tzinfo=timezone.utc),
        ],
        "volume_information": [{"path": "\\\\VOLUME"}],
        "referenced_files": ["C:\\Windows\\System32\\notepad.exe"],
        "parser_backend": "synthetic-test",
        "prefetch_version": 30,
    }

    event = _event_from_prefetch_metadata(metadata, source_path)

    assert isinstance(event, CommonEvent)
    assert event.source_artifact == "Prefetch"
    assert event.event_category == "program_execution"
    assert event.event_action == "program_executed"
    assert event.object == "notepad.exe"
    assert event.timestamp_utc.tzinfo is not None
    assert event.timestamp_utc.utcoffset() is not None
    assert event.raw_evidence["run_count"] == 4
    assert event.raw_evidence["executable_name"] == "notepad.exe"
    assert event.provenance["parser_backend"] == "synthetic-test"
    assert event.provenance["timestamp_field"] == "last_run_time"


def test_event_from_prefetch_metadata_without_timestamp_returns_none(tmp_path):
    metadata = {
        "executable_name": "notepad.exe",
        "run_count": 4,
        "parser_backend": "synthetic-test",
    }

    with pytest.warns(RuntimeWarning, match="missing execution timestamp"):
        assert _event_from_prefetch_metadata(metadata, tmp_path / "NOTEPAD.EXE-12345678.pf") is None


def test_select_primary_last_run_time_uses_most_recent_run_time():
    older = datetime(2026, 6, 20, 8, 0, tzinfo=timezone.utc)
    newer = datetime(2026, 6, 20, 9, 0, tzinfo=timezone.utc)
    metadata = {"last_run_times_utc": [older, newer]}

    assert _select_primary_last_run_time(metadata) == newer


def test_parse_invalid_pf_without_backend_does_not_break(tmp_path, monkeypatch):
    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", None)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", "backend unavailable")
    pf_path = tmp_path / "INVALID.EXE-12345678.pf"
    pf_path.write_bytes(b"not a real prefetch")

    with pytest.warns(RuntimeWarning, match="backend unavailable"):
        assert parse(tmp_path) == []


def test_parse_respects_max_files_with_synthetic_backend(tmp_path, monkeypatch):
    first = tmp_path / "A.EXE-11111111.pf"
    second = tmp_path / "B.EXE-22222222.pf"
    first.write_bytes(b"PF")
    second.write_bytes(b"PF")

    def fake_backend(path):
        return {
            "name": "tool.exe",
            "exec_count": 1,
            "last_exec_time": "2026-06-20 10:00:00",
            "prefetch_hash": "ABC",
            "format_version": 30,
        }

    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", fake_backend)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", None)

    assert len(parse(tmp_path, max_files=1)) == 1


def test_parse_backend_without_backend_name_defaults_to_prefetch_parser(tmp_path, monkeypatch):
    pf_path = tmp_path / "NOTEPAD.EXE-12345678.pf"
    pf_path.write_bytes(b"PF")

    def fake_backend(path):
        return {
            "name": "NOTEPAD.EXE",
            "exec_count": 1,
            "last_exec_time": "2026-06-20 10:00:00",
            "prefetch_hash": "12345678",
            "format_version": 30,
        }

    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", fake_backend)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", None)

    events = parse(tmp_path)

    assert len(events) == 1
    assert events[0].raw_evidence["parser_backend"] == "prefetch-parser"
    assert events[0].provenance["parser_backend"] == "prefetch-parser"


def test_pipeline_still_runs_with_empty_prefetch_folder(tmp_path):
    evidence_root = tmp_path / "evidence"
    output_root = tmp_path / "output"
    (evidence_root / "prefetch").mkdir(parents=True)

    result = run_pipeline(evidence_root, output_root)

    assert result["parser_errors"] == []
    assert (output_root / "events.json").exists()


def test_parse_generates_prefetch_event_from_valid_json_sidecar(tmp_path, monkeypatch):
    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", None)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", "backend unavailable")
    pf_path = tmp_path / "NOTEPAD.EXE-12345678.pf"
    sidecar_path = tmp_path / "NOTEPAD.EXE-12345678.json"
    pf_path.write_bytes(b"placeholder")
    sidecar_path.write_text(
        json.dumps(
            {
                "executable_name": "NOTEPAD.EXE",
                "prefetch_hash": "12345678",
                "run_count": 1,
                "last_run_time_utc": "2026-06-20T14:05:00Z",
                "last_run_times_utc": ["2026-06-20T14:05:00Z"],
                "volume_information": [],
                "referenced_files": [],
                "parser_backend": "external_metadata_json",
                "prefetch_version": "unknown",
            }
        ),
        encoding="utf-8",
    )

    events = parse(tmp_path)

    assert len(events) == 1
    event = events[0]
    assert event.source_artifact == "Prefetch"
    assert event.raw_evidence["parser_backend"] == "external_metadata_json"
    assert event.event_category == "program_execution"
    assert event.event_action == "program_executed"
    assert event.object == "NOTEPAD.EXE"


def test_parse_invalid_json_sidecar_returns_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", None)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", "backend unavailable")
    (tmp_path / "NOTEPAD.EXE-12345678.pf").write_bytes(b"placeholder")
    (tmp_path / "NOTEPAD.EXE-12345678.json").write_text("{invalid json", encoding="utf-8")

    with pytest.warns(RuntimeWarning, match="invalid Prefetch sidecar"):
        assert parse(tmp_path) == []


def test_parse_sidecar_without_timestamp_generates_no_event(tmp_path, monkeypatch):
    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", None)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", "backend unavailable")
    (tmp_path / "NOTEPAD.EXE-12345678.pf").write_bytes(b"placeholder")
    (tmp_path / "NOTEPAD.EXE-12345678.json").write_text(
        json.dumps({"executable_name": "NOTEPAD.EXE", "run_count": 1}),
        encoding="utf-8",
    )

    with pytest.warns(RuntimeWarning, match="missing execution timestamp"):
        assert parse(tmp_path) == []


def test_parse_pf_without_sidecar_and_without_backend_generates_no_event(tmp_path, monkeypatch):
    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", None)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", "backend unavailable")
    (tmp_path / "NOTEPAD.EXE-12345678.pf").write_bytes(b"placeholder")

    with pytest.warns(RuntimeWarning, match="no JSON sidecar found"):
        assert parse(tmp_path) == []


def test_generate_sample_prefetch_metadata_creates_two_pf_and_two_json_files(tmp_path):
    output_dir = tmp_path / "prefetch" / "sample"

    sidecars = generate_sample_prefetch_metadata(output_dir=output_dir, overwrite=True)

    assert len(sidecars) == 2
    assert len(list(output_dir.glob("*.pf"))) == 2
    assert len(list(output_dir.glob("*.json"))) == 2
    assert (output_dir / "NOTEPAD.EXE-12345678.pf").exists()
    assert (output_dir / "NOTEPAD.EXE-12345678.json").exists()
    assert (output_dir / "POWERSHELL.EXE-87654321.pf").exists()
    assert (output_dir / "POWERSHELL.EXE-87654321.json").exists()


def test_parse_generated_sample_prefetch_metadata_returns_two_events(tmp_path, monkeypatch):
    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", None)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", "backend unavailable")
    output_dir = tmp_path / "prefetch" / "sample"
    generate_sample_prefetch_metadata(output_dir=output_dir, overwrite=True)

    events = parse(output_dir)

    assert len(events) == 2
    assert {event.object for event in events} == {"NOTEPAD.EXE", "POWERSHELL.EXE"}


def test_pipeline_processes_synthetic_prefetch_sidecars(tmp_path, monkeypatch):
    monkeypatch.setattr(prefetch_parser, "_BACKEND_CHECKED", True)
    monkeypatch.setattr(prefetch_parser, "_PREFETCH2JSON", None)
    monkeypatch.setattr(prefetch_parser, "_BACKEND_IMPORT_ERROR", "backend unavailable")
    evidence_root = tmp_path / "evidence"
    output_root = tmp_path / "output"
    generate_sample_prefetch_metadata(output_dir=evidence_root / "prefetch" / "sample", overwrite=True)

    result = run_pipeline(evidence_root, output_root)

    prefetch_events = [event for event in result["events"] if event.source_artifact == "Prefetch"]
    assert len(prefetch_events) == 2
    assert (output_root / "events.json").exists()

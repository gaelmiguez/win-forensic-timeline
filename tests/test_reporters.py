import csv
import json
from datetime import datetime, timezone

from core.event_model import CommonEvent
from correlator.timeline_correlator import build_timeline
from reporters.csv_reporter import export_timeline_csv
from reporters.json_reporter import export_events_json, export_events_jsonl
from reporters.markdown_reporter import generate_markdown_report


def make_event():
    return CommonEvent.create(
        timestamp_utc=datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
        timestamp_local=None,
        timestamp_type="created",
        source_artifact="browser",
        source_location="evidence/browser/history.sqlite",
        event_category="browser_history",
        event_action="visit",
        object="https://example.com",
        description="Visited example.com",
        raw_evidence={"url": "https://example.com"},
        parser_module="parsers.browser_history_parser",
        traceability_ref="browser:history:1",
        confidence=0.8,
        provenance={"test": True},
    )


def test_reporters_generate_expected_files(tmp_path):
    events = [make_event()]
    df = build_timeline(events)

    csv_path = export_timeline_csv(df, tmp_path / "timeline.csv")
    json_path = export_events_json(events, tmp_path / "events.json")
    jsonl_path = export_events_jsonl(events, tmp_path / "events.jsonl")
    markdown_path = generate_markdown_report(events, df, tmp_path / "report.md")

    assert csv_path.exists()
    assert json_path.exists()
    assert jsonl_path.exists()
    assert markdown_path.exists()
    assert "Total de eventos: 1" in markdown_path.read_text(encoding="utf-8")


def test_csv_reporter_serializes_complex_fields_as_json(tmp_path):
    events = [make_event()]
    df = build_timeline(events)

    csv_path = export_timeline_csv(df, tmp_path / "timeline.csv")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert json.loads(row["raw_evidence"]) == {"url": "https://example.com"}
    assert json.loads(row["provenance"]) == {"test": True}

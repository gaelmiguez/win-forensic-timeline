from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone

from gui.config import CANONICAL_EVENT_FIELDS
from gui.models import FilterCriteria
from gui.services.export_service import (
    build_export,
    build_filter_manifest,
    canonical_records,
)


def test_canonical_records_have_exactly_sixteen_fields(event_frame):
    records = canonical_records(event_frame)

    assert tuple(records[0]) == CANONICAL_EVENT_FIELDS
    assert len(records[0]) == 16
    assert not any(key.startswith("_ui_") for key in records[0])


def test_json_and_jsonl_exports_preserve_unicode(event_frame):
    json_payload = build_export(event_frame, "json")
    jsonl_payload = build_export(event_frame, "jsonl")

    assert len(json.loads(json_payload.content.decode("utf-8"))) == 3
    assert len(jsonl_payload.content.decode("utf-8").strip().splitlines()) == 3
    assert "Ejecución" in json_payload.content.decode("utf-8")


def test_csv_export_contains_canonical_header(event_frame):
    payload = build_export(event_frame, "csv")
    rows = list(csv.DictReader(io.StringIO(payload.content.decode("utf-8-sig"))))

    assert tuple(rows[0]) == CANONICAL_EVENT_FIELDS
    assert len(rows) == 3


def test_empty_export_is_valid(event_frame):
    payload = build_export(event_frame.iloc[0:0], "json")

    assert json.loads(payload.content.decode("utf-8")) == []
    assert payload.record_count == 0


def test_manifest_masks_full_output_path():
    payload = build_filter_manifest(
        FilterCriteria(text="notepad"),
        r"C:\controlled\output\run-01",
        10,
        2,
        datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    manifest = json.loads(payload.content.decode("utf-8"))

    assert manifest["source_output_root"] == "run-01"
    assert "controlled" not in payload.content.decode("utf-8")
    assert manifest["filters"]["text"] == "notepad"

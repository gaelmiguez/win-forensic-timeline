from __future__ import annotations

import csv

import pandas as pd

from gui.config import CANONICAL_EVENT_FIELDS
from gui.models import LoadStatus
from gui.services.timeline_repository import load_timeline


def timeline_row(canonical_event):
    row = dict(canonical_event)
    row["timestamp_local"] = ""
    row["raw_evidence"] = '{"url": "https://example.com/"}'
    row["provenance"] = '{"parser": "browser_history_parser"}'
    return row


def write_csv(path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_loads_valid_timeline(tmp_path, canonical_event):
    path = tmp_path / "timeline.csv"
    write_csv(path, CANONICAL_EVENT_FIELDS, [timeline_row(canonical_event)])

    result = load_timeline(path)

    assert result.status is LoadStatus.SUCCESS
    assert result.records_accepted == 1
    assert result.data.iloc[0]["_ui_raw_evidence"]["url"] == "https://example.com/"


def test_empty_csv_without_header_is_error(tmp_path):
    path = tmp_path / "timeline.csv"
    path.write_text("", encoding="utf-8")

    result = load_timeline(path)

    assert result.status is LoadStatus.ERROR
    assert result.issues[0].code == "timeline_empty_file"


def test_header_only_csv_is_empty(tmp_path):
    path = tmp_path / "timeline.csv"
    write_csv(path, CANONICAL_EVENT_FIELDS, [])

    result = load_timeline(path)

    assert result.status is LoadStatus.EMPTY
    assert result.records_read == 0


def test_missing_required_column_is_error(tmp_path, canonical_event):
    path = tmp_path / "timeline.csv"
    fields = [field for field in CANONICAL_EVENT_FIELDS if field != "event_id"]
    row = timeline_row(canonical_event)
    row.pop("event_id")
    write_csv(path, fields, [row])

    result = load_timeline(path)

    assert result.issues[0].code == "timeline_missing_columns"
    assert result.records_rejected == 1


def test_additional_column_is_preserved_with_warning(tmp_path, canonical_event):
    path = tmp_path / "timeline.csv"
    row = timeline_row(canonical_event)
    row["extension"] = "kept"
    write_csv(path, (*CANONICAL_EVENT_FIELDS, "extension"), [row])

    result = load_timeline(path)

    assert result.data.iloc[0]["extension"] == "kept"
    assert any(issue.code == "timeline_extra_columns" for issue in result.issues)


def test_invalid_timestamp_is_preserved_but_not_parsed(tmp_path, canonical_event):
    path = tmp_path / "timeline.csv"
    row = timeline_row(canonical_event)
    row["timestamp_utc"] = "invalid"
    write_csv(path, CANONICAL_EVENT_FIELDS, [row])

    result = load_timeline(path)

    assert result.data.iloc[0]["timestamp_utc"] == "invalid"
    assert pd.isna(result.data.iloc[0]["_ui_timestamp_utc"])
    assert any(issue.code == "timeline_invalid_timestamp" for issue in result.issues)


def test_invalid_serialized_json_warns_and_preserves_text(tmp_path, canonical_event):
    path = tmp_path / "timeline.csv"
    row = timeline_row(canonical_event)
    row["raw_evidence"] = "{invalid"
    write_csv(path, CANONICAL_EVENT_FIELDS, [row])

    result = load_timeline(path)

    assert result.data.iloc[0]["raw_evidence"] == "{invalid"
    assert result.data.iloc[0]["_ui_raw_evidence"] is None
    assert any(
        issue.code == "timeline_invalid_serialized_json" for issue in result.issues
    )


def test_path_with_spaces_is_supported(tmp_path, canonical_event):
    folder = tmp_path / "output con espacios"
    folder.mkdir()
    path = folder / "timeline.csv"
    write_csv(path, CANONICAL_EVENT_FIELDS, [timeline_row(canonical_event)])

    assert load_timeline(path).records_accepted == 1

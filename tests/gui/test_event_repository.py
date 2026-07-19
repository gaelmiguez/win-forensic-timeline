from __future__ import annotations

import json
from copy import deepcopy

import pandas as pd

from gui.models import LoadStatus
from gui.services.event_repository import load_events


def write_events(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_loads_valid_event_with_all_16_keys(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    write_events(path, [canonical_event])

    result = load_events(path)

    assert result.status is LoadStatus.SUCCESS
    assert result.records_accepted == 1
    assert result.data.iloc[0]["event_id"] == "event-001"
    assert str(result.data["_ui_timestamp_utc"].dt.tz) == "UTC"


def test_missing_file_returns_error(tmp_path):
    result = load_events(tmp_path / "events.json")

    assert result.status is LoadStatus.ERROR
    assert result.issues[0].code == "events_file_not_found"


def test_empty_file_returns_invalid_json(tmp_path):
    path = tmp_path / "events.json"
    path.write_text("", encoding="utf-8")

    result = load_events(path)

    assert result.status is LoadStatus.ERROR
    assert result.issues[0].code == "events_invalid_json"


def test_malformed_json_is_controlled(tmp_path):
    path = tmp_path / "events.json"
    path.write_text("[{", encoding="utf-8")

    assert load_events(path).issues[0].code == "events_invalid_json"


def test_non_list_root_is_rejected(tmp_path):
    path = tmp_path / "events.json"
    write_events(path, {"events": []})

    assert load_events(path).issues[0].code == "events_invalid_root"


def test_missing_canonical_key_rejects_row(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    event = deepcopy(canonical_event)
    event.pop("traceability_ref")
    write_events(path, [event])

    result = load_events(path)

    assert result.records_rejected == 1
    assert result.status is LoadStatus.ERROR
    assert result.issues[0].row_index == 0


def test_unknown_field_is_preserved_with_warning(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    event = deepcopy(canonical_event)
    event["future_extension"] = "kept"
    write_events(path, [event])

    result = load_events(path)

    assert result.data.iloc[0]["future_extension"] == "kept"
    assert any(issue.code == "event_unknown_fields" for issue in result.issues)


def test_invalid_timestamp_rejects_event(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    event = deepcopy(canonical_event)
    event["timestamp_utc"] = "not-a-date"
    write_events(path, [event])

    result = load_events(path)

    assert result.records_rejected == 1
    assert any(issue.code == "event_invalid_timestamp_utc" for issue in result.issues)


def test_duplicate_event_id_rejects_second_row(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    write_events(path, [canonical_event, canonical_event])

    result = load_events(path)

    assert result.status is LoadStatus.PARTIAL
    assert result.records_accepted == 1
    assert result.records_rejected == 1
    assert any(issue.code == "event_duplicate_id" for issue in result.issues)


def test_complex_raw_evidence_is_preserved(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    event = deepcopy(canonical_event)
    event["raw_evidence"] = {"nested": [{"value": "áéí"}], "count": 2}
    write_events(path, [event])

    result = load_events(path)

    assert result.data.iloc[0]["raw_evidence"]["nested"][0]["value"] == "áéí"


def test_empty_provenance_is_accepted_with_warning(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    event = deepcopy(canonical_event)
    event["provenance"] = {}
    write_events(path, [event])

    result = load_events(path)

    assert result.records_accepted == 1
    assert any(issue.code == "event_empty_provenance" for issue in result.issues)


def test_partial_load_accounts_for_valid_and_invalid_rows(tmp_path, canonical_event):
    path = tmp_path / "events.json"
    invalid = deepcopy(canonical_event)
    invalid["event_id"] = "event-invalid"
    invalid["timestamp_utc"] = "invalid"
    write_events(path, [canonical_event, invalid])

    result = load_events(path)

    assert (result.records_read, result.records_accepted, result.records_rejected) == (
        2,
        1,
        1,
    )
    assert result.status is LoadStatus.PARTIAL


def test_empty_list_is_a_valid_empty_dataset(tmp_path):
    path = tmp_path / "events.json"
    write_events(path, [])

    result = load_events(path)

    assert result.status is LoadStatus.EMPTY
    assert isinstance(result.data, pd.DataFrame)

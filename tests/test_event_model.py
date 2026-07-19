from datetime import datetime, timezone

import pytest

from core.event_model import CommonEvent
from core.exceptions import EventValidationError


def make_event(**overrides):
    data = {
        "timestamp_utc": datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
        "timestamp_local": None,
        "timestamp_type": "created",
        "source_artifact": "evtx",
        "source_location": "evidence/evtx/sample.evtx",
        "event_category": "authentication",
        "event_action": "logon",
        "object": "user@example",
        "description": "Sample normalized event",
        "raw_evidence": {"event_id": 4624},
        "parser_module": "parsers.evtx_parser",
        "traceability_ref": "evtx:sample:1",
        "confidence": 0.95,
        "provenance": {"parser": "stub"},
        "scenario_id": "scenario-001",
    }
    data.update(overrides)
    return CommonEvent.create(**data)


def test_create_valid_common_event_generates_event_id():
    event = make_event()

    assert event.event_id
    assert isinstance(event.event_id, str)


def test_to_dict_converts_datetimes_to_iso_8601():
    event = make_event()

    data = event.to_dict()

    assert data["timestamp_utc"] == "2024-01-01T12:00:00+00:00"
    assert data["timestamp_local"] is None


def test_naive_timestamp_utc_fails():
    with pytest.raises(EventValidationError, match="timezone-aware"):
        make_event(timestamp_utc=datetime(2024, 1, 1, 12, 0))


def test_naive_timestamp_local_fails():
    with pytest.raises(EventValidationError, match="timestamp_local must be timezone-aware"):
        make_event(timestamp_local=datetime(2024, 1, 1, 13, 0))


def test_aware_timestamp_local_is_valid():
    event = make_event(timestamp_local=datetime(2024, 1, 1, 13, 0, tzinfo=timezone.utc))

    assert event.timestamp_local == datetime(2024, 1, 1, 13, 0, tzinfo=timezone.utc)


def test_confidence_out_of_range_fails():
    with pytest.raises(EventValidationError, match="between 0 and 1"):
        make_event(confidence=1.5)

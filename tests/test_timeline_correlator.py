from datetime import datetime, timezone

import pytest

from core.event_model import CommonEvent
from correlator.timeline_correlator import build_timeline


def make_event(timestamp_utc):
    return CommonEvent.create(
        timestamp_utc=timestamp_utc,
        timestamp_local=None,
        timestamp_type="created",
        source_artifact="evtx",
        source_location="evidence/evtx/sample.evtx",
        event_category="system",
        event_action="observed",
        object=None,
        description="Sample event",
        raw_evidence={},
        parser_module="parsers.evtx_parser",
        traceability_ref=f"ref:{timestamp_utc}",
        confidence=0.9,
        provenance={"test": True},
    )


def test_build_timeline_sorts_events_by_timestamp_utc():
    later = make_event(datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc))
    earlier = make_event(datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc))

    df = build_timeline([later, earlier])

    assert list(df["event_id"]) == [earlier.event_id, later.event_id]


def test_build_timeline_accepts_mixed_iso_precision():
    with_microseconds = make_event(datetime(2024, 1, 1, 10, 0, 0, 123456, tzinfo=timezone.utc))
    without_microseconds = make_event(datetime(2024, 1, 1, 10, 1, 0, tzinfo=timezone.utc))

    df = build_timeline([without_microseconds, with_microseconds])

    assert list(df["event_id"]) == [with_microseconds.event_id, without_microseconds.event_id]


def test_build_timeline_with_empty_list():
    df = build_timeline([])

    assert df.empty
    assert "timestamp_utc" in df.columns


def test_build_timeline_rejects_forced_naive_timestamp():
    event = make_event(datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc))
    event.timestamp_utc = datetime(2024, 1, 1, 12, 0)

    with pytest.raises(ValueError, match="naive timestamps are not accepted"):
        build_timeline([event])

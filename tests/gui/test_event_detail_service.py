from __future__ import annotations

from gui.services.event_detail_service import (
    event_has_traceability,
    find_event,
    is_reliably_synthetic,
    mask_path,
)


def test_find_event_returns_selected_record(event_frame):
    event = find_event(event_frame, "event-002")

    assert event is not None
    assert event["object"] == "NOTEPAD.EXE"


def test_find_event_handles_missing_identifier(event_frame):
    assert find_event(event_frame, "missing") is None


def test_mask_path_hides_parent_components():
    assert mask_path(r"C:\controlled\evidence\sample.evtx") == ".../sample.evtx"
    assert mask_path(r"C:\controlled\evidence\sample.evtx", True).startswith("C:")


def test_traceability_requires_reference_and_provenance(event_frame):
    assert event_has_traceability(find_event(event_frame, "event-001"))
    assert not event_has_traceability(find_event(event_frame, "event-003"))


def test_synthetic_classification_requires_explicit_scenario(event_frame):
    assert is_reliably_synthetic(find_event(event_frame, "event-002"))
    event = find_event(event_frame, "event-001")
    event["scenario_id"] = "default"
    assert not is_reliably_synthetic(event)

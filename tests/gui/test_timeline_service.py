from __future__ import annotations

import pandas as pd

from gui.services.timeline_service import build_timeline_view


def test_timeline_uses_detailed_mode_below_limit(event_frame):
    view = build_timeline_view(event_frame, detailed_limit=10)

    assert view.mode == "detailed"
    assert view.valid_timestamps == 2
    assert view.invalid_timestamps == 1
    assert len(view.data) == 2


def test_timeline_uses_aggregated_mode_above_limit(event_frame):
    view = build_timeline_view(event_frame, "hora", detailed_limit=1)

    assert view.mode == "aggregated"
    assert view.granularity == "hora"
    assert view.data["events"].sum() == 2


def test_timeline_handles_missing_timestamp_column():
    frame = pd.DataFrame({"source_artifact": ["EVTX"]})
    view = build_timeline_view(frame)

    assert view.mode == "detailed"
    assert view.valid_timestamps == 0
    assert view.invalid_timestamps == 1


def test_timeline_does_not_modify_input(event_frame):
    original = event_frame.copy(deep=True)
    build_timeline_view(event_frame)

    pd.testing.assert_frame_equal(event_frame, original)

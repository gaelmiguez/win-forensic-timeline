from __future__ import annotations

import pandas as pd

from gui.models import FilterCriteria
from gui.services.dashboard_service import aggregate_temporal
from gui.services.filter_service import filter_events


def test_vectorized_filter_and_aggregation_handle_100k_rows():
    size = 100_000
    frame = pd.DataFrame(
        {
            "timestamp_utc": pd.date_range(
                "2024-01-01", periods=size, freq="s", tz="UTC"
            ),
            "source_artifact": ["EVTX", "BrowserHistory"] * (size // 2),
            "event_category": "system_event",
            "event_action": "windows_event",
            "parser_module": "test_parser",
            "scenario_id": None,
            "object": "Application:1",
            "description": "controlled performance row",
            "traceability_ref": "row:1",
            "provenance": [{"parser": "test"}] * size,
            "confidence": 0.8,
        }
    )
    result = filter_events(
        frame, FilterCriteria(source_artifacts=("BrowserHistory",), text="controlled")
    )
    aggregated = aggregate_temporal(result.data, "hora")

    assert len(result.data) == 50_000
    assert aggregated["events"].sum() == 50_000

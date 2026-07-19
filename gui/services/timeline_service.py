"""Adaptive detailed and aggregated timeline views."""

from __future__ import annotations

import pandas as pd

from gui.config import DETAILED_TIMELINE_LIMIT
from gui.models import TimelineView
from gui.services.dashboard_service import (
    aggregate_temporal,
    choose_temporal_granularity,
)


def build_timeline_view(
    frame: pd.DataFrame,
    granularity: str | None = None,
    detailed_limit: int = DETAILED_TIMELINE_LIMIT,
) -> TimelineView:
    """Return one event per point or an explicitly aggregated view."""
    timestamp_column = (
        "_ui_timestamp_utc" if "_ui_timestamp_utc" in frame else "timestamp_utc"
    )
    timestamps = (
        pd.to_datetime(frame[timestamp_column], errors="coerce", utc=True)
        if timestamp_column in frame
        else pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")
    )
    valid_mask = timestamps.notna()
    valid_count = int(valid_mask.sum())
    invalid_count = int((~valid_mask).sum())
    valid = frame.loc[valid_mask].copy(deep=True)
    valid["_ui_timestamp_utc"] = timestamps.loc[valid_mask]

    if valid_count <= detailed_limit:
        return TimelineView(
            mode="detailed",
            data=valid.sort_values("_ui_timestamp_utc", kind="stable").reset_index(
                drop=True
            ),
            granularity=None,
            valid_timestamps=valid_count,
            invalid_timestamps=invalid_count,
        )

    selected = granularity or choose_temporal_granularity(valid)
    return TimelineView(
        mode="aggregated",
        data=aggregate_temporal(valid, selected),
        granularity=selected,
        valid_timestamps=valid_count,
        invalid_timestamps=invalid_count,
    )

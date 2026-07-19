"""Deterministic sorting and pagination for event tables."""

from __future__ import annotations

from math import ceil

import pandas as pd

from gui.models import PageSlice


SORTABLE_COLUMNS = {
    "timestamp_utc",
    "source_artifact",
    "event_category",
    "event_action",
    "confidence",
}


def paginate_events(
    frame: pd.DataFrame,
    page: int = 1,
    page_size: int = 50,
    sort_column: str = "timestamp_utc",
    ascending: bool = True,
) -> PageSlice:
    """Return a clamped page without modifying the source DataFrame."""
    if page_size <= 0:
        raise ValueError("page_size must be positive")
    working = frame.copy(deep=True)
    selected_sort = sort_column if sort_column in SORTABLE_COLUMNS else "timestamp_utc"
    internal_sort = (
        "_ui_timestamp_utc"
        if selected_sort == "timestamp_utc" and "_ui_timestamp_utc" in working
        else selected_sort
    )
    if internal_sort in working:
        if selected_sort == "confidence":
            working["_ui_sort_confidence"] = pd.to_numeric(
                working["confidence"], errors="coerce"
            )
            internal_sort = "_ui_sort_confidence"
        working = working.sort_values(
            internal_sort, ascending=ascending, na_position="last", kind="stable"
        )
    total_rows = len(working)
    total_pages = max(1, ceil(total_rows / page_size))
    current_page = min(max(int(page), 1), total_pages)
    start = (current_page - 1) * page_size
    data = working.iloc[start : start + page_size].copy(deep=True)
    data = data.drop(columns=["_ui_sort_confidence"], errors="ignore")
    return PageSlice(data, current_page, page_size, total_rows, total_pages)

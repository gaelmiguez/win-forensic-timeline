from __future__ import annotations

import pytest

from gui.services.pagination_service import paginate_events


def test_pagination_returns_requested_slice(event_frame):
    page = paginate_events(event_frame, page=2, page_size=2)

    assert page.page == 2
    assert page.total_pages == 2
    assert len(page.data) == 1


def test_pagination_clamps_page_outside_range(event_frame):
    page = paginate_events(event_frame, page=99, page_size=2)

    assert page.page == 2


def test_pagination_sorts_confidence_without_mutating_input(event_frame):
    original_columns = tuple(event_frame.columns)
    page = paginate_events(
        event_frame, page=1, page_size=3, sort_column="confidence", ascending=False
    )

    assert page.data.iloc[0]["confidence"] == 0.9
    assert tuple(event_frame.columns) == original_columns


def test_pagination_empty_dataset(event_frame):
    page = paginate_events(event_frame.iloc[0:0], page=4, page_size=25)

    assert page.page == 1
    assert page.total_pages == 1
    assert page.total_rows == 0


def test_pagination_rejects_invalid_page_size(event_frame):
    with pytest.raises(ValueError):
        paginate_events(event_frame, page_size=0)

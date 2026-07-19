from __future__ import annotations

import pandas as pd
import pytest

from gui.models import FilterCriteria
from gui.services.filter_service import (
    available_filter_values,
    confidence_by_source,
    count_traceable_events,
    filter_events,
)


@pytest.mark.parametrize(
    ("criteria", "expected_id"),
    [
        (FilterCriteria(source_artifacts=("Prefetch",)), "event-002"),
        (FilterCriteria(event_categories=("persistence",)), "event-003"),
        (FilterCriteria(event_actions=("url_visit",)), "event-001"),
        (FilterCriteria(parser_modules=("registry_parser",)), "event-003"),
        (FilterCriteria(scenario_ids=("S_PREFETCH_SYNTH",)), "event-002"),
    ],
)
def test_individual_value_filters(event_frame, criteria, expected_id):
    result = filter_events(event_frame, criteria)

    assert result.data["event_id"].tolist() == [expected_id]


def test_combined_filters(event_frame):
    criteria = FilterCriteria(
        source_artifacts=("BrowserHistory",),
        event_actions=("url_visit",),
        confidence_min=0.85,
    )

    assert filter_events(event_frame, criteria).data["event_id"].tolist() == [
        "event-001"
    ]


def test_text_search_is_case_insensitive(event_frame):
    result = filter_events(event_frame, FilterCriteria(text="notepad"))

    assert result.data["event_id"].tolist() == ["event-002"]


def test_temporal_range_is_inclusive_and_excludes_invalid(event_frame):
    result = filter_events(
        event_frame,
        FilterCriteria(
            start_utc="2024-01-10T09:00:00Z",
            end_utc="2024-01-10T09:05:00Z",
        ),
    )

    assert result.data["event_id"].tolist() == ["event-001", "event-002"]
    assert len(event_frame) == 3


def test_traceability_filter(event_frame):
    present = filter_events(event_frame, FilterCriteria(has_traceability=True))
    absent = filter_events(event_frame, FilterCriteria(has_traceability=False))

    assert present.data["event_id"].tolist() == ["event-001", "event-002"]
    assert absent.data["event_id"].tolist() == ["event-003"]


def test_confidence_interval_is_numeric(event_frame):
    result = filter_events(
        event_frame, FilterCriteria(confidence_min=0.8, confidence_max=0.86)
    )

    assert result.data["event_id"].tolist() == ["event-002"]


def test_input_dataframe_is_not_modified(event_frame):
    original = event_frame.copy(deep=True)

    filter_events(event_frame, FilterCriteria(text="example"))

    pd.testing.assert_frame_equal(event_frame, original)


def test_empty_dataset_is_supported():
    empty = pd.DataFrame()

    result = filter_events(empty, FilterCriteria(text="anything"))

    assert result.data.empty
    assert result.issues


def test_missing_column_produces_warning_without_failure(event_frame):
    frame = event_frame.drop(columns=["source_artifact"])

    result = filter_events(
        frame, FilterCriteria(source_artifacts=("BrowserHistory",))
    )

    assert len(result.data) == len(frame)
    assert result.issues[0].code == "filter_column_missing"


def test_available_values_are_sorted_and_ignore_empty(event_frame):
    values, issues = available_filter_values(event_frame)

    assert values["source_artifact"] == ["BrowserHistory", "Prefetch", "Registry"]
    assert not issues


def test_count_traceable_events(event_frame):
    count, issues = count_traceable_events(event_frame)

    assert count == 2
    assert not issues


def test_confidence_is_grouped_by_source_not_globally(event_frame):
    grouped, issues = confidence_by_source(event_frame)

    assert not issues
    assert set(grouped["source_artifact"]) == {
        "BrowserHistory",
        "Prefetch",
        "Registry",
    }
    assert "mean_confidence" not in grouped.columns

import csv
import json
from datetime import datetime, timezone

import pytest

from validation.validator import (
    find_best_match,
    load_events,
    load_ground_truth,
    object_matches,
    parse_utc_datetime,
    validate_events,
    write_report_md,
    write_results_csv,
    write_summary_json,
)


def event(
    event_id="E1",
    timestamp_utc="2024-01-10T09:00:00+00:00",
    source_artifact="BrowserHistory",
    event_action="url_visit",
    object_value="https://example.com/",
    description=None,
    raw_evidence=None,
    provenance=None,
    confidence=0.9,
):
    return {
        "event_id": event_id,
        "timestamp_utc": timestamp_utc,
        "source_artifact": source_artifact,
        "event_action": event_action,
        "object": object_value,
        "description": description if description is not None else f"Visited {object_value}",
        "raw_evidence": raw_evidence if raw_evidence is not None else {"url": object_value},
        "provenance": provenance if provenance is not None else {"parser": "test"},
        "confidence": confidence,
    }


def gt(
    gt_id="GT001",
    start_time_utc="2024-01-10T09:00:00Z",
    expected_object="https://example.com/",
    expected_sources="BrowserHistory",
    tolerance_seconds="5",
    action="url_visit",
):
    return {
        "gt_id": gt_id,
        "scenario_id": "S_TEST",
        "action": action,
        "expected_object": expected_object,
        "start_time_utc": start_time_utc,
        "tolerance_seconds": tolerance_seconds,
        "expected_sources": expected_sources,
    }


def test_load_events_from_json(tmp_path):
    path = tmp_path / "events.json"
    path.write_text(json.dumps([event()]), encoding="utf-8")

    assert load_events(path)[0]["event_id"] == "E1"


def test_load_ground_truth_from_csv(tmp_path):
    path = tmp_path / "ground_truth.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=gt().keys())
        writer.writeheader()
        writer.writerow(gt())

    assert load_ground_truth(path)[0]["gt_id"] == "GT001"


def test_correct_event_by_source_object_and_time():
    results, summary = validate_events([event()], [gt()])

    assert results[0]["result"] == "correcto"
    assert summary["correct"] == 1


def test_not_detected_when_outside_tolerance():
    late_event = event(timestamp_utc="2024-01-10T09:01:00+00:00")

    results, summary = validate_events([late_event], [gt(tolerance_seconds="5")])

    assert results[0]["result"] == "no_detectado"
    assert summary["not_detected"] == 1


def test_partial_when_time_and_source_match_but_object_does_not():
    other_event = event(object_value="https://other.example/", raw_evidence={"url": "https://other.example/"})

    results, summary = validate_events([other_event], [gt(expected_object="https://example.com/")])

    assert results[0]["result"] == "parcial"
    assert summary["partial"] == 1


def test_selects_candidate_with_smallest_time_delta():
    events = [
        event(event_id="E_FAR", timestamp_utc="2024-01-10T09:00:04+00:00"),
        event(event_id="E_NEAR", timestamp_utc="2024-01-10T09:00:01+00:00"),
    ]

    match, status = find_best_match(gt(tolerance_seconds="10"), events, set())

    assert status == "correcto"
    assert match["event_id"] == "E_NEAR"


def test_does_not_reuse_event_when_alternative_exists():
    events = [
        event(event_id="E1", timestamp_utc="2024-01-10T09:00:00+00:00"),
        event(event_id="E2", timestamp_utc="2024-01-10T09:00:01+00:00"),
    ]
    ground_truth = [
        gt(gt_id="GT001", tolerance_seconds="10"),
        gt(gt_id="GT002", tolerance_seconds="10"),
    ]

    results, _ = validate_events(events, ground_truth)

    assert results[0]["matched_event_id"] == "E1"
    assert results[1]["matched_event_id"] == "E2"


def test_calculates_coverage_rate():
    results, summary = validate_events([event()], [gt(), gt(gt_id="GT002", start_time_utc="2024-01-10T10:00:00Z")])

    assert results[1]["result"] == "no_detectado"
    assert summary["coverage_rate"] == 0.5


def test_calculates_correct_rate():
    _, summary = validate_events([event()], [gt(), gt(gt_id="GT002", start_time_utc="2024-01-10T10:00:00Z")])

    assert summary["correct_rate"] == 0.5


def test_calculates_average_time_delta_seconds():
    events = [event(timestamp_utc="2024-01-10T09:00:02+00:00")]

    _, summary = validate_events(events, [gt(tolerance_seconds="5")])

    assert summary["average_time_delta_seconds"] == 2.0
    assert summary["max_time_delta_seconds"] == 2.0


def test_calculates_traceability_rate():
    events = [
        event(event_id="E1", provenance={"parser": "test"}),
        event(event_id="E2", timestamp_utc="2024-01-10T09:00:01+00:00", provenance={}),
    ]
    ground_truth = [
        gt(gt_id="GT001", tolerance_seconds="10"),
        gt(gt_id="GT002", tolerance_seconds="10"),
    ]

    _, summary = validate_events(events, ground_truth)

    assert summary["traceability_rate"] == 0.5


def test_write_results_csv(tmp_path):
    results, _ = validate_events([event()], [gt()])
    path = tmp_path / "validation_results.csv"

    write_results_csv(results, path)

    content = path.read_text(encoding="utf-8")
    assert "gt_id,scenario_id,action" in content
    assert "correcto" in content


def test_write_summary_json(tmp_path):
    _, summary = validate_events([event()], [gt()])
    path = tmp_path / "validation_summary.json"

    write_summary_json(summary, path)

    assert json.loads(path.read_text(encoding="utf-8"))["correct"] == 1


def test_write_report_md(tmp_path):
    results, summary = validate_events([event()], [gt()])
    path = tmp_path / "validation_report.md"

    write_report_md(results, summary, path)

    text = path.read_text(encoding="utf-8")
    assert "# Validation Report" in text
    assert "correcto" in text


def test_supports_multiple_expected_sources():
    evtx_event = event(source_artifact="EVTX", object_value="Application:1001", raw_evidence={"event_id": "1001"})

    results, _ = validate_events(
        [evtx_event],
        [gt(expected_sources="BrowserHistory|EVTX", expected_object="1001")],
    )

    assert results[0]["result"] == "correcto"


def test_object_matches_object_description_and_raw_evidence():
    event_data = event(
        object_value="unrelated",
        description="Something else",
        raw_evidence={"url": "https://example.com/path"},
    )

    assert object_matches("https://example.com/path", event_data)
    assert object_matches("something else", event_data)
    assert object_matches("unrelated", event_data)


def test_parse_utc_datetime_rejects_naive_or_invalid_values():
    assert parse_utc_datetime("2024-01-10T09:00:00Z") == datetime(
        2024, 1, 10, 9, 0, tzinfo=timezone.utc
    )
    with pytest.raises(ValueError, match="timezone-aware"):
        parse_utc_datetime("2024-01-10T09:00:00")
    with pytest.raises(ValueError, match="Invalid UTC datetime"):
        parse_utc_datetime("not-a-date")


def test_empty_ground_truth_does_not_break():
    results, summary = validate_events([event()], [])

    assert results == []
    assert summary["ground_truth_total"] == 0
    assert summary["coverage_rate"] == 0.0
    assert summary["average_time_delta_seconds"] is None

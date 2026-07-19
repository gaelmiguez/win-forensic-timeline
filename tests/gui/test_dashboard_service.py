from __future__ import annotations

import pandas as pd

from gui.services.dashboard_service import (
    aggregate_temporal,
    choose_temporal_granularity,
    compute_dashboard_metrics,
    confidence_values_by_source,
    count_by,
    mixed_dataset_notice,
    traceability_by_source,
)


def test_dashboard_metrics_cover_sources_time_and_traceability(event_frame):
    metrics = compute_dashboard_metrics(event_frame, 2, 1, 3)

    assert metrics.total_events == 3
    assert metrics.source_count == 3
    assert metrics.traceable_events == 2
    assert metrics.validation_scenarios == 2
    assert metrics.rejected_rows == 1
    assert metrics.issue_count == 3
    assert metrics.start_utc.isoformat().startswith("2024-01-10T09:00:00")


def test_dashboard_metrics_handle_empty_dataset():
    metrics = compute_dashboard_metrics(pd.DataFrame())

    assert metrics.total_events == 0
    assert metrics.start_utc is None
    assert metrics.end_utc is None


def test_counts_and_temporal_aggregation_ignore_invalid_timestamp(event_frame):
    counts = count_by(event_frame, "source_artifact")
    temporal = aggregate_temporal(event_frame, "hora")

    assert counts["events"].sum() == 3
    assert temporal["events"].sum() == 2
    assert choose_temporal_granularity(event_frame) == "minuto"


def test_confidence_is_kept_per_source(event_frame):
    values = confidence_values_by_source(event_frame)

    assert set(values["source_artifact"]) == {
        "BrowserHistory",
        "Prefetch",
        "Registry",
    }
    assert "mean" not in values.columns


def test_traceability_is_grouped_by_source(event_frame):
    grouped = traceability_by_source(event_frame)

    assert grouped["events"].sum() == 3
    registry = grouped.loc[grouped["source_artifact"].eq("Registry")]
    assert registry.iloc[0]["traceability"] == "Sin trazabilidad"


def test_mixed_dataset_notice_counts_only_explicit_known_scenarios():
    synthetic = pd.DataFrame(
        [
            {"source_artifact": "BrowserHistory", "scenario_id": "S_BROWSER_SYNTH"}
            for _ in range(3)
        ]
        + [
            {"source_artifact": "Prefetch", "scenario_id": "S_PREFETCH_SYNTH"}
            for _ in range(2)
        ]
        + [
            {"source_artifact": "Registry", "scenario_id": "S_REGISTRY_SYNTH"}
            for _ in range(2)
        ]
        + [
            {"source_artifact": "EVTX", "scenario_id": None}
            for _ in range(1458)
        ]
    )

    assert mixed_dataset_notice(synthetic) == (
        "Conjunto mixto: 7 eventos sintéticos controlados y 1458 eventos EVTX reales."
    )


def test_mixed_dataset_notice_does_not_classify_unknown_scenarios():
    frame = pd.DataFrame(
        [
            {"source_artifact": "EVTX", "scenario_id": None},
            {"source_artifact": "BrowserHistory", "scenario_id": "UNKNOWN_CASE"},
        ]
    )

    assert mixed_dataset_notice(frame) is None


def test_partial_known_synthetic_mix_uses_no_unverifiable_counts():
    frame = pd.DataFrame(
        [
            {"source_artifact": "EVTX", "scenario_id": None},
            {"source_artifact": "Registry", "scenario_id": "S_REGISTRY_SYNTH"},
        ]
    )

    assert mixed_dataset_notice(frame) == (
        "Conjunto mixto: eventos sintéticos controlados y procesamiento EVTX real."
    )

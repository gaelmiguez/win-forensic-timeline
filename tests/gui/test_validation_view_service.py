from __future__ import annotations

import pandas as pd
import pytest

from gui.models import ValidationScenario
from gui.services.validation_view_service import (
    compact_validation_results,
    enrich_validation_results,
    format_validation_results_for_display,
    metric_rows,
    scenario_display_name,
    scenario_is_controlled,
)


def test_default_scenario_is_not_classified_as_synthetic():
    scenario = ValidationScenario(identifier="default", summary={})

    assert scenario_display_name(scenario) == "Escenario no clasificado: default"
    assert not scenario_is_controlled(scenario)


def test_explicit_synthetic_identifier_is_controlled():
    scenario = ValidationScenario(identifier="browser_synthetic")

    assert scenario_is_controlled(scenario)
    assert scenario_display_name(scenario) == "BrowserHistory sintético"


def test_known_scenario_id_has_friendly_name():
    scenario = ValidationScenario(
        identifier="prefetch_synthetic",
        results=pd.DataFrame([{"scenario_id": "S_PREFETCH_SYNTH"}]),
    )

    assert scenario_display_name(scenario) == "Prefetch sintético"


def test_unknown_scenario_is_not_silently_classified():
    scenario = ValidationScenario(identifier="CASE_WITH_UNKNOWN_SCOPE")

    assert scenario_display_name(scenario) == (
        "Escenario no clasificado: CASE_WITH_UNKNOWN_SCOPE"
    )


def test_missing_metrics_remain_unavailable():
    rows = dict(metric_rows(ValidationScenario(identifier="sample", summary={"correct": 2})))

    assert rows["Correctos"] == 2
    assert rows["Falsos positivos"] is None


def test_strict_precision_uses_precision_rate_not_correct_rate():
    rows = dict(
        metric_rows(
            ValidationScenario(
                identifier="sample",
                summary={"correct_rate": 0.50, "precision_rate": 0.75},
            )
        )
    )

    assert rows["Tasa de correctos"] == 0.50
    assert rows["Precisión estricta"] == 0.75


def test_enrichment_adds_normalized_object_and_traceability(event_frame):
    results = pd.DataFrame(
        [
            {
                "matched_event_id": "event-001",
                "gt_id": "GT-1",
                "result": "correcto",
            }
        ]
    )
    scenario = ValidationScenario(identifier="sample", results=results)
    enriched = enrich_validation_results(scenario, event_frame)

    assert enriched.iloc[0]["normalized_object"] == "https://example.com/"
    assert bool(enriched.iloc[0]["traceability"])


def test_enrichment_handles_missing_matched_event(event_frame):
    scenario = ValidationScenario(
        identifier="sample",
        results=pd.DataFrame([{"matched_event_id": "missing"}]),
    )
    enriched = enrich_validation_results(scenario, event_frame)

    assert enriched.iloc[0]["normalized_object"] is None
    assert not bool(enriched.iloc[0]["traceability"])


@pytest.mark.parametrize(
    ("source", "expected", "normalized"),
    [
        ("BrowserHistory", "https://example.com/", "https://example.com/"),
        ("Prefetch", "NOTEPAD.EXE", "NOTEPAD.EXE"),
        (
            "Registry",
            "ExampleApp",
            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\ExampleApp",
        ),
    ],
)
def test_correct_result_uses_event_reference_in_compact_view(
    source: str, expected: str, normalized: str
):
    event_id = f"event-{source.casefold()}-001"
    events = pd.DataFrame(
        [
            {
                "event_id": event_id,
                "source_artifact": source,
                "object": normalized,
                "traceability_ref": "controlled-reference",
                "provenance": {"parser": "test"},
            }
        ]
    )
    scenario = ValidationScenario(
        identifier=f"{source.casefold()}_synthetic",
        results=pd.DataFrame(
            [
                {
                    "gt_id": "GT-001",
                    "result": "correcto",
                    "expected_object": expected,
                    "matched_event_id": event_id,
                }
            ]
        ),
    )

    enriched = enrich_validation_results(scenario, events)
    compact = compact_validation_results(enriched)

    assert compact.iloc[0]["expected_object"] == expected
    assert compact.iloc[0]["matched_event_reference"].startswith("event-")
    assert "normalized_object" not in compact.columns
    assert enriched.iloc[0]["normalized_object"] == normalized


def test_validation_timestamps_are_formatted_only_in_display_copy():
    original = pd.DataFrame(
        [{"expected_time_utc": "2024-01-10T09:00:00+00:00", "detected_time_utc": "invalid"}]
    )

    display = format_validation_results_for_display(original)

    assert display.iloc[0]["expected_time_utc"] == "2024-01-10 09:00:00Z"
    assert display.iloc[0]["detected_time_utc"] == "invalid"
    assert original.iloc[0]["expected_time_utc"] == "2024-01-10T09:00:00+00:00"

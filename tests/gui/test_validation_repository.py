from __future__ import annotations

import csv
import json

import pytest

from gui.config import VALIDATION_RESULT_FIELDS
from gui.models import LoadStatus
from gui.services.output_catalog import inspect_output_catalog
from gui.services.validation_repository import load_validation_outputs


def summary():
    return {
        "ground_truth_total": 1,
        "correct": 1,
        "partial": 0,
        "not_detected": 0,
        "false_positives": 0,
        "coverage_rate": 1.0,
        "correct_rate": 1.0,
        "precision_rate": 1.0,
        "average_time_delta_seconds": 0.0,
        "max_time_delta_seconds": 0.0,
        "traceability_rate": 1.0,
    }


def result_row(result="correcto"):
    return {
        "gt_id": "GT-001",
        "scenario_id": "S_TEST",
        "action": "url_visit",
        "expected_time_utc": "2024-01-10T09:00:00Z",
        "expected_object": "https://example.com/",
        "expected_sources": "BrowserHistory",
        "matched_event_id": "event-001",
        "detected_time_utc": "2024-01-10T09:00:00+00:00",
        "time_delta_seconds": "0.0",
        "result": result,
        "matched_source": "BrowserHistory",
        "notes": "fixture",
    }


def write_summary(path, payload=None):
    path.write_text(json.dumps(payload or summary()), encoding="utf-8")


def write_results(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=VALIDATION_RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_loads_valid_summary_and_results(tmp_path):
    write_summary(tmp_path / "validation_summary_sample.json")
    write_results(tmp_path / "validation_results_sample.csv", [result_row()])

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert loaded.status is LoadStatus.SUCCESS
    assert loaded.data[0].identifier == "sample"
    assert loaded.data[0].summary["correct"] == 1
    assert loaded.data[0].results.iloc[0]["result"] == "correcto"


@pytest.mark.parametrize(
    "result", ["correcto", "parcial", "no_detectado", "falso_positivo"]
)
def test_accepts_real_validator_result_values(tmp_path, result):
    write_results(tmp_path / "validation_results_case.csv", [result_row(result)])

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert loaded.data[0].results.iloc[0]["result"] == result


def test_does_not_require_false_positive_rows(tmp_path):
    payload = summary()
    payload["false_positives"] = 4
    write_summary(tmp_path / "validation_summary_case.json", payload)
    write_results(tmp_path / "validation_results_case.csv", [result_row("correcto")])

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert loaded.data[0].summary["false_positives"] == 4
    assert set(loaded.data[0].results["result"]) == {"correcto"}


def test_summary_without_results_is_reported(tmp_path):
    write_summary(tmp_path / "validation_summary_orphan.json")

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert any(issue.code == "validation_results_missing" for issue in loaded.issues)


def test_results_without_summary_are_reported(tmp_path):
    write_results(tmp_path / "validation_results_orphan.csv", [result_row()])

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert any(issue.code == "validation_summary_missing" for issue in loaded.issues)


def test_invalid_summary_json_is_controlled(tmp_path):
    (tmp_path / "validation_summary_bad.json").write_text("{", encoding="utf-8")

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert loaded.status is LoadStatus.ERROR
    assert any(
        issue.code == "validation_summary_invalid_json" for issue in loaded.issues
    )


def test_invalid_results_schema_is_controlled(tmp_path):
    (tmp_path / "validation_results_bad.csv").write_text("wrong\nvalue\n", encoding="utf-8")

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert any(
        issue.code == "validation_results_missing_columns" for issue in loaded.issues
    )


def test_multiple_scenarios_remain_separate(tmp_path):
    for name in ("alpha", "beta"):
        write_summary(tmp_path / f"validation_summary_{name}.json")
        write_results(tmp_path / f"validation_results_{name}.csv", [result_row()])

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert [scenario.identifier for scenario in loaded.data] == ["alpha", "beta"]


def test_unknown_result_row_is_rejected(tmp_path):
    write_results(tmp_path / "validation_results_case.csv", [result_row("inventado")])

    loaded = load_validation_outputs(inspect_output_catalog(tmp_path))

    assert loaded.records_rejected == 1
    assert any(
        issue.code == "validation_result_unknown_value" for issue in loaded.issues
    )

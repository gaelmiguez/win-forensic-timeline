from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


FIXTURE_ROOT = Path(__file__).parents[1] / "fixtures" / "gui" / "capture_validation"


def test_capture_validation_fixtures_keep_controlled_sources_separate():
    expected = {
        "browser_synthetic": ("BrowserHistory", 3),
        "prefetch_synthetic": ("Prefetch", 2),
        "registry_synthetic": ("Registry", 2),
    }

    for scenario, (source, total) in expected.items():
        summary = json.loads(
            (FIXTURE_ROOT / f"validation_summary_{scenario}.json").read_text(
                encoding="utf-8"
            )
        )
        results = pd.read_csv(FIXTURE_ROOT / f"validation_results_{scenario}.csv")

        assert summary["ground_truth_total"] == total
        assert summary["correct"] == total
        assert len(results) == total
        assert set(results["expected_sources"]) == {source}
        assert "EVTX" not in set(results["expected_sources"])


def test_capture_validation_has_exactly_three_controlled_scenarios():
    summaries = sorted(FIXTURE_ROOT.glob("validation_summary_*.json"))
    results = sorted(FIXTURE_ROOT.glob("validation_results_*.csv"))

    assert len(summaries) == 3
    assert len(results) == 3

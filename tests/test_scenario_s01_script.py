import csv
import subprocess
import sqlite3
from datetime import datetime, timedelta, timezone

from scripts import run_scenario_s01_browser_evtx as scenario_module
from scripts.run_scenario_s01_browser_evtx import (
    GROUND_TRUTH_HEADER,
    export_application_evtx,
    main,
    run_scenario,
)


def test_scenario_s01_generates_browser_history_and_ground_truth_with_skip_evtx(tmp_path):
    scenario_root = tmp_path / "evidence" / "scenarios" / "s01"
    output_root = tmp_path / "output" / "scenarios" / "s01"

    result = run_scenario(
        scenario_root=scenario_root,
        output_root=output_root,
        overwrite=True,
        skip_evtx=True,
        run_pipeline_enabled=False,
        run_validator_enabled=False,
    )

    history_path = scenario_root / "browser" / "sample" / "History"
    ground_truth_path = output_root / "ground_truth_s01_browser_evtx.csv"

    assert result.browser_history_generated is True
    assert result.ground_truth_rows == 3
    assert history_path.exists()
    assert ground_truth_path.exists()

    with sqlite3.connect(history_path) as connection:
        url_count = connection.execute("SELECT COUNT(*) FROM urls").fetchone()[0]
        visit_count = connection.execute("SELECT COUNT(*) FROM visits").fetchone()[0]

    assert url_count == 3
    assert visit_count == 3

    with ground_truth_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    assert reader.fieldnames == GROUND_TRUTH_HEADER
    assert len(rows) == 3
    assert {row["expected_sources"] for row in rows} == {"BrowserHistory"}
    assert all(row["gt_id"].startswith("GT-S01-BR-") for row in rows)
    assert not any(row["expected_sources"] == "EVTX" for row in rows)


def test_scenario_s01_overwrite_replaces_only_selected_roots(tmp_path):
    scenario_root = tmp_path / "evidence" / "scenarios" / "s01"
    output_root = tmp_path / "output" / "scenarios" / "s01"
    sibling_evidence = tmp_path / "evidence" / "other"
    sibling_output = tmp_path / "output" / "other"

    scenario_root.mkdir(parents=True)
    output_root.mkdir(parents=True)
    sibling_evidence.mkdir(parents=True)
    sibling_output.mkdir(parents=True)

    (scenario_root / "old_evidence.txt").write_text("old", encoding="utf-8")
    (output_root / "old_output.txt").write_text("old", encoding="utf-8")
    (sibling_evidence / "keep.txt").write_text("keep", encoding="utf-8")
    (sibling_output / "keep.txt").write_text("keep", encoding="utf-8")

    run_scenario(
        scenario_root=scenario_root,
        output_root=output_root,
        overwrite=True,
        skip_evtx=True,
        run_pipeline_enabled=False,
        run_validator_enabled=False,
    )

    assert not (scenario_root / "old_evidence.txt").exists()
    assert not (output_root / "old_output.txt").exists()
    assert (sibling_evidence / "keep.txt").exists()
    assert (sibling_output / "keep.txt").exists()


def test_scenario_s01_cli_skip_evtx_without_pipeline_or_validator(tmp_path):
    scenario_root = tmp_path / "evidence" / "scenarios" / "s01"
    output_root = tmp_path / "output" / "scenarios" / "s01"

    exit_code = main(
        [
            "--scenario-root",
            str(scenario_root),
            "--output-root",
            str(output_root),
            "--overwrite",
            "--skip-evtx",
            "--no-run-pipeline",
            "--no-run-validator",
        ]
    )

    assert exit_code == 0
    assert (scenario_root / "browser" / "sample" / "History").exists()
    assert (output_root / "ground_truth_s01_browser_evtx.csv").exists()


def test_scenario_s01_browser_history_timestamps_are_not_future(tmp_path):
    scenario_root = tmp_path / "evidence" / "scenarios" / "s01"
    output_root = tmp_path / "output" / "scenarios" / "s01"
    started_at = datetime.now(timezone.utc)

    run_scenario(
        scenario_root=scenario_root,
        output_root=output_root,
        overwrite=True,
        skip_evtx=True,
        run_pipeline_enabled=False,
        run_validator_enabled=False,
    )

    finished_at = datetime.now(timezone.utc)
    ground_truth_path = output_root / "ground_truth_s01_browser_evtx.csv"
    with ground_truth_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    timestamps = [_parse_z(row["start_time_utc"]) for row in rows]
    assert max(timestamps) <= finished_at + timedelta(seconds=2)
    assert max(timestamps) >= started_at - timedelta(seconds=5)
    assert all(timestamp <= finished_at + timedelta(seconds=2) for timestamp in timestamps)


def test_scenario_s01_main_returns_error_when_pipeline_fails(tmp_path, monkeypatch):
    scenario_root = tmp_path / "evidence" / "scenarios" / "s01"
    output_root = tmp_path / "output" / "scenarios" / "s01"

    def fake_run_command(command):
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="pipeline failed")

    monkeypatch.setattr(scenario_module, "run_command", fake_run_command)

    exit_code = main(
        [
            "--scenario-root",
            str(scenario_root),
            "--output-root",
            str(output_root),
            "--overwrite",
            "--skip-evtx",
        ]
    )

    assert exit_code == 1


def test_scenario_s01_evtx_no_time_filter_is_passed_to_exporter(tmp_path, monkeypatch):
    captured_commands = []

    def fake_run(command, **kwargs):
        captured_commands.append(command)
        (tmp_path / "Application.evtx").write_bytes(b"EVTX")
        return subprocess.CompletedProcess(command, 0, stdout="exported", stderr="")

    monkeypatch.setattr(scenario_module.subprocess, "run", fake_run)

    exported, warnings = export_application_evtx(
        output_dir=tmp_path,
        last_hours=1,
        overwrite=True,
        python_executable="python",
        no_time_filter=True,
    )

    assert exported is True
    assert warnings == []
    assert captured_commands
    assert "--no-time-filter" in captured_commands[0]


def _parse_z(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from gui.models import PipelineStatus
from gui.services.pipeline_service import (
    PipelineService,
    create_unique_run_directory,
    validate_pipeline_paths,
)


def test_pipeline_service_calls_runner_and_uses_unique_output(tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    calls = []

    def runner(input_root, output_root):
        calls.append((input_root, output_root))
        target = output_root / "events.json"
        target.write_text("[]", encoding="utf-8")
        return {
            "events": [object(), object()],
            "timeline": pd.DataFrame([{}, {}]),
            "processed_artifacts": ["browser"],
            "skipped_artifacts": ["evtx"],
            "parser_errors": [],
            "outputs": [target],
        }

    result = PipelineService(runner).run(evidence, tmp_path / "new-output-base")

    assert result.status is PipelineStatus.SUCCESS
    assert result.events_normalized == 2
    assert calls[0][0] == evidence.resolve()
    assert calls[0][1].parent.name == "gui_runs"
    assert result.outputs == ("events.json",)


def test_pipeline_service_marks_parser_errors_as_partial(tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()

    def runner(input_root, output_root):
        return {
            "events": [],
            "timeline": pd.DataFrame(),
            "processed_artifacts": [],
            "skipped_artifacts": [],
            "parser_errors": [f"parser failed below {input_root}"],
            "outputs": [],
        }

    result = PipelineService(runner).run(evidence, tmp_path / "runs")

    assert result.status is PipelineStatus.PARTIAL
    assert "<evidence>" in result.parser_errors[0]


def test_pipeline_service_controls_runner_exception(tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()

    def runner(input_root, output_root):
        raise RuntimeError(f"cannot read {input_root}")

    result = PipelineService(runner).run(evidence, tmp_path / "runs")

    assert result.status is PipelineStatus.ERROR
    assert result.error_code == "RuntimeError"
    assert "<evidence>" in result.error_message


def test_pipeline_paths_reject_missing_input(tmp_path):
    result = validate_pipeline_paths(tmp_path / "missing", tmp_path / "runs")

    assert not result.is_valid
    assert any(issue.code == "input_not_found" for issue in result.issues)


def test_pipeline_paths_reject_identical_roots(tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    result = validate_pipeline_paths(evidence, evidence)

    assert not result.is_valid
    assert any(issue.code == "input_output_identical" for issue in result.issues)


def test_pipeline_paths_reject_output_below_evidence(tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    result = validate_pipeline_paths(evidence, evidence / "outputs")

    assert not result.is_valid
    assert any(issue.code == "output_inside_input" for issue in result.issues)


def test_unique_run_directory_handles_collision(tmp_path):
    now = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    first = create_unique_run_directory(tmp_path, now)
    second = create_unique_run_directory(tmp_path, now)

    assert first.name.startswith("20240101_120000_000000_")
    assert second.name.startswith("20240101_120000_000000_")
    assert first != second


def test_pipeline_service_does_not_modify_input_files(tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    marker = evidence / "marker.txt"
    marker.write_text("original", encoding="utf-8")

    def runner(input_root, output_root):
        return {
            "events": [],
            "timeline": pd.DataFrame(),
            "processed_artifacts": [],
            "skipped_artifacts": [],
            "parser_errors": [],
            "outputs": [],
        }

    PipelineService(runner).run(evidence, tmp_path / "runs")

    assert marker.read_text(encoding="utf-8") == "original"

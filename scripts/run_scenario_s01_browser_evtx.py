"""Orchestrate scenario S01 with synthetic BrowserHistory and optional EVTX."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sqlite3
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

WINDOWS_EPOCH_UTC = datetime(1601, 1, 1, tzinfo=timezone.utc)
SCENARIO_ID = "S01_BROWSER_EVTX"
GROUND_TRUTH_HEADER = [
    "gt_id",
    "scenario_id",
    "action",
    "expected_object",
    "start_time_utc",
    "tolerance_seconds",
    "expected_sources",
]
BROWSER_VISITS = [
    ("GT-S01-BR-001", "https://example.com/", "Example Domain", 0),
    ("GT-S01-BR-002", "https://www.incibe.es/", "INCIBE", 60),
    ("GT-S01-BR-003", "https://www.osi.es/", "Oficina de Seguridad del Internauta", 120),
]
CONTROLLED_EVTX_EVENTS = [
    ("GT-S01-EVTX-001", "901", "WinForensicTimeline S01 controlled event start"),
    ("GT-S01-EVTX-002", "902", "WinForensicTimeline S01 controlled event end"),
]


@dataclass
class ScenarioResult:
    scenario_root: Path
    output_root: Path
    ground_truth_path: Path
    ground_truth_rows: int = 0
    browser_history_generated: bool = False
    evtx_skipped: bool = False
    eventcreate_available: bool = False
    eventcreate_succeeded: bool = False
    evtx_exported: bool = False
    pipeline_executed: bool = False
    validator_executed: bool = False
    validation_summary: dict | None = None
    warnings: list[str] = field(default_factory=list)


def datetime_to_chrome_time(value: datetime) -> int:
    """Convert an aware UTC datetime to Chrome/WebKit microseconds since 1601."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime_to_chrome_time expects a timezone-aware datetime.")

    delta = value.astimezone(timezone.utc) - WINDOWS_EPOCH_UTC
    return int(delta.total_seconds() * 1_000_000)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and optionally validate scenario S01_BROWSER_EVTX evidence."
    )
    parser.add_argument(
        "--scenario-root",
        default=str(Path("evidence") / "scenarios" / "s01"),
        help="Scenario evidence root. Default: evidence/scenarios/s01.",
    )
    parser.add_argument(
        "--output-root",
        default=str(Path("output") / "scenarios" / "s01"),
        help="Scenario output root. Default: output/scenarios/s01.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace previous S01 evidence/output folders.")
    parser.add_argument("--skip-evtx", action="store_true", help="Skip eventcreate and EVTX export.")
    parser.add_argument("--evtx-last-hours", type=int, default=1, help="EVTX export time window. Default: 1.")
    parser.add_argument(
        "--evtx-no-time-filter",
        action="store_true",
        help="Pass --no-time-filter to the EVTX exporter if EVTX export is attempted.",
    )
    parser.add_argument("--event-source", default="WinForensicTimelineS01", help="Windows event source name.")
    parser.add_argument("--no-run-pipeline", action="store_true", help="Only generate evidence and ground truth.")
    parser.add_argument("--no-run-validator", action="store_true", help="Skip validation after the pipeline.")
    parser.add_argument("--python-executable", default=sys.executable, help="Python executable for subprocesses.")
    return parser


def prepare_directories(scenario_root: Path, output_root: Path, overwrite: bool) -> None:
    """Create scenario directories, optionally replacing only the selected roots."""

    if overwrite:
        _remove_tree_safely(scenario_root)
        _remove_tree_safely(output_root)

    (scenario_root / "browser" / "sample").mkdir(parents=True, exist_ok=True)
    (scenario_root / "evtx" / "windows_export").mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)


def generate_browser_history(history_path: Path, scenario_start_utc: datetime) -> list[dict[str, str]]:
    """Create a Chromium History SQLite database and return ground truth rows."""

    history_path.parent.mkdir(parents=True, exist_ok=True)
    if history_path.exists():
        history_path.unlink()

    rows: list[dict[str, str]] = []
    with sqlite3.connect(history_path) as connection:
        connection.execute("CREATE TABLE urls (id INTEGER PRIMARY KEY, url TEXT NOT NULL, title TEXT)")
        connection.execute(
            "CREATE TABLE visits (id INTEGER PRIMARY KEY, url INTEGER NOT NULL, visit_time INTEGER NOT NULL)"
        )

        for visit_id, (gt_id, url, title, offset_seconds) in enumerate(BROWSER_VISITS, start=1):
            visited_at = scenario_start_utc + timedelta(seconds=offset_seconds)
            connection.execute(
                "INSERT INTO urls (id, url, title) VALUES (?, ?, ?)",
                (visit_id, url, title),
            )
            connection.execute(
                "INSERT INTO visits (id, url, visit_time) VALUES (?, ?, ?)",
                (visit_id, visit_id, datetime_to_chrome_time(visited_at)),
            )
            rows.append(
                {
                    "gt_id": gt_id,
                    "scenario_id": SCENARIO_ID,
                    "action": "url_visit",
                    "expected_object": url,
                    "start_time_utc": _iso_z(visited_at),
                    "tolerance_seconds": "5",
                    "expected_sources": "BrowserHistory",
                }
            )

        connection.commit()

    return rows


def generate_controlled_evtx_events(event_source: str) -> tuple[list[dict[str, str]], list[str], bool]:
    """Try to create controlled Windows Application log events with eventcreate."""

    warnings: list[str] = []
    eventcreate = shutil.which("eventcreate")
    if eventcreate is None:
        warnings.append("eventcreate is not available; EVTX ground truth rows were not generated.")
        return [], warnings, False

    rows: list[dict[str, str]] = []
    all_succeeded = True
    for gt_id, event_id, description in CONTROLLED_EVTX_EVENTS:
        timestamp_utc = datetime.now(timezone.utc)
        command = [
            eventcreate,
            "/L",
            "APPLICATION",
            "/T",
            "INFORMATION",
            "/ID",
            event_id,
            "/SO",
            event_source,
            "/D",
            description,
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode != 0:
            all_succeeded = False
            warnings.append(
                f"eventcreate failed for Event ID {event_id}; EVTX row omitted. "
                f"Reason: {_compact_output(completed.stdout, completed.stderr)}"
            )
            continue

        rows.append(
            {
                "gt_id": gt_id,
                "scenario_id": SCENARIO_ID,
                "action": "windows_event",
                "expected_object": f"Application:{event_id}",
                "start_time_utc": _iso_z(timestamp_utc),
                "tolerance_seconds": "120",
                "expected_sources": "EVTX",
            }
        )

    return rows, warnings, all_succeeded and bool(rows)


def export_application_evtx(
    output_dir: Path,
    last_hours: int,
    overwrite: bool,
    python_executable: str,
    no_time_filter: bool = False,
) -> tuple[bool, list[str]]:
    """Export Application.evtx for the scenario using the existing EVTX export helper."""

    warnings: list[str] = []
    exporter = Path("scripts") / "export_windows_evtx.py"
    if not exporter.exists():
        return False, ["scripts/export_windows_evtx.py was not found; EVTX export skipped."]

    command = [
        python_executable,
        str(exporter),
        "--logs",
        "Application",
        "--last-hours",
        str(last_hours),
        "--output",
        str(output_dir),
    ]
    if overwrite:
        command.append("--overwrite")
    if no_time_filter:
        command.append("--no-time-filter")

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    evtx_path = output_dir / "Application.evtx"
    if completed.returncode != 0 or not evtx_path.exists():
        warnings.append(f"EVTX export failed or produced no Application.evtx: {_compact_output(completed.stdout, completed.stderr)}")
        return False, warnings

    return True, warnings


def write_ground_truth(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=GROUND_TRUTH_HEADER)
        writer.writeheader()
        writer.writerows(rows)


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def run_scenario(
    scenario_root: Path,
    output_root: Path,
    overwrite: bool = False,
    skip_evtx: bool = False,
    evtx_last_hours: int = 1,
    evtx_no_time_filter: bool = False,
    event_source: str = "WinForensicTimelineS01",
    run_pipeline_enabled: bool = True,
    run_validator_enabled: bool = True,
    python_executable: str = sys.executable,
) -> ScenarioResult:
    """Generate S01 evidence, ground truth and optional pipeline/validation outputs."""

    scenario_root = Path(scenario_root)
    output_root = Path(output_root)
    result = ScenarioResult(
        scenario_root=scenario_root,
        output_root=output_root,
        ground_truth_path=output_root / "ground_truth_s01_browser_evtx.csv",
    )

    prepare_directories(scenario_root, output_root, overwrite=overwrite)

    scenario_start_utc = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(seconds=120)
    ground_truth_rows = generate_browser_history(
        scenario_root / "browser" / "sample" / "History",
        scenario_start_utc,
    )
    result.browser_history_generated = True

    result.evtx_skipped = skip_evtx
    if not skip_evtx:
        evtx_rows, evtx_warnings, eventcreate_succeeded = generate_controlled_evtx_events(event_source)
        result.eventcreate_available = shutil.which("eventcreate") is not None
        result.eventcreate_succeeded = eventcreate_succeeded
        result.warnings.extend(evtx_warnings)

        if evtx_rows:
            exported, export_warnings = export_application_evtx(
                scenario_root / "evtx" / "windows_export",
                evtx_last_hours,
                overwrite=True,
                python_executable=python_executable,
                no_time_filter=evtx_no_time_filter,
            )
            result.evtx_exported = exported
            result.warnings.extend(export_warnings)
            if exported:
                ground_truth_rows.extend(evtx_rows)
            else:
                result.warnings.append("EVTX ground truth rows were omitted because Application.evtx was not exported.")
        else:
            result.warnings.append("No controlled EVTX events were generated; scenario continues with BrowserHistory only.")

    write_ground_truth(ground_truth_rows, result.ground_truth_path)
    result.ground_truth_rows = len(ground_truth_rows)

    if run_pipeline_enabled:
        pipeline_command = [
            python_executable,
            "main.py",
            "--input",
            str(scenario_root),
            "--output",
            str(output_root),
        ]
        pipeline = run_command(pipeline_command)
        result.pipeline_executed = pipeline.returncode == 0
        if pipeline.returncode != 0:
            result.warnings.append(f"Pipeline failed: {_compact_output(pipeline.stdout, pipeline.stderr)}")

    if run_pipeline_enabled and run_validator_enabled and result.pipeline_executed:
        validator_command = [
            python_executable,
            "-m",
            "validation.validator",
            "--events",
            str(output_root / "events.json"),
            "--ground-truth",
            str(result.ground_truth_path),
            "--output",
            str(output_root / "validation_results_s01.csv"),
            "--summary",
            str(output_root / "validation_summary_s01.json"),
            "--report",
            str(output_root / "validation_report_s01.md"),
        ]
        validator = run_command(validator_command)
        result.validator_executed = validator.returncode == 0
        if validator.returncode != 0:
            result.warnings.append(f"Validator failed: {_compact_output(validator.stdout, validator.stderr)}")
        else:
            summary_path = output_root / "validation_summary_s01.json"
            if summary_path.exists():
                result.validation_summary = json.loads(summary_path.read_text(encoding="utf-8"))
    elif run_pipeline_enabled and run_validator_enabled and not result.pipeline_executed:
        result.warnings.append("Validator was skipped because the pipeline did not complete successfully.")

    return result


def scenario_succeeded(result: ScenarioResult, pipeline_requested: bool, validator_requested: bool) -> bool:
    """Return True when all requested scenario stages completed successfully."""

    if not result.browser_history_generated:
        return False
    if pipeline_requested and not result.pipeline_executed:
        return False
    if validator_requested and not result.validator_executed:
        return False
    return True


def print_summary(result: ScenarioResult) -> None:
    print("S01_BROWSER_EVTX scenario execution completed.")
    print(f"Evidence root: {result.scenario_root}")
    print(f"Output root: {result.output_root}")
    print(f"Ground truth: {result.ground_truth_path}")
    print(f"Ground truth rows: {result.ground_truth_rows}")
    print(f"BrowserHistory generated: {_yes_no(result.browser_history_generated)}")
    print(f"EVTX skipped: {_yes_no(result.evtx_skipped)}")
    if result.evtx_skipped:
        print("eventcreate available: not checked")
        print("eventcreate succeeded: not attempted")
        print("EVTX exported: not attempted")
    else:
        print(f"eventcreate available: {_yes_no(result.eventcreate_available)}")
        print(f"eventcreate succeeded: {_yes_no(result.eventcreate_succeeded)}")
        print(f"EVTX exported: {_yes_no(result.evtx_exported)}")
    print(f"Pipeline executed: {_yes_no(result.pipeline_executed)}")
    print(f"Validator executed: {_yes_no(result.validator_executed)}")
    if result.validation_summary is not None:
        print("Validation summary:")
        for key, value in result.validation_summary.items():
            print(f"  - {key}: {value}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")
    else:
        print("Warnings: none")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    pipeline_requested = not args.no_run_pipeline
    validator_requested = pipeline_requested and not args.no_run_validator
    result = run_scenario(
        scenario_root=Path(args.scenario_root),
        output_root=Path(args.output_root),
        overwrite=args.overwrite,
        skip_evtx=args.skip_evtx,
        evtx_last_hours=args.evtx_last_hours,
        evtx_no_time_filter=args.evtx_no_time_filter,
        event_source=args.event_source,
        run_pipeline_enabled=pipeline_requested,
        run_validator_enabled=validator_requested,
        python_executable=args.python_executable,
    )
    print_summary(result)
    return 0 if scenario_succeeded(result, pipeline_requested, validator_requested) else 1


def _iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _remove_tree_safely(path: Path) -> None:
    resolved = path.resolve()
    cwd = Path.cwd().resolve()
    forbidden = {cwd, cwd.parent, Path.home().resolve(), Path(path.anchor).resolve()}
    if resolved in forbidden:
        raise ValueError(f"Refusing to remove unsafe path: {path}")
    if path.exists():
        shutil.rmtree(path)


def _compact_output(stdout: str, stderr: str) -> str:
    combined = " ".join(part.strip() for part in (stdout, stderr) if part and part.strip())
    return combined or "command returned a non-zero exit code without output"


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


if __name__ == "__main__":
    raise SystemExit(main())

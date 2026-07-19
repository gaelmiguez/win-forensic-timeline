"""Export Windows EVTX logs with wevtutil for controlled prototype testing."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


DEFAULT_LOGS = ["Application", "System"]
DEFAULT_OUTPUT = Path("evidence") / "evtx" / "windows_export"


@dataclass
class ExportResult:
    log_name: str
    status: str
    output_path: Path | None = None
    size_bytes: int | None = None
    message: str = ""


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export selected Windows Event Logs to EVTX files with wevtutil."
    )
    parser.add_argument(
        "--logs",
        nargs="+",
        default=DEFAULT_LOGS,
        help="Windows Event Log names to export. Default: Application System.",
    )
    parser.add_argument(
        "--last-hours",
        type=int,
        default=24,
        help="Time window in hours for the XPath filter. Default: 24.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Destination folder for exported EVTX files.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing EVTX files.",
    )
    parser.add_argument(
        "--no-time-filter",
        action="store_true",
        help="If the time-filtered export fails, retry without the time filter.",
    )
    return parser


def export_logs(
    logs: list[str],
    last_hours: int,
    output_dir: Path,
    overwrite: bool,
    allow_no_time_filter_fallback: bool,
) -> list[ExportResult]:
    """Export requested logs and return per-log results."""

    output_dir.mkdir(parents=True, exist_ok=True)
    wevtutil = shutil.which("wevtutil")
    if wevtutil is None:
        return [
            ExportResult(
                log_name=log_name,
                status="failed",
                message="wevtutil is not available in PATH.",
            )
            for log_name in logs
        ]

    results: list[ExportResult] = []
    for log_name in logs:
        destination = output_dir / f"{_safe_log_filename(log_name)}.evtx"
        if destination.exists() and not overwrite:
            results.append(
                ExportResult(
                    log_name=log_name,
                    status="skipped",
                    output_path=destination,
                    size_bytes=destination.stat().st_size,
                    message="Destination exists; use --overwrite to replace it.",
                )
            )
            continue

        result = _export_single_log(
            wevtutil=wevtutil,
            log_name=log_name,
            destination=destination,
            last_hours=last_hours,
            overwrite=overwrite,
            use_time_filter=True,
        )
        if result.status == "exported":
            results.append(result)
            continue

        warning = result.message
        if allow_no_time_filter_fallback:
            fallback = _export_single_log(
                wevtutil=wevtutil,
                log_name=log_name,
                destination=destination,
                last_hours=last_hours,
                overwrite=True,
                use_time_filter=False,
            )
            if fallback.status == "exported":
                fallback.message = f"Exported without time filter after filtered export failed: {warning}"
            results.append(fallback)
        else:
            result.message = (
                f"{warning} Re-run with --no-time-filter to retry this log without a time filter."
            )
            results.append(result)

    return results


def _export_single_log(
    wevtutil: str,
    log_name: str,
    destination: Path,
    last_hours: int,
    overwrite: bool,
    use_time_filter: bool,
) -> ExportResult:
    command = [wevtutil, "epl", log_name, str(destination)]
    if use_time_filter:
        command.append(f"/q:{_time_filter_query(last_hours)}")
    if overwrite:
        command.append("/ow:true")

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        message = _compact_command_output(completed.stdout, completed.stderr)
        return ExportResult(log_name=log_name, status="failed", output_path=destination, message=message)

    size = destination.stat().st_size if destination.exists() else 0
    return ExportResult(
        log_name=log_name,
        status="exported",
        output_path=destination,
        size_bytes=size,
        message="Exported with time filter." if use_time_filter else "Exported without time filter.",
    )


def _time_filter_query(last_hours: int) -> str:
    if last_hours <= 0:
        raise ValueError("--last-hours must be greater than zero.")

    milliseconds = last_hours * 60 * 60 * 1000
    return f"*[System[TimeCreated[timediff(@SystemTime) <= {milliseconds}]]]"


def _safe_log_filename(log_name: str) -> str:
    safe = "".join(character if character.isalnum() or character in ("-", "_") else "_" for character in log_name)
    return safe.strip("_") or "WindowsLog"


def _compact_command_output(stdout: str, stderr: str) -> str:
    combined = "\n".join(part.strip() for part in (stdout, stderr) if part and part.strip())
    return combined or "wevtutil returned a non-zero exit code without output."


def _display_path(path: Path | None) -> str:
    if path is None:
        return "n/a"
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def print_summary(results: list[ExportResult], requested_logs: list[str]) -> None:
    exported = [result for result in results if result.status == "exported"]
    failed = [result for result in results if result.status == "failed"]
    skipped = [result for result in results if result.status == "skipped"]

    print("EVTX export summary")
    print(f"Logs requested: {', '.join(requested_logs)}")
    print(f"Logs exported: {', '.join(result.log_name for result in exported) or 'none'}")
    print(f"Logs skipped: {', '.join(result.log_name for result in skipped) or 'none'}")
    print(f"Logs failed: {', '.join(result.log_name for result in failed) or 'none'}")
    print("Results:")
    for result in results:
        size = result.size_bytes if result.size_bytes is not None else "n/a"
        print(
            f"  - {result.log_name}: {result.status}; "
            f"path={_display_path(result.output_path)}; size_bytes={size}; {result.message}"
        )


def main() -> int:
    args = build_arg_parser().parse_args()
    output_dir = Path(args.output)
    results = export_logs(
        logs=args.logs,
        last_hours=args.last_hours,
        output_dir=output_dir,
        overwrite=args.overwrite,
        allow_no_time_filter_fallback=args.no_time_filter,
    )
    print_summary(results, args.logs)

    return 0 if any(result.status == "exported" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

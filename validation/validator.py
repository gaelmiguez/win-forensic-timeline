"""Ground-truth validation engine for normalized forensic events."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

RESULT_FIELDS = [
    "gt_id",
    "scenario_id",
    "action",
    "expected_time_utc",
    "expected_object",
    "expected_sources",
    "matched_event_id",
    "detected_time_utc",
    "time_delta_seconds",
    "result",
    "matched_source",
    "notes",
]


def load_events(path: Path) -> list[dict]:
    """Load normalized events from events.json."""

    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Events file must contain a JSON list: {path}")
    return [event for event in data if isinstance(event, dict)]


def load_ground_truth(path: Path) -> list[dict]:
    """Load ground-truth rows from CSV."""

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def parse_utc_datetime(value: str) -> datetime:
    """Parse a timezone-aware ISO timestamp and normalize it to UTC."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError("UTC datetime value must be a non-empty string.")

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"Invalid UTC datetime: {value}") from exc

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"UTC datetime must be timezone-aware: {value}")

    return parsed.astimezone(timezone.utc)


def validate_events(
    events: list[dict],
    ground_truth: list[dict],
    include_false_positives: bool = False,
) -> tuple[list[dict], dict]:
    """Validate events against ground truth and return result rows plus summary."""

    used_event_ids: set[str] = set()
    results: list[dict] = []
    valid_gt_total = 0
    matched_time_deltas: list[float] = []
    traceable_matches = 0

    for gt_row in ground_truth:
        try:
            expected_time = parse_utc_datetime(gt_row.get("start_time_utc", ""))
            tolerance = _parse_tolerance(gt_row.get("tolerance_seconds", "0"))
        except ValueError as exc:
            results.append(_result_row(gt_row, result="no_detectado", notes=f"Invalid ground truth row: {exc}"))
            continue

        valid_gt_total += 1
        match, match_status = find_best_match(gt_row, events, used_event_ids)
        if match is None:
            results.append(
                _result_row(
                    gt_row,
                    expected_time=expected_time,
                    result="no_detectado",
                    notes="No candidate matched source and time window.",
                )
            )
            continue

        event_id = str(match.get("event_id") or "")
        if event_id:
            used_event_ids.add(event_id)

        detected_time = parse_utc_datetime(str(match.get("timestamp_utc")))
        delta = abs((detected_time - expected_time).total_seconds())
        matched_time_deltas.append(delta)
        if match.get("provenance"):
            traceable_matches += 1

        results.append(
            _result_row(
                gt_row,
                expected_time=expected_time,
                matched_event=match,
                detected_time=detected_time,
                time_delta_seconds=delta,
                result=match_status,
                notes=_match_notes(gt_row, match, match_status),
            )
        )

    false_positive_count = (
        _count_false_positives(events, ground_truth, used_event_ids) if include_false_positives else 0
    )
    if include_false_positives:
        results.extend(_false_positive_rows(events, ground_truth, used_event_ids))

    summary = _build_summary(
        results=results,
        ground_truth_total=valid_gt_total,
        false_positive_count=false_positive_count,
        matched_time_deltas=matched_time_deltas,
        traceable_matches=traceable_matches,
    )
    return results, summary


def find_best_match(
    gt_row: dict,
    events: list[dict],
    used_event_ids: set[str],
) -> tuple[dict | None, str]:
    """Find the best event candidate for one ground-truth row."""

    expected_time = parse_utc_datetime(gt_row.get("start_time_utc", ""))
    tolerance = _parse_tolerance(gt_row.get("tolerance_seconds", "0"))
    expected_sources = _split_sources(gt_row.get("expected_sources", ""))
    candidates: list[tuple[tuple[int, float, float], dict, bool]] = []

    for event in events:
        if not source_matches(expected_sources, event):
            continue

        try:
            event_time = parse_utc_datetime(str(event.get("timestamp_utc")))
        except ValueError:
            continue

        delta = abs((event_time - expected_time).total_seconds())
        if delta > tolerance:
            continue

        event_id = str(event.get("event_id") or "")
        object_ok = object_matches(gt_row.get("expected_object", ""), event)
        unused_priority = 0 if event_id and event_id not in used_event_ids else 1
        object_priority = 0 if object_ok else 1
        confidence = _safe_float(event.get("confidence"), default=0.0)
        candidates.append(((unused_priority, object_priority, delta, -confidence), event, object_ok))

    if not candidates:
        return None, "no_detectado"

    candidates.sort(key=lambda item: item[0])
    _, best_event, object_ok = candidates[0]
    return best_event, "correcto" if object_ok else "parcial"


def object_matches(expected_object: str, event: dict) -> bool:
    """Return True when expected_object appears in object, description, or raw_evidence."""

    if not expected_object or not expected_object.strip():
        return True

    expected = expected_object.strip().casefold()
    searchable_values = [
        event.get("object"),
        event.get("description"),
        json.dumps(event.get("raw_evidence", {}), ensure_ascii=False, default=str),
    ]
    return any(expected in str(value).casefold() for value in searchable_values if value is not None)


def source_matches(expected_sources: list[str], event: dict) -> bool:
    """Return True when event source_artifact is one of the expected sources."""

    if not expected_sources:
        return True
    source = str(event.get("source_artifact") or "").casefold()
    return source in {expected.casefold() for expected in expected_sources}


def write_results_csv(results: list[dict], path: Path) -> None:
    """Write validation result rows to CSV."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        for row in results:
            writer.writerow({field: row.get(field, "") for field in RESULT_FIELDS})


def write_summary_json(summary: dict, path: Path) -> None:
    """Write validation summary metrics to JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report_md(results: list[dict], summary: dict, path: Path) -> None:
    """Write a Markdown validation report."""

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Validation Report",
        "",
        "> Advertencia: la validación depende del ground truth proporcionado.",
        "",
        "## Métricas",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- `{key}`: {value}")

    lines.extend(["", "## Resultados por Ground Truth", ""])
    lines.append("| gt_id | scenario_id | action | result | matched_event_id | time_delta_seconds | matched_source | notes |")
    lines.append("| --- | --- | --- | --- | --- | ---: | --- | --- |")
    for row in results:
        lines.append(
            "| {gt_id} | {scenario_id} | {action} | {result} | {matched_event_id} | "
            "{time_delta_seconds} | {matched_source} | {notes} |".format(
                **{key: _markdown_cell(row.get(key, "")) for key in RESULT_FIELDS}
            )
        )

    not_detected = [row for row in results if row.get("result") == "no_detectado"]
    if not_detected:
        lines.extend(["", "## Eventos no detectados", ""])
        for row in not_detected:
            lines.append(f"- `{row.get('gt_id')}`: {row.get('notes') or 'sin coincidencia'}")

    if summary.get("false_positives", 0) == 0:
        lines.extend(
            [
                "",
                "## Nota sobre falsos positivos",
                "",
                "El cálculo exhaustivo de falsos positivos se activa con `--include-false-positives`.",
            ]
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_validation(
    events_path: Path,
    ground_truth_path: Path,
    output_path: Path,
    summary_path: Path,
    report_path: Path,
    include_false_positives: bool = False,
) -> tuple[list[dict], dict]:
    """Run validation and write all output artifacts."""

    events = load_events(events_path)
    ground_truth = load_ground_truth(ground_truth_path)
    results, summary = validate_events(events, ground_truth, include_false_positives)
    write_results_csv(results, output_path)
    write_summary_json(summary, summary_path)
    write_report_md(results, summary, report_path)
    return results, summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate normalized events against ground truth.")
    parser.add_argument("--events", default="output/events.json")
    parser.add_argument("--ground-truth", default="validation/ground_truth.csv")
    parser.add_argument("--output", default="output/validation_results.csv")
    parser.add_argument("--summary", default="output/validation_summary.json")
    parser.add_argument("--report", default="output/validation_report.md")
    parser.add_argument("--include-false-positives", action="store_true")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    results, summary = run_validation(
        events_path=Path(args.events),
        ground_truth_path=Path(args.ground_truth),
        output_path=Path(args.output),
        summary_path=Path(args.summary),
        report_path=Path(args.report),
        include_false_positives=args.include_false_positives,
    )
    print("Validation completed.")
    print(f"Ground truth rows evaluated: {summary['ground_truth_total']}")
    print(f"Results written: {args.output}")
    print(f"Summary written: {args.summary}")
    print(f"Report written: {args.report}")
    print(f"Correct: {summary['correct']}")
    print(f"Partial: {summary['partial']}")
    print(f"Not detected: {summary['not_detected']}")
    print(f"False positives: {summary['false_positives']}")
    return 0


def _result_row(
    gt_row: dict,
    expected_time: datetime | None = None,
    matched_event: dict | None = None,
    detected_time: datetime | None = None,
    time_delta_seconds: float | None = None,
    result: str = "no_detectado",
    notes: str = "",
) -> dict:
    return {
        "gt_id": gt_row.get("gt_id", ""),
        "scenario_id": gt_row.get("scenario_id", ""),
        "action": gt_row.get("action", ""),
        "expected_time_utc": expected_time.isoformat() if expected_time else gt_row.get("start_time_utc", ""),
        "expected_object": gt_row.get("expected_object", ""),
        "expected_sources": gt_row.get("expected_sources", ""),
        "matched_event_id": (matched_event or {}).get("event_id", ""),
        "detected_time_utc": detected_time.isoformat() if detected_time else "",
        "time_delta_seconds": "" if time_delta_seconds is None else _format_seconds(time_delta_seconds),
        "result": result,
        "matched_source": (matched_event or {}).get("source_artifact", ""),
        "notes": notes,
    }


def _build_summary(
    results: list[dict],
    ground_truth_total: int,
    false_positive_count: int,
    matched_time_deltas: list[float],
    traceable_matches: int,
) -> dict:
    correct = sum(1 for row in results if row.get("result") == "correcto")
    partial = sum(1 for row in results if row.get("result") == "parcial")
    not_detected = sum(1 for row in results if row.get("result") == "no_detectado")
    matched = correct + partial
    precision_denominator = correct + partial + false_positive_count

    return {
        "ground_truth_total": ground_truth_total,
        "correct": correct,
        "partial": partial,
        "not_detected": not_detected,
        "false_positives": false_positive_count,
        "coverage_rate": _safe_ratio(matched, ground_truth_total),
        "correct_rate": _safe_ratio(correct, ground_truth_total),
        "precision_rate": _safe_ratio(correct, precision_denominator),
        "average_time_delta_seconds": (
            sum(matched_time_deltas) / len(matched_time_deltas) if matched_time_deltas else None
        ),
        "max_time_delta_seconds": max(matched_time_deltas) if matched_time_deltas else None,
        "traceability_rate": _safe_ratio(traceable_matches, matched),
    }


def _count_false_positives(events: list[dict], ground_truth: list[dict], used_event_ids: set[str]) -> int:
    expected_sources = _all_expected_sources(ground_truth)
    window = _global_ground_truth_window(ground_truth)
    if not expected_sources or window is None:
        return 0

    start, end = window
    count = 0
    for event in events:
        event_id = str(event.get("event_id") or "")
        if event_id in used_event_ids or not source_matches(expected_sources, event):
            continue
        try:
            event_time = parse_utc_datetime(str(event.get("timestamp_utc")))
        except ValueError:
            continue
        if start <= event_time <= end:
            count += 1
    return count


def _false_positive_rows(events: list[dict], ground_truth: list[dict], used_event_ids: set[str]) -> list[dict]:
    expected_sources = _all_expected_sources(ground_truth)
    window = _global_ground_truth_window(ground_truth)
    if not expected_sources or window is None:
        return []

    rows: list[dict] = []
    start, end = window
    for event in events:
        event_id = str(event.get("event_id") or "")
        if event_id in used_event_ids or not source_matches(expected_sources, event):
            continue
        try:
            event_time = parse_utc_datetime(str(event.get("timestamp_utc")))
        except ValueError:
            continue
        if start <= event_time <= end:
            rows.append(
                {
                    "gt_id": "",
                    "scenario_id": event.get("scenario_id", ""),
                    "action": event.get("event_action", ""),
                    "expected_time_utc": "",
                    "expected_object": "",
                    "expected_sources": "|".join(expected_sources),
                    "matched_event_id": event_id,
                    "detected_time_utc": event_time.isoformat(),
                    "time_delta_seconds": "",
                    "result": "falso_positivo",
                    "matched_source": event.get("source_artifact", ""),
                    "notes": "Unmatched event within the global ground-truth validation window.",
                }
            )
    return rows


def _global_ground_truth_window(ground_truth: list[dict]) -> tuple[datetime, datetime] | None:
    windows: list[tuple[datetime, datetime]] = []
    for row in ground_truth:
        try:
            center = parse_utc_datetime(row.get("start_time_utc", ""))
            tolerance = _parse_tolerance(row.get("tolerance_seconds", "0"))
        except ValueError:
            continue
        delta = timedelta(seconds=tolerance)
        windows.append((center - delta, center + delta))
    if not windows:
        return None
    return min(start for start, _ in windows), max(end for _, end in windows)


def _all_expected_sources(ground_truth: list[dict]) -> list[str]:
    sources: list[str] = []
    for row in ground_truth:
        for source in _split_sources(row.get("expected_sources", "")):
            if source not in sources:
                sources.append(source)
    return sources


def _split_sources(value: str) -> list[str]:
    return [source.strip() for source in str(value or "").split("|") if source.strip()]


def _parse_tolerance(value: str) -> float:
    try:
        tolerance = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid tolerance_seconds: {value}") from exc
    if tolerance < 0:
        raise ValueError("tolerance_seconds must be non-negative.")
    return tolerance


def _safe_ratio(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _format_seconds(value: float) -> str:
    return str(int(value)) if value.is_integer() else f"{value:.6f}".rstrip("0").rstrip(".")


def _match_notes(gt_row: dict, event: dict, match_status: str) -> str:
    notes: list[str] = []
    if match_status == "correcto":
        notes.append("Matched source, time window, and expected object.")
    elif match_status == "parcial":
        notes.append("Matched source and time window, but expected object was not found clearly.")
    if gt_row.get("action") and gt_row.get("action") != event.get("event_action"):
        notes.append("Action differs from event_action; not treated as a hard failure.")
    return " ".join(notes)


def _markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())

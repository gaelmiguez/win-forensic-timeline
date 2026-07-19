"""Pure filtering helpers for normalized event tables."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable

import pandas as pd

from gui.models import FilterCriteria, FilterResult, IssueSeverity, LoadIssue


def _missing_column_issue(column: str) -> LoadIssue:
    return LoadIssue(
        IssueSeverity.WARNING,
        "filter_column_missing",
        f"No se aplicó el filtro porque falta la columna {column}.",
        field=column,
    )


def _as_utc_timestamp(value: datetime | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        return timestamp.tz_localize("UTC")
    return timestamp.tz_convert("UTC")


def _apply_values(
    frame: pd.DataFrame,
    column: str,
    values: Iterable[str],
    issues: list[LoadIssue],
) -> pd.DataFrame:
    selected = tuple(value for value in values if value != "")
    if not selected:
        return frame
    if column not in frame.columns:
        issues.append(_missing_column_issue(column))
        return frame
    return frame.loc[frame[column].isin(selected)].copy()


def _provenance_present(value: object) -> bool:
    if isinstance(value, dict):
        return bool(value)
    if isinstance(value, str) and value.strip():
        try:
            decoded = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return False
        return isinstance(decoded, dict) and bool(decoded)
    return False


def filter_events(frame: pd.DataFrame, criteria: FilterCriteria) -> FilterResult:
    """Return a filtered copy without changing the input DataFrame."""
    filtered = frame.copy(deep=True)
    issues: list[LoadIssue] = []

    if criteria.start_utc is not None or criteria.end_utc is not None:
        timestamp_column = (
            "_ui_timestamp_utc"
            if "_ui_timestamp_utc" in filtered.columns
            else "timestamp_utc"
        )
        if timestamp_column not in filtered.columns:
            issues.append(_missing_column_issue("timestamp_utc"))
        else:
            timestamps = pd.to_datetime(
                filtered[timestamp_column], errors="coerce", utc=True
            )
            mask = timestamps.notna()
            if criteria.start_utc is not None:
                mask &= timestamps >= _as_utc_timestamp(criteria.start_utc)
            if criteria.end_utc is not None:
                mask &= timestamps <= _as_utc_timestamp(criteria.end_utc)
            filtered = filtered.loc[mask].copy()

    for column, values in (
        ("source_artifact", criteria.source_artifacts),
        ("event_category", criteria.event_categories),
        ("event_action", criteria.event_actions),
        ("parser_module", criteria.parser_modules),
        ("scenario_id", criteria.scenario_ids),
    ):
        filtered = _apply_values(filtered, column, values, issues)

    if criteria.text.strip():
        searchable = (
            "object",
            "description",
            "event_action",
            "source_artifact",
        )
        available = [column for column in searchable if column in filtered.columns]
        missing = [column for column in searchable if column not in filtered.columns]
        issues.extend(_missing_column_issue(column) for column in missing)
        if available:
            combined = filtered[available].fillna("").astype(str).agg(" ".join, axis=1)
            filtered = filtered.loc[
                combined.str.contains(criteria.text.strip(), case=False, regex=False)
            ].copy()

    if criteria.has_traceability is not None:
        needed = {"traceability_ref", "provenance"}
        if not needed.issubset(filtered.columns):
            for column in sorted(needed - set(filtered.columns)):
                issues.append(_missing_column_issue(column))
        else:
            refs = filtered["traceability_ref"].fillna("").astype(str).str.strip().ne("")
            provenances = filtered["provenance"].map(_provenance_present)
            traceable = refs & provenances
            filtered = filtered.loc[
                traceable if criteria.has_traceability else ~traceable
            ].copy()

    if criteria.confidence_min is not None or criteria.confidence_max is not None:
        if "confidence" not in filtered.columns:
            issues.append(_missing_column_issue("confidence"))
        else:
            confidence = pd.to_numeric(filtered["confidence"], errors="coerce")
            mask = confidence.notna()
            if criteria.confidence_min is not None:
                mask &= confidence >= criteria.confidence_min
            if criteria.confidence_max is not None:
                mask &= confidence <= criteria.confidence_max
            filtered = filtered.loc[mask].copy()

    return FilterResult(data=filtered, issues=issues)


def available_filter_values(
    frame: pd.DataFrame,
) -> tuple[dict[str, list[str]], list[LoadIssue]]:
    """Return deterministic distinct values for selectable filters."""
    columns = (
        "source_artifact",
        "event_category",
        "event_action",
        "parser_module",
        "scenario_id",
    )
    values: dict[str, list[str]] = {}
    issues: list[LoadIssue] = []
    for column in columns:
        if column not in frame.columns:
            values[column] = []
            issues.append(_missing_column_issue(column))
            continue
        distinct = {
            str(value).strip()
            for value in frame[column].dropna().tolist()
            if str(value).strip()
        }
        values[column] = sorted(distinct, key=str.casefold)
    return values, issues


def count_traceable_events(frame: pd.DataFrame) -> tuple[int, list[LoadIssue]]:
    """Count rows with both a traceability reference and non-empty provenance."""
    needed = {"traceability_ref", "provenance"}
    if not needed.issubset(frame.columns):
        return 0, [
            _missing_column_issue(column)
            for column in sorted(needed - set(frame.columns))
        ]
    refs = frame["traceability_ref"].fillna("").astype(str).str.strip().ne("")
    provenances = frame["provenance"].map(_provenance_present)
    return int((refs & provenances).sum()), []


def confidence_by_source(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[LoadIssue]]:
    """Summarize parser-assigned confidence by source, never as a global mean."""
    required = {"source_artifact", "confidence"}
    if not required.issubset(frame.columns):
        return pd.DataFrame(), [
            _missing_column_issue(column)
            for column in sorted(required - set(frame.columns))
        ]
    working = frame[["source_artifact", "confidence"]].copy()
    working["confidence"] = pd.to_numeric(working["confidence"], errors="coerce")
    working = working.dropna(subset=["source_artifact", "confidence"])
    rows: list[dict[str, object]] = []
    for source, group in working.groupby("source_artifact", sort=True):
        values = group["confidence"]
        rows.append(
            {
                "source_artifact": source,
                "events_with_confidence": int(values.count()),
                "median_confidence": float(values.median()),
                "confidence_0_00_0_49": int((values < 0.5).sum()),
                "confidence_0_50_0_79": int(
                    ((values >= 0.5) & (values < 0.8)).sum()
                ),
                "confidence_0_80_1_00": int((values >= 0.8).sum()),
            }
        )
    return pd.DataFrame(rows), []

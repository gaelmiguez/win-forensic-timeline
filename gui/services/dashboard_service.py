"""Pure dashboard metrics and aggregations."""

from __future__ import annotations

import json

import pandas as pd

from gui.models import DashboardMetrics


GRANULARITY_FREQUENCIES = {
    "minuto": "min",
    "hora": "h",
    "día": "D",
    "semana": "W-MON",
}

KNOWN_SYNTHETIC_SCENARIOS = frozenset(
    {"S_BROWSER_SYNTH", "S_PREFETCH_SYNTH", "S_REGISTRY_SYNTH"}
)


def _timestamp_series(frame: pd.DataFrame) -> pd.Series:
    column = "_ui_timestamp_utc" if "_ui_timestamp_utc" in frame else "timestamp_utc"
    if column not in frame:
        return pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")
    return pd.to_datetime(frame[column], errors="coerce", utc=True)


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


def traceability_mask(frame: pd.DataFrame) -> pd.Series:
    """Return rows with a reference and non-empty provenance."""
    if "traceability_ref" not in frame or "provenance" not in frame:
        return pd.Series(False, index=frame.index, dtype=bool)
    references = frame["traceability_ref"].fillna("").astype(str).str.strip().ne("")
    return references & frame["provenance"].map(_provenance_present)


def mixed_dataset_notice(frame: pd.DataFrame) -> str | None:
    """Describe an explicit synthetic/EVTX mix without classifying unknown scenarios."""
    if "scenario_id" not in frame or "source_artifact" not in frame:
        return None
    scenarios = frame["scenario_id"].fillna("").astype(str).str.upper()
    synthetic_mask = scenarios.isin(KNOWN_SYNTHETIC_SCENARIOS)
    evtx_mask = frame["source_artifact"].fillna("").astype(str).str.casefold().eq("evtx")
    synthetic_count = int(synthetic_mask.sum())
    evtx_count = int(evtx_mask.sum())
    if not synthetic_count or not evtx_count:
        return None
    observed = frozenset(scenarios.loc[synthetic_mask].unique())
    if observed == KNOWN_SYNTHETIC_SCENARIOS:
        return (
            f"Conjunto mixto: {synthetic_count} eventos sintéticos controlados y "
            f"{evtx_count} eventos EVTX reales."
        )
    return "Conjunto mixto: eventos sintéticos controlados y procesamiento EVTX real."


def compute_dashboard_metrics(
    frame: pd.DataFrame,
    validation_scenarios: int = 0,
    rejected_rows: int = 0,
    issue_count: int = 0,
) -> DashboardMetrics:
    """Compute non-inferential top-level metrics for one loaded dataset."""
    timestamps = _timestamp_series(frame).dropna()
    source_count = (
        int(frame["source_artifact"].dropna().astype(str).nunique())
        if "source_artifact" in frame
        else 0
    )
    return DashboardMetrics(
        total_events=len(frame),
        source_count=source_count,
        start_utc=timestamps.min() if not timestamps.empty else None,
        end_utc=timestamps.max() if not timestamps.empty else None,
        traceable_events=int(traceability_mask(frame).sum()),
        validation_scenarios=validation_scenarios,
        rejected_rows=rejected_rows,
        issue_count=issue_count,
    )


def count_by(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """Count non-empty values deterministically for one column."""
    if column not in frame:
        return pd.DataFrame(columns=[column, "events"])
    values = frame[column].fillna("No disponible").astype(str)
    values = values.mask(values.str.strip().eq(""), "No disponible")
    return (
        values.value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="events")
        .sort_values(["events", column], ascending=[False, True], kind="stable")
        .reset_index(drop=True)
    )


def choose_temporal_granularity(frame: pd.DataFrame) -> str:
    """Choose a readable interval from valid UTC range and event volume."""
    timestamps = _timestamp_series(frame).dropna()
    if timestamps.empty:
        return "día"
    span = timestamps.max() - timestamps.min()
    if span <= pd.Timedelta(hours=6) and len(timestamps) <= 20_000:
        return "minuto"
    if span <= pd.Timedelta(days=7):
        return "hora"
    if span <= pd.Timedelta(days=180):
        return "día"
    return "semana"


def aggregate_temporal(
    frame: pd.DataFrame, granularity: str | None = None
) -> pd.DataFrame:
    """Aggregate valid timestamps by interval and source."""
    selected = granularity or choose_temporal_granularity(frame)
    frequency = GRANULARITY_FREQUENCIES.get(selected, "D")
    if "source_artifact" not in frame:
        return pd.DataFrame(columns=["timestamp_utc", "source_artifact", "events"])
    timestamps = _timestamp_series(frame)
    working = pd.DataFrame(
        {
            "timestamp_utc": timestamps,
            "source_artifact": frame["source_artifact"].fillna("Desconocida"),
        },
        index=frame.index,
    ).dropna(subset=["timestamp_utc"])
    if working.empty:
        return pd.DataFrame(columns=["timestamp_utc", "source_artifact", "events"])
    return (
        working.groupby(
            [pd.Grouper(key="timestamp_utc", freq=frequency), "source_artifact"],
            observed=True,
        )
        .size()
        .reset_index(name="events")
        .sort_values(["timestamp_utc", "source_artifact"], kind="stable")
        .reset_index(drop=True)
    )


def confidence_values_by_source(frame: pd.DataFrame) -> pd.DataFrame:
    """Return numeric parser indicators with their source labels."""
    if "confidence" not in frame or "source_artifact" not in frame:
        return pd.DataFrame(columns=["source_artifact", "confidence"])
    result = frame[["source_artifact", "confidence"]].copy()
    result["source_artifact"] = result["source_artifact"].fillna("Desconocida")
    result["confidence"] = pd.to_numeric(result["confidence"], errors="coerce")
    return result.dropna(subset=["confidence"]).reset_index(drop=True)


def traceability_by_source(frame: pd.DataFrame) -> pd.DataFrame:
    """Count events with and without traceability for each source."""
    if "source_artifact" not in frame:
        return pd.DataFrame(columns=["source_artifact", "traceability", "events"])
    working = pd.DataFrame(
        {
            "source_artifact": frame["source_artifact"].fillna("Desconocida"),
            "traceability": traceability_mask(frame).map(
                {True: "Con trazabilidad", False: "Sin trazabilidad"}
            ),
        }
    )
    return (
        working.groupby(["source_artifact", "traceability"], observed=True)
        .size()
        .reset_index(name="events")
        .sort_values(["source_artifact", "traceability"], kind="stable")
        .reset_index(drop=True)
    )

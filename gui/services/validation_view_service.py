"""Presentation-safe helpers for loaded validation scenarios."""

from __future__ import annotations

import pandas as pd

from gui.models import ValidationScenario


VALIDATION_METRICS = (
    ("Eventos esperados", "ground_truth_total"),
    ("Correctos", "correct"),
    ("Parciales", "partial"),
    ("No detectados", "not_detected"),
    ("Falsos positivos", "false_positives"),
    ("Cobertura", "coverage_rate"),
    ("Tasa de correctos", "correct_rate"),
    ("Precisión estricta", "precision_rate"),
    ("Trazabilidad", "traceability_rate"),
    ("Delta medio (s)", "average_time_delta_seconds"),
    ("Delta máximo (s)", "max_time_delta_seconds"),
)

SCENARIO_DISPLAY_NAMES = {
    "BROWSER_SYNTHETIC": "BrowserHistory sintético",
    "S_BROWSER_SYNTH": "BrowserHistory sintético",
    "PREFETCH_SYNTHETIC": "Prefetch sintético",
    "S_PREFETCH_SYNTH": "Prefetch sintético",
    "REGISTRY_SYNTHETIC": "Registry sintético",
    "S_REGISTRY_SYNTH": "Registry sintético",
}

DISPLAY_TIMESTAMP_FIELDS = ("expected_time_utc", "detected_time_utc")
COMPACT_VALIDATION_FIELDS = (
    "gt_id",
    "result",
    "expected_object",
    "matched_event_reference",
    "expected_time_utc",
    "time_delta_seconds",
    "traceability",
)


def scenario_display_name(scenario: ValidationScenario) -> str:
    """Return an explicit friendly name only for known controlled scenarios."""
    if scenario.identifier == "default":
        return "Escenario no clasificado: default"
    candidates = [scenario.identifier.upper()]
    if scenario.results is not None and "scenario_id" in scenario.results:
        candidates.extend(
            scenario.results["scenario_id"].dropna().astype(str).str.upper().unique()
        )
    for candidate in candidates:
        if candidate in SCENARIO_DISPLAY_NAMES:
            return SCENARIO_DISPLAY_NAMES[candidate]
    return f"Escenario no clasificado: {scenario.identifier}"


def scenario_is_controlled(scenario: ValidationScenario) -> bool:
    """Classify only scenarios whose identifier or rows explicitly say synthetic."""
    if "synthetic" in scenario.identifier.casefold():
        return True
    if scenario.results is None or "scenario_id" not in scenario.results:
        return False
    return scenario.results["scenario_id"].astype(str).str.contains(
        "SYNTH", case=False, regex=False
    ).any()


def metric_rows(scenario: ValidationScenario) -> list[tuple[str, object | None]]:
    """Return known metrics without substituting missing values with zero."""
    summary = scenario.summary or {}
    return [(label, summary.get(key)) for label, key in VALIDATION_METRICS]


def enrich_validation_results(
    scenario: ValidationScenario, events: pd.DataFrame
) -> pd.DataFrame:
    """Add event context without claiming which searchable field caused the match."""
    if scenario.results is None:
        return pd.DataFrame()
    results = scenario.results.copy(deep=True)
    if events.empty or "event_id" not in events:
        results["normalized_object"] = None
        results["matched_event_source"] = None
        results["matched_traceability_ref"] = None
        results["traceability"] = None
        return results
    event_index = events.drop_duplicates("event_id").set_index("event_id")

    def event_value(event_id: object, field: str):
        key = str(event_id or "")
        if not key or key not in event_index.index or field not in event_index:
            return None
        return event_index.at[key, field]

    results["normalized_object"] = results["matched_event_id"].map(
        lambda value: event_value(value, "object")
    )
    results["matched_event_source"] = results["matched_event_id"].map(
        lambda value: event_value(value, "source_artifact")
    )
    results["matched_traceability_ref"] = results["matched_event_id"].map(
        lambda value: event_value(value, "traceability_ref")
    )
    results["traceability"] = results["matched_event_id"].map(
        lambda value: bool(event_value(value, "traceability_ref"))
        and bool(event_value(value, "provenance"))
    )
    return results


def compact_matched_event_id(value: object) -> str:
    """Return a compact reference while preserving the full ID in the detail view."""
    event_id = str(value or "").strip()
    if not event_id:
        return "Sin coincidencia"
    return event_id if len(event_id) <= 14 else f"{event_id[:8]}…"


def compact_validation_results(results: pd.DataFrame) -> pd.DataFrame:
    """Build the main table without presenting a normalized object as the match value."""
    compact = results.copy(deep=True)
    if "matched_event_id" in compact:
        compact["matched_event_reference"] = compact["matched_event_id"].map(
            compact_matched_event_id
        )
    visible = [field for field in COMPACT_VALIDATION_FIELDS if field in compact]
    return compact.loc[:, visible]


def format_validation_results_for_display(results: pd.DataFrame) -> pd.DataFrame:
    """Format timestamps for the table without changing loaded validation values."""
    display = results.copy(deep=True)
    for field in DISPLAY_TIMESTAMP_FIELDS:
        if field not in display:
            continue
        original = display[field].copy()
        parsed = pd.to_datetime(original, errors="coerce", utc=True)
        formatted = parsed.dt.strftime("%Y-%m-%d %H:%M:%SZ")
        display[field] = formatted.where(parsed.notna(), original)
    return display

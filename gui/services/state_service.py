"""Serializable session-state defaults independent from Streamlit."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

from gui.models import FilterCriteria


STATE_DEFAULTS = {
    "active_output_root": None,
    "catalog": None,
    "event_result": None,
    "timeline_result": None,
    "validation_result": None,
    "active_filters": FilterCriteria(),
    "selected_event_id": None,
    "selected_validation_id": None,
    "pipeline_result": None,
    "pipeline_state": "idle",
    "load_issues": [],
    "load_requested": False,
    "show_full_paths": False,
}


def initialize_state(state: MutableMapping[str, Any]) -> None:
    """Populate missing GUI session keys without replacing existing values."""
    for key, value in STATE_DEFAULTS.items():
        if key not in state:
            state[key] = list(value) if isinstance(value, list) else value


def clear_loaded_results(state: MutableMapping[str, Any]) -> None:
    """Clear dataset-dependent state while preserving pipeline history."""
    for key in (
        "active_output_root",
        "catalog",
        "event_result",
        "timeline_result",
        "validation_result",
        "selected_event_id",
        "selected_validation_id",
    ):
        state[key] = None
    state["active_filters"] = FilterCriteria()
    state["load_issues"] = []


def has_loaded_events(state: MutableMapping[str, Any]) -> bool:
    """Return whether a non-empty accepted event dataset is available."""
    result = state.get("event_result")
    return bool(result is not None and result.records_accepted and not result.data.empty)

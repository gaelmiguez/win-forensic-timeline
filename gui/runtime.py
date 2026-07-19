"""Streamlit cache and session integration for read-only repositories."""

from __future__ import annotations

from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from gui.models import FileFingerprint, OutputCatalog
from gui.services.event_repository import load_events
from gui.services.output_catalog import inspect_output_catalog
from gui.services.path_service import validate_output_root
from gui.services.state_service import clear_loaded_results
from gui.services.timeline_repository import load_timeline
from gui.services.validation_repository import load_validation_outputs


@st.cache_data(show_spinner=False)
def _cached_events(path_text: str, size: int, mtime_ns: int):
    del size, mtime_ns
    return load_events(Path(path_text))


@st.cache_data(show_spinner=False)
def _cached_timeline(path_text: str, size: int, mtime_ns: int):
    del size, mtime_ns
    return load_timeline(Path(path_text))


@st.cache_data(show_spinner=False)
def _cached_validations(
    root_text: str,
    summary_paths: tuple[str, ...],
    result_paths: tuple[str, ...],
    fingerprint_keys: tuple[tuple[str, int, int], ...],
):
    del fingerprint_keys
    catalog = OutputCatalog(
        root=Path(root_text),
        validation_summaries=tuple(Path(path) for path in summary_paths),
        validation_results=tuple(Path(path) for path in result_paths),
    )
    return load_validation_outputs(catalog)


def _fingerprint_key(path: Path) -> tuple[str, int, int] | None:
    try:
        fingerprint = FileFingerprint.from_path(path)
    except (OSError, RuntimeError):
        return None
    return (str(fingerprint.resolved_path), fingerprint.size, fingerprint.mtime_ns)


def clear_gui_cache() -> None:
    """Clear only data cached by the GUI."""
    _cached_events.clear()
    _cached_timeline.clear()
    _cached_validations.clear()


def load_output_into_state(
    root_value: str | Path, state: MutableMapping[str, Any]
) -> bool:
    """Load one validated output root and update serializable session state."""
    validation = validate_output_root(root_value)
    if not validation.is_valid or validation.path is None:
        clear_loaded_results(state)
        state["load_issues"] = list(validation.issues)
        state["load_requested"] = True
        return False

    catalog = inspect_output_catalog(validation.path)
    event_result = None
    timeline_result = None
    validation_result = None
    issues = list(catalog.issues)

    if catalog.events_json is not None:
        key = _fingerprint_key(catalog.events_json)
        event_result = (
            _cached_events(*key) if key is not None else load_events(catalog.events_json)
        )
        issues.extend(event_result.issues)

    if catalog.timeline_csv is not None:
        key = _fingerprint_key(catalog.timeline_csv)
        timeline_result = (
            _cached_timeline(*key)
            if key is not None
            else load_timeline(catalog.timeline_csv)
        )
        issues.extend(timeline_result.issues)

    validation_paths = catalog.validation_summaries + catalog.validation_results
    if validation_paths:
        keys = tuple(_fingerprint_key(path) for path in validation_paths)
        if all(key is not None for key in keys):
            validation_result = _cached_validations(
                str(catalog.root),
                tuple(str(path) for path in catalog.validation_summaries),
                tuple(str(path) for path in catalog.validation_results),
                tuple(key for key in keys if key is not None),
            )
        else:
            validation_result = load_validation_outputs(catalog)
        issues.extend(validation_result.issues)

    clear_loaded_results(state)
    state["active_output_root"] = str(validation.path)
    state["catalog"] = catalog
    state["event_result"] = event_result
    state["timeline_result"] = timeline_result
    state["validation_result"] = validation_result
    state["load_issues"] = issues
    state["load_requested"] = True
    return bool(catalog.recognized_files)


def reload_output(state: MutableMapping[str, Any]) -> bool:
    """Invalidate GUI caches and reload the active root."""
    root = state.get("active_output_root")
    if not root:
        return False
    clear_gui_cache()
    return load_output_into_state(root, state)


def loaded_events(state: MutableMapping[str, Any]) -> pd.DataFrame:
    """Return the loaded accepted events or an empty DataFrame."""
    result = state.get("event_result")
    if result is None or result.data is None:
        return pd.DataFrame()
    return result.data

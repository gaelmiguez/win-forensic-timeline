"""Event lookup, path masking and traceability helpers."""

from __future__ import annotations

from pathlib import PurePath, PureWindowsPath

import pandas as pd


def find_event(frame: pd.DataFrame, event_id: str | None) -> dict | None:
    """Return one event dictionary by stable identifier."""
    if not event_id or "event_id" not in frame:
        return None
    matches = frame.loc[frame["event_id"].astype(str).eq(str(event_id))]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def mask_path(value: object, show_full: bool = False) -> str:
    """Mask local path components unless explicitly requested."""
    text = str(value or "")
    if show_full or not text:
        return text
    path = PureWindowsPath(text) if "\\" in text else PurePath(text)
    return f".../{path.name}" if path.name else "..."


def event_has_traceability(event: dict) -> bool:
    """Return whether an event has both reference and provenance."""
    return bool(str(event.get("traceability_ref") or "").strip()) and bool(
        event.get("provenance")
    )


def is_reliably_synthetic(event: dict) -> bool:
    """Recognize only explicit scenario identifiers that declare synthetic data."""
    scenario = str(event.get("scenario_id") or "").upper()
    return "SYNTH" in scenario

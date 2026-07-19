"""Timeline construction utilities based on pandas."""

from __future__ import annotations

from dataclasses import fields
from datetime import datetime, timezone
from typing import Iterable

import pandas as pd

from core.event_model import CommonEvent


def _is_timezone_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


def _event_columns() -> list[str]:
    return [field.name for field in fields(CommonEvent)]


def _require_aware_datetime(value: datetime, name: str) -> None:
    if not isinstance(value, datetime):
        raise ValueError(f"{name} must be a datetime instance.")
    if not _is_timezone_aware(value):
        raise ValueError(f"{name} must be timezone-aware; naive timestamps are not accepted.")


def build_timeline(events: Iterable[CommonEvent]) -> pd.DataFrame:
    """Convert CommonEvent objects to a DataFrame sorted by timestamp_utc."""

    event_list = list(events)
    if not event_list:
        return pd.DataFrame(columns=_event_columns())

    for index, event in enumerate(event_list):
        if not isinstance(event, CommonEvent):
            raise ValueError(f"events[{index}] must be a CommonEvent instance.")
        _require_aware_datetime(event.timestamp_utc, f"events[{index}].timestamp_utc")

    records = [event.to_dict() for event in event_list]
    df = pd.DataFrame(records, columns=_event_columns())
    # Support ISO timestamps with and without microseconds while normalizing to UTC.
    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"],
        utc=True,
        errors="raise",
        format="mixed",
    )

    return df.sort_values("timestamp_utc", ascending=True).reset_index(drop=True)


def filter_by_time_window(
    df: pd.DataFrame,
    start_utc: datetime,
    end_utc: datetime,
) -> pd.DataFrame:
    """Return rows whose timestamp_utc falls inside the inclusive UTC window."""

    _require_aware_datetime(start_utc, "start_utc")
    _require_aware_datetime(end_utc, "end_utc")

    if start_utc > end_utc:
        raise ValueError("start_utc must be earlier than or equal to end_utc.")

    if df.empty:
        return df.copy()

    if "timestamp_utc" not in df.columns:
        raise ValueError("DataFrame must contain a timestamp_utc column.")

    # Keep the naive timestamp guard compatible with mixed ISO precision.
    timestamps = pd.to_datetime(df["timestamp_utc"], utc=False, errors="raise", format="mixed")
    for index, value in timestamps.items():
        if isinstance(value, pd.Timestamp) and value.tzinfo is None:
            raise ValueError(f"df.timestamp_utc[{index}] is naive; naive timestamps are not accepted.")

    start = start_utc.astimezone(timezone.utc)
    end = end_utc.astimezone(timezone.utc)
    timestamps_utc = pd.to_datetime(
        df["timestamp_utc"],
        utc=True,
        errors="raise",
        format="mixed",
    )
    mask = (timestamps_utc >= start) & (timestamps_utc <= end)
    return df.loc[mask].reset_index(drop=True)

"""Timestamp conversion helpers.

All public helpers return timezone-aware datetimes normalized to UTC.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from core.exceptions import TimeConversionError

WINDOWS_EPOCH_UTC = datetime(1601, 1, 1, tzinfo=timezone.utc)


def ensure_utc(dt: datetime) -> datetime:
    """Return a timezone-aware UTC datetime.

    If a naive datetime is received, this prototype assumes the value is already
    expressed in UTC and attaches the UTC timezone. This assumption is explicit
    for baseline reproducibility and must be revisited when parser-specific
    local-time semantics are implemented.
    """

    if not isinstance(dt, datetime):
        raise TimeConversionError("ensure_utc expects a datetime instance.")

    if dt.tzinfo is None or dt.utcoffset() is None:
        # Baseline assumption: naive datetimes are interpreted as UTC.
        return dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)


def filetime_to_utc(filetime: int) -> datetime:
    """Convert a Windows FILETIME integer to a timezone-aware UTC datetime."""

    if isinstance(filetime, bool) or not isinstance(filetime, int):
        raise TimeConversionError("FILETIME value must be an integer.")
    if filetime < 0:
        raise TimeConversionError("FILETIME value must be non-negative.")

    try:
        return WINDOWS_EPOCH_UTC + timedelta(microseconds=filetime // 10)
    except OverflowError as exc:
        raise TimeConversionError(f"Invalid FILETIME value: {filetime}") from exc


def chrome_time_to_utc(chrome_timestamp: int) -> datetime:
    """Convert a Chrome/WebKit timestamp to a timezone-aware UTC datetime."""

    if isinstance(chrome_timestamp, bool) or not isinstance(chrome_timestamp, int):
        raise TimeConversionError("Chrome timestamp must be an integer.")
    if chrome_timestamp < 0:
        raise TimeConversionError("Chrome timestamp must be non-negative.")

    try:
        return WINDOWS_EPOCH_UTC + timedelta(microseconds=chrome_timestamp)
    except OverflowError as exc:
        raise TimeConversionError(f"Invalid Chrome timestamp: {chrome_timestamp}") from exc


def parse_iso_to_utc(value: str) -> datetime:
    """Parse an ISO 8601 string and return a timezone-aware UTC datetime.

    If the parsed ISO value is naive, ensure_utc documents and applies the
    baseline assumption that the value is already in UTC.
    """

    if not isinstance(value, str) or not value.strip():
        raise TimeConversionError("ISO timestamp must be a non-empty string.")

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise TimeConversionError(f"Invalid ISO timestamp: {value}") from exc

    return ensure_utc(parsed)

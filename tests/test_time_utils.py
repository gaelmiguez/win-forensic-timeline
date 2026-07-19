from datetime import datetime, timezone

from core.time_utils import ensure_utc, filetime_to_utc, parse_iso_to_utc


def test_filetime_to_utc_known_unix_epoch_value():
    result = filetime_to_utc(116444736000000000)

    assert result == datetime(1970, 1, 1, tzinfo=timezone.utc)


def test_ensure_utc_with_aware_datetime():
    aware = datetime(2024, 1, 1, 13, 0, tzinfo=timezone.utc)

    result = ensure_utc(aware)

    assert result == aware
    assert result.tzinfo == timezone.utc


def test_parse_iso_to_utc_with_z_suffix():
    result = parse_iso_to_utc("2024-01-01T12:00:00Z")

    assert result == datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)

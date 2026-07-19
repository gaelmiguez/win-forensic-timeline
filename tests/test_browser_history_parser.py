import sqlite3
from datetime import datetime, timezone

import pytest

from core.event_model import CommonEvent
from parsers.browser_history_parser import parse

WINDOWS_EPOCH_UTC = datetime(1601, 1, 1, tzinfo=timezone.utc)


def chrome_time(value: datetime) -> int:
    delta = value.astimezone(timezone.utc) - WINDOWS_EPOCH_UTC
    return int(delta.total_seconds() * 1_000_000)


def create_history_db(path, rows=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = rows or [
        (
            1,
            "https://example.com/",
            "Example Domain",
            datetime(2024, 1, 10, 9, 0, tzinfo=timezone.utc),
        )
    ]

    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE urls (id INTEGER PRIMARY KEY, url TEXT NOT NULL, title TEXT)")
        connection.execute(
            "CREATE TABLE visits (id INTEGER PRIMARY KEY, url INTEGER NOT NULL, visit_time INTEGER NOT NULL)"
        )
        for visit_id, url, title, visited_at in rows:
            connection.execute(
                "INSERT INTO urls (id, url, title) VALUES (?, ?, ?)",
                (visit_id, url, title),
            )
            connection.execute(
                "INSERT INTO visits (id, url, visit_time) VALUES (?, ?, ?)",
                (visit_id, visit_id, chrome_time(visited_at)),
            )
        connection.commit()


def test_parser_returns_common_events_for_valid_history(tmp_path):
    history_path = tmp_path / "browser" / "Chrome" / "History"
    create_history_db(history_path)

    events = parse(tmp_path / "browser")

    assert len(events) == 1
    event = events[0]
    assert isinstance(event, CommonEvent)
    assert event.timestamp_utc.tzinfo is not None
    assert event.timestamp_utc.utcoffset() is not None
    assert event.timestamp_utc.tzinfo == timezone.utc
    assert event.source_artifact == "BrowserHistory"
    assert event.event_category == "web_activity"
    assert event.event_action == "url_visit"
    assert "https://example.com/" in event.object
    assert event.provenance["normalization_method"] == "chrome_time_to_utc"


def test_parser_returns_empty_list_for_empty_folder(tmp_path):
    browser_dir = tmp_path / "browser"
    browser_dir.mkdir()

    assert parse(browser_dir) == []


def test_parser_ignores_sqlite_without_required_tables(tmp_path):
    history_path = tmp_path / "browser" / "History"
    history_path.parent.mkdir(parents=True)
    with sqlite3.connect(history_path) as connection:
        connection.execute("CREATE TABLE unrelated (id INTEGER PRIMARY KEY)")
        connection.commit()

    with pytest.warns(RuntimeWarning, match="without urls/visits tables"):
        assert parse(tmp_path / "browser") == []

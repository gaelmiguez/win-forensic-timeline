"""Chromium browser history parser.

This module parses Chrome/Edge-like SQLite History files and converts visits
into CommonEvent objects. It is intentionally conservative: invalid files,
unexpected schemas, and malformed rows are skipped with controlled warnings.
"""

from __future__ import annotations

import shutil
import sqlite3
import tempfile
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from core.event_model import CommonEvent
from core.time_utils import chrome_time_to_utc

SQLITE_HEADER = b"SQLite format 3\x00"
REQUIRED_TABLES = {"urls", "visits"}
KNOWN_HISTORY_NAMES = {"History", "History.sqlite", "history.sqlite"}


def parse(input_path: str | Path) -> list[CommonEvent]:
    """Parse Chromium History SQLite files into CommonEvent objects.

    The parser searches recursively for Chrome/Edge History files below
    input_path. Each candidate is copied to a temporary location before opening
    it with sqlite3, reducing read failures when a browser keeps the original
    database locked.
    """

    events: list[CommonEvent] = []
    for history_path in _discover_history_files(Path(input_path)):
        try:
            with _copy_to_temporary_file(history_path) as temporary_path:
                events.extend(_parse_history_file(history_path, temporary_path))
        except (OSError, sqlite3.Error) as exc:
            _warn(f"Ignoring unreadable browser history file {history_path}: {exc}")

    return events


def _discover_history_files(input_path: Path) -> list[Path]:
    """Return History file candidates below input_path."""

    if not input_path.exists():
        return []

    candidates = [input_path] if input_path.is_file() else [path for path in input_path.rglob("*") if path.is_file()]
    discovered: list[Path] = []

    for candidate in candidates:
        if candidate.name in KNOWN_HISTORY_NAMES:
            discovered.append(candidate)
            continue

        if candidate.suffix == "" and _looks_like_sqlite(candidate):
            discovered.append(candidate)

    return sorted(discovered)


def _looks_like_sqlite(path: Path) -> bool:
    """Return True if path has a SQLite database header."""

    try:
        with path.open("rb") as handle:
            return handle.read(len(SQLITE_HEADER)) == SQLITE_HEADER
    except OSError as exc:
        _warn(f"Unable to inspect browser history candidate {path}: {exc}")
        return False


def _has_required_tables(connection: sqlite3.Connection) -> bool:
    """Return True if the database has urls and visits tables."""

    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name IN ('urls', 'visits')"
    ).fetchall()
    table_names = {row[0] for row in rows}
    return REQUIRED_TABLES.issubset(table_names)


@contextmanager
def _copy_to_temporary_file(source_path: Path) -> Iterator[Path]:
    """Copy a History file to a temporary directory and yield the copy path."""

    with tempfile.TemporaryDirectory(prefix="wft_browser_history_") as temp_dir:
        target_path = Path(temp_dir) / source_path.name
        shutil.copy2(source_path, target_path)
        yield target_path


def _parse_history_file(source_path: Path, sqlite_path: Path) -> list[CommonEvent]:
    """Parse a copied SQLite History file."""

    if not _looks_like_sqlite(sqlite_path):
        _warn(f"Ignoring non-SQLite browser history candidate {source_path}")
        return []

    try:
        connection = sqlite3.connect(f"file:{sqlite_path}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        _warn(f"Ignoring corrupt browser history file {source_path}: {exc}")
        return []

    try:
        if not _has_required_tables(connection):
            _warn(f"Ignoring browser history file without urls/visits tables: {source_path}")
            return []

        return _rows_to_events(source_path, connection)
    except sqlite3.Error as exc:
        _warn(f"Ignoring browser history file with invalid SQLite content {source_path}: {exc}")
        return []
    finally:
        connection.close()


def _rows_to_events(source_path: Path, connection: sqlite3.Connection) -> list[CommonEvent]:
    query = """
        SELECT
            visits.id AS visit_id,
            visits.url AS url_id,
            visits.visit_time AS visit_time,
            urls.url AS page_url,
            urls.title AS page_title
        FROM visits
        JOIN urls ON visits.url = urls.id
        WHERE visits.visit_time IS NOT NULL
        ORDER BY visits.visit_time ASC, visits.id ASC
    """

    events: list[CommonEvent] = []
    browser_family = _infer_browser_family(source_path)

    for row in connection.execute(query):
        visit_id, url_id, visit_time, page_url, page_title = row
        try:
            if not page_url:
                raise ValueError("URL is empty")
            timestamp_utc = chrome_time_to_utc(int(visit_time))
            visit_id_text = str(visit_id)

            raw_evidence = {
                "url": page_url,
                "title": page_title,
                "visit_time": visit_time,
                "visit_id": visit_id,
                "url_id": url_id,
                "browser_family": browser_family,
            }
            provenance = {
                "artifact": "BrowserHistory",
                "source_path": str(source_path),
                "sqlite_tables": ["urls", "visits"],
                "record_id": visit_id,
                "timestamp_field": "visits.visit_time",
                "timestamp_format": "Chrome/WebKit timestamp",
                "normalization_method": "chrome_time_to_utc",
                "parser": "browser_history_parser",
            }

            events.append(
                CommonEvent.create(
                    timestamp_utc=timestamp_utc,
                    timestamp_local=None,
                    timestamp_type="browser_visit_time",
                    source_artifact="BrowserHistory",
                    source_location=str(source_path),
                    event_category="web_activity",
                    event_action="url_visit",
                    object=page_url,
                    description=f"Visita web detectada: {page_url}",
                    raw_evidence=raw_evidence,
                    parser_module="browser_history_parser",
                    traceability_ref=f"History:{visit_id_text}",
                    confidence=0.95,
                    provenance=provenance,
                )
            )
        except Exception as exc:
            _warn(f"Skipping browser history row {visit_id!r} in {source_path}: {exc}")

    return events


def _infer_browser_family(source_path: Path) -> str | None:
    """Infer browser family from path segments when possible."""

    lowered_parts = [part.lower() for part in source_path.parts]
    joined = " ".join(lowered_parts)

    if "edge" in joined or "microsoft" in joined:
        return "Edge"
    if "chrome" in joined or "google" in joined:
        return "Chrome"
    if "chromium" in joined:
        return "Chromium"

    return None


def _warn(message: str) -> None:
    warnings.warn(message, RuntimeWarning, stacklevel=2)

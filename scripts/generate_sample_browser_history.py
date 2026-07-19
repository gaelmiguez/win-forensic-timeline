"""Generate a synthetic Chromium History evidence file for demos and tests."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

WINDOWS_EPOCH_UTC = datetime(1601, 1, 1, tzinfo=timezone.utc)
SAMPLE_HISTORY_PATH = Path("evidence") / "browser" / "sample" / "History"


def datetime_to_chrome_time(value: datetime) -> int:
    """Convert an aware datetime to Chrome/WebKit microseconds since 1601 UTC."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime_to_chrome_time expects a timezone-aware datetime.")

    delta = value.astimezone(timezone.utc) - WINDOWS_EPOCH_UTC
    return int(delta.total_seconds() * 1_000_000)


def generate_sample_history(output_path: Path = SAMPLE_HISTORY_PATH) -> Path:
    """Create a synthetic History SQLite database with three visits."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    visits = [
        (
            1,
            "https://example.com/",
            "Example Domain",
            datetime(2024, 1, 10, 9, 0, 0, tzinfo=timezone.utc),
        ),
        (
            2,
            "https://www.incibe.es/",
            "INCIBE",
            datetime(2024, 1, 10, 9, 5, 0, tzinfo=timezone.utc),
        ),
        (
            3,
            "https://www.osi.es/",
            "Oficina de Seguridad del Internauta",
            datetime(2024, 1, 10, 9, 10, 0, tzinfo=timezone.utc),
        ),
    ]

    with sqlite3.connect(output_path) as connection:
        connection.execute("CREATE TABLE urls (id INTEGER PRIMARY KEY, url TEXT NOT NULL, title TEXT)")
        connection.execute(
            "CREATE TABLE visits (id INTEGER PRIMARY KEY, url INTEGER NOT NULL, visit_time INTEGER NOT NULL)"
        )

        for url_id, url, title, visit_dt in visits:
            connection.execute(
                "INSERT INTO urls (id, url, title) VALUES (?, ?, ?)",
                (url_id, url, title),
            )
            connection.execute(
                "INSERT INTO visits (id, url, visit_time) VALUES (?, ?, ?)",
                (url_id, url_id, datetime_to_chrome_time(visit_dt)),
            )

        connection.commit()

    return output_path


def main() -> int:
    output_path = generate_sample_history()
    print(f"Synthetic browser history created: {output_path}")
    print("Rows inserted: 3 urls, 3 visits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

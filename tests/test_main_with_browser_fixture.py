import json
import sqlite3
from datetime import datetime, timezone

from main import run_pipeline

WINDOWS_EPOCH_UTC = datetime(1601, 1, 1, tzinfo=timezone.utc)


def chrome_time(value: datetime) -> int:
    delta = value.astimezone(timezone.utc) - WINDOWS_EPOCH_UTC
    return int(delta.total_seconds() * 1_000_000)


def test_run_pipeline_generates_browser_history_events_and_timeline(tmp_path):
    evidence_root = tmp_path / "evidence"
    output_root = tmp_path / "output"
    history_path = evidence_root / "browser" / "sample" / "History"
    history_path.parent.mkdir(parents=True)

    with sqlite3.connect(history_path) as connection:
        connection.execute("CREATE TABLE urls (id INTEGER PRIMARY KEY, url TEXT NOT NULL, title TEXT)")
        connection.execute(
            "CREATE TABLE visits (id INTEGER PRIMARY KEY, url INTEGER NOT NULL, visit_time INTEGER NOT NULL)"
        )
        rows = [
            (1, "https://first.example/", "First", datetime(2024, 1, 10, 9, 0, tzinfo=timezone.utc)),
            (2, "https://second.example/", "Second", datetime(2024, 1, 10, 9, 5, tzinfo=timezone.utc)),
        ]
        for visit_id, url, title, visited_at in rows:
            connection.execute("INSERT INTO urls (id, url, title) VALUES (?, ?, ?)", (visit_id, url, title))
            connection.execute(
                "INSERT INTO visits (id, url, visit_time) VALUES (?, ?, ?)",
                (visit_id, visit_id, chrome_time(visited_at)),
            )
        connection.commit()

    result = run_pipeline(evidence_root, output_root)

    assert len(result["events"]) == 2
    assert len(result["timeline"]) == 2
    assert (output_root / "events.json").exists()
    assert (output_root / "timeline.csv").exists()

    events_json = json.loads((output_root / "events.json").read_text(encoding="utf-8"))
    assert events_json[0]["source_artifact"] == "BrowserHistory"
    assert events_json[0]["timestamp_utc"].endswith("+00:00")

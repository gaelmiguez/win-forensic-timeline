"""JSON and JSON Lines event reporters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from core.event_model import CommonEvent


def _event_to_dict(event: CommonEvent) -> dict:
    if not isinstance(event, CommonEvent):
        raise ValueError("JSON reporters expect CommonEvent instances.")
    return event.to_dict()


def export_events_json(events: Iterable[CommonEvent], output_path: str | Path) -> Path:
    """Export events as a JSON array."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [_event_to_dict(event) for event in events]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return path


def export_events_jsonl(events: Iterable[CommonEvent], output_path: str | Path) -> Path:
    """Export events as newline-delimited JSON."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps(_event_to_dict(event), ensure_ascii=False, default=str)
        for event in events
    ]
    content = "\n".join(lines)
    if lines:
        content += "\n"
    path.write_text(content, encoding="utf-8")
    return path

"""Baseline event normalizer."""

from __future__ import annotations

from typing import Iterable

from core.event_model import CommonEvent


def normalize_events(events: Iterable[CommonEvent]) -> list[CommonEvent]:
    """Return events unchanged until parser-specific normalization is added."""

    return list(events)

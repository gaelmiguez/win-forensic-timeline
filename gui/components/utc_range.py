"""UTC range summary shared by temporal views."""

from __future__ import annotations

from datetime import datetime

import streamlit as st


def _format(value: datetime | None) -> str:
    return value.strftime("%Y-%m-%d %H:%M UTC") if value is not None else "No disponible"


def render_utc_range(start: datetime | None, end: datetime | None) -> None:
    """Render the main UTC range without suggesting local-time precision."""
    st.caption(f"Rango UTC · {_format(start)} → {_format(end)}")

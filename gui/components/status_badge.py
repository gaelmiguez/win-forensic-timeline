"""Compact semantic badges for operational state."""

from __future__ import annotations

import streamlit as st


BADGE_COLORS = {
    "success": "green",
    "warning": "orange",
    "error": "red",
    "info": "blue",
    "neutral": "gray",
}


def render_status_badge(label: str, status: str = "neutral") -> None:
    """Render a text-labelled status that never relies on color alone."""
    st.badge(label, color=BADGE_COLORS.get(status, "gray"))

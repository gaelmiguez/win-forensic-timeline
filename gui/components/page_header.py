"""Consistent page headings for the forensic GUI."""

from __future__ import annotations

import streamlit as st


def render_page_header(
    title: str,
    description: str,
    *,
    status: tuple[str, str] | None = None,
) -> None:
    """Render a compact heading with optional operational status."""
    heading, state = st.columns([5, 2], vertical_alignment="center")
    with heading:
        st.title(title)
        st.caption(description)
    if status:
        from gui.components.status_badge import render_status_badge

        with state:
            render_status_badge(status[0], status[1])
    st.divider()

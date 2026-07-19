"""Consistent source legend for forensic views."""

from __future__ import annotations

import streamlit as st


SOURCE_BADGES = {
    "BrowserHistory": "blue",
    "EVTX": "violet",
    "Prefetch": "orange",
    "Registry": "green",
    "Desconocida": "gray",
}


def render_source_legend(sources: list[str] | tuple[str, ...]) -> None:
    """Render source labels with redundant text and color encoding."""
    unique = sorted({str(source or "Desconocida") for source in sources})
    if not unique:
        return
    with st.container(horizontal=True, gap="small"):
        st.caption("Fuentes")
        for source in unique:
            st.badge(source, color=SOURCE_BADGES.get(source, "gray"))

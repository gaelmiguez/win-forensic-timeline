"""Presentation helpers for output loading status."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from gui.models import LoadResult, LoadStatus


def render_file_status(label: str, path: Path | None, result: LoadResult | None) -> None:
    """Render a compact status line without exposing full local paths."""
    if path is None:
        st.badge(f"{label} · Ausente", color="gray")
        return
    if result is None:
        st.badge(f"{label} · Detectado", color="blue")
        return
    detail = (
        f"{result.records_accepted} aceptados, "
        f"{result.records_rejected} rechazados"
    )
    if result.status is LoadStatus.ERROR:
        st.badge(f"{label} · Error", color="red")
        st.caption(detail)
    elif result.status is LoadStatus.PARTIAL:
        st.badge(f"{label} · Parcial", color="orange")
        st.caption(detail)
    elif result.status is LoadStatus.EMPTY:
        st.badge(f"{label} · Vacío", color="gray")
    else:
        st.badge(f"{label} · OK", color="green")

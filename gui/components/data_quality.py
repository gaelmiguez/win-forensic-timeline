"""Data-quality summary for accepted, rejected and traceable events."""

from __future__ import annotations

import streamlit as st


def render_data_quality_summary(
    *, accepted: int, rejected: int, traceable: int, issues: int
) -> None:
    """Render explicit quality counts without synthesizing a quality score."""
    with st.container(border=True):
        st.subheader("Calidad de carga")
        for label, value in (
            ("Aceptados", accepted),
            ("Rechazados", rejected),
            ("Trazables", traceable),
            ("Incidencias", issues),
        ):
            st.markdown(f"**{label}:** {value}")

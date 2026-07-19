"""Methodological scope notice shared by validation views."""

from __future__ import annotations

import streamlit as st


def render_methodology_warning() -> None:
    """Keep controlled validation metrics in their proper scope."""
    st.info(
        "Las métricas de los escenarios controlados validan el pipeline en "
        "condiciones conocidas. No representan por sí solas el comportamiento "
        "ante evidencias reales complejas, incompletas o ambiguas."
    )

"""Shared empty-state messages."""

from __future__ import annotations

import streamlit as st


def render_empty_state(
    title: str = "No hay resultados cargados",
    message: str = "Cargue resultados existentes o ejecute un análisis desde Inicio.",
) -> None:
    """Render a clear empty state without raising an exception."""
    with st.container(border=True):
        st.subheader(title)
        st.write(message)
        st.caption("La aplicación permanece en modo local y no modifica evidencias ni resultados.")


def render_error_state(title: str, message: str) -> None:
    """Render a bounded error state without exposing a traceback."""
    with st.container(border=True):
        st.subheader(title)
        st.error(message)
        st.caption("Revise la ruta o el estado de los archivos y vuelva a intentarlo.")

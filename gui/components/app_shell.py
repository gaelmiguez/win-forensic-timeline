"""Application identity and persistent sidebar context."""

from __future__ import annotations

import streamlit as st

from gui.config import GUI_VERSION
from gui.theme.theme_loader import (
    APP_BRAND_DARK_PATH,
    APP_BRAND_PATH,
    APP_MARK_PATH,
    current_theme_is_dark,
)


def render_app_identity() -> None:
    """Render the original local mark and concise workspace identity."""
    brand = APP_BRAND_DARK_PATH if current_theme_is_dark() else APP_BRAND_PATH
    st.logo(str(brand), size="large", icon_image=str(APP_MARK_PATH))


def render_sidebar_footer() -> None:
    """Render persistent local, UTC and data-state context."""
    with st.sidebar:
        st.divider()
        data_state = "Datos cargados" if st.session_state.get("event_result") else "Sin datos"
        st.caption(f"Solo local · UTC · Versión {GUI_VERSION} · {data_state}")

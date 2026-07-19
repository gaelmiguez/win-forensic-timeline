"""Entry point for the local forensic results GUI."""

from __future__ import annotations

import streamlit as st

from gui.components.app_shell import render_app_identity, render_sidebar_footer
from gui.services.state_service import initialize_state
from gui.theme.theme_loader import APP_MARK_PATH, load_forensic_clarity_theme


def main() -> None:
    """Configure the application and run the selected page."""
    st.set_page_config(
        page_title="Win Forensic Timeline",
        page_icon=str(APP_MARK_PATH),
        layout="wide",
        initial_sidebar_state="expanded",
    )
    load_forensic_clarity_theme()
    render_app_identity()
    initialize_state(st.session_state)

    pages = {
        "Análisis": [
            st.Page("pages/home.py", title="Inicio y ejecución", icon=":material/home:", default=True),
            st.Page("pages/dashboard.py", title="Dashboard", icon=":material/space_dashboard:"),
            st.Page("pages/timeline.py", title="Timeline", icon=":material/timeline:"),
            st.Page("pages/event_explorer.py", title="Explorador", icon=":material/table_view:"),
            st.Page("pages/event_detail.py", title="Detalle", icon=":material/manage_search:"),
        ],
        "Comprobación": [
            st.Page("pages/validation.py", title="Validación", icon=":material/fact_check:"),
            st.Page("pages/export.py", title="Exportación", icon=":material/download:"),
        ],
        "Sistema": [
            st.Page("pages/about.py", title="Ayuda y limitaciones", icon=":material/help:"),
        ],
    }
    st.navigation(pages, position="sidebar").run()
    render_sidebar_footer()


if __name__ == "__main__":
    main()

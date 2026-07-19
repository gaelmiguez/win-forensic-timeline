"""High-signal event summary used by detail and contextual navigation."""

from __future__ import annotations

from collections.abc import Mapping

import streamlit as st

from gui.components.status_badge import render_status_badge


def render_event_summary(event: Mapping[str, object], traceable: bool) -> None:
    """Render event identity, time and action before heavy evidence fields."""
    with st.container(border=True):
        top = st.columns([4, 1])
        top[0].subheader(str(event.get("object") or "Objeto no disponible"))
        with top[1]:
            render_status_badge(
                "Trazabilidad disponible" if traceable else "Trazabilidad incompleta",
                "success" if traceable else "warning",
            )
        st.caption(f"ID del evento · {event.get('event_id') or 'No disponible'}")
        details = st.columns(4)
        details[0].caption("Timestamp UTC")
        details[0].write(event.get("timestamp_utc") or "No disponible")
        details[1].caption("Fuente")
        details[1].write(event.get("source_artifact") or "No disponible")
        details[2].caption("Acción")
        details[2].write(event.get("event_action") or "No disponible")
        details[3].caption("Parser")
        details[3].write(event.get("parser_module") or "No disponible")

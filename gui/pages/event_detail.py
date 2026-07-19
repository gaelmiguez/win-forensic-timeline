"""Normalized event detail and provenance inspection."""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from gui.components.empty_state import render_empty_state
from gui.components.event_summary import render_event_summary
from gui.components.page_header import render_page_header
from gui.config import CONFIDENCE_HELP_TEXT, EVENT_FIELD_LABELS
from gui.runtime import loaded_events
from gui.services.event_detail_service import (
    event_has_traceability,
    find_event,
    is_reliably_synthetic,
    mask_path,
)


NORMALIZED_FIELDS = (
    "timestamp_utc",
    "timestamp_local",
    "timestamp_type",
    "source_artifact",
    "event_category",
    "event_action",
    "object",
    "description",
    "parser_module",
    "confidence",
    "scenario_id",
)


def _json_value(value: object) -> object:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    if isinstance(value, float) and pd.isna(value):
        return None
    return value


def _display_value(value: object) -> object:
    """Return a human-readable placeholder for absent scalar values."""
    if value in (None, ""):
        return "No disponible"
    if not isinstance(value, (dict, list, tuple)):
        try:
            if pd.isna(value):
                return "No disponible"
        except (TypeError, ValueError):
            pass
    return value


def _render_field_grid(event: pd.Series) -> None:
    rows = [NORMALIZED_FIELDS[index : index + 2] for index in range(0, len(NORMALIZED_FIELDS), 2)]
    for fields in rows:
        columns = st.columns(2)
        for column, field in zip(columns, fields):
            column.caption(EVENT_FIELD_LABELS[field])
            value = _display_value(event.get(field))
            if field == "confidence":
                column.info(str(value))
                column.caption(CONFIDENCE_HELP_TEXT)
            else:
                column.write(value)


def render() -> None:
    render_page_header(
        "Detalle y trazabilidad",
        "Inspección del evento normalizado, su localización y la procedencia registrada.",
    )
    frame = loaded_events(st.session_state)
    if frame.empty:
        render_empty_state()
        return
    ids = [str(value) for value in frame["event_id"].dropna().tolist()]
    current = st.session_state.get("selected_event_id")
    selected = st.selectbox(
        "ID del evento",
        ids,
        index=ids.index(current) if current in ids else None,
        placeholder="Seleccione un evento",
        key="detail_event_selection",
    )
    if not selected:
        render_empty_state("Ningún evento seleccionado", "Elija un evento para inspeccionarlo.")
        return
    st.session_state["selected_event_id"] = selected
    event = find_event(frame, selected)
    if event is None:
        st.error("El evento seleccionado ya no existe en el dataset cargado.")
        return

    traceable = event_has_traceability(event)
    render_event_summary(event, traceable)
    parsed_timestamp = pd.to_datetime(event.get("timestamp_utc"), errors="coerce", utc=True)
    notices = []
    if not traceable:
        notices.append("La trazabilidad del evento está ausente o incompleta.")
    if pd.isna(parsed_timestamp):
        notices.append("El timestamp UTC no puede interpretarse.")
    if is_reliably_synthetic(event):
        notices.append("El identificador de escenario declara explícitamente datos sintéticos.")
    for notice in notices:
        st.warning(notice)

    normalized_column, provenance_column = st.columns([3, 2], gap="large")
    with normalized_column:
        with st.container(border=True):
            st.subheader("Evento normalizado")
            _render_field_grid(event)
    with provenance_column:
        with st.container(border=True):
            st.subheader("Localización y referencia")
            show_full = st.toggle(
                "Mostrar rutas completas",
                value=bool(st.session_state.get("show_full_paths", False)),
                key="detail_show_full_paths",
            )
            st.session_state["show_full_paths"] = show_full
            location = mask_path(event.get("source_location"), show_full=show_full)
            st.caption(EVENT_FIELD_LABELS["source_location"])
            st.code(location or "No disponible", language=None)
            st.caption(EVENT_FIELD_LABELS["traceability_ref"])
            st.code(str(event.get("traceability_ref") or "No disponible"), language=None)
            st.caption(
                "La ruta completa permanece oculta por defecto para reducir exposición accidental."
            )

    evidence_tab, provenance_tab, event_tab = st.tabs(
        ["Evidencia cruda", "Procedencia (provenance)", "Evento completo"]
    )
    with evidence_tab:
        st.json(_json_value(event.get("raw_evidence")), expanded=False)
    with provenance_tab:
        provenance = _json_value(event.get("provenance"))
        if not provenance:
            st.warning("No hay procedencia estructurada disponible.")
        st.json(provenance, expanded=False)
        st.caption(
            "La procedencia (provenance) documenta la evidencia original, el parser, la transformación "
            "temporal y la referencia de trazabilidad."
        )
    with event_tab:
        canonical = {
            key: _json_value(event.get(key))
            for key in event.keys()
            if not str(key).startswith("_ui_")
        }
        st.json(canonical, expanded=False)


render()

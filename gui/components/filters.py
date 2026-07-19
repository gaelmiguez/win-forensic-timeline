"""Reusable Streamlit controls backed by the pure filter service."""

from __future__ import annotations

from datetime import datetime, time, timezone

import pandas as pd
import streamlit as st

from gui.models import FilterCriteria, FilterResult
from gui.services.filter_service import available_filter_values, filter_events


def _defaults(current: FilterCriteria, field: str, available: list[str]) -> list[str]:
    selected = getattr(current, field)
    return [value for value in selected if value in available]


def render_event_filters(
    frame: pd.DataFrame, key_prefix: str = "shared"
) -> FilterResult:
    """Render all supported filters and return their pure-service result."""
    current = st.session_state.get("active_filters", FilterCriteria())
    values, value_issues = available_filter_values(frame)
    with st.container(border=True):
        heading = st.columns([5, 1], vertical_alignment="center")
        heading[0].subheader("Filtros de investigación")
        top = st.columns([1.2, 1, 1, 1.6])
        sources = top[0].multiselect(
            "Fuente",
            values["source_artifact"],
            default=_defaults(current, "source_artifacts", values["source_artifact"]),
            placeholder="Seleccionar…",
            key=f"{key_prefix}_sources",
        )
        categories = top[1].multiselect(
            "Categoría",
            values["event_category"],
            default=_defaults(current, "event_categories", values["event_category"]),
            placeholder="Seleccionar…",
            key=f"{key_prefix}_categories",
        )
        actions = top[2].multiselect(
            "Acción",
            values["event_action"],
            default=_defaults(current, "event_actions", values["event_action"]),
            placeholder="Seleccionar…",
            key=f"{key_prefix}_actions",
        )
        text = top[3].text_input(
            "Texto en objeto, descripción, acción o fuente",
            value=current.text,
            key=f"{key_prefix}_text",
        )

        with st.expander("Más filtros", expanded=False):
            middle = st.columns(3)
            parsers = middle[0].multiselect(
                "Parser",
                values["parser_module"],
                default=_defaults(current, "parser_modules", values["parser_module"]),
                placeholder="Seleccionar…",
                key=f"{key_prefix}_parsers",
            )
            scenarios = middle[1].multiselect(
                "Escenario",
                values["scenario_id"],
                default=_defaults(current, "scenario_ids", values["scenario_id"]),
                placeholder="Seleccionar…",
                key=f"{key_prefix}_scenarios",
            )
            traceability_label = middle[2].selectbox(
                "Trazabilidad",
                ("Todos", "Con trazabilidad", "Sin trazabilidad"),
                key=f"{key_prefix}_traceability",
            )

            timestamp_values = frame.get("_ui_timestamp_utc")
            if timestamp_values is None:
                timestamp_values = frame.get("timestamp_utc")
            timestamps = (
                pd.to_datetime(timestamp_values, errors="coerce", utc=True)
                if timestamp_values is not None
                else pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")
            )
            valid_timestamps = timestamps.dropna()
            range_enabled = st.checkbox(
                "Aplicar rango temporal UTC",
                value=current.start_utc is not None or current.end_utc is not None,
                disabled=valid_timestamps.empty,
                key=f"{key_prefix}_range_enabled",
            )
            start_utc = None
            end_utc = None
            if range_enabled and not valid_timestamps.empty:
                date_columns = st.columns(2)
                start_date = date_columns[0].date_input(
                    "Fecha inicial UTC",
                    value=valid_timestamps.min().date(),
                    min_value=valid_timestamps.min().date(),
                    max_value=valid_timestamps.max().date(),
                    key=f"{key_prefix}_start_date",
                )
                end_date = date_columns[1].date_input(
                    "Fecha final UTC",
                    value=valid_timestamps.max().date(),
                    min_value=valid_timestamps.min().date(),
                    max_value=valid_timestamps.max().date(),
                    key=f"{key_prefix}_end_date",
                )
                start_utc = datetime.combine(start_date, time.min, tzinfo=timezone.utc)
                end_utc = datetime.combine(end_date, time.max, tzinfo=timezone.utc)

            confidence_enabled = st.checkbox(
                "Filtrar indicador de confianza",
                value=current.confidence_min is not None
                or current.confidence_max is not None,
                disabled="confidence" not in frame,
                key=f"{key_prefix}_confidence_enabled",
            )
            confidence_min = None
            confidence_max = None
            if confidence_enabled:
                confidence_min, confidence_max = st.slider(
                    "Intervalo del indicador de confianza",
                    min_value=0.0,
                    max_value=1.0,
                    value=(
                        current.confidence_min if current.confidence_min is not None else 0.0,
                        current.confidence_max if current.confidence_max is not None else 1.0,
                    ),
                    step=0.05,
                    key=f"{key_prefix}_confidence",
                )

        if heading[1].button("Restablecer", key=f"{key_prefix}_reset"):
            st.session_state["active_filters"] = FilterCriteria()
            for suffix in (
                "sources",
                "categories",
                "actions",
                "parsers",
                "scenarios",
                "traceability",
                "text",
                "range_enabled",
                "start_date",
                "end_date",
                "confidence_enabled",
                "confidence",
            ):
                st.session_state.pop(f"{key_prefix}_{suffix}", None)
            st.rerun()

    traceability = {
        "Todos": None,
        "Con trazabilidad": True,
        "Sin trazabilidad": False,
    }[traceability_label]
    criteria = FilterCriteria(
        start_utc=start_utc,
        end_utc=end_utc,
        source_artifacts=tuple(sources),
        event_categories=tuple(categories),
        event_actions=tuple(actions),
        parser_modules=tuple(parsers),
        scenario_ids=tuple(scenarios),
        text=text,
        has_traceability=traceability,
        confidence_min=confidence_min,
        confidence_max=confidence_max,
    )
    st.session_state["active_filters"] = criteria
    result = filter_events(frame, criteria)
    result.issues = value_issues + result.issues
    return result

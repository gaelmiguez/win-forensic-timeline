"""Operational dashboard for loaded normalized events."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from gui.components.empty_state import render_empty_state
from gui.components.dataset_context import render_dataset_context
from gui.components.event_table import render_event_table
from gui.components.metrics import render_metric_grid
from gui.components.page_header import render_page_header
from gui.components.source_legend import render_source_legend
from gui.components.utc_range import render_utc_range
from gui.config import SOURCE_COLORS
from gui.runtime import loaded_events
from gui.services.dashboard_service import (
    aggregate_temporal,
    compute_dashboard_metrics,
    confidence_values_by_source,
    count_by,
    traceability_by_source,
)
from gui.theme.plotly_theme import apply_forensic_clarity_theme
from gui.theme.theme_loader import current_theme_is_dark


def _chart(
    figure, *, title: str, height: int = 330, show_legend: bool | None = None
) -> None:
    st.plotly_chart(
        apply_forensic_clarity_theme(
            figure,
            title=title,
            height=height,
            dark=current_theme_is_dark(),
            show_legend=show_legend,
        ),
        width="stretch",
    )


def render() -> None:
    render_page_header(
        "Dashboard",
        "Panorama operativo de volumen, tiempo, procedencia y calidad de carga.",
        status=("UTC", "info"),
    )
    frame = loaded_events(st.session_state)
    if frame.empty:
        render_empty_state()
        return
    validation_result = st.session_state.get("validation_result")
    event_result = st.session_state.get("event_result")
    metrics = compute_dashboard_metrics(
        frame,
        validation_scenarios=len(validation_result.data) if validation_result else 0,
        rejected_rows=event_result.records_rejected if event_result else 0,
        issue_count=len(st.session_state.get("load_issues", [])),
    )
    render_metric_grid(
        (
            ("Eventos válidos", metrics.total_events),
            ("Fuentes", metrics.source_count),
            ("Con trazabilidad", metrics.traceable_events),
            ("Escenarios", metrics.validation_scenarios),
            ("Rechazados", metrics.rejected_rows),
            ("Incidencias", metrics.issue_count),
        ),
        columns=3,
    )
    render_utc_range(metrics.start_utc, metrics.end_utc)
    render_dataset_context(frame)
    render_source_legend(frame["source_artifact"].dropna().astype(str).tolist())

    source_counts = count_by(frame, "source_artifact")
    category_counts = count_by(frame, "event_category")
    temporal = aggregate_temporal(frame)
    confidence = confidence_values_by_source(frame)
    traceability = traceability_by_source(frame)

    primary = st.columns([2, 1], gap="large")
    with primary[0]:
        if temporal.empty:
            st.warning("No hay timestamps válidos para representar actividad temporal.")
        else:
            _chart(
                px.line(
                    temporal,
                    x="timestamp_utc",
                    y="events",
                    color="source_artifact",
                    color_discrete_map=SOURCE_COLORS,
                    markers=True,
                    labels={
                        "timestamp_utc": "Tiempo UTC",
                        "events": "Eventos",
                        "source_artifact": "Fuente",
                    },
                ),
                title="Actividad temporal",
                height=390,
                show_legend=False,
            )
    with primary[1]:
        _chart(
            px.bar(
                source_counts,
                x="events",
                y="source_artifact",
                color="source_artifact",
                color_discrete_map=SOURCE_COLORS,
                orientation="h",
                labels={"source_artifact": "Fuente", "events": "Eventos"},
            ),
            title="Eventos por fuente",
            height=390,
            show_legend=False,
        )

    categories_tab, trace_tab, confidence_tab = st.tabs(
        ["Categorías", "Trazabilidad", "Indicador de confianza por fuente"]
    )
    with categories_tab:
        _chart(
            px.bar(
                category_counts.head(12),
                x="event_category",
                y="events",
                labels={"event_category": "Categoría", "events": "Eventos"},
            ),
            title="Categorías más frecuentes",
            show_legend=False,
        )
    with trace_tab:
        _chart(
            px.bar(
                traceability,
                x="source_artifact",
                y="events",
                color="traceability",
                barmode="stack",
                labels={
                    "source_artifact": "Fuente",
                    "events": "Eventos",
                    "traceability": "Estado",
                },
            ),
            title="Trazabilidad por fuente",
        )
    with confidence_tab:
        if confidence.empty:
            st.info("No hay valores del indicador de confianza disponibles.")
        else:
            _chart(
                px.box(
                    confidence,
                    x="source_artifact",
                    y="confidence",
                    color="source_artifact",
                    color_discrete_map=SOURCE_COLORS,
                    points="outliers",
                    labels={"source_artifact": "Fuente", "confidence": "Indicador"},
                ),
                title="Distribución heurística por fuente",
            )
            st.caption(
                "Indicador heurístico asignado por cada parser; no constituye una "
                "probabilidad calibrada ni permite comparar directamente fuentes diferentes."
            )

    st.subheader("Eventos recientes")
    recent = frame.sort_values("_ui_timestamp_utc", ascending=False, na_position="last").head(12)
    render_event_table(recent, key="dashboard_recent_events")


render()

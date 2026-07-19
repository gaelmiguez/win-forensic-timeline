"""Interactive detailed or aggregated temporal view."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from gui.components.empty_state import render_empty_state
from gui.components.dataset_context import render_dataset_context
from gui.components.event_table import render_event_table
from gui.components.filters import render_event_filters
from gui.components.issues import render_issues
from gui.components.page_header import render_page_header
from gui.components.source_legend import render_source_legend
from gui.config import DETAILED_TIMELINE_LIMIT, EVENT_FIELD_LABELS, SOURCE_COLORS
from gui.runtime import loaded_events
from gui.services.timeline_service import build_timeline_view
from gui.theme.plotly_theme import apply_forensic_clarity_theme
from gui.theme.theme_loader import current_theme_is_dark


def _shorten(value: object, limit: int = 120) -> str:
    text = str(value or "")
    return text if len(text) <= limit else text[: limit - 3] + "..."


def render() -> None:
    render_page_header(
        "Timeline",
        "Exploración temporal en UTC con detalle adaptativo y agregación explícita.",
    )
    frame = loaded_events(st.session_state)
    if frame.empty:
        render_empty_state()
        return
    render_dataset_context(frame)
    filtered = render_event_filters(frame, key_prefix="timeline")
    render_issues(filtered.issues)
    if filtered.data.empty:
        render_empty_state("Sin coincidencias", "Modifique los filtros activos.")
        return

    mode_controls = st.columns([3, 1])
    requested_granularity = mode_controls[1].selectbox(
        "Granularidad agregada",
        ("automática", "minuto", "hora", "día", "semana"),
        key="timeline_granularity",
    )
    view = build_timeline_view(
        filtered.data,
        None if requested_granularity == "automática" else requested_granularity,
    )
    with mode_controls[0]:
        st.badge(
            "Vista detallada" if view.mode == "detailed" else "Vista agregada",
            color="blue" if view.mode == "detailed" else "orange",
        )
        st.caption(
            f"{view.valid_timestamps} timestamps válidos · "
            f"{view.invalid_timestamps} inválidos · referencia UTC"
        )
    render_source_legend(filtered.data["source_artifact"].dropna().astype(str).tolist())
    if view.invalid_timestamps:
        st.warning(
            f"{view.invalid_timestamps} evento(s) con timestamp inválido no aparecen "
            "en la gráfica, pero permanecen en el dataset original."
        )

    if view.mode == "detailed":
        plot_frame = view.data.copy()
        descriptions = plot_frame.get("description")
        plot_frame["_ui_description_short"] = (
            descriptions.map(_shorten) if descriptions is not None else ""
        )
        hover_data = {
            column: True
            for column in (
                "event_action",
                "object",
                "_ui_description_short",
                "parser_module",
                "confidence",
                "event_id",
            )
            if column in plot_frame
        }
        figure = px.scatter(
            plot_frame,
            x="_ui_timestamp_utc",
            y="source_artifact",
            color="source_artifact",
            color_discrete_map=SOURCE_COLORS,
            hover_name="object" if "object" in plot_frame else None,
            hover_data=hover_data,
            labels={
                "_ui_timestamp_utc": "Tiempo UTC",
                "source_artifact": "Fuente",
                "event_action": EVENT_FIELD_LABELS["event_action"],
                "object": EVENT_FIELD_LABELS["object"],
                "_ui_description_short": EVENT_FIELD_LABELS["description"],
                "parser_module": EVENT_FIELD_LABELS["parser_module"],
                "confidence": EVENT_FIELD_LABELS["confidence"],
                "event_id": EVENT_FIELD_LABELS["event_id"],
            },
        )
        figure.update_traces(marker={"size": 9, "opacity": 0.82})
        st.plotly_chart(
            apply_forensic_clarity_theme(
                figure,
                title=f"Eventos individuales · {view.valid_timestamps} visibles",
                height=520,
                dark=current_theme_is_dark(),
            ),
            width="stretch",
            key="timeline_detailed_chart",
        )
        ids = plot_frame.get("event_id")
        if ids is not None:
            options = [str(value) for value in ids.dropna().tolist()]
            selection = st.columns([3, 1])
            selected = selection[0].selectbox(
                "Seleccionar ID del evento",
                options,
                index=options.index(st.session_state.get("selected_event_id"))
                if st.session_state.get("selected_event_id") in options
                else None,
                placeholder="Seleccione un evento",
                key="timeline_event_selection",
            )
            if selected:
                st.session_state["selected_event_id"] = selected
                selection[1].page_link(
                    "pages/event_detail.py",
                    label="Abrir detalle",
                    icon=":material/manage_search:",
                )
        st.subheader("Eventos visibles")
        render_event_table(plot_frame.head(12), key="timeline_visible_events")
    else:
        st.warning(
            f"Vista agregada por {view.granularity}: {view.valid_timestamps} eventos "
            f"superan el umbral de {DETAILED_TIMELINE_LIMIT}. La agregación no oculta "
            "eventos; los resume por intervalo y fuente."
        )
        if view.data.empty:
            st.info("No hay timestamps válidos para agregar.")
            return
        figure = px.bar(
            view.data,
            x="timestamp_utc",
            y="events",
            color="source_artifact",
            color_discrete_map=SOURCE_COLORS,
            barmode="stack",
            labels={
                "timestamp_utc": "Tiempo UTC",
                "events": "Eventos",
                "source_artifact": "Fuente",
            },
        )
        st.plotly_chart(
            apply_forensic_clarity_theme(
                figure,
                title=f"Actividad agregada · {view.valid_timestamps} eventos",
                height=520,
                dark=current_theme_is_dark(),
            ),
            width="stretch",
            key="timeline_aggregated_chart",
        )


render()

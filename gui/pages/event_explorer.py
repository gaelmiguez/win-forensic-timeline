"""Filtered, sorted and paginated event explorer."""

from __future__ import annotations

import streamlit as st

from gui.components.empty_state import render_empty_state
from gui.components.event_table import render_event_table
from gui.components.filters import render_event_filters
from gui.components.issues import render_issues
from gui.components.metrics import render_metric_grid
from gui.components.page_header import render_page_header
from gui.config import DEFAULT_PAGE_SIZE, PAGE_SIZE_OPTIONS
from gui.runtime import loaded_events
from gui.services.pagination_service import paginate_events


SORT_LABELS = {
    "Timestamp UTC": "timestamp_utc",
    "Fuente": "source_artifact",
    "Categoría": "event_category",
    "Acción": "event_action",
    "Indicador de confianza": "confidence",
}


def render() -> None:
    render_page_header(
        "Explorador de eventos",
        "Tabla operativa con filtrado, ordenación, paginación y selección persistente.",
    )
    frame = loaded_events(st.session_state)
    if frame.empty:
        render_empty_state()
        return
    filtered = render_event_filters(frame, key_prefix="explorer")
    render_issues(filtered.issues)
    st.subheader("Resultados filtrados")
    controls = st.columns([1.2, 1, 1, 1])
    sort_label = controls[0].selectbox("Ordenar por", tuple(SORT_LABELS))
    ascending = controls[1].selectbox("Dirección", ("Ascendente", "Descendente"))
    page_size = controls[2].selectbox(
        "Filas por página",
        PAGE_SIZE_OPTIONS,
        index=PAGE_SIZE_OPTIONS.index(DEFAULT_PAGE_SIZE),
    )
    requested_page = controls[3].number_input(
        "Página", min_value=1, value=1, step=1, key="explorer_page"
    )
    page = paginate_events(
        filtered.data,
        int(requested_page),
        int(page_size),
        SORT_LABELS[sort_label],
        ascending == "Ascendente",
    )
    render_metric_grid(
        (
            ("Eventos filtrados", page.total_rows),
            ("Página", f"{page.page} de {page.total_pages}"),
            ("Filas visibles", len(page.data)),
        ),
        columns=3,
    )
    if page.data.empty:
        render_empty_state("Sin coincidencias", "Modifique los filtros activos.")
        return
    render_event_table(page.data, key="explorer_event_table")
    ids = (
        [str(value) for value in page.data["event_id"].dropna().tolist()]
        if "event_id" in page.data
        else []
    )
    if ids:
        current = st.session_state.get("selected_event_id")
        index = ids.index(current) if current in ids else None
        selected = st.selectbox(
            "ID del evento seleccionado",
            ids,
            index=index,
            placeholder="Seleccione un evento",
            key="explorer_event_selection",
        )
        if selected:
            st.session_state["selected_event_id"] = selected
            st.page_link(
                "pages/event_detail.py",
                label="Abrir detalle y trazabilidad",
                icon=":material/manage_search:",
            )


render()

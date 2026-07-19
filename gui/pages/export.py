"""Explicit in-memory export of the filtered canonical event set."""

from __future__ import annotations

import streamlit as st

from gui.components.empty_state import render_empty_state
from gui.components.event_table import render_event_table
from gui.components.filters import render_event_filters
from gui.components.issues import render_issues
from gui.components.metrics import render_metric_grid
from gui.components.page_header import render_page_header
from gui.runtime import loaded_events
from gui.services.export_service import build_export, build_filter_manifest


FORMAT_LABELS = {"CSV": "csv", "JSON": "json", "JSONL": "jsonl"}


def _size_label(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KiB"
    return f"{size / (1024 * 1024):.1f} MiB"


def render() -> None:
    render_page_header(
        "Exportación",
        "Preparación explícita y en memoria del conjunto filtrado de CommonEvent.",
    )
    frame = loaded_events(st.session_state)
    if frame.empty:
        render_empty_state()
        return
    st.warning(
        "Las exportaciones pueden contener rutas, nombres de usuario, identificadores "
        "del sistema y otros datos sensibles. Revise el contenido antes de compartirlo."
    )
    filtered = render_event_filters(frame, key_prefix="export")
    render_issues(filtered.issues)
    render_metric_grid(
        (("Eventos de origen", len(frame)), ("Eventos filtrados", len(filtered.data))),
        columns=2,
    )
    if filtered.data.empty:
        render_empty_state("Sin eventos para exportar", "Modifique los filtros activos.")
        return

    settings, preview = st.columns([1, 2], gap="large")
    with settings:
        with st.container(border=True):
            st.subheader("Preparar descarga")
            format_label = st.radio(
                "Formato",
                tuple(FORMAT_LABELS),
                horizontal=True,
                key="export_format",
            )
            include_manifest = st.checkbox(
                "Preparar también el manifiesto de filtros", value=True
            )
            payload = build_export(filtered.data, FORMAT_LABELS[format_label])
            st.caption(f"Tamaño estimado · {_size_label(len(payload.content))}")
            st.download_button(
                f"Descargar {format_label}",
                data=payload.content,
                file_name=payload.file_name,
                mime=payload.mime_type,
                type="primary",
                use_container_width=True,
            )
            if include_manifest:
                manifest = build_filter_manifest(
                    st.session_state["active_filters"],
                    st.session_state.get("active_output_root"),
                    len(frame),
                    len(filtered.data),
                )
                st.download_button(
                    "Descargar manifiesto JSON",
                    data=manifest.content,
                    file_name=manifest.file_name,
                    mime=manifest.mime_type,
                    use_container_width=True,
                )
    with preview:
        st.subheader("Vista previa")
        render_event_table(filtered.data.head(12), key="export_preview")
        st.caption("Vista limitada a 12 filas; la descarga contiene todo el conjunto filtrado.")

    st.caption(
        "La exportación conserva las 16 claves canónicas de CommonEvent, excluye "
        "campos internos _ui_* y no escribe archivos automáticamente."
    )
    st.caption(
        "El enmascaramiento visual de rutas en Detalle no altera la copia exportada. "
        "Revise rutas y datos sensibles antes de compartir el archivo."
    )


render()

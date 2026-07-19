"""Load existing outputs or run a new isolated analysis."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from gui.components.data_quality import render_data_quality_summary
from gui.components.issues import render_issues
from gui.components.load_status import render_file_status
from gui.components.metrics import render_metric_grid
from gui.components.page_header import render_page_header
from gui.components.section_panel import section_panel
from gui.components.status_badge import render_status_badge
from gui.config import DEFAULT_EVIDENCE_ROOT, DEFAULT_GUI_RUN_ROOT, DEFAULT_OUTPUT_ROOT
from gui.models import PipelineStatus
from gui.runtime import load_output_into_state, reload_output
from gui.services.dashboard_service import compute_dashboard_metrics
from gui.services.pipeline_service import PipelineService
from gui.services.state_service import has_loaded_events


def _loaded_metrics():
    event_result = st.session_state.get("event_result")
    validation_result = st.session_state.get("validation_result")
    frame = event_result.data if event_result is not None else pd.DataFrame()
    return compute_dashboard_metrics(
        frame,
        validation_scenarios=len(validation_result.data) if validation_result else 0,
        rejected_rows=event_result.records_rejected if event_result else 0,
        issue_count=len(st.session_state.get("load_issues", [])),
    )


def _render_loaded_summary() -> None:
    catalog = st.session_state.get("catalog")
    event_result = st.session_state.get("event_result")
    validation_result = st.session_state.get("validation_result")
    if catalog is None:
        st.caption("Cargue un directorio de resultados para ver su estado aquí.")
        return
    metrics = _loaded_metrics()
    render_metric_grid(
        (
            ("Archivos", len(catalog.recognized_files)),
            ("Eventos", metrics.total_events),
            ("Rechazados", metrics.rejected_rows),
            ("Validaciones", metrics.validation_scenarios),
        ),
        columns=2,
    )
    status = st.columns(2)
    with status[0]:
        render_file_status("Eventos", catalog.events_json, event_result)
    with status[1]:
        render_file_status(
            "Timeline", catalog.timeline_csv, st.session_state.get("timeline_result")
        )
    if validation_result is None:
        st.badge("Validación ausente", color="gray")
    else:
        st.badge(f"Validaciones · {len(validation_result.data)}", color="green")
    if event_result is not None:
        render_data_quality_summary(
            accepted=event_result.records_accepted,
            rejected=event_result.records_rejected,
            traceable=metrics.traceable_events,
            issues=metrics.issue_count,
        )
    render_issues(st.session_state.get("load_issues", []))


def _render_pipeline_result() -> None:
    result = st.session_state.get("pipeline_result")
    if result is None:
        st.caption("No se ha ejecutado un análisis desde esta sesión.")
        return
    if result.status is PipelineStatus.SUCCESS:
        render_status_badge("Ejecución correcta", "success")
    elif result.status is PipelineStatus.PARTIAL:
        render_status_badge("Ejecución parcial", "warning")
    else:
        render_status_badge("Ejecución fallida", "error")
        st.error(result.error_message or "El análisis no pudo completarse.")
        return
    render_metric_grid(
        (
            ("Eventos", result.events_normalized),
            ("Timeline", result.timeline_rows),
            ("Artefactos", len(result.processed_artifacts)),
            ("Duración", f"{result.duration_seconds:.2f} s"),
        ),
        columns=2,
    )
    st.caption("Archivos generados: " + ", ".join(result.outputs))
    if result.parser_errors:
        with st.expander("Advertencias técnicas sanitizadas"):
            for message in result.parser_errors:
                st.warning(message)


def render() -> None:
    render_page_header(
        "Win Forensic Timeline",
        "Espacio local de correlación de evidencias Windows.",
        status=("Solo lectura sobre evidencias", "success"),
    )
    st.info(
        "Modo local: la interfaz revisa resultados existentes y nunca modifica las "
        "evidencias de origen. La referencia temporal principal es UTC."
    )

    workspace, context = st.columns([2, 1], gap="large")
    with workspace:
        with section_panel(
            "Cargar resultados existentes",
            "Seleccione una carpeta generada previamente por el pipeline.",
        ):
            output_value = st.text_input(
                "Directorio de resultados",
                value=st.session_state.get("active_output_root") or str(DEFAULT_OUTPUT_ROOT),
                key="home_output_root",
            )
            actions = st.columns([2, 1])
            if actions[0].button(
                "Cargar resultados", type="primary", use_container_width=True
            ):
                if not load_output_into_state(output_value, st.session_state):
                    st.error("No se encontraron resultados válidos en la ruta indicada.")
            if actions[1].button("Recargar", use_container_width=True):
                if not reload_output(st.session_state):
                    st.warning("No hay una raíz activa que recargar.")
            if st.session_state.get("load_issues") and st.session_state.get("catalog") is None:
                render_issues(st.session_state["load_issues"], expanded=True)

        with section_panel(
            "Ejecutar nuevo análisis",
            "Ejecuta el análisis en un directorio aislado y carga automáticamente "
            "los resultados generados.",
        ):
            input_value = st.text_input(
                "Directorio de evidencias",
                value=str(DEFAULT_EVIDENCE_ROOT),
                key="pipeline_input",
            )
            output_base = st.text_input(
                "Directorio para nuevas ejecuciones",
                value=str(DEFAULT_GUI_RUN_ROOT),
                key="pipeline_output_base",
            )
            confirmed = st.checkbox(
                "Confirmo el uso de evidencias en modo de solo lectura.",
                key="pipeline_read_only_confirmed",
            )
            run_disabled = st.session_state.get("pipeline_state") == "running" or not confirmed
            if st.button(
                "Ejecutar análisis",
                type="primary",
                disabled=run_disabled,
                key="run_pipeline_button",
            ):
                st.session_state["pipeline_state"] = "running"
                with st.spinner("Ejecutando el pipeline sin estimación porcentual..."):
                    result = PipelineService().run(Path(input_value), Path(output_base))
                st.session_state["pipeline_result"] = result
                st.session_state["pipeline_state"] = result.status.value
                if result.output_root is not None and result.status is not PipelineStatus.ERROR:
                    load_output_into_state(result.output_root, st.session_state)
                st.rerun()

    with context:
        with section_panel("Estado de resultados", "Resumen de la raíz activa."):
            _render_loaded_summary()
        with section_panel("Última ejecución", "Estado de la sesión actual."):
            _render_pipeline_result()
        if has_loaded_events(st.session_state):
            st.page_link(
                "pages/dashboard.py",
                label="Abrir Dashboard",
                icon=":material/arrow_forward:",
            )


render()

"""Per-scenario validation results and methodological context."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from gui.components.empty_state import render_empty_state
from gui.components.issues import render_issues
from gui.components.methodology_warning import render_methodology_warning
from gui.components.metrics import render_metric_grid
from gui.components.page_header import render_page_header
from gui.runtime import loaded_events
from gui.services.validation_view_service import (
    compact_validation_results,
    enrich_validation_results,
    format_validation_results_for_display,
    metric_rows,
    scenario_display_name,
    scenario_is_controlled,
)
from gui.theme.plotly_theme import apply_forensic_clarity_theme
from gui.theme.theme_loader import current_theme_is_dark


COMPACT_RESULT_COLUMNS = {
    "gt_id": "ID GT",
    "result": "Resultado",
    "expected_object": "Objeto esperado",
    "matched_event_reference": "Evento",
    "expected_time_utc": "Timestamp esperado",
    "time_delta_seconds": "Delta (s)",
    "traceability": "Trazabilidad",
}

DETAIL_RESULT_COLUMNS = {
    "matched_event_id": "ID completo del evento",
    "matched_event_source": "Fuente",
    "normalized_object": "Objeto normalizado",
    "detected_time_utc": "Timestamp detectado",
    "matched_traceability_ref": "Referencia del evento",
}


def _themed(figure, title: str, height: int = 330):
    return apply_forensic_clarity_theme(
        figure, title=title, height=height, dark=current_theme_is_dark()
    )


def render() -> None:
    render_page_header(
        "Validación",
        "Resultados y métricas separados por escenario y contextualizados metodológicamente.",
    )
    validation_result = st.session_state.get("validation_result")
    if validation_result is None or not validation_result.data:
        render_empty_state(
            "No hay validaciones cargadas",
            "Cargue una raíz con validation_summary_*.json o validation_results_*.csv.",
        )
        return
    scenarios = validation_result.data
    identifiers = [scenario.identifier for scenario in scenarios]
    current = st.session_state.get("selected_validation_id")
    selector, context = st.columns([2, 3], vertical_alignment="bottom")
    selected_id = selector.selectbox(
        "Escenario",
        identifiers,
        index=identifiers.index(current) if current in identifiers else 0,
        format_func=lambda value: scenario_display_name(
            next(item for item in scenarios if item.identifier == value)
        ),
        key="validation_scenario_selection",
    )
    selector.caption(f"ID técnico · {selected_id}")
    st.session_state["selected_validation_id"] = selected_id
    scenario = next(item for item in scenarios if item.identifier == selected_id)
    with context:
        if scenario_is_controlled(scenario):
            st.badge("Escenario sintético controlado", color="blue")
        elif scenario.identifier == "default":
            st.badge("Escenario no clasificado: default", color="gray")
        else:
            st.badge("Clasificación no declarada", color="gray")
    render_methodology_warning()
    if "evtx" in scenario.identifier.casefold() and not scenario_is_controlled(scenario):
        st.warning("No se afirma que EVTX disponga de ground truth controlado.")

    render_metric_grid(metric_rows(scenario), columns=6)
    events = loaded_events(st.session_state)
    results = enrich_validation_results(scenario, events)
    results_tab, charts_tab, method_tab = st.tabs(
        ["Resultados", "Gráficas", "Metodología"]
    )
    with results_tab:
        if results.empty:
            st.info("No hay filas de resultados asociadas a este resumen.")
        else:
            display_results = format_validation_results_for_display(results)
            compact_results = compact_validation_results(display_results)
            visible = [
                column for column in COMPACT_RESULT_COLUMNS if column in compact_results
            ]
            st.dataframe(
                compact_results.loc[:, visible].rename(columns=COMPACT_RESULT_COLUMNS),
                width="stretch",
                hide_index=True,
                column_config={
                    "ID GT": st.column_config.TextColumn(width="small"),
                    "Resultado": st.column_config.TextColumn(width="small"),
                    "Objeto esperado": st.column_config.TextColumn(width="medium"),
                    "Evento": st.column_config.TextColumn(width="small"),
                    "Timestamp esperado": st.column_config.TextColumn(width="medium"),
                    "Delta (s)": st.column_config.NumberColumn(width="small"),
                    "Trazabilidad": st.column_config.CheckboxColumn(width="small"),
                },
            )
            detail_visible = [
                column for column in DETAIL_RESULT_COLUMNS if column in display_results
            ]
            if detail_visible:
                with st.expander("Detalle de eventos emparejados"):
                    st.caption(
                        "El validador confirma la coincidencia buscando el objeto esperado "
                        "en el objeto normalizado, la descripción o la evidencia cruda. El "
                        "CSV no identifica cuál de esos campos produjo la coincidencia."
                    )
                    st.dataframe(
                        display_results.loc[:, detail_visible].rename(
                            columns=DETAIL_RESULT_COLUMNS
                        ),
                        width="stretch",
                        hide_index=True,
                    )
            st.caption(
                "El conteo de falsos positivos procede principalmente del resumen agregado; "
                "no se exigen filas adicionales en el CSV."
            )
    with charts_tab:
        if results.empty:
            st.info("No hay filas suficientes para construir gráficas.")
        else:
            result_counts = (
                results["result"].value_counts().rename_axis("result").reset_index(name="rows")
                if "result" in results
                else pd.DataFrame()
            )
            charts = st.columns(2)
            with charts[0]:
                if not result_counts.empty:
                    st.plotly_chart(
                        _themed(
                            px.bar(
                                result_counts,
                                x="result",
                                y="rows",
                                labels={"result": "Resultado", "rows": "Filas"},
                            ),
                            "Distribución de resultados",
                        ),
                        width="stretch",
                    )
            with charts[1]:
                if "time_delta_seconds" in results:
                    deltas = pd.to_numeric(
                        results["time_delta_seconds"], errors="coerce"
                    ).dropna()
                    if not deltas.empty:
                        st.plotly_chart(
                            _themed(
                                px.histogram(
                                    x=deltas,
                                    labels={"x": "Delta temporal (s)", "count": "Filas"},
                                ),
                                "Desviación temporal",
                            ),
                            width="stretch",
                        )
    with method_tab:
        st.subheader("Alcance de interpretación")
        st.write(
            "Los escenarios controlados comprueban normalización, emparejamiento temporal y "
            "trazabilidad bajo condiciones conocidas. No constituyen una precisión global "
            "ni sustituyen la evaluación sobre datasets reales anotados."
        )
        st.write(
            "EVTX aporta procesamiento de volumen real, pero permanece separado de los "
            "escenarios con ground truth controlado."
        )
    render_issues(scenario.issues)


render()

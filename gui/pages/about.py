"""Methodology, supported artifacts and explicit limitations."""

from __future__ import annotations

import streamlit as st

from gui.components.methodology_warning import render_methodology_warning
from gui.components.page_header import render_page_header
from gui.config import CANONICAL_EVENT_FIELDS, GUI_VERSION
from gui.services.version_service import read_project_revision


def render() -> None:
    render_page_header(
        "Ayuda, metodología y limitaciones",
        "Referencia operativa sobre alcance, interpretación, privacidad y versión.",
        status=(f"Versión {GUI_VERSION}", "neutral"),
    )
    revision = read_project_revision()
    st.caption(f"Revisión local del proyecto · {revision or 'No disponible'}")
    purpose, sources, method, privacy, limits = st.tabs(
        ["Propósito", "Fuentes", "Método", "Privacidad", "Limitaciones"]
    )
    with purpose:
        st.subheader("Espacio de correlación forense local")
        st.write(
            "La aplicación carga resultados normalizados, facilita su exploración y puede "
            "invocar localmente el pipeline existente. La secuencia es artefacto, parser, "
            "CommonEvent, correlación temporal, timeline, reportes y validación."
        )
        st.info("Referencia temporal principal: UTC. Modo local sin servicios externos.")
    with sources:
        supported, excluded = st.columns(2, gap="large")
        with supported:
            st.subheader("Fuentes soportadas")
            st.markdown(
                "- BrowserHistory desde SQLite Chromium.\n"
                "- EVTX desde registros exportados.\n"
                "- Prefetch mediante JSON sidecar.\n"
                "- Registry mediante JSON externo."
            )
        with excluded:
            st.subheader("Fuera de alcance")
            st.write(
                "UserAssist, Amcache, SRUM, Jump Lists, LNK, MFT/USN Journal, "
                "ShellBags, Prefetch binario nativo y hives Registry binarios."
            )
    with method:
        st.subheader("CommonEvent y trazabilidad")
        st.write(
            "CommonEvent conserva 16 campos canónicos. Los timestamps originales, la "
            "evidencia cruda (raw_evidence), la referencia de trazabilidad "
            "(traceability_ref) y la procedencia (provenance) mantienen el enlace con el origen."
        )
        with st.expander("Ver las 16 claves canónicas"):
            st.code("\n".join(CANONICAL_EVENT_FIELDS), language=None)
        st.subheader("Indicador de confianza")
        st.write(
            "Es un indicador heurístico asignado por cada parser. No es una probabilidad "
            "calibrada ni permite comparar directamente fuentes diferentes."
        )
        st.subheader("Validación")
        render_methodology_warning()
        st.write(
            "EVTX aporta procesamiento de volumen real, pero no dispone de ground truth "
            "controlado por la limitación de permisos observada con eventcreate."
        )
    with privacy:
        st.subheader("Controles de privacidad")
        st.write(
            "La aplicación escucha en loopback, no usa telemetría ni servicios externos, "
            "no modifica evidencias y separa cada ejecución en un directorio único."
        )
        st.write(
            "Las rutas completas se ocultan por defecto. Las exportaciones requieren una "
            "acción explícita y pueden contener datos sensibles."
        )
    with limits:
        st.subheader("Límites conocidos")
        st.markdown(
            "- El rendimiento depende del equipo y del volumen cargado.\n"
            "- Los campos pesados permanecen en memoria para el detalle.\n"
            "- La timeline se agrega de forma explícita al superar el umbral.\n"
            "- La validación sintética no equivale a una investigación real anotada.\n"
            "- La GUI no reemplaza el criterio profesional del analista."
        )


render()

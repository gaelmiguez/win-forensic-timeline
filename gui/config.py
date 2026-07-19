"""Shared constants for GUI infrastructure."""

from pathlib import Path

from gui.theme.tokens import SOURCE_COLORS

DEFAULT_OUTPUT_ROOT = Path("output")
DEFAULT_EVIDENCE_ROOT = Path("evidence")
DEFAULT_GUI_RUN_ROOT = Path("artifacts/gui_pipeline_runs")
GUI_VERSION = "0.9.0"
CONFIDENCE_HELP_TEXT = (
    "Valor heurístico asignado por el parser; no representa una probabilidad "
    "estadística calibrada."
)
DETAILED_TIMELINE_LIMIT = 5_000
DEFAULT_PAGE_SIZE = 50
PAGE_SIZE_OPTIONS = (25, 50, 100)

CANONICAL_EVENT_FIELDS = (
    "event_id",
    "timestamp_utc",
    "timestamp_local",
    "timestamp_type",
    "source_artifact",
    "source_location",
    "event_category",
    "event_action",
    "object",
    "description",
    "raw_evidence",
    "parser_module",
    "traceability_ref",
    "confidence",
    "provenance",
    "scenario_id",
)

EVENT_FIELD_LABELS = {
    "event_id": "ID del evento",
    "timestamp_utc": "Timestamp UTC",
    "timestamp_local": "Timestamp local",
    "timestamp_type": "Tipo de timestamp",
    "source_artifact": "Artefacto de origen",
    "source_location": "Localización de origen",
    "event_category": "Categoría",
    "event_action": "Acción",
    "object": "Objeto",
    "description": "Descripción",
    "raw_evidence": "Evidencia cruda",
    "parser_module": "Parser",
    "traceability_ref": "Referencia de trazabilidad",
    "confidence": "Indicador de confianza",
    "provenance": "Procedencia (provenance)",
    "scenario_id": "ID del escenario",
}

REQUIRED_TEXT_EVENT_FIELDS = (
    "event_id",
    "timestamp_utc",
    "timestamp_type",
    "source_artifact",
    "source_location",
    "event_category",
    "event_action",
    "description",
    "parser_module",
    "traceability_ref",
)

TIMELINE_JSON_FIELDS = ("raw_evidence", "provenance")

VALIDATION_RESULT_FIELDS = (
    "gt_id",
    "scenario_id",
    "action",
    "expected_time_utc",
    "expected_object",
    "expected_sources",
    "matched_event_id",
    "detected_time_utc",
    "time_delta_seconds",
    "result",
    "matched_source",
    "notes",
)

VALIDATION_RESULT_VALUES = frozenset(
    {"correcto", "parcial", "no_detectado", "falso_positivo"}
)

VALIDATION_SUMMARY_FIELDS = (
    "ground_truth_total",
    "correct",
    "partial",
    "not_detected",
    "false_positives",
    "coverage_rate",
    "correct_rate",
    "precision_rate",
    "average_time_delta_seconds",
    "max_time_delta_seconds",
    "traceability_rate",
)

PREVIEW_COLUMNS = (
    "timestamp_utc",
    "source_artifact",
    "event_category",
    "event_action",
    "object",
    "description",
    "parser_module",
    "scenario_id",
)

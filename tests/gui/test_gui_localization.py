from __future__ import annotations

from pathlib import Path

from gui.config import EVENT_FIELD_LABELS, GUI_VERSION


ROOT = Path(__file__).parents[2]
VISIBLE_SOURCE_FILES = tuple((ROOT / "gui" / "pages").glob("*.py")) + tuple(
    (ROOT / "gui" / "components").glob("*.py")
)


def test_visible_gui_text_avoids_unlocalized_or_internal_phrases():
    visible_source = "\n".join(
        path.read_text(encoding="utf-8") for path in VISIBLE_SOURCE_FILES
    )
    forbidden = (
        "Choose options",
        "Confidence por fuente",
        '"Confidence"',
        '"Issues"',
        "Ground truth ID",
        "Local only",
        "Windows evidence correlation workspace",
        "controlled synthetic",
        "GUI 9.2-9.8",
        "main.run_pipeline()",
        "Cargado · events",
        "Cargado · timeline",
        "Press Enter to apply",
    )

    assert not [phrase for phrase in forbidden if phrase in visible_source]


def test_every_multiselect_has_spanish_placeholder():
    source = (ROOT / "gui" / "components" / "filters.py").read_text(encoding="utf-8")

    assert source.count(".multiselect(") == 5
    assert source.count('placeholder="Seleccionar…"') == 5


def test_event_field_labels_cover_humanized_detail_fields():
    expected = {
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
        "parser_module": "Parser",
        "traceability_ref": "Referencia de trazabilidad",
        "confidence": "Indicador de confianza",
        "scenario_id": "ID del escenario",
    }

    assert {field: EVENT_FIELD_LABELS[field] for field in expected} == expected
    assert GUI_VERSION == "0.9.0"


def test_page_headers_do_not_render_eyebrows():
    pages = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "gui" / "pages").glob("*.py")
    )

    assert "eyebrow=" not in pages


def test_quality_labels_are_compact_and_never_ellipsized():
    source = (ROOT / "gui" / "components" / "data_quality.py").read_text(
        encoding="utf-8"
    )

    for label in ("Aceptados", "Rechazados", "Trazables", "Incidencias"):
        assert f'("{label}",' in source
    assert "text-overflow" not in source


def test_confidence_detail_is_informational_not_success_colored():
    source = (ROOT / "gui" / "pages" / "event_detail.py").read_text(
        encoding="utf-8"
    )

    assert 'if field == "confidence"' in source
    assert "column.info" in source
    assert "probabilidad" in source or "CONFIDENCE_HELP_TEXT" in source
    assert "column.success" not in source

from pathlib import Path
import json
import shutil

import pytest

pytest.importorskip("streamlit", reason="GUI dependencies are installed separately")

from streamlit.testing.v1 import AppTest

from gui.runtime import load_output_into_state
from gui.services.state_service import initialize_state


APP_PATH = Path(__file__).parents[2] / "gui" / "app.py"
CAPTURE_VALIDATION_ROOT = APP_PATH.parents[1] / "tests" / "fixtures" / "gui" / "capture_validation"


def test_application_starts_in_empty_state():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)

    assert not app.exception
    assert app.title[0].value == "Win Forensic Timeline"
    assert any("Cargar resultados existentes" in item.value for item in app.subheader)
    assert any("Modo local" in item.value for item in app.info)
    visible = "\n".join(
        item.value for group in (app.caption, app.markdown, app.subheader) for item in group
    )
    assert "main.run_pipeline()" not in visible
    assert "GUI 9.2-9.8" not in visible
    assert "Windows evidence correlation workspace" not in visible


def test_invalid_path_does_not_raise_uncaught_exception(tmp_path):
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)
    app.text_input[0].set_value(str(tmp_path / "missing"))
    app.button[0].click().run(timeout=20)

    assert not app.exception
    assert any("no existe" in item.value.lower() for item in app.error)


def test_invalid_output_clears_previous_loaded_state(tmp_path):
    state = {"catalog": "stale", "event_result": "stale"}
    initialize_state(state)

    loaded = load_output_into_state(tmp_path / "missing", state)

    assert not loaded
    assert state["catalog"] is None
    assert state["event_result"] is None
    assert state["load_issues"]


def test_pipeline_boundary_does_not_use_subprocess():
    service_path = APP_PATH.parent / "services" / "pipeline_service.py"
    source = service_path.read_text(encoding="utf-8")

    assert "from main import run_pipeline" in source
    assert "subprocess" not in source
    assert "shell=True" not in source


def test_application_loads_synthetic_output(tmp_path, canonical_event):
    (tmp_path / "events.json").write_text(
        json.dumps([canonical_event], ensure_ascii=False), encoding="utf-8"
    )
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)
    app.text_input[0].set_value(str(tmp_path))
    app.button[0].click().run(timeout=20)

    assert not app.exception
    assert any("Estado de resultados" in item.value for item in app.subheader)
    assert any(item.value == "1" for item in app.metric)


@pytest.mark.parametrize(
    "page",
    [
        "pages/dashboard.py",
        "pages/timeline.py",
        "pages/event_explorer.py",
        "pages/event_detail.py",
        "pages/export.py",
    ],
)
def test_data_pages_render_loaded_synthetic_output(tmp_path, canonical_event, page):
    (tmp_path / "events.json").write_text(
        json.dumps([canonical_event], ensure_ascii=False), encoding="utf-8"
    )
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)
    app.text_input[0].set_value(str(tmp_path))
    app.button[0].click().run(timeout=20)
    app.switch_page(page).run(timeout=20)

    assert not app.exception


@pytest.mark.parametrize(
    ("page", "title"),
    [
        ("pages/dashboard.py", "Dashboard"),
        ("pages/timeline.py", "Timeline"),
        ("pages/event_explorer.py", "Explorador de eventos"),
        ("pages/event_detail.py", "Detalle y trazabilidad"),
        ("pages/validation.py", "Validación"),
        ("pages/export.py", "Exportación"),
        ("pages/about.py", "Ayuda, metodología y limitaciones"),
    ],
)
def test_navigation_pages_start_without_outputs(page, title):
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)
    app.switch_page(page).run(timeout=20)

    assert not app.exception
    assert app.title[0].value == title


def test_validation_page_lists_three_real_controlled_scenarios(tmp_path, canonical_event):
    (tmp_path / "events.json").write_text(
        json.dumps([canonical_event], ensure_ascii=False), encoding="utf-8"
    )
    for path in CAPTURE_VALIDATION_ROOT.iterdir():
        shutil.copy2(path, tmp_path / path.name)

    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)
    app.text_input[0].set_value(str(tmp_path))
    app.button[0].click().run(timeout=20)
    app.switch_page("pages/validation.py").run(timeout=20)

    assert not app.exception
    assert app.selectbox[0].options == [
        "BrowserHistory sintético",
        "Prefetch sintético",
        "Registry sintético",
    ]
    assert all("EVTX" not in option for option in app.selectbox[0].options)


def test_event_detail_renders_selected_event_without_traceback(tmp_path, canonical_event):
    (tmp_path / "events.json").write_text(
        json.dumps([canonical_event], ensure_ascii=False), encoding="utf-8"
    )
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)
    app.text_input[0].set_value(str(tmp_path))
    app.button[0].click().run(timeout=20)
    app.switch_page("pages/event_detail.py").run(timeout=20)
    app.selectbox[0].select(canonical_event["event_id"]).run(timeout=20)

    assert not app.exception
    assert any(item.value == "Evento normalizado" for item in app.subheader)
    assert any("ID del evento" in item.value for item in app.caption)

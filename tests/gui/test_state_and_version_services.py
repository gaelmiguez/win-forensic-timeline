from __future__ import annotations

from gui.services.state_service import clear_loaded_results, initialize_state
from gui.services.version_service import read_project_revision


def test_state_defaults_do_not_replace_existing_value():
    state = {"active_output_root": "chosen"}
    initialize_state(state)

    assert state["active_output_root"] == "chosen"
    assert "active_filters" in state


def test_clear_results_preserves_pipeline_history():
    state = {"pipeline_result": "kept"}
    initialize_state(state)
    state["event_result"] = "loaded"
    clear_loaded_results(state)

    assert state["event_result"] is None
    assert state["pipeline_result"] == "kept"


def test_project_revision_can_be_read_without_subprocess():
    revision = read_project_revision()

    assert revision is None or len(revision) == 7

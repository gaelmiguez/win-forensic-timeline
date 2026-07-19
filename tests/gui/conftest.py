from __future__ import annotations

from copy import deepcopy

import pandas as pd
import pytest


@pytest.fixture
def canonical_event():
    return {
        "event_id": "event-001",
        "timestamp_utc": "2024-01-10T09:00:00+00:00",
        "timestamp_local": None,
        "timestamp_type": "visit_time",
        "source_artifact": "BrowserHistory",
        "source_location": "evidence/browser/sample/History",
        "event_category": "browser_activity",
        "event_action": "url_visit",
        "object": "https://example.com/",
        "description": "Visita sintética a example.com",
        "raw_evidence": {"url": "https://example.com/", "title": "Ejemplo"},
        "parser_module": "browser_history_parser",
        "traceability_ref": "History:urls:1",
        "confidence": 0.9,
        "provenance": {"parser": "browser_history_parser"},
        "scenario_id": "S_GUI_TEST",
    }


@pytest.fixture
def event_frame(canonical_event):
    first = deepcopy(canonical_event)
    second = deepcopy(canonical_event)
    second.update(
        {
            "event_id": "event-002",
            "timestamp_utc": "2024-01-10T09:05:00+00:00",
            "source_artifact": "Prefetch",
            "event_category": "program_execution",
            "event_action": "program_executed",
            "object": "NOTEPAD.EXE",
            "description": "Ejecución controlada de Notepad",
            "parser_module": "prefetch_parser",
            "traceability_ref": "NOTEPAD.EXE-12345678.pf",
            "confidence": 0.85,
            "provenance": {"parser_backend": "external_metadata_json"},
            "scenario_id": "S_PREFETCH_SYNTH",
        }
    )
    third = deepcopy(canonical_event)
    third.update(
        {
            "event_id": "event-003",
            "timestamp_utc": "invalid",
            "source_artifact": "Registry",
            "event_category": "persistence",
            "event_action": "registry_autorun_configured",
            "object": "ExampleApp",
            "description": "Autorun controlado",
            "parser_module": "registry_parser",
            "traceability_ref": "",
            "confidence": 0.75,
            "provenance": {},
            "scenario_id": "S_REGISTRY_SYNTH",
        }
    )
    frame = pd.DataFrame([first, second, third])
    frame["_ui_timestamp_utc"] = pd.to_datetime(
        frame["timestamp_utc"], errors="coerce", utc=True
    )
    return frame

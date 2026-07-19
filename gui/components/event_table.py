"""Privacy-aware event table rendering."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from gui.config import EVENT_FIELD_LABELS
from gui.services.dashboard_service import traceability_mask


VISIBLE_EVENT_COLUMNS = (
    "timestamp_utc",
    "source_artifact",
    "event_category",
    "event_action",
    "object",
    "description",
    "parser_module",
    "confidence",
    "scenario_id",
    "traceability",
)


def prepare_event_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Return only operational columns plus a traceability label."""
    visible = frame.copy(deep=True)
    visible["traceability"] = traceability_mask(visible).map(
        {True: "Disponible", False: "Incompleta"}
    )
    columns = [column for column in VISIBLE_EVENT_COLUMNS if column in visible]
    return visible.loc[:, columns]


def render_event_table(frame: pd.DataFrame, key: str) -> None:
    """Render a bounded event table without heavy evidence fields."""
    display = prepare_event_table(frame).rename(
        columns={**EVENT_FIELD_LABELS, "traceability": "Trazabilidad"}
    )
    st.dataframe(
        display,
        width="stretch",
        hide_index=True,
        key=key,
    )

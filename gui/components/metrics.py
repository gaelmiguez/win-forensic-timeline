"""Compact metric rendering helpers."""

from __future__ import annotations

from collections.abc import Sequence
from numbers import Number

import streamlit as st


def render_metric_grid(metrics: Sequence[tuple[str, object]], columns: int = 4) -> None:
    """Render compact top-level metric strips without inventing aggregate scores."""
    for offset in range(0, len(metrics), columns):
        with st.container(border=True):
            row = st.columns(columns)
            for index, (label, value) in enumerate(metrics[offset : offset + columns]):
                if value is None:
                    display_value: str | Number = "No disponible"
                elif isinstance(value, (str, Number)):
                    display_value = value
                else:
                    display_value = str(value)
                row[index].metric(label, display_value)

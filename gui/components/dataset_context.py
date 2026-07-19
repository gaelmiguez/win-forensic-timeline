"""Compact methodological context for mixed loaded datasets."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from gui.services.dashboard_service import mixed_dataset_notice


def render_dataset_context(frame: pd.DataFrame) -> None:
    """Show a dataset-composition note only when it can be derived safely."""
    notice = mixed_dataset_notice(frame)
    if notice:
        st.caption(notice)

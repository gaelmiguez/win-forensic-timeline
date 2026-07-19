"""Restrained containers reserved for conceptual blocks."""

from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

import streamlit as st


@contextmanager
def section_panel(title: str, description: str | None = None) -> Iterator[None]:
    """Create one semantic panel with a concise heading."""
    with st.container(border=True):
        st.subheader(title)
        if description:
            st.caption(description)
        yield

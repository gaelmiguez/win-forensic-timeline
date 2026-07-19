"""Structured issue rendering without sensitive paths or tracebacks."""

from __future__ import annotations

import streamlit as st

from gui.models import IssueSeverity, LoadIssue


def render_issues(issues: list[LoadIssue], expanded: bool = False) -> None:
    """Render loader issues using only file names and structured context."""
    if not issues:
        return
    with st.expander("Problemas de carga", expanded=expanded):
        for issue in issues:
            location = f" [{issue.path.name}]" if issue.path is not None else ""
            if issue.row_index is not None:
                location += f" fila {issue.row_index}"
            if issue.field:
                location += f" campo {issue.field}"
            message = f"{issue.code}{location}: {issue.message}"
            if issue.severity is IssueSeverity.ERROR:
                st.error(message)
            elif issue.severity is IssueSeverity.WARNING:
                st.warning(message)
            else:
                st.info(message)

"""One Plotly styling boundary for every forensic chart."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

from gui.theme.tokens import DARK_PLOTLY, LIGHT_PLOTLY


def apply_forensic_clarity_theme(
    figure: go.Figure,
    *,
    title: str | None = None,
    height: int = 360,
    dark: bool = False,
    show_legend: bool | None = None,
) -> go.Figure:
    """Apply the shared restrained theme without changing chart semantics."""
    palette = DARK_PLOTLY if dark else LIGHT_PLOTLY
    figure.update_layout(
        title={"text": title, "x": 0, "xanchor": "left"} if title else None,
        height=height,
        margin={"l": 24, "r": 16, "t": 52 if title else 20, "b": 28},
        paper_bgcolor=palette["paper"],
        plot_bgcolor=palette["paper"],
        font={
            "family": "Segoe UI, system-ui, sans-serif",
            "size": 13,
            "color": palette["text"],
        },
        title_font={"size": 16, "color": palette["text"]},
        hoverlabel={
            "bgcolor": "#F8FAFC" if not dark else "#1D2939",
            "bordercolor": palette["grid"],
            "font": {"color": palette["text"], "size": 12},
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"size": 11, "color": palette["muted"]},
            "title": None,
        },
        showlegend=show_legend,
        hovermode="closest",
    )
    axis_style: dict[str, Any] = {
        "showgrid": True,
        "gridcolor": palette["grid"],
        "gridwidth": 1,
        "linecolor": palette["axis"],
        "zeroline": False,
        "tickfont": {"color": palette["muted"], "size": 11},
        "title_font": {"color": palette["muted"], "size": 12},
        "automargin": True,
    }
    figure.update_xaxes(**axis_style)
    figure.update_yaxes(**axis_style)
    return figure

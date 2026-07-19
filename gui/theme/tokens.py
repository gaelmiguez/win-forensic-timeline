"""Central color and layout tokens shared by Streamlit and Plotly."""

SOURCE_COLORS = {
    "BrowserHistory": "#0071E3",
    "EVTX": "#5856D6",
    "Prefetch": "#C75C00",
    "Registry": "#16856C",
    "Desconocida": "#667085",
}

STATUS_COLORS = {
    "success": "#16856C",
    "warning": "#A15C00",
    "error": "#B42318",
    "info": "#0071E3",
    "neutral": "#667085",
}

LIGHT_PLOTLY = {
    "text": "#243247",
    "muted": "#667085",
    "grid": "#D8DEE8",
    "axis": "#98A2B3",
    "paper": "rgba(0,0,0,0)",
}

DARK_PLOTLY = {
    "text": "#E7ECF3",
    "muted": "#AAB4C3",
    "grid": "#344054",
    "axis": "#667085",
    "paper": "rgba(0,0,0,0)",
}

PLOTLY_COLOR_SEQUENCE = tuple(SOURCE_COLORS.values())

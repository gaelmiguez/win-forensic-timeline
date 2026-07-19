from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("streamlit", reason="GUI dependencies are installed separately")
pytest.importorskip("plotly", reason="GUI dependencies are installed separately")
import plotly.graph_objects as go

from gui.theme.plotly_theme import apply_forensic_clarity_theme
from gui.theme import theme_loader
from gui.theme.theme_loader import (
    APP_BRAND_DARK_PATH,
    APP_BRAND_PATH,
    APP_MARK_PATH,
    CSS_PATH,
    DARK_CSS_PATH,
)
from gui.theme.tokens import SOURCE_COLORS


ROOT = Path(__file__).parents[2]


def test_forensic_source_colors_match_documented_semantics():
    assert SOURCE_COLORS == {
        "BrowserHistory": "#0071E3",
        "EVTX": "#5856D6",
        "Prefetch": "#C75C00",
        "Registry": "#16856C",
        "Desconocida": "#667085",
    }


def test_css_is_local_css_only_and_uses_stable_streamlit_selectors():
    source = CSS_PATH.read_text(encoding="utf-8")

    assert "[data-testid=\"stAppViewContainer\"]" in source
    assert "[data-testid=\"stSidebar\"]" in source
    assert "@media (prefers-color-scheme: dark)" not in source
    assert "http://" not in source
    assert "https://" not in source
    assert "@import" not in source
    assert "javascript:" not in source
    assert "nth-child" not in source
    dark_source = DARK_CSS_PATH.read_text(encoding="utf-8")
    assert "#101828" in dark_source
    assert "#4da3ff" in dark_source.casefold()
    assert "#000000" not in dark_source
    assert '[data-testid="stBaseButton-primary"]' in source
    assert "color: #ffffff !important" in source
    assert '[data-testid="stIconMaterial"]' in source


def test_svg_mark_is_original_static_vector_without_active_content():
    source = APP_MARK_PATH.read_text(encoding="utf-8")

    assert "<svg" in source
    assert "<circle" in source
    assert "<script" not in source.casefold()
    assert "foreignObject" not in source
    assert "http://www.w3.org/2000/svg" in source
    assert "https://" not in source
    for brand_path in (APP_BRAND_PATH, APP_BRAND_DARK_PATH):
        brand = brand_path.read_text(encoding="utf-8")
        assert "Win Forensic Timeline" in brand
        assert "<script" not in brand.casefold()
        assert "https://" not in brand


def test_primary_button_contrast_meets_wcag_aa():
    def luminance(hex_color: str) -> float:
        values = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
        channels = [
            value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
            for value in values
        ]
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

    foreground = luminance("#FFFFFF")
    for background_color in ("#0071E3", "#005FBF", "#667085"):
        light, dark = sorted((foreground, luminance(background_color)), reverse=True)
        assert (light + 0.05) / (dark + 0.05) >= 4.5


def test_primary_button_colors_are_theme_independent():
    source = CSS_PATH.read_text(encoding="utf-8").casefold()

    assert "background: #0071e3 !important" in source
    assert "background: #005fbf !important" in source
    assert "background: #667085 !important" in source


def test_main_content_reserves_header_clearance_without_fragile_offsets():
    source = CSS_PATH.read_text(encoding="utf-8").casefold()

    assert "padding-top: 5rem" in source
    assert "margin-top: -" not in source
    assert "position: absolute" not in source
    assert "text-overflow: clip" in source


def test_theme_loader_uses_streamlit_theme_as_single_source(monkeypatch):
    class StreamlitStub:
        def __init__(self, theme_type: str):
            self.context = SimpleNamespace(theme={"type": theme_type})
            self.loaded = []

        def html(self, path):
            self.loaded.append(path)

    light = StreamlitStub("light")
    monkeypatch.setattr(theme_loader, "st", light)
    theme_loader.load_forensic_clarity_theme()
    assert light.loaded == [CSS_PATH]

    dark = StreamlitStub("dark")
    monkeypatch.setattr(theme_loader, "st", dark)
    theme_loader.load_forensic_clarity_theme()
    assert dark.loaded == [CSS_PATH, DARK_CSS_PATH]


def test_plotly_theme_is_consistent_in_light_and_dark_modes():
    light = apply_forensic_clarity_theme(go.Figure(), title="Light", dark=False)
    dark = apply_forensic_clarity_theme(go.Figure(), title="Dark", dark=True)

    assert light.layout.height == 360
    assert light.layout.paper_bgcolor == "rgba(0,0,0,0)"
    assert light.layout.font.color == "#243247"
    assert dark.layout.font.color == "#E7ECF3"
    assert dark.layout.xaxis.gridcolor == "#344054"


def test_every_chart_page_uses_the_central_plotly_theme():
    for relative in (
        "gui/pages/dashboard.py",
        "gui/pages/timeline.py",
        "gui/pages/validation.py",
    ):
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert "apply_forensic_clarity_theme" in source


def test_app_uses_css_loader_and_contains_no_unsafe_html_or_javascript():
    sources = [
        path.read_text(encoding="utf-8")
        for path in (ROOT / "gui").rglob("*.py")
    ]
    combined = "\n".join(sources)

    assert "load_forensic_clarity_theme" in (ROOT / "gui/app.py").read_text(
        encoding="utf-8"
    )
    assert "unsafe_allow_html=True" not in combined
    assert "unsafe_allow_javascript=True" not in combined
    assert "subprocess" not in combined


def test_streamlit_theme_keeps_loopback_and_privacy_controls():
    config = (ROOT / ".streamlit/config.toml").read_text(encoding="utf-8")

    assert 'address = "127.0.0.1"' in config
    assert "gatherUsageStats = false" in config
    assert 'primaryColor = "#0071E3"' in config
    assert 'baseRadius = "8px"' in config

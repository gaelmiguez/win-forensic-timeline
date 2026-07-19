"""Load the local CSS and expose the current native Streamlit theme."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


ASSET_ROOT = Path(__file__).resolve().parents[1] / "assets"
CSS_PATH = ASSET_ROOT / "forensic_clarity.css"
DARK_CSS_PATH = ASSET_ROOT / "forensic_clarity_dark.css"
APP_MARK_PATH = ASSET_ROOT / "app_mark.svg"
APP_BRAND_PATH = ASSET_ROOT / "app_brand.svg"
APP_BRAND_DARK_PATH = ASSET_ROOT / "app_brand_dark.svg"


def load_forensic_clarity_theme() -> None:
    """Load the audited local CSS file without JavaScript or remote resources."""
    st.html(CSS_PATH)
    if current_theme_is_dark():
        st.html(DARK_CSS_PATH)


def current_theme_is_dark() -> bool:
    """Return whether Streamlit reports its native dark appearance."""
    theme = getattr(st.context, "theme", {}) or {}
    return str(theme.get("type") or "").casefold() == "dark"

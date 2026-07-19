"""Auxiliary file collector for prototype inputs.

This module is a convenience helper for copying already available files into
the evidence tree. It is not an advanced forensic acquisition component and
does not claim to preserve all acquisition metadata required by a formal chain
of custody.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any


def collect_artifacts(source_paths: dict[str, Any], destination_root: str | Path) -> list[dict[str, str]]:
    """Create destination folders and copy existing files into them.

    source_paths can map an artifact name to either a path string or to a
    dictionary with keys like enabled and path. Missing paths are skipped.
    """

    destination = Path(destination_root)
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[dict[str, str]] = []

    for artifact_name, spec in source_paths.items():
        enabled = True
        raw_path: str | Path | None

        if isinstance(spec, dict):
            enabled = bool(spec.get("enabled", True))
            raw_path = spec.get("path")
        else:
            raw_path = spec

        artifact_destination = destination / artifact_name
        artifact_destination.mkdir(parents=True, exist_ok=True)

        if not enabled or raw_path is None:
            continue

        source = Path(raw_path)
        if not source.exists():
            continue

        sources = [source] if source.is_file() else [item for item in source.iterdir() if item.is_file()]
        for item in sources:
            target = artifact_destination / item.name
            shutil.copy2(item, target)
            copied.append(
                {
                    "artifact": artifact_name,
                    "source": str(item),
                    "destination": str(target),
                }
            )

    return copied

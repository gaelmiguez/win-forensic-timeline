"""Discovery of known output files without reading their contents."""

from __future__ import annotations

from pathlib import Path

from gui.models import IssueSeverity, LoadIssue, OutputCatalog
from gui.services.path_service import UnsafeOutputPathError, safe_output_child


def _safe_known_file(root: Path, path: Path, issues: list[LoadIssue]) -> Path | None:
    try:
        resolved = safe_output_child(root, path)
    except UnsafeOutputPathError:
        issues.append(
            LoadIssue(
                IssueSeverity.WARNING,
                "output_link_outside_root",
                "Se ignoró un enlace que sale del directorio de resultados.",
                path=path,
            )
        )
        return None
    if not resolved.is_file():
        return None
    return resolved


def inspect_output_catalog(root: Path) -> OutputCatalog:
    """Return a deterministic catalog of recognized files below one root."""
    resolved_root = root.expanduser().resolve(strict=True)
    issues: list[LoadIssue] = []

    def exact(name: str) -> Path | None:
        return _safe_known_file(resolved_root, resolved_root / name, issues)

    def matches(pattern: str) -> tuple[Path, ...]:
        detected: list[Path] = []
        try:
            candidates = sorted(
                resolved_root.glob(pattern), key=lambda path: path.name.casefold()
            )
        except OSError as exc:
            issues.append(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "output_catalog_error",
                    f"No se pudo inspeccionar el catálogo: {exc}",
                    path=resolved_root,
                )
            )
            return ()
        for candidate in candidates:
            safe = _safe_known_file(resolved_root, candidate, issues)
            if safe is not None:
                detected.append(safe)
        return tuple(detected)

    def combined(exact_name: str, pattern: str) -> tuple[Path, ...]:
        paths = list(matches(pattern))
        direct = exact(exact_name)
        if direct is not None and direct not in paths:
            paths.append(direct)
        return tuple(sorted(paths, key=lambda path: path.name.casefold()))

    return OutputCatalog(
        root=resolved_root,
        events_json=exact("events.json"),
        events_jsonl=exact("events.jsonl"),
        timeline_csv=exact("timeline.csv"),
        report_md=exact("report.md"),
        validation_summaries=combined(
            "validation_summary.json", "validation_summary_*.json"
        ),
        validation_results=combined(
            "validation_results.csv", "validation_results_*.csv"
        ),
        ground_truth_files=matches("ground_truth*.csv"),
        issues=issues,
    )

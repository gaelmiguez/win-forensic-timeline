"""Safe path validation for local output directories."""

from __future__ import annotations

import os
from pathlib import Path

from gui.models import IssueSeverity, LoadIssue, PathValidationResult


class UnsafeOutputPathError(ValueError):
    """Raised when a requested output file escapes its validated root."""


def validate_output_root(value: str | Path) -> PathValidationResult:
    """Resolve and validate an existing, readable output directory."""
    raw_value = str(value).strip()
    if not raw_value:
        return PathValidationResult(
            path=None,
            issues=(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "empty_output_path",
                    "La ruta de resultados no puede estar vacía.",
                ),
            ),
        )

    try:
        candidate = Path(raw_value).expanduser().resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        return PathValidationResult(
            path=None,
            issues=(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "invalid_output_path",
                    f"No se pudo resolver la ruta: {exc}",
                ),
            ),
        )

    if not candidate.exists():
        return PathValidationResult(
            path=None,
            issues=(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "output_path_not_found",
                    "La ruta de resultados no existe.",
                    path=candidate,
                ),
            ),
        )
    if not candidate.is_dir():
        return PathValidationResult(
            path=None,
            issues=(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "output_path_not_directory",
                    "La ruta de resultados no es un directorio.",
                    path=candidate,
                ),
            ),
        )
    if not os.access(candidate, os.R_OK):
        return PathValidationResult(
            path=None,
            issues=(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "output_path_not_readable",
                    "No hay permisos de lectura sobre la ruta de resultados.",
                    path=candidate,
                ),
            ),
        )

    try:
        next(candidate.iterdir(), None)
    except PermissionError:
        return PathValidationResult(
            path=None,
            issues=(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "output_path_permission_denied",
                    "No se puede inspeccionar el directorio por falta de permisos.",
                    path=candidate,
                ),
            ),
        )
    except OSError as exc:
        return PathValidationResult(
            path=None,
            issues=(
                LoadIssue(
                    IssueSeverity.ERROR,
                    "output_path_unavailable",
                    f"No se puede inspeccionar el directorio: {exc}",
                    path=candidate,
                ),
            ),
        )

    return PathValidationResult(path=candidate)


def safe_output_child(root: Path, child: str | Path) -> Path:
    """Resolve a candidate and ensure it remains below the validated root."""
    resolved_root = root.expanduser().resolve(strict=True)
    candidate = Path(child)
    if not candidate.is_absolute():
        candidate = resolved_root / candidate
    resolved_candidate = candidate.expanduser().resolve(strict=False)
    try:
        resolved_candidate.relative_to(resolved_root)
    except ValueError as exc:
        raise UnsafeOutputPathError(
            "La ruta solicitada queda fuera del directorio de resultados validado."
        ) from exc
    return resolved_candidate

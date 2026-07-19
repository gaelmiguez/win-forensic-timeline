"""Safe application boundary around main.run_pipeline()."""

from __future__ import annotations

import os
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import uuid4

from main import run_pipeline

from gui.models import (
    IssueSeverity,
    LoadIssue,
    PipelinePathValidation,
    PipelineRunResult,
    PipelineStatus,
)


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_pipeline_paths(
    input_root: str | Path, output_base: str | Path
) -> PipelinePathValidation:
    """Validate pipeline roots without creating or modifying either path."""
    issues: list[LoadIssue] = []
    try:
        evidence = Path(str(input_root).strip()).expanduser().resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        return PipelinePathValidation(
            None,
            None,
            (LoadIssue(IssueSeverity.ERROR, "invalid_input_path", str(exc)),),
        )
    try:
        output = Path(str(output_base).strip()).expanduser().resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        return PipelinePathValidation(
            evidence,
            None,
            (LoadIssue(IssueSeverity.ERROR, "invalid_output_path", str(exc)),),
        )

    if not evidence.exists():
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "input_not_found",
                "La ruta de evidencias no existe.",
                evidence,
            )
        )
    elif not evidence.is_dir():
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "input_not_directory",
                "La ruta de evidencias no es un directorio.",
                evidence,
            )
        )
    elif not os.access(evidence, os.R_OK):
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "input_not_readable",
                "La ruta de evidencias no tiene permisos de lectura.",
                evidence,
            )
        )

    if output.exists() and not output.is_dir():
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "output_not_directory",
                "La raíz de salida existe y no es un directorio.",
                output,
            )
        )
    output_parent = output if output.exists() else output.parent
    writable_parent = output_parent
    while not writable_parent.exists() and writable_parent != writable_parent.parent:
        writable_parent = writable_parent.parent
    if not writable_parent.exists() or not writable_parent.is_dir():
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "output_parent_not_found",
                "El directorio padre de la salida no existe.",
                output_parent,
            )
        )
    elif not os.access(writable_parent, os.W_OK):
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "output_not_writable",
                "La raíz de salida no tiene permisos de escritura.",
                writable_parent,
            )
        )

    if evidence == output:
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "input_output_identical",
                "Las rutas de evidencia y salida no pueden ser idénticas.",
            )
        )
    elif _is_relative_to(output, evidence):
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "output_inside_input",
                "La salida no puede estar dentro de la evidencia.",
            )
        )

    return PipelinePathValidation(evidence, output, tuple(issues))


def create_unique_run_directory(
    output_base: Path, now: datetime | None = None
) -> Path:
    """Create a unique timestamped run directory below output_base/gui_runs."""
    timestamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%d_%H%M%S_%f")
    parent = output_base / "gui_runs"
    parent.mkdir(parents=True, exist_ok=True)
    for _ in range(10):
        candidate = parent / f"{timestamp}_{uuid4().hex[:6]}"
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue
    raise FileExistsError("No se pudo reservar un directorio de ejecución único.")


def _sanitize_message(message: str, input_root: Path, output_root: Path | None) -> str:
    sanitized = str(message).replace(str(input_root), "<evidence>")
    if output_root is not None:
        sanitized = sanitized.replace(str(output_root), "<output>")
    return sanitized.replace(str(Path.home()), "~")


class PipelineService:
    """Run the existing pipeline directly and adapt its result for the GUI."""

    def __init__(self, runner: Callable[..., dict[str, Any]] | None = None) -> None:
        self._runner = runner or run_pipeline

    def run(self, input_root: str | Path, output_base: str | Path) -> PipelineRunResult:
        validation = validate_pipeline_paths(input_root, output_base)
        if not validation.is_valid:
            first = next(
                issue
                for issue in validation.issues
                if issue.severity is IssueSeverity.ERROR
            )
            return PipelineRunResult(
                status=PipelineStatus.ERROR,
                error_code=first.code,
                error_message=first.message,
            )

        assert validation.input_root is not None
        assert validation.output_base is not None
        started = perf_counter()
        run_root: Path | None = None
        try:
            run_root = create_unique_run_directory(validation.output_base)
            result = self._runner(validation.input_root, run_root)
        except Exception as exc:
            return PipelineRunResult(
                status=PipelineStatus.ERROR,
                output_root=run_root,
                duration_seconds=perf_counter() - started,
                error_code=type(exc).__name__,
                error_message=_sanitize_message(
                    str(exc) or "Fallo inesperado del pipeline.",
                    validation.input_root,
                    run_root,
                ),
            )

        parser_errors = tuple(
            _sanitize_message(str(error), validation.input_root, run_root)
            for error in result.get("parser_errors", [])
        )
        status = PipelineStatus.PARTIAL if parser_errors else PipelineStatus.SUCCESS
        outputs = tuple(Path(path).name for path in result.get("outputs", []))
        events = result.get("events", [])
        timeline = result.get("timeline")
        return PipelineRunResult(
            status=status,
            output_root=run_root,
            processed_artifacts=tuple(result.get("processed_artifacts", [])),
            skipped_artifacts=tuple(result.get("skipped_artifacts", [])),
            parser_errors=parser_errors,
            events_normalized=len(events),
            timeline_rows=len(timeline) if timeline is not None else 0,
            outputs=outputs,
            duration_seconds=perf_counter() - started,
        )

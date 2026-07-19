"""Read-only loading of validation summaries and result rows."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import pandas as pd

from gui.config import (
    VALIDATION_RESULT_FIELDS,
    VALIDATION_RESULT_VALUES,
    VALIDATION_SUMMARY_FIELDS,
)
from gui.models import (
    IssueSeverity,
    LoadIssue,
    LoadResult,
    LoadStatus,
    OutputCatalog,
    ValidationScenario,
)


def _scenario_key(path: Path, prefix: str) -> str:
    stem = path.stem
    marker = f"{prefix}_"
    return stem[len(marker) :] if stem.startswith(marker) else "default"


def _load_summary(path: Path) -> tuple[dict[str, Any] | None, list[LoadIssue]]:
    issues: list[LoadIssue] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except JSONDecodeError as exc:
        return None, [
            LoadIssue(
                IssueSeverity.ERROR,
                "validation_summary_invalid_json",
                f"El resumen no contiene JSON válido (línea {exc.lineno}).",
                path,
            )
        ]
    except (OSError, UnicodeError) as exc:
        return None, [
            LoadIssue(
                IssueSeverity.ERROR,
                "validation_summary_read_error",
                f"No se pudo leer el resumen: {exc}",
                path,
            )
        ]
    if not isinstance(payload, dict):
        return None, [
            LoadIssue(
                IssueSeverity.ERROR,
                "validation_summary_invalid_root",
                "El resumen de validación debe ser un objeto JSON.",
                path,
            )
        ]
    missing = [field for field in VALIDATION_SUMMARY_FIELDS if field not in payload]
    if missing:
        issues.append(
            LoadIssue(
                IssueSeverity.WARNING,
                "validation_summary_missing_metrics",
                f"El resumen no contiene todas las métricas conocidas: {', '.join(missing)}.",
                path,
            )
        )
    return dict(payload), issues


def _load_results(path: Path) -> tuple[pd.DataFrame | None, list[LoadIssue], int, int]:
    issues: list[LoadIssue] = []
    try:
        frame = pd.read_csv(path, encoding="utf-8", dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        return None, [
            LoadIssue(
                IssueSeverity.ERROR,
                "validation_results_empty_file",
                "El CSV de resultados está vacío y no contiene cabecera.",
                path,
            )
        ], 0, 0
    except (OSError, UnicodeError, pd.errors.ParserError) as exc:
        return None, [
            LoadIssue(
                IssueSeverity.ERROR,
                "validation_results_read_error",
                f"No se pudo leer el CSV de resultados: {exc}",
                path,
            )
        ], 0, 0

    missing = [field for field in VALIDATION_RESULT_FIELDS if field not in frame.columns]
    if missing:
        return None, [
            LoadIssue(
                IssueSeverity.ERROR,
                "validation_results_missing_columns",
                f"Faltan columnas de resultados: {', '.join(missing)}.",
                path,
            )
        ], len(frame), len(frame)

    extra = sorted(set(frame.columns) - set(VALIDATION_RESULT_FIELDS))
    if extra:
        issues.append(
            LoadIssue(
                IssueSeverity.WARNING,
                "validation_results_extra_columns",
                f"Se conservaron columnas adicionales: {', '.join(extra)}.",
                path,
            )
        )

    valid_mask = frame["result"].isin(VALIDATION_RESULT_VALUES)
    for row_index in frame.index[~valid_mask]:
        issues.append(
            LoadIssue(
                IssueSeverity.ERROR,
                "validation_result_unknown_value",
                f"Resultado no admitido: {frame.at[row_index, 'result']}.",
                path,
                int(row_index),
                "result",
            )
        )
    accepted = frame.loc[valid_mask].copy(deep=True).reset_index(drop=True)
    return accepted, issues, len(frame), int((~valid_mask).sum())


def load_validation_outputs(catalog: OutputCatalog) -> LoadResult:
    """Load every detected validation scenario without selecting one silently."""
    summary_paths = {
        _scenario_key(path, "validation_summary"): path
        for path in catalog.validation_summaries
    }
    result_paths = {
        _scenario_key(path, "validation_results"): path
        for path in catalog.validation_results
    }
    keys = sorted(set(summary_paths) | set(result_paths), key=str.casefold)
    scenarios: list[ValidationScenario] = []
    all_issues: list[LoadIssue] = []
    records_read = 0
    records_accepted = 0
    records_rejected = 0

    for key in keys:
        scenario = ValidationScenario(
            identifier=key,
            summary_path=summary_paths.get(key),
            results_path=result_paths.get(key),
        )
        if scenario.summary_path is None:
            scenario.issues.append(
                LoadIssue(
                    IssueSeverity.WARNING,
                    "validation_summary_missing",
                    "Hay resultados CSV sin resumen JSON asociado.",
                    scenario.results_path,
                )
            )
        else:
            scenario.summary, issues = _load_summary(scenario.summary_path)
            scenario.issues.extend(issues)
            records_read += 1
            if scenario.summary is None:
                records_rejected += 1
            else:
                records_accepted += 1

        if scenario.results_path is None:
            scenario.issues.append(
                LoadIssue(
                    IssueSeverity.WARNING,
                    "validation_results_missing",
                    "Hay un resumen JSON sin resultados CSV asociados.",
                    scenario.summary_path,
                )
            )
        else:
            scenario.results, issues, read, rejected = _load_results(
                scenario.results_path
            )
            scenario.issues.extend(issues)
            records_read += read
            records_rejected += rejected
            if scenario.results is not None:
                records_accepted += len(scenario.results)

        all_issues.extend(scenario.issues)
        scenarios.append(scenario)

    if not keys:
        status = LoadStatus.EMPTY
    elif not records_accepted and any(
        issue.severity is IssueSeverity.ERROR for issue in all_issues
    ):
        status = LoadStatus.ERROR
    elif records_rejected:
        status = LoadStatus.PARTIAL
    else:
        status = LoadStatus.SUCCESS

    return LoadResult(
        data=scenarios,
        records_read=records_read,
        records_accepted=records_accepted,
        records_rejected=records_rejected,
        issues=all_issues,
        status=status,
    )

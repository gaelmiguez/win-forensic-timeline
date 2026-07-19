"""Typed data structures shared by GUI services and components."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class IssueSeverity(str, Enum):
    """Severity assigned to a structured loading issue."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class LoadStatus(str, Enum):
    """Overall status of a loading operation."""

    SUCCESS = "success"
    PARTIAL = "partial"
    EMPTY = "empty"
    ERROR = "error"


@dataclass(frozen=True)
class FileFingerprint:
    """Cheap file identity used to invalidate GUI caches."""

    resolved_path: Path
    size: int
    mtime_ns: int

    @classmethod
    def from_path(cls, path: Path) -> FileFingerprint:
        resolved = path.expanduser().resolve(strict=True)
        stat = resolved.stat()
        return cls(resolved_path=resolved, size=stat.st_size, mtime_ns=stat.st_mtime_ns)


@dataclass(frozen=True)
class LoadIssue:
    """Structured warning or error produced while loading a file."""

    severity: IssueSeverity
    code: str
    message: str
    path: Path | None = None
    row_index: int | None = None
    field: str | None = None


@dataclass
class LoadResult:
    """Data and accounting returned by a read-only loader."""

    data: Any
    records_read: int = 0
    records_accepted: int = 0
    records_rejected: int = 0
    issues: list[LoadIssue] = field(default_factory=list)
    fingerprint: FileFingerprint | None = None
    status: LoadStatus = LoadStatus.EMPTY

    @property
    def has_errors(self) -> bool:
        return any(issue.severity is IssueSeverity.ERROR for issue in self.issues)


@dataclass(frozen=True)
class PathValidationResult:
    """Result of validating a user-supplied output directory."""

    path: Path | None
    issues: tuple[LoadIssue, ...] = ()

    @property
    def is_valid(self) -> bool:
        return self.path is not None and not any(
            issue.severity is IssueSeverity.ERROR for issue in self.issues
        )


@dataclass
class OutputCatalog:
    """Known output files detected below one validated root."""

    root: Path
    events_json: Path | None = None
    events_jsonl: Path | None = None
    timeline_csv: Path | None = None
    report_md: Path | None = None
    validation_summaries: tuple[Path, ...] = ()
    validation_results: tuple[Path, ...] = ()
    ground_truth_files: tuple[Path, ...] = ()
    issues: list[LoadIssue] = field(default_factory=list)

    @property
    def recognized_files(self) -> tuple[Path, ...]:
        singular = (
            self.events_json,
            self.events_jsonl,
            self.timeline_csv,
            self.report_md,
        )
        paths = [path for path in singular if path is not None]
        paths.extend(self.validation_summaries)
        paths.extend(self.validation_results)
        paths.extend(self.ground_truth_files)
        return tuple(sorted(paths, key=lambda path: path.name.casefold()))


@dataclass
class ValidationScenario:
    """Summary and optional per-ground-truth rows for one scenario."""

    identifier: str
    summary: dict[str, Any] | None = None
    results: Any = None
    summary_path: Path | None = None
    results_path: Path | None = None
    issues: list[LoadIssue] = field(default_factory=list)


@dataclass(frozen=True)
class FilterCriteria:
    """Combinable event filters independent from Streamlit."""

    start_utc: datetime | str | None = None
    end_utc: datetime | str | None = None
    source_artifacts: tuple[str, ...] = ()
    event_categories: tuple[str, ...] = ()
    event_actions: tuple[str, ...] = ()
    parser_modules: tuple[str, ...] = ()
    scenario_ids: tuple[str, ...] = ()
    text: str = ""
    has_traceability: bool | None = None
    confidence_min: float | None = None
    confidence_max: float | None = None


@dataclass
class FilterResult:
    """Filtered copy plus non-fatal issues caused by absent columns."""

    data: Any
    issues: list[LoadIssue] = field(default_factory=list)


class PipelineStatus(str, Enum):
    """Outcome of one GUI-triggered pipeline execution."""

    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"


@dataclass
class PipelineRunResult:
    """Sanitized summary returned by PipelineService."""

    status: PipelineStatus
    output_root: Path | None = None
    processed_artifacts: tuple[str, ...] = ()
    skipped_artifacts: tuple[str, ...] = ()
    parser_errors: tuple[str, ...] = ()
    events_normalized: int = 0
    timeline_rows: int = 0
    outputs: tuple[str, ...] = ()
    duration_seconds: float = 0.0
    error_code: str | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class PipelinePathValidation:
    """Validated evidence and output roots for a pipeline run."""

    input_root: Path | None
    output_base: Path | None
    issues: tuple[LoadIssue, ...] = ()

    @property
    def is_valid(self) -> bool:
        return (
            self.input_root is not None
            and self.output_base is not None
            and not any(issue.severity is IssueSeverity.ERROR for issue in self.issues)
        )


@dataclass(frozen=True)
class DashboardMetrics:
    """Top-level dataset metrics displayed by the dashboard."""

    total_events: int
    source_count: int
    start_utc: Any
    end_utc: Any
    traceable_events: int
    validation_scenarios: int
    rejected_rows: int
    issue_count: int


@dataclass(frozen=True)
class TimelineView:
    """Detailed or aggregated temporal representation."""

    mode: str
    data: Any
    granularity: str | None
    valid_timestamps: int
    invalid_timestamps: int


@dataclass(frozen=True)
class PageSlice:
    """One deterministic page from an event DataFrame."""

    data: Any
    page: int
    page_size: int
    total_rows: int
    total_pages: int


@dataclass(frozen=True)
class ExportPayload:
    """In-memory export ready for a Streamlit download button."""

    content: bytes
    mime_type: str
    file_name: str
    record_count: int

"""Shared forensic event model.

The CommonEvent dataclass is the normalization contract between parsers,
correlators, reporters, and validation routines.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from core.exceptions import EventValidationError


def _is_timezone_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


@dataclass
class CommonEvent:
    """Normalized forensic event shared by all prototype modules."""

    event_id: str
    timestamp_utc: datetime
    timestamp_local: Optional[datetime]
    timestamp_type: str
    source_artifact: str
    source_location: str
    event_category: str
    event_action: str
    object: Optional[str]
    description: str
    raw_evidence: Any
    parser_module: str
    traceability_ref: str
    confidence: float
    provenance: dict
    scenario_id: Optional[str] = None

    @classmethod
    def create(cls, **kwargs: Any) -> "CommonEvent":
        """Create an event with an automatically generated UUID4 event_id."""

        kwargs["event_id"] = str(uuid4())
        return cls(**kwargs)

    def __post_init__(self) -> None:
        if not isinstance(self.timestamp_utc, datetime):
            raise EventValidationError("timestamp_utc must be a datetime instance.")

        if not _is_timezone_aware(self.timestamp_utc):
            raise EventValidationError("timestamp_utc must be timezone-aware.")

        if self.timestamp_local is not None:
            if not isinstance(self.timestamp_local, datetime):
                raise EventValidationError("timestamp_local must be a datetime instance or None.")
            if not _is_timezone_aware(self.timestamp_local):
                raise EventValidationError("timestamp_local must be timezone-aware when provided.")

        if isinstance(self.confidence, bool) or not isinstance(self.confidence, (int, float)):
            raise EventValidationError("confidence must be a numeric value between 0 and 1.")

        if not 0 <= float(self.confidence) <= 1:
            raise EventValidationError("confidence must be between 0 and 1.")

        required_text_fields = (
            "event_id",
            "timestamp_type",
            "source_artifact",
            "source_location",
            "event_category",
            "event_action",
            "description",
            "parser_module",
            "traceability_ref",
        )
        for field_name in required_text_fields:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise EventValidationError(f"{field_name} must not be empty.")

        if not isinstance(self.provenance, dict):
            raise EventValidationError("provenance must be a dictionary.")

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable dictionary, converting datetimes to ISO 8601."""

        data = asdict(self)
        data["timestamp_utc"] = self.timestamp_utc.isoformat()
        data["timestamp_local"] = (
            self.timestamp_local.isoformat() if self.timestamp_local is not None else None
        )
        return data

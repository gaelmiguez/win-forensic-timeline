"""Custom exceptions used by the prototype."""


class EventValidationError(ValueError):
    """Raised when a CommonEvent violates the shared event contract."""


class TimeConversionError(ValueError):
    """Raised when a timestamp cannot be converted to UTC safely."""

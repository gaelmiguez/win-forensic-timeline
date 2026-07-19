from pathlib import Path

import pytest

from gui.services import path_service
from gui.models import FileFingerprint
from gui.services.path_service import (
    UnsafeOutputPathError,
    safe_output_child,
    validate_output_root,
)


def test_valid_directory_is_resolved(tmp_path):
    result = validate_output_root(tmp_path)

    assert result.is_valid
    assert result.path == tmp_path.resolve()


def test_missing_path_is_rejected(tmp_path):
    result = validate_output_root(tmp_path / "missing")

    assert not result.is_valid
    assert result.issues[0].code == "output_path_not_found"


def test_file_is_rejected_as_output_directory(tmp_path):
    path = tmp_path / "events.json"
    path.write_text("[]", encoding="utf-8")

    result = validate_output_root(path)

    assert not result.is_valid
    assert result.issues[0].code == "output_path_not_directory"


def test_path_with_spaces_is_supported(tmp_path):
    spaced = tmp_path / "output con espacios"
    spaced.mkdir()

    assert validate_output_root(str(spaced)).path == spaced.resolve()


def test_unreadable_path_returns_structured_error(tmp_path, monkeypatch):
    monkeypatch.setattr(path_service.os, "access", lambda *_args: False)

    result = validate_output_root(tmp_path)

    assert result.issues[0].code == "output_path_not_readable"


def test_expanduser_is_applied(tmp_path, monkeypatch):
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv("HOME", str(tmp_path))
    output = tmp_path / "output"
    output.mkdir()

    result = validate_output_root("~/output")

    assert result.path == output.resolve()


def test_safe_child_rejects_escape(tmp_path):
    root = tmp_path / "output"
    root.mkdir()

    with pytest.raises(UnsafeOutputPathError):
        safe_output_child(root, Path("..") / "outside.json")


def test_safe_child_accepts_file_below_root(tmp_path):
    root = tmp_path / "output"
    root.mkdir()

    assert safe_output_child(root, "events.json") == (root / "events.json").resolve()


def test_file_fingerprint_changes_when_output_changes(tmp_path):
    path = tmp_path / "events.json"
    path.write_text("[]", encoding="utf-8")
    before = FileFingerprint.from_path(path)
    path.write_text('[{"changed": true}]', encoding="utf-8")
    after = FileFingerprint.from_path(path)

    assert before.resolved_path == after.resolved_path
    assert (before.size, before.mtime_ns) != (after.size, after.mtime_ns)

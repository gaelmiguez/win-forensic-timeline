"""Read the local Git revision without spawning a process."""

from __future__ import annotations

from pathlib import Path


def read_project_revision(project_root: Path | None = None) -> str | None:
    """Return a short local revision when the simple Git layout is readable."""
    root = (project_root or Path(__file__).resolve().parents[2]).resolve()
    git_path = root / ".git"
    try:
        if git_path.is_file():
            marker = git_path.read_text(encoding="utf-8").strip()
            if not marker.startswith("gitdir:"):
                return None
            git_path = (root / marker.split(":", 1)[1].strip()).resolve()
        head = (git_path / "HEAD").read_text(encoding="utf-8").strip()
        if head.startswith("ref:"):
            reference = head.split(":", 1)[1].strip()
            revision = (git_path / reference).read_text(encoding="utf-8").strip()
        else:
            revision = head
    except (OSError, UnicodeError):
        return None
    return revision[:7] if revision else None

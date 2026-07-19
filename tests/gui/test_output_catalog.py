import os

import pytest

from gui.services.output_catalog import inspect_output_catalog


def test_empty_folder_has_no_recognized_outputs(tmp_path):
    catalog = inspect_output_catalog(tmp_path)

    assert catalog.recognized_files == ()


def test_detects_only_events_json(tmp_path):
    events = tmp_path / "events.json"
    events.write_text("[]", encoding="utf-8")

    catalog = inspect_output_catalog(tmp_path)

    assert catalog.events_json == events.resolve()
    assert len(catalog.recognized_files) == 1


def test_detects_multiple_validation_scenarios_deterministically(tmp_path):
    for name in (
        "validation_summary_zeta.json",
        "validation_summary_alpha.json",
        "validation_results_zeta.csv",
        "validation_results_alpha.csv",
    ):
        (tmp_path / name).write_text("{}", encoding="utf-8")

    catalog = inspect_output_catalog(tmp_path)

    assert [path.name for path in catalog.validation_summaries] == [
        "validation_summary_alpha.json",
        "validation_summary_zeta.json",
    ]
    assert [path.name for path in catalog.validation_results] == [
        "validation_results_alpha.csv",
        "validation_results_zeta.csv",
    ]


def test_detects_default_validation_names(tmp_path):
    (tmp_path / "validation_summary.json").write_text("{}", encoding="utf-8")
    (tmp_path / "validation_results.csv").write_text("x", encoding="utf-8")

    catalog = inspect_output_catalog(tmp_path)

    assert [path.name for path in catalog.validation_summaries] == [
        "validation_summary.json"
    ]
    assert [path.name for path in catalog.validation_results] == [
        "validation_results.csv"
    ]


def test_unknown_files_are_ignored(tmp_path):
    (tmp_path / "notes.txt").write_text("ignored", encoding="utf-8")

    assert inspect_output_catalog(tmp_path).recognized_files == ()


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlinks unavailable")
def test_symlink_outside_root_is_ignored_when_supported(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("[]", encoding="utf-8")
    link = root / "events.json"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("Windows symlink creation is not permitted")

    catalog = inspect_output_catalog(root)

    assert catalog.events_json is None
    assert any(issue.code == "output_link_outside_root" for issue in catalog.issues)

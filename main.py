"""Command-line entry point for the win-forensic-timeline prototype."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

import yaml

from correlator.timeline_correlator import build_timeline
from parsers import browser_history_parser, evtx_parser, prefetch_parser, registry_parser
from reporters.csv_reporter import export_timeline_csv
from reporters.json_reporter import export_events_json, export_events_jsonl
from reporters.markdown_reporter import generate_markdown_report

ParserFunction = Callable[[str | Path], list]

PARSERS: dict[str, ParserFunction] = {
    "evtx": evtx_parser.parse,
    "prefetch": prefetch_parser.parse,
    "registry": registry_parser.parse,
    "browser": browser_history_parser.parse,
}


def load_yaml_if_exists(path: Path) -> dict:
    """Load a YAML configuration file, returning an empty dict if absent."""

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    if not isinstance(loaded, dict):
        raise ValueError(f"Configuration file must contain a mapping: {path}")

    return loaded


def resolve_artifact_path(name: str, spec: dict, input_root: Path) -> Path:
    """Resolve an artifact path from config, falling back to the CLI input root."""

    configured_path = spec.get("path")
    if not configured_path:
        path = input_root / name
        return path if path.is_absolute() else Path.cwd() / path

    path = Path(configured_path)
    if path.is_absolute():
        return path

    parts = path.parts
    if parts and parts[0] in {input_root.name, "evidence"}:
        return input_root / Path(*parts[1:])

    return input_root / path


def run_pipeline(input_root: str | Path, output_root: str | Path) -> dict:
    """Run the extraction/parsing/correlation/reporting pipeline."""

    input_root = Path(input_root)
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    settings = load_yaml_if_exists(Path("config") / "settings.yaml")
    artifacts_config = load_yaml_if_exists(Path("config") / "artifacts.yaml")

    events = []
    processed_artifacts: list[str] = []
    skipped_artifacts: list[str] = []
    parser_errors: list[str] = []

    for artifact_name, parser in PARSERS.items():
        spec = artifacts_config.get(artifact_name, {})
        if spec is None:
            spec = {}
        if not isinstance(spec, dict):
            parser_errors.append(f"{artifact_name}: invalid artifact configuration")
            continue

        if not bool(spec.get("enabled", True)):
            skipped_artifacts.append(artifact_name)
            continue

        artifact_path = resolve_artifact_path(artifact_name, spec, input_root)
        processed_artifacts.append(artifact_name)

        try:
            parsed_events = parser(artifact_path)
        except Exception as exc:
            parser_errors.append(f"{artifact_name}: {exc}")
            continue

        events.extend(parsed_events)

    timeline_df = build_timeline(events)

    export_events_json(events, output_root / "events.json")
    export_events_jsonl(events, output_root / "events.jsonl")
    export_timeline_csv(timeline_df, output_root / "timeline.csv")
    generate_markdown_report(events, timeline_df, output_root / "report.md")

    return {
        "settings": settings,
        "events": events,
        "timeline": timeline_df,
        "processed_artifacts": processed_artifacts,
        "skipped_artifacts": skipped_artifacts,
        "parser_errors": parser_errors,
        "outputs": [
            output_root / "events.json",
            output_root / "events.jsonl",
            output_root / "timeline.csv",
            output_root / "report.md",
        ],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Baseline CLI for Windows forensic timeline normalization and reporting."
    )
    parser.add_argument("--input", default="evidence", help="Evidence root folder.")
    parser.add_argument("--output", default="output", help="Output folder.")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    input_root = Path(args.input)
    output_root = Path(args.output)

    result = run_pipeline(input_root=input_root, output_root=output_root)

    print("win-forensic-timeline prototype execution completed.")
    print(f"Input root: {input_root}")
    print(f"Output root: {output_root}")
    print(f"Artifacts processed: {', '.join(result['processed_artifacts']) or 'none'}")
    if result["skipped_artifacts"]:
        print(f"Artifacts skipped: {', '.join(result['skipped_artifacts'])}")
    if result["parser_errors"]:
        print("Parser warnings:")
        for error in result["parser_errors"]:
            print(f"  - {error}")
    print(f"Events normalized: {len(result['events'])}")
    print(f"Timeline rows: {len(result['timeline'])}")
    print("Generated outputs:")
    for output in result["outputs"]:
        print(f"  - {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Generate synthetic Registry autorun metadata for validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_OUTPUT = Path("evidence") / "registry" / "sample"

SAMPLE_REGISTRY_ENTRIES = [
    {
        "hive": "HKCU",
        "key_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "value_name": "ExampleApp",
        "value_type": "REG_SZ",
        "value_data": "C:\\Tools\\ExampleApp.exe",
        "last_write_time_utc": "2024-01-10T09:25:00Z",
        "scenario_id": "S_REGISTRY_SYNTH",
    },
    {
        "hive": "HKCU",
        "key_path": "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
        "value_name": "UpdaterTask",
        "value_type": "REG_SZ",
        "value_data": "C:\\Tools\\UpdaterTask.exe /once",
        "last_write_time_utc": "2024-01-10T09:30:00Z",
        "scenario_id": "S_REGISTRY_SYNTH",
    },
]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate controlled Registry autorun metadata.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Destination folder. Default: evidence/registry/sample.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing autoruns.json.")
    return parser


def generate_sample_registry_metadata(output_dir: Path = DEFAULT_OUTPUT, overwrite: bool = False) -> Path:
    """Create an autoruns.json metadata file without touching the live Registry."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "autoruns.json"
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Registry sample already exists at {output_path}; use --overwrite.")

    metadata = {
        "parser_backend": "external_registry_json",
        "artifact": "Registry",
        "source_type": "autoruns",
        "entries": SAMPLE_REGISTRY_ENTRIES,
    }
    output_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def main() -> int:
    args = build_arg_parser().parse_args()
    output_path = generate_sample_registry_metadata(Path(args.output), overwrite=args.overwrite)

    print(f"Synthetic Registry metadata created: {output_path}")
    print(f"Entries generated: {len(SAMPLE_REGISTRY_ENTRIES)}")
    print("Expected events:")
    for entry in SAMPLE_REGISTRY_ENTRIES:
        print(
            f"  - {entry['value_name']} at {entry['last_write_time_utc']} "
            f"({entry['hive']}\\{entry['key_path']})"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

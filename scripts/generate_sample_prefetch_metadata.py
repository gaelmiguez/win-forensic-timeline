"""Generate synthetic Prefetch placeholder files with JSON metadata sidecars."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_OUTPUT = Path("evidence") / "prefetch" / "sample"

SAMPLE_PREFETCH_ENTRIES = [
    {
        "file_name": "NOTEPAD.EXE-12345678",
        "executable_name": "NOTEPAD.EXE",
        "prefetch_hash": "12345678",
        "run_count": 1,
        "last_run_time_utc": "2024-01-10T09:15:00Z",
        "last_run_times_utc": ["2024-01-10T09:15:00Z"],
        "prefetch_version": "unknown",
    },
    {
        "file_name": "POWERSHELL.EXE-87654321",
        "executable_name": "POWERSHELL.EXE",
        "prefetch_hash": "87654321",
        "run_count": 2,
        "last_run_time_utc": "2024-01-10T09:20:00Z",
        "last_run_times_utc": ["2024-01-10T09:20:00Z"],
        "prefetch_version": "unknown",
    },
]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate controlled Prefetch placeholders and JSON metadata sidecars."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Destination folder. Default: evidence/prefetch/sample.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing sample files.")
    return parser


def generate_sample_prefetch_metadata(output_dir: Path = DEFAULT_OUTPUT, overwrite: bool = False) -> list[Path]:
    """Create placeholder .pf files and JSON sidecars with controlled metadata."""

    output_dir.mkdir(parents=True, exist_ok=True)
    if overwrite:
        for existing_path in list(output_dir.glob("*.pf")) + list(output_dir.glob("*.json")):
            existing_path.unlink()

    generated_sidecars: list[Path] = []

    for entry in SAMPLE_PREFETCH_ENTRIES:
        pf_path = output_dir / f"{entry['file_name']}.pf"
        json_path = output_dir / f"{entry['file_name']}.json"

        if not overwrite and (pf_path.exists() or json_path.exists()):
            raise FileExistsError(f"Sample Prefetch files already exist for {entry['file_name']}; use --overwrite.")

        pf_path.write_bytes(b"WFT synthetic Prefetch placeholder; metadata is stored in the JSON sidecar.\n")

        metadata = {
            "executable_name": entry["executable_name"],
            "prefetch_hash": entry["prefetch_hash"],
            "run_count": entry["run_count"],
            "last_run_time_utc": entry["last_run_time_utc"],
            "last_run_times_utc": entry["last_run_times_utc"],
            "volume_information": [],
            "referenced_files": [],
            "parser_backend": "external_metadata_json",
            "prefetch_version": entry["prefetch_version"],
        }
        json_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        generated_sidecars.append(json_path)

    return generated_sidecars


def main() -> int:
    args = build_arg_parser().parse_args()
    output_dir = Path(args.output)
    sidecars = generate_sample_prefetch_metadata(output_dir=output_dir, overwrite=args.overwrite)

    print(f"Synthetic Prefetch metadata created: {output_dir}")
    print(f"Sidecars generated: {len(sidecars)}")
    print("Expected events:")
    for entry in SAMPLE_PREFETCH_ENTRIES:
        print(
            f"  - {entry['executable_name']} at {entry['last_run_time_utc']} "
            f"(run_count={entry['run_count']})"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Download Hugging Face datasets and export their tables as JSONL."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd
from huggingface_hub import snapshot_download


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = PROJECT_ROOT / "data" / "reference"
RAW_ROOT = REFERENCE_ROOT / "huggingface"
EXPORT_ROOT = REFERENCE_ROOT / "exports"
SUPPORTED_SUFFIXES = {".csv", ".json", ".jsonl", ".parquet"}
EXCLUDED_DATA_FILES = {"dataset_summary.json", "manifest.json"}


@dataclass(frozen=True)
class DatasetSpec:
    repo_id: str
    directory_name: str


DATASETS = (
    DatasetSpec(
        repo_id="mindweave/help-desk-tickets",
        directory_name="mindweave_help-desk-tickets",
    ),
    DatasetSpec(
        repo_id="bdragun/service-desk-tickets",
        directory_name="bdragun_service-desk-tickets",
    ),
    DatasetSpec(
        repo_id="Console-AI/IT-helpdesk-synthetic-tickets",
        directory_name="Console-AI_IT-helpdesk-synthetic-tickets",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download the configured Hugging Face dataset repositories and "
            "export every tabular file to JSONL."
        )
    )
    parser.add_argument(
        "--dataset",
        choices=("all", *(spec.directory_name for spec in DATASETS)),
        default="all",
        help="Download one configured dataset or all datasets (default: all).",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Download raw repositories without generating JSONL exports.",
    )
    return parser.parse_args()


def selected_datasets(name: str) -> Iterable[DatasetSpec]:
    if name == "all":
        return DATASETS
    return (next(spec for spec in DATASETS if spec.directory_name == name),)


def download_dataset(spec: DatasetSpec) -> Path:
    destination = RAW_ROOT / spec.directory_name
    destination.mkdir(parents=True, exist_ok=True)

    print(f"[download] {spec.repo_id} -> {destination}")
    snapshot_download(
        repo_id=spec.repo_id,
        repo_type="dataset",
        local_dir=destination,
    )
    return destination


def find_data_files(raw_directory: Path) -> list[Path]:
    files = []
    for path in raw_directory.rglob("*"):
        relative_parts = path.relative_to(raw_directory).parts
        if (
            path.is_file()
            and path.suffix.lower() in SUPPORTED_SUFFIXES
            and path.name not in EXCLUDED_DATA_FILES
            and ".cache" not in relative_parts
            and not path.name.startswith("._")
        ):
            files.append(path)
    return sorted(files)


def load_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, low_memory=False)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".jsonl":
        return pd.read_json(path, lines=True)
    if suffix == ".json":
        try:
            return pd.read_json(path, lines=True)
        except ValueError:
            return pd.read_json(path)
    raise ValueError(f"Unsupported data file: {path}")


def export_relative_path(source: Path, raw_directory: Path) -> Path:
    relative = source.relative_to(raw_directory)
    if relative.parts and relative.parts[0] == "data":
        relative = Path(*relative.parts[1:])
    return relative.with_suffix(".jsonl")


def export_dataset(spec: DatasetSpec, raw_directory: Path) -> None:
    export_directory = EXPORT_ROOT / spec.directory_name
    export_directory.mkdir(parents=True, exist_ok=True)

    manifest_files = []
    data_files = find_data_files(raw_directory)
    if not data_files:
        raise RuntimeError(f"No supported data files found in {raw_directory}")

    for source in data_files:
        table = load_table(source)
        relative_output = export_relative_path(source, raw_directory)
        output = export_directory / relative_output
        output.parent.mkdir(parents=True, exist_ok=True)
        table.to_json(
            output,
            orient="records",
            lines=True,
            force_ascii=False,
            date_format="iso",
        )

        manifest_files.append(
            {
                "source": str(source.relative_to(raw_directory)),
                "export": str(output.relative_to(export_directory)),
                "rows": len(table),
                "columns": [str(column) for column in table.columns],
            }
        )
        print(f"[export] {source.name}: {len(table):,} rows -> {output}")

    manifest = {
        "dataset_id": spec.repo_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "format": "jsonl",
        "files": manifest_files,
    }
    manifest_path = export_directory / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

    for spec in selected_datasets(args.dataset):
        raw_directory = download_dataset(spec)
        if not args.download_only:
            export_dataset(spec, raw_directory)


if __name__ == "__main__":
    main()

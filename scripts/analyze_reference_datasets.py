#!/usr/bin/env python3
"""Create a compact structural summary of local reference datasets."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = PROJECT_ROOT / "data" / "reference" / "huggingface"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "reference_dataset_summary.json"
SAMPLE_LIMIT = 5
SNIPPET_LIMIT = 140

DATASETS = {
    "mindweave/help-desk-tickets": {
        "directory": "mindweave_help-desk-tickets",
        "data_globs": ("data/*.csv",),
        "text_fields": ("summary", "description", "body"),
        "category_fields": ("category_id", "affected_service", "service"),
        "scoped_category_fields": {
            "category_name": ("categories.csv", "name"),
        },
        "priority_fields": ("priority",),
        "escalation_fields": (
            "escalated",
            "outage_related",
            "breach_type",
            "sla_target_hours",
        ),
        "conversation_fields": ("body", "visibility", "team", "ticket_id"),
    },
    "bdragun/service-desk-tickets": {
        "directory": "bdragun_service-desk-tickets",
        "data_globs": ("data/*.parquet",),
        "text_fields": (),
        "category_fields": ("category", "source_type"),
        "scoped_category_fields": {},
        "priority_fields": (),
        "escalation_fields": (),
        "conversation_fields": ("conversations", "source_id", "source_type"),
    },
    "Console-AI/IT-helpdesk-synthetic-tickets": {
        "directory": "Console-AI_IT-helpdesk-synthetic-tickets",
        "data_globs": ("*.csv",),
        "text_fields": ("subject", "description"),
        "category_fields": ("category",),
        "scoped_category_fields": {},
        "priority_fields": ("priority",),
        "escalation_fields": (),
        "conversation_fields": (),
    },
}


def compact_values(series: pd.Series, limit: int = SAMPLE_LIMIT) -> list[str]:
    values = series.dropna().astype(str).str.strip()
    values = values[values != ""]
    counts = Counter(values)
    return [value for value, _ in counts.most_common(limit)]


def compact_snippets(series: pd.Series, limit: int = 3) -> list[str]:
    snippets = []
    for value in series.dropna().astype(str):
        text = re.sub(r"\s+", " ", value).strip()
        if text and text not in snippets:
            snippets.append(text[:SNIPPET_LIMIT])
        if len(snippets) == limit:
            break
    return snippets


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, low_memory=False)
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported reference file: {path}")


def discover_files(directory: Path, globs: Iterable[str]) -> list[Path]:
    paths = {
        path
        for pattern in globs
        for path in directory.glob(pattern)
        if path.is_file() and not path.name.startswith("._")
    }
    return sorted(paths)


def detect_license(directory: Path) -> str | None:
    readme = directory / "README.md"
    if not readme.exists():
        return None
    match = re.search(
        r"^license:\s*([^\n]+)",
        readme.read_text(encoding="utf-8", errors="replace"),
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def parse_conversation_summary(frames: list[pd.DataFrame]) -> dict[str, Any] | None:
    role_counts: Counter[str] = Counter()
    message_count_samples = []
    source_types: Counter[str] = Counter()
    source_ids: Counter[str] = Counter()
    sample_user_prompts: list[str] = []
    priority_mentions: Counter[str] = Counter()
    escalation_keyword_counts: Counter[str] = Counter()

    for frame in frames:
        if "source_type" in frame:
            source_types.update(frame["source_type"].dropna().astype(str))
        if "source_id" in frame:
            source_ids.update(frame["source_id"].dropna().astype(str))
        if "conversations" not in frame:
            continue
        for raw_value in frame["conversations"].dropna():
            try:
                messages = json.loads(raw_value) if isinstance(raw_value, str) else raw_value
            except (json.JSONDecodeError, TypeError):
                continue
            if not isinstance(messages, list):
                continue
            message_count_samples.append(len(messages))
            conversation_text = " ".join(
                message.get("content", "")
                for message in messages
                if isinstance(message, dict)
                and isinstance(message.get("content"), str)
            ).lower()
            for keyword in ("escalat", "sla", "outage"):
                if keyword in conversation_text:
                    escalation_keyword_counts[keyword] += 1
            for message in messages:
                if isinstance(message, dict) and isinstance(message.get("role"), str):
                    role_counts[message["role"]] += 1
                    if message["role"] == "assistant":
                        for priority in re.findall(
                            r"\b(critical|high|medium|low) priority\b",
                            message.get("content", ""),
                            flags=re.IGNORECASE,
                        ):
                            priority_mentions[priority.title()] += 1
                    if (
                        message["role"] == "user"
                        and isinstance(message.get("content"), str)
                        and len(sample_user_prompts) < 3
                    ):
                        prompt = re.sub(r"\s+", " ", message["content"]).strip()
                        if prompt and prompt not in sample_user_prompts:
                            sample_user_prompts.append(prompt[:SNIPPET_LIMIT])

    if not role_counts and not source_types:
        return None
    return {
        "format": "JSON-encoded list of role/content message objects",
        "message_roles": dict(sorted(role_counts.items())),
        "messages_per_conversation": sorted(set(message_count_samples))[:SAMPLE_LIMIT],
        "source_types": [value for value, _ in source_types.most_common(SAMPLE_LIMIT)],
        "sample_source_ids": [value for value, _ in source_ids.most_common(SAMPLE_LIMIT)],
        "sample_user_prompts": sample_user_prompts,
        "priority_mentions": dict(priority_mentions.most_common()),
        "escalation_keyword_counts": dict(escalation_keyword_counts),
    }


def collect_field_values(
    frames: list[pd.DataFrame], field_names: Iterable[str]
) -> dict[str, Any]:
    values = {}
    for field in field_names:
        matching = [frame[field] for frame in frames if field in frame.columns]
        if matching:
            values[field] = compact_values(pd.concat(matching, ignore_index=True))
    return values


def collect_text_snippets(
    frames: list[pd.DataFrame], field_names: Iterable[str]
) -> dict[str, list[str]]:
    snippets = {}
    for field in field_names:
        matching = [frame[field] for frame in frames if field in frame.columns]
        if matching:
            snippets[field] = compact_snippets(pd.concat(matching, ignore_index=True))
    return snippets


def summarize_dataset(dataset_id: str, config: dict[str, Any]) -> dict[str, Any]:
    directory = REFERENCE_ROOT / config["directory"]
    if not directory.exists():
        raise FileNotFoundError(f"Missing dataset directory: {directory}")

    files = discover_files(directory, config["data_globs"])
    if not files:
        raise FileNotFoundError(f"No data files found in: {directory}")

    frames = [read_table(path) for path in files]
    file_summaries = [
        {
            "path": str(path.relative_to(PROJECT_ROOT)),
            "rows": len(frame),
            "columns": [str(column) for column in frame.columns],
        }
        for path, frame in zip(files, frames)
    ]

    sample_categories = collect_field_values(frames, config["category_fields"])
    for output_name, (file_name, field_name) in config[
        "scoped_category_fields"
    ].items():
        matching_frames = [
            frame
            for path, frame in zip(files, frames)
            if path.name == file_name and field_name in frame.columns
        ]
        if matching_frames:
            sample_categories[output_name] = compact_values(
                pd.concat(
                    [frame[field_name] for frame in matching_frames],
                    ignore_index=True,
                )
            )

    conversation_summary = parse_conversation_summary(frames)
    sample_priorities = collect_field_values(frames, config["priority_fields"])
    escalation_values = collect_field_values(frames, config["escalation_fields"])
    if conversation_summary:
        if conversation_summary["priority_mentions"]:
            sample_priorities["derived_from_conversation_text"] = list(
                conversation_summary["priority_mentions"]
            )
        if conversation_summary["escalation_keyword_counts"]:
            escalation_values["conversation_keyword_counts"] = (
                conversation_summary["escalation_keyword_counts"]
            )

    return {
        "local_directory": str(directory.relative_to(PROJECT_ROOT)),
        "license": detect_license(directory),
        "files": file_summaries,
        "total_rows_across_files": sum(len(frame) for frame in frames),
        "detected_columns": sorted(
            {str(column) for frame in frames for column in frame.columns}
        ),
        "sample_categories": sample_categories,
        "sample_priorities_or_severities": sample_priorities,
        "sample_issue_text": collect_text_snippets(frames, config["text_fields"]),
        "possible_escalation_values": escalation_values,
        "possible_comment_or_conversation_structure": {
            "detected_fields": [
                field
                for field in config["conversation_fields"]
                if any(field in frame.columns for frame in frames)
            ],
            "conversation_summary": conversation_summary,
        },
    }


def main() -> None:
    summary = {
        "purpose": (
            "Compact pattern summary for designing Korean runbooks and a synthetic "
            "evaluation set. This is not a raw-data export."
        ),
        "datasets": {
            dataset_id: summarize_dataset(dataset_id, config)
            for dataset_id, config in DATASETS.items()
        },
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote reference summary: {OUTPUT_PATH}")
    for dataset_id, dataset in summary["datasets"].items():
        print(
            f"- {dataset_id}: {len(dataset['files'])} files, "
            f"{dataset['total_rows_across_files']:,} rows"
        )


if __name__ == "__main__":
    main()

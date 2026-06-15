#!/usr/bin/env python3
"""Validate the Korean synthetic IT issue/evaluation dataset."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "eval_sets" / "korean_it_issues_v0.jsonl"
RUNBOOK_ROOT = PROJECT_ROOT / "data" / "runbooks"

REQUIRED_FIELDS = {
    "issue_id",
    "title",
    "description",
    "expected_category",
    "expected_severity",
    "expected_runbook_id",
    "expected_runbook_title",
    "expected_escalation",
    "expected_owner_team",
    "expected_missing_info",
    "reference_sources",
    "notes",
}
ALLOWED_SEVERITIES = {"Low", "Medium", "High", "Critical"}
EXPECTED_CATEGORY_COUNTS = {
    "VPN": 3,
    "MFA": 3,
    "Password": 3,
    "Account / Permission": 4,
    "Email": 3,
    "Network": 3,
    "SaaS Access": 3,
    "Security": 3,
    "Backup / Recovery": 2,
    "Hardware": 2,
    "General Escalation": 1,
}
ALLOWED_CATEGORIES = set(EXPECTED_CATEGORY_COUNTS)
ALLOWED_OWNER_TEAMS = {
    "IT 헬프데스크",
    "IT 인프라팀",
    "IAM팀",
    "보안팀",
    "메일/협업도구팀",
    "네트워크팀",
    "장비지원팀",
    "백업/스토리지팀",
}
ALLOWED_REFERENCE_SOURCES = {
    "mindweave/help-desk-tickets",
    "bdragun/service-desk-tickets",
    "Console-AI/IT-helpdesk-synthetic-tickets",
}


def load_runbooks() -> dict[str, str]:
    runbooks = {}
    for path in sorted(RUNBOOK_ROOT.glob("RB-*.md")):
        id_match = re.match(r"(RB-\d{3})_", path.name)
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        title_match = re.match(r"#\s+(RB-\d{3})\s+(.+)", first_line)
        if not id_match or not title_match:
            continue
        runbook_id = id_match.group(1)
        if runbook_id == title_match.group(1):
            runbooks[runbook_id] = title_match.group(2).strip()
    return runbooks


def load_jsonl(errors: list[str]) -> list[tuple[int, dict[str, Any]]]:
    records = []
    if not DATASET_PATH.exists():
        errors.append(f"Dataset does not exist: {DATASET_PATH}")
        return records

    for line_number, raw_line in enumerate(
        DATASET_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            errors.append(f"Line {line_number}: invalid JSON ({exc.msg})")
            continue
        if not isinstance(value, dict):
            errors.append(f"Line {line_number}: expected a JSON object")
            continue
        records.append((line_number, value))
    return records


def require_non_empty_string(
    record: dict[str, Any], field: str, label: str, errors: list[str]
) -> None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: {field} must be a non-empty string")


def validate_record(
    line_number: int,
    record: dict[str, Any],
    runbooks: dict[str, str],
    errors: list[str],
) -> None:
    label = record.get("issue_id") or f"line {line_number}"
    missing_fields = sorted(REQUIRED_FIELDS - record.keys())
    if missing_fields:
        errors.append(f"{label}: missing fields: {', '.join(missing_fields)}")

    for field in (
        "issue_id",
        "title",
        "description",
        "expected_category",
        "expected_severity",
        "expected_runbook_id",
        "expected_runbook_title",
        "expected_owner_team",
        "notes",
    ):
        require_non_empty_string(record, field, label, errors)

    issue_id = record.get("issue_id")
    if isinstance(issue_id, str) and not re.fullmatch(r"ISSUE-\d{3}", issue_id):
        errors.append(f"{label}: issue_id must match ISSUE-NNN")

    if record.get("expected_severity") not in ALLOWED_SEVERITIES:
        errors.append(
            f"{label}: invalid expected_severity "
            f"{record.get('expected_severity')!r}"
        )
    if record.get("expected_category") not in ALLOWED_CATEGORIES:
        errors.append(
            f"{label}: invalid expected_category "
            f"{record.get('expected_category')!r}"
        )
    if record.get("expected_owner_team") not in ALLOWED_OWNER_TEAMS:
        errors.append(
            f"{label}: invalid expected_owner_team "
            f"{record.get('expected_owner_team')!r}"
        )
    if not isinstance(record.get("expected_escalation"), bool):
        errors.append(f"{label}: expected_escalation must be a boolean")

    missing_info = record.get("expected_missing_info")
    if not isinstance(missing_info, list) or not all(
        isinstance(value, str) and value.strip() for value in missing_info or []
    ):
        errors.append(
            f"{label}: expected_missing_info must be a list of non-empty strings"
        )

    sources = record.get("reference_sources")
    if (
        not isinstance(sources, list)
        or not sources
        or not all(isinstance(value, str) for value in sources)
    ):
        errors.append(f"{label}: reference_sources must be a non-empty string list")
    elif invalid_sources := sorted(set(sources) - ALLOWED_REFERENCE_SOURCES):
        errors.append(
            f"{label}: unknown reference_sources: {', '.join(invalid_sources)}"
        )

    runbook_id = record.get("expected_runbook_id")
    if runbook_id not in runbooks:
        errors.append(f"{label}: runbook not found: {runbook_id!r}")
    elif record.get("expected_runbook_title") != runbooks[runbook_id]:
        errors.append(
            f"{label}: runbook title mismatch for {runbook_id}; "
            f"expected {runbooks[runbook_id]!r}"
        )


def main() -> int:
    errors: list[str] = []
    runbooks = load_runbooks()
    records = load_jsonl(errors)

    for line_number, record in records:
        validate_record(line_number, record, runbooks, errors)

    issue_ids = [
        record.get("issue_id")
        for _, record in records
        if isinstance(record.get("issue_id"), str)
    ]
    duplicates = sorted(
        issue_id for issue_id, count in Counter(issue_ids).items() if count > 1
    )
    if duplicates:
        errors.append(f"Duplicate issue_id values: {', '.join(duplicates)}")

    if len(records) != 30:
        errors.append(f"Expected 30 cases, found {len(records)}")

    category_counts = Counter(
        record.get("expected_category") for _, record in records
    )
    if dict(category_counts) != EXPECTED_CATEGORY_COUNTS:
        errors.append(
            "Category distribution mismatch: "
            + json.dumps(dict(category_counts), ensure_ascii=False, sort_keys=True)
        )

    severity_counts = Counter(
        record.get("expected_severity") for _, record in records
    )
    escalation_counts = Counter(
        record.get("expected_escalation") for _, record in records
    )

    print("Synthetic dataset validation")
    print(f"- Dataset: {DATASET_PATH.relative_to(PROJECT_ROOT)}")
    print(f"- Parsed cases: {len(records)}")
    print(f"- Discovered runbooks: {len(runbooks)}")
    print(
        "- Categories: "
        + ", ".join(
            f"{category}={category_counts[category]}"
            for category in EXPECTED_CATEGORY_COUNTS
        )
    )
    print(
        "- Severities: "
        + ", ".join(
            f"{severity}={severity_counts[severity]}"
            for severity in ("Low", "Medium", "High", "Critical")
        )
    )
    print(
        f"- Escalation: true={escalation_counts[True]}, "
        f"false={escalation_counts[False]}"
    )

    if errors:
        print(f"- Result: FAIL ({len(errors)} errors)")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("- Result: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Project v0 Status — Dataset & Runbook Foundation

## 1. Meaning of Project v0

Project v0 defines the dataset, Runbook knowledge base, schema, and validation
criteria for Enterprise IT Runbook Agent. It does not yet include an implemented
Agent system.

## 2. Completed Work

- Project topic defined: Enterprise IT Runbook Agent
- Three reference datasets reviewed
- Korean Runbook KB drafted
- Korean synthetic issue/eval dataset created
- Evaluation schema and controlled labels designed
- Dataset validation script created
- Project-level versioning and naming rules clarified
- Raw reference data separated from commit-ready project artifacts

## 3. Current Artifacts

- `docs/REFERENCE_DATASET_REVIEW.md`
- `docs/SYNTHETIC_DATASET_DESIGN.md`
- `docs/VERSION_PLAN.md`
- `data/runbooks/`
- `data/eval_sets/korean_it_issues_v0.jsonl`
- `scripts/validate_synthetic_dataset.py`

The current Project v0 eval dataset contains 30 Korean synthetic cases and maps
them to 11 Runbooks. The earlier baseline is retained as
`data/eval_sets/korean_it_issues_draft.jsonl` for review history only.

## 4. What v0 Is For

The Project v0 dataset is not user-facing production data. It is a test/eval
dataset used to validate whether the future Agent can:

- classify issue category and severity
- retrieve the expected Runbook
- detect missing information
- decide escalation and owner-team routing
- produce schema-compliant structured output

## 5. Meaning of `expected_escalation`

`expected_escalation` indicates whether an issue should be routed or escalated
beyond the first-level IT helpdesk.

- `false`: the first-level IT helpdesk can handle the issue using an approved
  Runbook and its standard permissions.
- `true`: the issue should be routed to a specialized team or a higher-level
  response process for investigation, change, or incident handling.

This field represents routing responsibility, not severity alone. A high-impact
issue may still remain with the helpdesk when the cause and approved response
are already known, while a medium-severity issue may require specialist routing.

## 6. What v0 Does Not Include

- Agent workflow implementation
- RAG retrieval pipeline implementation
- embedding or vector-store implementation
- LLM-based response generation
- evaluation runner
- API server
- web UI
- trace storage
- quantitative evaluation results

## 7. Next Step

Project v1 will implement the minimum end-to-end Agent workflow using the
Project v0 Runbook KB and eval dataset as its initial knowledge and test
foundation.

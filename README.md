# Enterprise IT Runbook Agent

An Agentic RAG project for classifying enterprise IT issues, retrieving relevant
Runbooks, and generating resolution plans, verification steps, and
escalation/routing drafts.

## Current Stage

This repository is currently at **Project v0 - Dataset & Runbook Foundation**.
Project v0 is not an Agent implementation release. It defines the foundational
assets required for future Agent development:

- Review of Hugging Face reference dataset structures
- Draft Korean IT Runbook knowledge base
- Korean synthetic issue/evaluation dataset
- Evaluation schema and validation criteria

The Agent workflow, RAG pipeline, API, UI, and quantitative evaluation results
have not yet been implemented. See the [Version Plan](docs/VERSION_PLAN.md) and
[Project v0 Status](docs/PROJECT_V0_STATUS.md) for details.

## Project Versions

| Version | Name | Purpose |
| --- | --- | --- |
| Project v0 | Dataset & Runbook Foundation | Define the problem space, Runbook KB, synthetic evaluation dataset, schema, and validation criteria |
| Project v1 | Minimum Agent Workflow | Implement the minimum end-to-end Agent workflow using Project v0 assets |
| Project v2 | Evaluation-Driven Agent Improvement | Improve retrieval and workflow behavior through quantitative evaluation and failure analysis |

## Project v0 Artifacts

- `docs/REFERENCE_DATASET_REVIEW.md`
- `docs/SYNTHETIC_DATASET_DESIGN.md`
- `data/runbooks/`
- `data/eval_sets/korean_it_issues_v0.jsonl`
- `scripts/validate_synthetic_dataset.py`

`data/eval_sets/korean_it_issues_draft.jsonl` preserves the baseline from before
the Project v0 evaluation dataset was refined. The current validation target is
`korean_it_issues_v0.jsonl`.

## Validation

```bash
python scripts/validate_synthetic_dataset.py
```

Local Hugging Face source datasets and exports are stored under
`data/reference/` and must not be committed to Git.

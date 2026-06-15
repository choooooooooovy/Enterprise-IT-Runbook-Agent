# Version Plan

## 1. Purpose

This document defines the project-level versioning strategy for Enterprise IT
Runbook Agent. Version names describe the maturity of the whole project, not
revisions of an individual dataset, Runbook, script, or document.

## 2. Version Overview

| Version | Name | Purpose |
| --- | --- | --- |
| Project v0 | Dataset & Runbook Foundation | Define the problem space, Korean Runbook KB, synthetic eval dataset, schemas, and validation criteria |
| Project v1 | Minimum Agent Workflow | Implement the first end-to-end Agent workflow using the Project v0 Runbook KB and eval dataset |
| Project v2 | Evaluation-Driven Agent Improvement | Expand the eval dataset and improve the Agent based on quantitative metrics and failure analysis |

## 3. Project v0 — Dataset & Runbook Foundation

Project v0 is a foundation stage, not an Agent implementation stage. It defines
what the future Agent should know, what outputs it should produce, and how its
behavior will be evaluated.

Project v0 includes:

- reference dataset review
- Korean Runbook knowledge base
- Korean synthetic issue/eval dataset
- schema design and controlled labels
- validation script and validation criteria
- dataset and Runbook README documentation

The current `data/runbooks/` documents and
`data/eval_sets/korean_it_issues_v0.jsonl` belong to Project v0.

## 4. Project v1 — Minimum Agent Workflow

Project v1 will implement the first minimum end-to-end workflow:

- issue intake
- issue classification
- Runbook retrieval
- missing information check
- resolution plan generation
- verification
- escalation/routing ticket draft
- trace logging

The workflow will consume the Runbook KB and eval dataset established in
Project v0. Project v1 has not yet been implemented.

## 5. Project v2 — Evaluation-Driven Agent Improvement

Project v2 will improve the Agent using measured behavior and failure analysis:

- eval dataset expansion
- baseline versus improved metric comparison
- classification, retrieval, and routing failure analysis
- retrieval and indexing improvement
- prompt and workflow improvement
- reproducible evaluation report

## 6. Naming Rules

Project version names refer to whole-project maturity. They must not be used as
ad hoc labels for a dataset refinement, document revision, or branch that is
unrelated to the corresponding project stage.

Current dataset and Runbook outputs belong to Project v0. Dataset iterations
inside the same project stage should use descriptive names such as `draft`,
`baseline`, or a dated revision when preservation is necessary.

Project v1 is reserved for the future Minimum Agent Workflow implementation.
The current foundation dataset must not be described as "dataset v1."

## 7. Branch Management Rules

- Work on one task-specific branch at a time.
- Do not push directly to `main`.
- After a PR is merged, delete the remote branch.
- Branch names should describe the task without creating ambiguous version labels.
- Use project-level version names only when the task is explicitly tied to that project version.

Recommended examples:

```text
chore/align-versioning-v0
feat/minimum-agent-workflow
feat/rag-pipeline
eval/add-eval-runner
docs/update-evaluation-report
```

Avoid names such as `data/refine-synthetic-dataset-v1` because a dataset
revision label can be confused with the Project v1 Agent implementation stage.

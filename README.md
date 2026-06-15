# Enterprise IT Runbook Agent

Enterprise IT 운영 이슈를 분류하고 관련 Runbook을 검색해 해결 계획, 검증,
escalation/routing 초안을 생성하는 Agentic RAG 프로젝트다.

## Current Stage

현재 repository는 **Project v0 — Dataset & Runbook Foundation** 단계다.
Project v0는 Agent 구현 버전이 아니라 다음 기반 자산을 정의하는 단계다.

- Hugging Face reference dataset 구조 검토
- 한국어 IT Runbook knowledge base 초안
- 한국어 synthetic issue/eval dataset
- 평가 schema와 validation 기준

Agent workflow, RAG pipeline, API, UI와 정량 평가 결과는 아직 구현되지 않았다.
자세한 범위는 [Version Plan](docs/VERSION_PLAN.md)과
[Project v0 Status](docs/PROJECT_V0_STATUS.md)를 참고한다.

## Project Versions

| Version | Name | Purpose |
| --- | --- | --- |
| Project v0 | Dataset & Runbook Foundation | 문제 공간, Runbook KB, synthetic eval dataset, schema와 검증 기준 정의 |
| Project v1 | Minimum Agent Workflow | Project v0 자산을 사용하는 최소 end-to-end Agent workflow 구현 |
| Project v2 | Evaluation-Driven Agent Improvement | 정량 평가와 실패 분석을 바탕으로 검색과 workflow 개선 |

## Project v0 Artifacts

- `docs/REFERENCE_DATASET_REVIEW.md`
- `docs/SYNTHETIC_DATASET_DESIGN.md`
- `data/runbooks/`
- `data/eval_sets/korean_it_issues_v0.jsonl`
- `scripts/validate_synthetic_dataset.py`

`data/eval_sets/korean_it_issues_draft.jsonl`은 Project v0 평가셋을 정제하기 전의
baseline 보관본이다. 현재 검증 기준 파일은 `korean_it_issues_v0.jsonl`이다.

## Validation

```bash
python scripts/validate_synthetic_dataset.py
```

로컬 Hugging Face 원본과 exports는 `data/reference/` 아래에 유지되며 Git에
commit하지 않는다.

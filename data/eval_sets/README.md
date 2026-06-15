# Korean IT Synthetic Issue/Eval Set

이 폴더는 Enterprise IT Runbook Agent의 초기 동작을 평가하기 위한 한국어
합성 issue set을 담는다.

- `korean_it_issues_v0.jsonl`: 최초 baseline 30건
- `korean_it_issues_v1.jsonl`: Hardware Runbook 매핑과 severity, escalation,
  missing-information 분포를 정제한 30건

실제 사용자 ticket이나 Hugging Face 원본 행을 번역한 데이터가 아니며,
현실적인 helpdesk 패턴을 참고해 프로젝트 용도에 맞게 새로 작성한 draft다.

구조 참고에 사용한 reference dataset:

- `mindweave/help-desk-tickets`: ticket, priority, SLA, escalation, team 구조
- `bdragun/service-desk-tickets`: ticket/QRG 검색과 단계별 답변 구조
- `Console-AI/IT-helpdesk-synthetic-tickets`: issue 제목과 설명의 표현 다양성

이 데이터셋은 category/severity 분류, Runbook 검색 hit, 필수 정보 누락 탐지,
escalation 판단, owner team routing, JSON schema 준수를 평가한다. 각 case의
`expected_*` 값은 정답 label 초안이며 `reference_sources`는 원문 provenance가
아니라 구조적 패턴을 참고한 출처를 뜻한다.

`expected_escalation`은 심각도 자체가 아니라 1차 IT 헬프데스크가 직접 처리할
수 있는지 여부다. `false`이면 `IT 헬프데스크`가 표준 절차로 처리하고,
`true`이면 `expected_owner_team`의 전문팀 또는 상위 대응 프로세스로 전달한다.

v1 실제 분포:

- Severity: Low 9, Medium 8, High 9, Critical 4
- Escalation: true 15, false 15
- Complete information: `expected_missing_info = []` 7건
- Hardware: 2건 모두 `RB-011 장비 및 하드웨어 장애 대응 Runbook`에 매핑

현재 한계:

- 30개 case뿐인 소규모 수동 합성 초안이다.
- 실제 조직의 서비스 구성, SLA, 승인 체계, 장애 빈도를 반영하지 않는다.
- expected label은 운영 전문가 검수를 거치지 않았다.
- 한국어 표현, 난이도, category 경계와 adversarial case가 제한적이다.
- production benchmark로 사용하기 전에 중복, 편향, 정답 타당성을 검토해야 한다.

검증:

```bash
python scripts/validate_synthetic_dataset.py
python scripts/validate_synthetic_dataset.py --file data/eval_sets/korean_it_issues_v0.jsonl
```

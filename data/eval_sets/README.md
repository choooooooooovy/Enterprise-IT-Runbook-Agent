# Korean IT Synthetic Issue/Eval Set

`korean_it_issues_v0.jsonl`은 Enterprise IT Runbook Agent의 초기 동작을
평가하기 위한 한국어 합성 issue set이다. 실제 사용자 ticket이나 Hugging Face
원본 행을 번역한 데이터가 아니며, 현실적인 helpdesk 패턴을 참고해 프로젝트
용도에 맞게 새로 작성한 v0 draft다.

구조 참고에 사용한 reference dataset:

- `mindweave/help-desk-tickets`: ticket, priority, SLA, escalation, team 구조
- `bdragun/service-desk-tickets`: ticket/QRG 검색과 단계별 답변 구조
- `Console-AI/IT-helpdesk-synthetic-tickets`: issue 제목과 설명의 표현 다양성

이 데이터셋은 category/severity 분류, Runbook 검색 hit, 필수 정보 누락 탐지,
escalation 판단, owner team routing, JSON schema 준수를 평가한다. 각 case의
`expected_*` 값은 정답 label 초안이며 `reference_sources`는 원문 provenance가
아니라 구조적 패턴을 참고한 출처를 뜻한다.

현재 한계:

- 30개 case뿐인 소규모 수동 합성 초안이다.
- 실제 조직의 서비스 구성, SLA, 승인 체계, 장애 빈도를 반영하지 않는다.
- expected label은 운영 전문가 검수를 거치지 않았다.
- 한국어 표현, 난이도, category 경계와 adversarial case가 제한적이다.
- production benchmark로 사용하기 전에 중복, 편향, 정답 타당성을 검토해야 한다.

검증:

```bash
python scripts/validate_synthetic_dataset.py
```

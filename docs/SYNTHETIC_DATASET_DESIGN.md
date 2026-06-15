# Synthetic Dataset Design

## 1. 목적과 범위

`korean_it_issues_v0.jsonl`은 Enterprise IT Runbook Agent의 Project v0
평가를 위한 한국어 합성 issue set이다. 운영 사실을 재현하는 학습 데이터가
아니라, 향후 Project v1에서 구현할 workflow의 분류·검색·판단·구조 준수
여부를 점검하기 위한 기반 데이터다.

`korean_it_issues_draft.jsonl`은 현재 Project v0 평가셋을 만들기 전의
baseline 보관본이며 기본 검증 대상이 아니다.

```text
Issue Intake
-> Issue Classification
-> Runbook Retrieval
-> Required Information Check
-> Resolution Plan Generation
-> Verification
-> Escalation Ticket Draft
```

Reference dataset은 ticket 구조와 표현 패턴만 제공한다. 각 case는 한국어
업무 환경에 맞게 새로 구성하며 원본 행을 복사하거나 번역하지 않는다.

## 2. JSONL Schema

각 줄은 하나의 JSON object이며 아래 필드를 모두 포함한다.

| Field | Type | Description |
| --- | --- | --- |
| `issue_id` | string | `ISSUE-001` 형식의 유일 식별자 |
| `title` | string | 한국어 issue 제목 |
| `description` | string | 영향 범위와 현재 증상을 포함한 한국어 설명 |
| `expected_category` | enum | 허용 category 중 하나 |
| `expected_severity` | enum | `Low`, `Medium`, `High`, `Critical` 중 하나 |
| `expected_runbook_id` | string | `data/runbooks`에 존재하는 Runbook ID |
| `expected_runbook_title` | string | 검색되어야 할 Runbook의 한국어 제목 |
| `expected_escalation` | boolean | 1차 헬프데스크가 직접 처리하지 않고 전문팀 또는 상위 프로세스로 전달해야 하는지 여부 |
| `expected_owner_team` | enum | 허용 owner team 중 하나 |
| `expected_missing_info` | string[] | 판단/조치 전에 추가로 필요한 정보 |
| `reference_sources` | string[] | 패턴 설계에 참고한 reference dataset ID |
| `notes` | string | case 의도와 평가 포인트에 대한 짧은 설명 |

예시:

```json
{
  "issue_id": "ISSUE-001",
  "title": "MFA 인증 후 VPN 연결이 끊기는 문제",
  "description": "오늘 오전부터 여러 원격 근무자가 MFA 인증 직후 VPN 연결이 끊긴다고 보고했습니다.",
  "expected_category": "VPN",
  "expected_severity": "High",
  "expected_runbook_id": "RB-001",
  "expected_runbook_title": "VPN 접속 장애 대응 Runbook",
  "expected_escalation": true,
  "expected_owner_team": "IT 인프라팀",
  "expected_missing_info": ["VPN 클라이언트 버전", "오류 메시지"],
  "reference_sources": ["mindweave/help-desk-tickets", "Console-AI/IT-helpdesk-synthetic-tickets"],
  "notes": "다수 사용자 영향과 인프라 escalation 판단을 평가한다."
}
```

## 3. Controlled Values

### Severity

- `Low`: 단일 사용자, 우회 가능, 업무 중단이 거의 없음
- `Medium`: 단일 또는 소수 사용자 업무가 부분 제한되며 표준 절차로 복구 가능
- `High`: 다수 사용자, 핵심 업무 중단, 보안 위험 또는 빠른 전문팀 대응 필요
- `Critical`: 전사/사업 핵심 서비스 중단, 광범위 보안 사고, 데이터 손실이
  진행 중이거나 즉시 incident 대응이 필요한 상태

사용자 표현의 "급함"만으로 severity를 올리지 않는다. 영향 사용자 수,
서비스 중요도, 우회 가능성, 보안 및 데이터 손실 위험을 함께 판단한다.

### Category

허용값:

```text
VPN
MFA
Password
Account / Permission
Email
Network
SaaS Access
Security
Backup / Recovery
Hardware
General Escalation
```

### Owner Team

허용값:

```text
IT 헬프데스크
IT 인프라팀
IAM팀
보안팀
메일/협업도구팀
네트워크팀
장비지원팀
백업/스토리지팀
```

## 4. Runbook Mapping

| Category | Primary Runbook | Specialist / Escalation Owner |
| --- | --- | --- |
| VPN | RB-001 | IT 인프라팀 |
| MFA | RB-002 | IAM팀 |
| Password | RB-003 | IT 헬프데스크 |
| Account / Permission | RB-004 | IAM팀 |
| Email | RB-005 | 메일/협업도구팀 |
| Network | RB-006 | 네트워크팀 |
| SaaS Access | RB-007 | IT 헬프데스크 |
| Security | RB-008 | 보안팀 |
| Backup / Recovery | RB-009 | 백업/스토리지팀 |
| Hardware | RB-011 | 장비지원팀 |
| General Escalation | RB-010 | IT 헬프데스크 |

RB-010은 표준 category로 명확히 분류할 수 없는 이슈의 영향도, 증거, 인계
정보를 정리하는 공통 escalation 정책이다. Hardware issue는 장비 기본 점검과
교체/수리 조건을 포함한 RB-011을 검색해야 한다. 표의 owner는 전문 조치가
필요할 때의 인계 대상이며, `expected_escalation = false`인 개별 case의 owner는
`IT 헬프데스크`다.

## 5. Escalation and Missing Information

`expected_escalation`은 severity의 다른 이름이 아니다. 이 값은 1차 IT
헬프데스크가 직접 처리할 수 있는지, 전문 담당 팀 또는 상위 대응 프로세스로
전달해야 하는지를 나타낸다.

- `false`: 1차 헬프데스크가 표준 Runbook과 승인된 권한으로 직접 처리한다.
  `expected_owner_team`은 `IT 헬프데스크`다.
- `true`: 네트워크, IAM, 보안, 장비, 백업 등 전문팀의 조사/변경 또는 상위
  incident 대응이 필요하다. `expected_owner_team`은 실제 인계 대상이다.

아래 중 하나에 해당하면 true를 우선 고려한다.

- 다수 사용자 또는 핵심 서비스에 동일 증상이 발생
- 보안 침해, 의심 로그인, 계정 탈취 가능성
- 데이터 손실, 백업 실패, 복구 무결성 위험
- 표준 조치 후에도 재현되거나 관리자 권한/인프라 변경이 필요
- SLA 위반 위험 또는 소유 팀이 헬프데스크 범위를 벗어남

`expected_missing_info`는 issue 본문에 없는 정보만 기록한다. 빈 배열은
현재 설명에 Runbook 선택과 다음 조치에 필요한 정보가 충분히 포함된
complete-information case를 뜻한다.

## 6. Dataset Composition

총 30개 case의 목표 category 분포:

| Category | Cases |
| --- | ---: |
| VPN | 3 |
| MFA | 3 |
| Password | 3 |
| Account / Permission | 4 |
| Email | 3 |
| Network | 3 |
| SaaS Access | 3 |
| Security | 3 |
| Backup / Recovery | 2 |
| Hardware | 2 |
| General Escalation | 1 |

severity, escalation, missing information, single/multiple-user impact를 섞는다.
각 case는 적어도 하나의 reference source를 기록하지만, 이는 원문 provenance가
아니라 어떤 구조적 패턴을 참고했는지를 나타낸다.

### Project v0 Distribution

현재 Project v0 평가셋의 실제 분포는 다음과 같다.

| Dimension | Distribution |
| --- | --- |
| Severity | Low 9, Medium 8, High 9, Critical 4 |
| Escalation | true 15, false 15 |
| Missing information | 빈 배열 7, 누락 항목 있음 23 |
| Runbook | RB-001~RB-009, RB-011은 category별 사용, RB-010은 General Escalation 1건 |

Critical은 성공한 계정 침해, 전사 DNS 중단, 고권한 자격 증명 노출, 핵심
백업 연속 실패처럼 즉시 대응이 필요한 case에 제한한다. complete-information
case는 VPN, MFA, Email, Network, SaaS Access, Security category에 포함한다.

## 7. Quality and Validation Rules

- 모든 자연어 필드는 한국어로 작성한다.
- `issue_id`는 유일해야 하며 case 수는 정확히 30개여야 한다.
- category, severity, owner는 controlled value만 사용한다.
- Runbook ID와 제목은 실제 파일과 일치해야 한다.
- 정답 label이 description에 그대로 노출되지 않도록 하되 판단 근거는 제공한다.
- 서로 다른 case가 같은 문장 템플릿의 숫자만 바꾼 형태가 되지 않게 한다.
- 원본 reference row, 인명, 이메일, URL, IP를 복사하지 않는다.
- Project v0 평가셋은 수동 검토 전제의 초안이며 production benchmark로
  간주하지 않는다.

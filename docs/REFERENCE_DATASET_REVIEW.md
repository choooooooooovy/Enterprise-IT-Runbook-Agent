# Reference Dataset Review

이 문서는 로컬에 내려받은 공개 Hugging Face 데이터셋을 구조 참고용으로
검토한 결과다. 원본 행을 프로젝트 데이터로 복제하거나 번역하지 않으며,
Project v0의 한국어 Runbook과 synthetic issue/eval set을 설계하기 위한
패턴만 사용한다. 이 검토는 Agent 구현이 아니라 Dataset & Runbook Foundation
단계의 산출물이다.

## 1. mindweave/help-desk-tickets

- Available files/splits:
  - `agents.csv`: 10행
  - `categories.csv`: 8행
  - `comments.csv`: 2,000행
  - `sla_breaches.csv`: 1,249행
  - `tickets.csv`: 1,000행
- Schema:
  - agents: `id`, `name`, `team`
  - categories: `id`, `name`, `service`
  - comments: `comment_id`, `ticket_id`, `agent_id`, `created_at`,
    `visibility`, `team`, `body`
  - SLA breaches: `breach_id`, `ticket_id`, `breach_type`,
    `sla_target_hours`, `actual_hours`, `breach_minutes`
  - tickets: 식별자/시간, `priority`, `status`, `channel`, category/agent
    참조, 요청 부서, 영향 서비스, `summary`, `description`, `escalated`,
    `outage_related`
- Useful fields:
  - Text: `summary`, `description`, comment의 `body`
  - Category: `category_id`, `affected_service`, categories 테이블의
    `name`과 `service`
  - Priority: `P1`~`P4`
  - Escalation/SLA: `escalated`, `outage_related`, SLA 목표와 실제 시간,
    breach 분
  - Conversation: ticket별 public/internal comment와 담당 team
  - 문서형 지식 필드는 없으며, ticket/comment/SLA 관계가 중심이다.
- What it can be used for:
  - ticket, comment, category, 담당 team, SLA를 연결하는 현실적인 ITSM 구조
  - 우선순위별 대응 시간, escalation 여부, 상태 전이 패턴
  - 단일 사용자 요청과 서비스 영향 이슈의 문장 길이 및 필드 구성
- Limitations:
  - 영어 합성 데이터이며 무료 샘플의 일부다.
  - `outage_related`는 로컬 샘플에서 모두 false라 outage 판단 학습에는
    충분하지 않다.
  - comment 본문은 반복되는 짧은 템플릿이 많아 답변 품질의 직접 기준으로
    쓰기 어렵다.
  - 원본 category와 프로젝트 category는 일대일로 대응하지 않는다.
- License / usage note:
  - README metadata 기준 `CC BY-NC 4.0`.
  - 비상업 조건과 저작자 표시 의무를 고려해야 한다. 이 프로젝트에서는
    원본 재배포 없이 구조와 분포만 참고한다.

## 2. bdragun/service-desk-tickets

- Available files/splits:
  - train Parquet: 711행
  - test Parquet: 178행
  - 총 889행이며 metadata상 ticket 485개, QRG 404개다.
- Schema:
  - `conversations`, `source_id`, `source_type`, `category`
  - `conversations`는 system/user/assistant 메시지 3개를 담은 JSON 문자열이다.
- Useful fields:
  - Text: user 질문과 assistant의 절차형 답변
  - Category: `knowledge-base`, `access-request`, `software`, `hardware`,
    `network`, `password-reset`
  - Priority: 별도 컬럼은 없지만 ticket 기반 assistant 답변에
    low/medium/high/critical 표현이 포함된다.
  - Escalation/SLA: 별도 컬럼은 없고 일부 대화 본문에서 escalation, SLA,
    outage 문맥을 확인할 수 있다.
  - Conversation: `source_type`으로 ticket과 QRG를 구분하고
    `source_id`로 TKT/QRG 근거를 표시한다.
  - Knowledge-base/QRG: QRG 기반 질의응답 404개가 명시적으로 존재한다.
- What it can be used for:
  - 문제 질문에서 ticket 또는 QRG 근거를 찾아 단계별 답변을 만드는 패턴
  - prerequisite, resolution, verification, source citation을 포함하는 문서 구조
  - access, password, network, hardware 등 Runbook 절차의 범위 참고
- Limitations:
  - 영어이며 특정 가상 조직의 제품명, 계정, IP, 인프라 구성을 포함한다.
  - 대화가 항상 3개 메시지로 정형화되어 실제 다중 턴 support 대화를
    충분히 대표하지 않는다.
  - priority와 escalation이 명시적 컬럼이 아니므로 텍스트 파싱 결과를
    정답 label로 간주하면 안 된다.
  - README에 license가 선언되어 있지 않아 재사용 조건을 별도로 확인해야 한다.
- License / usage note:
  - 2026-06-15 재확인 기준, 로컬 README front matter와 Hugging Face 공식
    dataset API의 `cardData`/tags 모두 license를 선언하지 않는다.
  - 불명확한 license 때문에 원문이나 답변을 파생 데이터에 복사하지 않고,
    QRG/ticket 구분과 절차형 응답 패턴만 참고한다.

## 3. Console-AI/IT-helpdesk-synthetic-tickets

- Available files/splits:
  - `tickets.csv`: 500행, 별도 split 없음
- Schema:
  - `id`, `subject`, `description`, `priority`, `category`, `createdAt`,
    `requesterEmail`
- Useful fields:
  - Text: `subject`, `description`
  - Category: Software, Account, Network, Security, Communication, Hardware,
    RemoteWork 등 11종
  - Priority: Low, Medium, High, Urgent
  - escalation/SLA, comment/conversation, knowledge-base/QRG 필드는 없다.
- What it can be used for:
  - helpdesk 제목과 설명의 다양한 사용자 표현
  - single-user와 multiple-user 영향 표현
  - account/network/security/hardware 등 넓은 category 후보 참고
- Limitations:
  - 영어 합성 데이터이며 category 분포가 Software에 치우쳐 있다.
  - escalation, owner team, resolution, verification 정보가 없다.
  - 이메일과 URL 등 프로젝트 평가에 불필요한 식별성 문자열이 포함될 수 있다.
  - `Urgent`는 프로젝트 severity enum에 없으므로 `Critical`로 기계 변환하지
    않고 영향 범위를 별도로 판단해야 한다.
- License / usage note:
  - README metadata 기준 `MIT`.
  - 본 프로젝트에서는 원본 행을 복제하지 않고 issue phrasing의 다양성만
    참고한다.

## Summary

- Recommended use of each dataset:
  - mindweave: ITSM 관계 구조, priority/SLA/escalation, team routing 참고
  - bdragun: ticket/QRG 기반 검색, prerequisite와 단계별 해결 절차 참고
  - Console-AI: 사용자 issue 제목/설명의 표현 다양성과 category 범위 참고
- Fields/patterns to reuse as reference:
  - 짧은 title과 상황 중심 description 분리
  - category, severity, 영향 범위, owner team, escalation을 명시적으로 분리
  - 필수 정보 확인 후 절차 수행, 검증, 실패 시 escalation하는 Runbook 구조
  - 검색 근거의 ID와 제목을 evaluation label로 제공하는 방식
- Fields/patterns not suitable for this project:
  - 원본 ID, 인명, 이메일, URL, IP, 조직명과 제품별 내부 설정
  - 영어 원문 또는 단순 한국어 번역
  - 원본 category/priority 값을 검토 없이 프로젝트 label로 직접 매핑
  - 반복 comment 템플릿, 과도하게 구체적인 가상 조직 해결 내역

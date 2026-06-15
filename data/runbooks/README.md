# Korean IT Runbooks

이 폴더는 Enterprise IT Runbook Agent가 검색하고 근거로 사용할 한국어
운영 절차 초안 11개를 담는다. 각 Runbook은 category, 증상, 필수 정보,
해결 절차, 검증, escalation 조건과 owner team을 명시한다. RB-011은 노트북,
주변기기, 프린터 등 Hardware issue의 기본 점검과 교체/수리 인계 기준을
담당하며 Hardware retrieval target으로 사용한다.

RAG pipeline은 issue의 category와 핵심 증상을 바탕으로 관련 Runbook을
검색한 뒤, `Required Information`의 누락 항목을 확인하고 `Resolution Steps`와
`Verification`에 근거한 대응 계획을 생성한다. escalation 조건에 해당하면
수집한 정보와 수행 결과를 소유 팀에 전달해야 한다.

`data/eval_sets/korean_it_issues_v0.jsonl`의 각 case는
`expected_runbook_id`와 `expected_runbook_title`로 이 폴더의 문서 하나를
가리킨다. Hardware case는 RB-011에 매핑되고, category가 불명확한 incident만
RB-010 일반 escalation 정책을 사용한다.

이 Runbook과 평가셋은 모두 Project v0 foundation 산출물이다. Project v1에서
구현할 Minimum Agent Workflow가 이 문서들을 검색 지식으로 사용하게 된다.
현재 문서는 draft이며 실제 조직의 도구, 승인 정책, SLA, 연락 체계에 맞춘
수동 검토가 필요하다.

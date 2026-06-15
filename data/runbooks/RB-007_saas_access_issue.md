# RB-007 SaaS 접근 장애 대응 Runbook

## Category
SaaS Access

## Symptoms
- 승인된 SaaS 애플리케이션에 로그인할 수 없다.
- 라이선스 또는 좌석 부족 메시지가 표시된다.
- SSO 후 반복 리디렉션되거나 특정 workspace가 보이지 않는다.

## Required Information
- 애플리케이션명과 tenant/workspace
- 대상 계정과 필요한 역할
- 오류 메시지와 마지막 정상 접근 시각
- SSO/직접 로그인 여부
- 라이선스 할당과 승인 정보

## Resolution Steps
1. 공급자 상태 페이지와 조직 tenant 장애 여부를 확인한다.
2. 계정 활성 상태, SSO 할당, 라이선스와 그룹 멤버십을 확인한다.
3. 브라우저의 새 개인 세션에서 로그인해 세션 문제를 분리한다.
4. 승인된 표준 역할과 workspace 멤버십을 적용한다.
5. 프로비저닝 동기화를 재시도하고 변경 전파를 기다린다.
6. 공급자 오류면 시간, 요청 ID, 영향 범위를 기록한다.

## Verification
- 새 세션에서 대상 workspace와 필요한 기능에 접근되는지 확인한다.
- 과도한 역할이나 중복 라이선스가 부여되지 않았는지 확인한다.

## Escalation Conditions
- 여러 사용자가 같은 SaaS에 접근하지 못한다.
- SSO/provisioning 오류가 지속되거나 공급자 지원이 필요하다.
- 고권한 역할 또는 추가 구매가 필요한 요청이다.

## Owner Team
IT 헬프데스크

## Related Keywords
- SaaS
- SSO
- 라이선스
- workspace
- 프로비저닝

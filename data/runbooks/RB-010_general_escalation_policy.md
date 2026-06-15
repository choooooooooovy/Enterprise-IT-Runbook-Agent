# RB-010 일반 Escalation 정책 Runbook

## Category
General Escalation

## Symptoms
- 기존 category로 명확히 분류되지 않거나 여러 서비스가 동시에 영향을 받는다.
- 표준 Runbook 조치 후에도 문제가 지속된다.
- hardware 고장, 공급자 장애, 관리자 변경 등 전문팀 작업이 필요하다.

## Required Information
- 영향 사용자, 위치, 서비스와 업무 영향
- 최초 발생 시각, 재현 절차, 오류 메시지
- 이미 수행한 조치와 결과
- 최근 변경, 관련 자산, 공급자 정보
- 현재 우회 방법과 SLA 위험

## Resolution Steps
1. 안전 또는 보안 위험이 있으면 사용을 중단하고 즉시 격리한다.
2. 영향 범위, 긴급도, 우회 가능성을 기준으로 severity를 정한다.
3. 관련 표준 Runbook의 비파괴적 초기 점검만 수행한다.
4. 재현 결과, 로그, 사진, 자산 번호 등 필요한 증거를 수집한다.
5. 소유 팀과 현재 incident/ticket을 확인해 중복 escalation을 피한다.
6. 문제, 영향, 수행 조치, 요청 사항을 구조화해 소유 팀에 인계한다.

## Verification
- 소유 팀이 ticket과 증거를 인수했는지 확인한다.
- 사용자에게 다음 업데이트 시각과 가능한 우회 방법을 안내한다.

## Escalation Conditions
- 다수 사용자 또는 핵심 업무가 중단됐다.
- 보안, 안전, 데이터 손실 위험이 있다.
- 장비 교체, 관리자 변경, 공급자 지원이 필요하다.
- SLA 위반이 임박했거나 소유 팀이 불명확하다.

## Owner Team
IT 헬프데스크

## Related Keywords
- 상위 지원
- 담당팀 이관
- 장비 고장
- 공급자 지원
- SLA
- 영향도

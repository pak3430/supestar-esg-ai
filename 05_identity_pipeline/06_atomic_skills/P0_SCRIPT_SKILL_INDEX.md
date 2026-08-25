# 수페스타 P0 스크립트 스킬 인덱스

- 기준일: 2026-08-21 KST
- 현재 상태: `PROJECT_CODE_CANDIDATE_VALIDATED + BUILD_CANDIDATE_7/7`
- 정식 상태: CCS canonical 승격·복합 스킬 governance·Runtime 배포 전

## 실제 코드가 있는 일곱 스킬

| 순서 | 스킬 | 실행 코드 | 주요 산출물 |
| ---: | --- | --- | --- |
| 0 | [질문 라우팅](supestar-question-routing/SKILL.md) | [run.py](supestar-question-routing/scripts/run.py) | ContextSnapshot, RouteDecision, Run Record |
| 1 | [ESG→탄소 행동경로](esg-carbon-action-path/SKILL.md) | [run.py](esg-carbon-action-path/scripts/run.py) | ActionPath, 설명 카드, 체크리스트 |
| 2 | [Scope 활동 분류](scope-activity-classification/SKILL.md) | [run.py](scope-activity-classification/scripts/run.py) | ScopeClassification, 근거 카드, 추가자료 요청 |
| 3 | [탄소시장·단위 비교](carbon-market-unit-comparison/SKILL.md) | [run.py](carbon-market-unit-comparison/scripts/run.py) | 비교표, 사용조건, 주장 주의사항 |
| 4 | [산림 E/S/G 매핑](forest-esg-impact-mapping/SKILL.md) | [run.py](forest-esg-impact-mapping/scripts/run.py) | E/S/G 지도, 누락축 질문 |
| 5 | [산림탄소 공식 절차](forest-carbon-procedure-guidance/SKILL.md) | [run.py](forest-carbon-procedure-guidance/scripts/run.py) | 절차 경로, 체크리스트, 공식 확인질문 |
| 6 | [거래 준비도 게이트](forest-carbon-transaction-readiness/SKILL.md) | [run.py](forest-carbon-transaction-readiness/scripts/run.py) | 11게이트 준비도표, 누락목록, 공식 질의서 |

일곱 `run.py`는 공통 결정론적 실행기 [supestar_skills.py](_shared/supestar_skills.py)를 호출한다. 각 실행은 입력이 같으면 같은 판정과 Run ID를 만들고, `PROCEED`, `REVIEW`, `STOP` 중 하나를 반환한다.

## 검증 자산

- [21개 판정 fixture](_shared/tests/fixtures.json): 7개 스킬마다 `PROCEED`, `REVIEW`, `STOP` 각 1개
- [자동 테스트](_shared/tests/test_supestar_skills.py): 결정론, 예상 판정, wrapper 실행, 산출물 landing 확인
- [일괄 시연 실행기](../tools/run_supestar_p0_demo.py): 각 스킬의 `PROCEED` fixture를 실제 실행
- [실행 증거 manifest](../../06_runtime/tests/p0_script_skill_demo_v1/manifest.json): 일곱 실행의 Run ID·결과·산출물 경로

## Build 구조 연결

- Build authoring vault: [supestar_mvp_v3](../../ccs_authoring/supestar_mvp_v3/AUTHORING_VAULT_BINDING.md)
- 거래 준비도 terminal Build Skill: [forest-carbon-transaction-readiness](../../ccs_authoring/supestar_mvp_v3/_skill/forest-carbon-transaction-readiness/SKILL.md)
- P0 Build7 검증: [완료검증 보고서](../../07_evidence/qa/2026-08-21_수페스타_P0_Build7_완료검증.md)

프로젝트 계층 코드는 실행된 후보이고 v3의 일곱 Skill은 구조화된 Build 후보다. 다음 단계에서 두 계층을 입력·출력 계약과 fixture로 결합해 각각의 Run Skill 및 Run Record를 만든다.

## 해석 경계

이 패키지는 단순 설명 문서가 아니라 입력을 판정하고 파일 산출물을 생성하는 실행 가능한 코드 후보이다. 다만 아직 CCS canonical Skill 또는 배포 완료 Skill이라고 부르지 않는다. 특히 거래 준비도 스킬은 증거 누락을 판정할 뿐 실제 거래·결제·등록부 이전·법률·세무·인증 확정을 수행하지 않는다.

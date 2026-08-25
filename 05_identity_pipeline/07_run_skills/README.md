# 수페스타 P0 Run Skill 7종

이 폴더는 검증된 Build Skill과 고정 실행 코드를 실제 사용자 입력에 결합하는 Run 계층이다. Concept·Build 원본을 복제하지 않고 [`RUN_SKILL_REGISTRY.json`](RUN_SKILL_REGISTRY.json)의 일대일 binding만 실행한다.

| Run Skill | Identity | 실행하는 Build Skill | 사용자 산출물 |
| --- | --- | --- | --- |
| [supestar-question-routing-run](supestar-question-routing-run/SKILL.md) | `USER_QUESTION` | `supestar-question-routing` | 질문 스냅샷, 단일 경로 판정 |
| [esg-carbon-action-path-run](esg-carbon-action-path-run/SKILL.md) | `ESG_MANAGEMENT` | `esg-carbon-action-path` | 행동경로, 설명카드, 다음 행동 |
| [scope-activity-classification-run](scope-activity-classification-run/SKILL.md) | `ORGANIZATIONAL_BOUNDARY` | `scope-activity-classification` | Scope 후보, 근거카드, 추가자료 |
| [carbon-market-unit-comparison-run](carbon-market-unit-comparison-run/SKILL.md) | `CLIMATE_CLAIM` | `carbon-market-unit-comparison` | 시장·단위 비교표, 주장 주의사항 |
| [forest-esg-impact-mapping-run](forest-esg-impact-mapping-run/SKILL.md) | `FOREST_CARBON_PROJECT` | `forest-esg-impact-mapping` | E/S/G 지도, 누락축 질문 |
| [forest-carbon-procedure-guidance-run](forest-carbon-procedure-guidance-run/SKILL.md) | `FOREST_CARBON_PROJECT` | `forest-carbon-procedure-guidance` | 공식 절차 경로, 체크리스트, 확인질문 |
| [forest-carbon-transaction-readiness-run](forest-carbon-transaction-readiness-run/SKILL.md) | `TRANSACTION_EVIDENCE_PACK` | `forest-carbon-transaction-readiness` | 11게이트 준비도, 누락증거, 질의서 초안 |

공통 실행·실패·권한 규칙은 [`RUN_LAYER_CONTRACT.md`](RUN_LAYER_CONTRACT.md)를 따른다. 21개 실제 fixture 실행은 [실행 manifest](../../06_runtime/tests/p0_run_skill_v1/manifest.json), 전체 검증은 [Run Skill 7종 완료검증 보고서](../../07_evidence/qa/2026-08-22_수페스타_P0_RunSkill7_구성검증.md)에서 확인한다. 이 계층은 `CANDIDATE`이며 Composite 또는 Runtime 배포가 아니다.

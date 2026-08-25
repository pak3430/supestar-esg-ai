# 수페스타 P0 추가 체인 작성 계약

이 폴더의 문서는 최종 `SKILL.md`가 아니라 Stage 1~5에서 이미 생성된 Identity에 서로 다른 실행 능력을 추가하기 위한 입력 계약이다. 계약을 구현한 프로젝트 계층의 스크립트형 후보는 [P0 스크립트 스킬 인덱스](../P0_SCRIPT_SKILL_INDEX.md)에서 확인한다.

- authoringVault: [supestar_mvp_v3](../../../ccs_authoring/supestar_mvp_v3/AUTHORING_VAULT_BINDING.md)
- identitySchemaCompatibility: `PASS`
- transactionEvidenceGrounding: `APPROVED_WITH_SCOPE_LIMITS`
- additionalChainIdentityGate: `7 / 7 PASS`

`additional_chain_authoring_skill`의 원칙에 따라 한 번의 실행은 다음 하나만 만든다.

`기존 Identity → 새 Goal facet → Task → Knowledge → Method → Action Skill`

## 작성 대상

| 순서 | 계약 | Target Identity | 상태 |
| ---: | --- | --- | --- |
| 0 | [질문 라우팅](00_supestar_question_routing_authoring_contract.md) | `USER_QUESTION` | `BUILD_CANDIDATE_AUTHORED` |
| 1 | [ESG→탄소 행동경로](01_esg_carbon_action_path_authoring_contract.md) | `ESG_MANAGEMENT` | `BUILD_CANDIDATE_AUTHORED` |
| 2 | [Scope 활동 분류](02_scope_activity_classification_authoring_contract.md) | `ORGANIZATIONAL_BOUNDARY` | `BUILD_CANDIDATE_AUTHORED` |
| 3 | [탄소시장·단위 비교](03_carbon_market_unit_comparison_authoring_contract.md) | `CLIMATE_CLAIM` | `BUILD_CANDIDATE_AUTHORED` |
| 4 | [산림 E/S/G 매핑](04_forest_esg_impact_mapping_authoring_contract.md) | `FOREST_CARBON_PROJECT` | `BUILD_CANDIDATE_AUTHORED` |
| 5 | [산림탄소 공식 절차](05_forest_carbon_procedure_guidance_authoring_contract.md) | `FOREST_CARBON_PROJECT` | `BUILD_CANDIDATE_AUTHORED` |
| 6 | [거래 준비도 게이트](06_forest_carbon_transaction_readiness_authoring_contract.md) | `TRANSACTION_EVIDENCE_PACK` | `BUILD_CANDIDATE_AUTHORED` |

## 공통 실행 계약

- 각 계약은 하나의 고정된 capability direction만 가진다.
- 기존 Concept Skill을 수정하거나 덮어쓰지 않는다.
- 각 새 Goal·Task·Knowledge·Method·Skill 이름은 대소문자 무시 기준으로 충돌하지 않아야 한다.
- 실제 체인은 승인된 authoring vault에 기록하고, 외부 runRoot에는 예약·실행 증거만 기록한다.
- `SKILL.md`는 Method가 확정된 뒤 마지막에 생성한다.
- 결과가 `reservation void`이면 빈 파일이나 임의 대체 Skill을 만들지 않는다.
- Action Skill의 출력에는 `runId`, `status`, `evidence`, `artifacts`, `missingEvidence`, `nextActions`가 있어야 한다.
- 모든 출력 상태는 `PROCEED`, `REVIEW`, `STOP` 중 하나다.
- 실제 거래·결제·등록부 이전·법률·세무 확정·공식 인증은 금지한다.

## 조합 전 통과 조건

1. 일곱 스킬 모두 서로 다른 입력·판정·산출물을 가진다.
2. 정상·REVIEW·STOP fixture가 각 스킬마다 최소 하나씩 존재한다.
3. 모든 근거 링크가 해석되고 기준일이 기록된다.
4. 질문 라우터의 route 값과 복합 스킬 내부 route 값이 정확히 일치한다.
5. 거래 준비도 스킬의 Identity 보강이 완료된다.
6. 각 스킬이 독립 실행되어 Run Record를 남긴다.

프로젝트 계층 코드 후보는 실행 조건을 통과했고 Identity 스키마 호환은 v2에서 해결됐다. 거래 증빙팩 근거를 범위 제한과 함께 승인한 v3에서 일곱 번째 체인을 작성해 P0 Build 후보 `7 / 7`을 완료했다. 이 결과들은 아직 Run Skill·Composite·배포물이 아니다.

## 관련 문서

- [MVP 스킬 선정 카탈로그](../../00_수페스타_MVP_스킬_선정_카탈로그_v1.md)
- [Identity 스키마 호환 완료보고서](../../../07_evidence/qa/2026-08-21_Identity스키마_호환처리_완료보고서.md)
- [P0 Build6 완료검증 보고서](../../../07_evidence/qa/2026-08-21_수페스타_P0_Build6_완료검증.md)
- [P0 Build7 완료검증 보고서](../../../07_evidence/qa/2026-08-21_수페스타_P0_Build7_완료검증.md)
- [복합 스킬 작성 요청](../../07_composite_skills/supestar_forest_esg_orchestrator/composite_authoring_request.md)

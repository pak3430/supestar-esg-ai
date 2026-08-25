# P0 Target Identity Bindings

- status: `CANDIDATE_BINDINGS`
- sourceRun: [Stage 1~5 verified run](../../ccs_runs/2026-08-20_esg_concept_v1/_record/stage_1_to_5_identity_pipeline_verified_run_record.md)
- compatibleAuthoringVault: [supestar_mvp_v2](../../ccs_authoring/supestar_mvp_v2/AUTHORING_VAULT_BINDING.md)
- identitySchemaCompatibility: `PASS`
- canonicalPromotion: `NOT_PERFORMED`

이 문서는 script-backed Action Skill이 어떤 source-linked Identity에서 갈라지는지 고정한다. 원본 Identity를 복제하거나 수정하지 않는다.

| Action capability | Target Identity | Source grounding |
| --- | --- | --- |
| 질문 라우팅 | [USER_QUESTION](../../ccs_runs/2026-08-20_esg_concept_v1/_identity/USER_QUESTION.md) | 구조요구사항의 UserQuestion |
| ESG→탄소 행동경로 | [ESG_MANAGEMENT](../../ccs_runs/2026-08-20_esg_concept_v1/_identity/ESG_MANAGEMENT.md) | ESG 목표·행동·책임 |
| Scope 활동 분류 | [ORGANIZATIONAL_BOUNDARY](../../ccs_runs/2026-08-20_esg_concept_v1/_identity/ORGANIZATIONAL_BOUNDARY.md) | 조직·운영 경계 필요조건 |
| 시장·단위 비교 | [CLIMATE_CLAIM](../../ccs_runs/2026-08-20_esg_concept_v1/_identity/CLIMATE_CLAIM.md) | VCM 절차와 주장 책임 |
| 산림 E/S/G 매핑 | [FOREST_CARBON_PROJECT](../../ccs_runs/2026-08-20_esg_concept_v1/_identity/FOREST_CARBON_PROJECT.md) | 산림탄소 사업의 검증 경로 |
| 산림탄소 절차 안내 | [FOREST_CARBON_PROJECT](../../ccs_runs/2026-08-20_esg_concept_v1/_identity/FOREST_CARBON_PROJECT.md) | 산림탄소 사업의 검증 경로 |
| 거래 준비도 | [TRANSACTION_EVIDENCE_PACK](TRANSACTION_EVIDENCE_PACK_grounding_patch_candidate.md) | 11개 거래 게이트와 증빙팩 보강 후보 |

이 P0 후보 계층은 실행 코드 검증을 먼저 수행하기 위한 project-layer derivation이다. heading 문법 차이는 별도 [v2 authoring vault](../../ccs_authoring/supestar_mvp_v2/SCHEMA_COMPATIBILITY_BINDING.md)에 의미 보존형으로 투영해 검증했으며, 정식 승격은 이 vault의 추가 체인 authoring과 이후 governance를 거쳐야 한다.

# 추가 체인 작성 계약 — 산림탄소 공식 절차 안내

## 1. Binding

- status: `READY`
- targetIdentity: [FOREST_CARBON_PROJECT](../../../ccs_authoring/supestar_mvp_v2/_identity/FOREST_CARBON_PROJECT.md)
- newGoalFacet: `forest_carbon_procedure_guidance`
- capabilityDirection: 산림탄소 사업의 현재 상태를 받아 다음 공식 절차·담당주체·선행조건·필요 산출물을 안내한다.
- distinctFromExistingChain: 기존 Concept Skill은 산림탄소 사업의 의미를 평가한다. 이 체인은 현재 단계에서 다음 단계로 이동하기 위한 체크리스트를 만든다.
- distinctFromSiblingFacet: `forest_esg_impact_mapping`은 E/S/G 영향과 책임을 평가한다. 이 facet은 공식 절차의 순서와 단계별 증거를 안내한다.

## 2. Reserved name set

| node | reserved name |
| --- | --- |
| goal | `forest_carbon_procedure_guidance` |
| task | `forest_carbon_procedure_guidance` |
| knowledge | `forest_carbon_procedure_guidance` |
| method | `forest_carbon_procedure_guidance` |
| skill | `forest-carbon-procedure-guidance` |

## 3. Input contract

| field | required | rule |
| --- | --- | --- |
| `projectType` | yes | 사용자가 알고 있는 사업 유형; 불명확하면 `UNKNOWN` |
| `currentStage` | yes | `PLANNING`, `ELIGIBILITY`, `REGISTERED`, `IMPLEMENTING`, `MONITORING`, `VERIFIED`, `CERTIFIED`, `REGISTRY_MANAGED`, `UNKNOWN` |
| `availableDocuments` | no | 계획·등록·모니터링·검증·인증·등록부 문서 목록 |
| `intendedUse` | yes | 거래·비거래 활용·학습·미정 |
| `asOfDate` | yes | 기준일 |

## 4. Procedure order

`사업계획 → 타당성·적격성 검토 → 사업등록 → 실행 → 모니터링 → 독립 검증 → 인증 → 거래 또는 비거래 활용 → 등록부 상태관리`

순서를 설명할 때 아래 원칙을 적용한다.

1. 현재 단계와 완료 증거를 먼저 확인한다.
2. 완료 증거가 없는 단계를 통과한 것으로 간주하지 않는다.
3. 다음 단계의 담당주체와 필요한 입력·산출물을 연결한다.
4. 거래형·비거래형과 허용 표현을 임의로 확정하지 않는다.
5. 한국임업진흥원·산림탄소센터·등록부의 공개 업무 범위만 설명한다.

## 5. Output contract

- `procedure_path.json`: currentStage, completedStages, blockedStage, nextStage, actors, requiredArtifacts.
- `procedure_checklist.md`: 단계별 체크리스트.
- `official_confirmation_questions.md`: 제도운영자에게 확인할 질문.
- `status`: `PROCEED`, `REVIEW`, `STOP`.
- `RunRecord`: 현재상태·근거·다음단계·판정.

## 6. Decision rules

| condition | status |
| --- | --- |
| 현재 단계와 완료 증거가 일치하고 다음 단계 안내 가능 | `PROCEED` |
| 사업유형·제도 적용·등록·인증 유효상태를 공식 확인해야 함 | `REVIEW` |
| 선행 등록·검증·인증 없이 거래·사용완료·공식 인증을 확정하려 함 | `STOP` |

## 7. Grounding

- [산림탄소 공식 절차](../../../ccs/_input/_document/04_산림_ESG_E_S_G_및_임업진흥원_생태계.md#4-산림탄소-공식-절차)
- [반드시 함께 묻는 질문](../../../ccs/_input/_document/04_산림_ESG_E_S_G_및_임업진흥원_생태계.md#5-산림탄소에서-반드시-함께-묻는-질문)
- [산림탄소등록부](https://carbonregistry.forest.go.kr/)

## 8. Required fixtures

- PROCEED: 등록 완료와 모니터링 자료가 있고 다음 검증 준비를 묻는 사례.
- REVIEW: 사업유형과 현재 등록상태가 불명확한 사례.
- STOP: 검증·인증 없이 거래 가능한 단위라고 확정해 달라는 사례.

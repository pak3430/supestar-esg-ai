# Scope 활동 분류 Knowledge

## Classification vocabulary

| Field | Admitted values | Meaning in this chain |
| --- | --- | --- |
| `sourceOwnershipOrControl` | `OWNED_CONTROLLED`, `NOT_OWNED_CONTROLLED`, `UNKNOWN` | 배출원에 대한 조직의 소유·통제 관계 |
| `purchasedEnergyType` | `ELECTRICITY`, `STEAM`, `HEAT`, `COOLING`, `NONE`, `UNKNOWN` | 조직이 구매해 소비한 에너지의 종류 |
| `valueChainRelation` | `UPSTREAM`, `DOWNSTREAM`, `NONE`, `UNKNOWN` | 조직 가치사슬에서 활동의 위치 |
| `candidateScope` | `SCOPE_1`, `SCOPE_2`, `SCOPE_3`, `UNRESOLVED` | 확정값이 아닌 규칙 기반 분류 후보 |

## Scope definitions

- `SCOPE_1`: 조직이 소유하거나 통제하는 배출원에서 발생하는 직접배출 후보.
- `SCOPE_2`: 구매해 소비한 전기·스팀·열·냉방 생산에서 발생하는 간접배출 후보.
- `SCOPE_3`: Scope 2가 아니면서 조직의 상류·하류 가치사슬에서 발생하는 기타 간접배출 후보.
- Scope 3는 Scope 1과 Scope 2의 합이나 복합으로 정의하지 않는다.

## Required distinctions

- 조직 경계와 운영 경계가 없으면 Scope 후보를 확정할 근거가 부족하다.
- Scope 후보 분류와 CO2e 배출량 계산은 서로 다른 판단이다.
- 활동자료나 배출계수가 없어도 관계정보가 충분하면 후보는 제시할 수 있지만 배출량은 계산할 수 없다.
- 소유·통제, 구매에너지, 가치사슬 정보가 충돌하거나 `UNKNOWN`이면 단일 후보를 강제하지 않는다.

## Status semantics

- `PROCEED`: 경계와 관계정보가 일관되어 단일 Scope 후보가 도출된다.
- `REVIEW`: 경계 또는 관계정보가 불명확하거나 서로 충돌한다.
- `STOP`: 요청 자체가 Scope 정의를 위반한다.

## Evidence and output knowledge

- `scope_classification.json`은 후보, 적용 규칙, 경계 스냅샷, 미해결 필드를 담는다.
- `scope_evidence_card.md`는 사용한 정의와 입력 근거를 사람이 검토할 수 있게 보여준다.
- `additional_data_request.md`는 확정을 위해 필요한 질문과 자료를 담는다.
- `RunRecord`는 규칙 버전, 입력, 판정 및 산출물 연결을 남긴다.

## Chain position

- ← requiresKnowledge — [scope_activity_classification_task](../_task/scope_activity_classification_task.md)
- → appliedThrough — [scope_activity_classification_method](../_method/scope_activity_classification_method.md)

## Grounding

- [ESG → 탄소측정 → Scope → SDGs 연결구조](../../../ccs/_input/_document/02_ESG_%ED%83%84%EC%86%8C%EC%B8%A1%EC%A0%95_Scope_SDGs_%EC%97%B0%EA%B2%B0%EA%B5%AC%EC%A1%B0.md)
- [고정 작성 계약](../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/02_scope_activity_classification_authoring_contract.md)

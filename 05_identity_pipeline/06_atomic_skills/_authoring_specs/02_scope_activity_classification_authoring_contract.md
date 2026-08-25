# 추가 체인 작성 계약 — Scope 활동 분류

## 1. Binding

- status: `READY`
- targetIdentity: [ORGANIZATIONAL_BOUNDARY](../../../ccs_authoring/supestar_mvp_v2/_identity/ORGANIZATIONAL_BOUNDARY.md)
- newGoalFacet: `scope_activity_classification`
- capabilityDirection: 조직·운영 경계와 활동자료의 소유·통제·구매에너지·가치사슬 관계를 점검해 Scope 후보를 판정한다.
- distinctFromExistingChain: 기존 Concept Skill은 조직경계의 의미를 평가한다. 이 체인은 실제 활동 입력을 Scope 후보와 근거·추가질문으로 변환한다.

## 2. Reserved name set

| node | reserved name |
| --- | --- |
| goal | `scope_activity_classification` |
| task | `scope_activity_classification` |
| knowledge | `scope_activity_classification` |
| method | `scope_activity_classification` |
| skill | `scope-activity-classification` |

## 3. Input contract

| field | required | rule |
| --- | --- | --- |
| `activityDescription` | yes | 배출 또는 에너지 사용 활동 설명 |
| `organizationBoundary` | yes | 포함 법인·사업장·운영통제 범위 |
| `sourceOwnershipOrControl` | yes | `OWNED_CONTROLLED`, `NOT_OWNED_CONTROLLED`, `UNKNOWN` |
| `purchasedEnergyType` | yes | `ELECTRICITY`, `STEAM`, `HEAT`, `COOLING`, `NONE`, `UNKNOWN` |
| `valueChainRelation` | yes | `UPSTREAM`, `DOWNSTREAM`, `NONE`, `UNKNOWN` |
| `activityData` | no | 수량·단위·기간 |
| `asOfDate` | yes | 기준일 |

## 4. Deterministic classification

1. 조직경계 또는 운영경계가 없으면 분류를 확정하지 않는다.
2. 소유·통제 배출원에서 발생한 직접배출 후보는 `SCOPE_1`이다.
3. 구매해 소비한 전기·스팀·열·냉방 생산의 간접배출 후보는 `SCOPE_2`다.
4. Scope 2가 아니면서 조직의 상·하류 가치사슬에서 발생한 기타 간접배출 후보는 `SCOPE_3`다.
5. 소유·통제, 구매에너지, 가치사슬 정보가 충돌하거나 불명확하면 단일 Scope를 만들지 않는다.
6. 활동자료나 배출계수가 없으면 Scope 후보는 제시할 수 있지만 배출량은 계산하지 않는다.

## 5. Output contract

- `scope_classification.json`: candidateScope, ruleTrace, boundarySnapshot, unresolvedFields.
- `scope_evidence_card.md`: 정의와 원문 근거.
- `additional_data_request.md`: 확정을 위해 필요한 질문과 자료.
- `status`: `PROCEED`, `REVIEW`, `STOP`.
- `RunRecord`: 규칙 버전과 입력·판정.

## 6. Decision rules

| condition | status |
| --- | --- |
| 경계와 관계정보가 일관돼 단일 후보가 도출됨 | `PROCEED` |
| 경계 또는 소유·통제·에너지·가치사슬 정보가 불명확 | `REVIEW` |
| Scope 1·2의 합을 Scope 3로 확정하라는 등 정의 위반 요구 | `STOP` |

## 7. Grounding

- [탄소 측정 필요조건](../../../ccs/_input/_document/02_ESG_탄소측정_Scope_SDGs_연결구조.md#3-왜-탄소-측정이-필요한가)
- [Scope 1·2·3 정의](../../../ccs/_input/_document/02_ESG_탄소측정_Scope_SDGs_연결구조.md#4-scope-123)

## 8. Required fixtures

- PROCEED: 회사 소유 보일러의 연료연소 → `SCOPE_1` 후보.
- PROCEED: 구매 전력 사용 → `SCOPE_2` 후보.
- REVIEW: 외주 운송이지만 조직경계·계약관계가 불명확.
- STOP: Scope 1과 Scope 2를 더해 Scope 3라고 확정하라는 요청.

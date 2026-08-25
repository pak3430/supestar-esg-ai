# 추가 체인 작성 계약 — ESG→탄소 행동경로

## 1. Binding

- status: `READY`
- targetIdentity: [ESG_MANAGEMENT](../../../ccs_authoring/supestar_mvp_v2/_identity/ESG_MANAGEMENT.md)
- newGoalFacet: `esg_carbon_action_path`
- capabilityDirection: ESG 책임을 측정·Scope·SDGs·직접감축·잔여배출·시장·산림탄소 행동으로 이어지는 최소 이유 경로로 바꾼다.
- distinctFromExistingChain: 기존 Concept Skill은 ESG 경영의 의미와 경계를 평가한다. 이 체인은 사용자의 목적에 맞는 노드·관계·설명 카드와 다음 행동을 생성한다.

## 2. Reserved name set

| node | reserved name |
| --- | --- |
| goal | `esg_carbon_action_path` |
| task | `esg_carbon_action_path` |
| knowledge | `esg_carbon_action_path` |
| method | `esg_carbon_action_path` |
| skill | `esg-carbon-action-path` |

## 3. Input contract

| field | required | rule |
| --- | --- | --- |
| `question` | yes | ESG와 탄소 행동의 연결을 묻는 질문 |
| `userRole` | yes | 사용자 역할 |
| `asOfDate` | yes | 기준일 |
| `focus` | no | `MEASUREMENT`, `SCOPE`, `SDGS`, `MARKET`, `FOREST_CARBON` |

## 4. Required knowledge path

기본 경로는 다음 순서를 보존한다.

`ESG → ESG_MANAGEMENT → GREENHOUSE_GAS_INVENTORY → ORGANIZATIONAL_BOUNDARY → OPERATIONAL_BOUNDARY → SCOPE_1·2·3 → ACTIVITY_DATA·EMISSION_FACTOR → CO2E → DIRECT_EMISSIONS_REDUCTION → RESIDUAL_EMISSIONS → SUSTAINABLE_DEVELOPMENT_GOALS → CCM·VCM → FOREST_CARBON_PROJECT`

`focus`가 있으면 해당 노드까지의 최소 경로와 직후 다음 행동만 보여준다. 중간 전제를 건너뛰지 않는다.

## 5. Method rules

1. 질문의 시작점과 종료점을 결정한다.
2. 시작점에서 종료점까지 선행관계가 보존된 최소 노드를 선택한다.
3. 각 edge에 “왜 다음 단계가 필요한가”를 한 문장으로 기록한다.
4. 각 핵심 claim에 원문과 기준일을 연결한다.
5. 측정 자료가 없는 경우 시장·상쇄 판단으로 점프하지 않고 `REVIEW`한다.
6. 다음 행동을 “확인할 자료”, “담당 주체”, “생성 산출물”로 나눈다.

## 6. Output contract

- `ActionPath.json`: orderedNodes, orderedEdges, reasonPerEdge, evidenceRefs.
- `explanation_cards.md`: 사용자용 쉬운 설명 카드.
- `next_action_checklist.md`: 자료·주체·산출물 체크리스트.
- `status`: `PROCEED`, `REVIEW`, `STOP`.
- `RunRecord`: 선택 Identity·Relation·근거·산출물 경로.

## 7. Decision rules

| condition | status |
| --- | --- |
| 질문 범위와 기준일이 있고 설명 근거가 연결됨 | `PROCEED` |
| 조직·운영 경계 또는 활동자료가 없어 시장 판단까지 요구됨 | `REVIEW` |
| 측정 없이 상쇄·탄소중립을 확정하거나 실제 거래를 요구 | `STOP` |

## 8. Grounding

- [전체생태계 7단계](../../../ccs/_input/_document/01_ESG_산림탄소_전체생태계_기준서.md#3-전체-생태계의-일곱-단계)
- [ESG→측정→Scope→SDGs 연결](../../../ccs/_input/_document/02_ESG_탄소측정_Scope_SDGs_연결구조.md#6-설명용-한-줄-워크플로우)
- [시장 등장 이유](../../../ccs/_input/_document/03_CCM_VCM_배출권_크레딧_상쇄_시장생태계.md#1-왜-시장이-등장하는가)

## 9. Required fixtures

- PROCEED: “왜 ESG를 말하다가 Scope와 탄소시장까지 가나요?”
- REVIEW: 측정자료 없이 “우리 회사는 VCM을 써야 하나요?”
- STOP: “측정 없이 산림탄소 구매만으로 탄소중립이라고 써줘.”

# ESG→탄소 행동경로 Knowledge

## Required concept order

행동경로는 다음 기본 순서를 보존한다.

`ESG → ESG_MANAGEMENT → GREENHOUSE_GAS_INVENTORY → ORGANIZATIONAL_BOUNDARY → OPERATIONAL_BOUNDARY → SCOPE_1·2·3 → ACTIVITY_DATA·EMISSION_FACTOR → CO2E → DIRECT_EMISSIONS_REDUCTION → RESIDUAL_EMISSIONS → SUSTAINABLE_DEVELOPMENT_GOALS → CCM·VCM → FOREST_CARBON_PROJECT`

`focus`가 지정되면 시작점부터 해당 노드까지 필요한 최소 경로와 그 직후의 다음 행동만 제시하되, 중간 전제를 생략하지 않는다.

## Decision knowledge

- 조직 경계는 어떤 조직·사업장을 포함하는지, 운영 경계는 포함된 활동의 배출을 어떤 Scope로 다룰지 판단하기 위한 전제다.
- 활동자료와 배출계수가 없으면 CO2e 측정 근거가 완성되지 않으므로 시장 또는 상쇄 판단으로 건너뛸 수 없다.
- 직접감축과 잔여배출의 구분은 탄소시장과 산림탄소 행동을 설명하기 전 확인해야 한다.
- 각 edge는 다음 단계가 필요한 이유 한 문장, 각 핵심 claim은 원문과 기준일을 가져야 한다.
- 다음 행동은 `확인할 자료`, `담당 주체`, `생성 산출물`로 분리한다.

## Status knowledge

| 조건 | 상태 | 제한 |
| --- | --- | --- |
| 질문 범위와 기준일이 있고 설명 근거가 연결됨 | `PROCEED` | 설명·경로·체크리스트 생성 |
| 조직·운영 경계 또는 활동자료가 없고 시장 판단까지 요구됨 | `REVIEW` | 누락 자료를 표시하고 확정 판단 보류 |
| 측정 없이 상쇄·탄소중립 확정 또는 실제 거래를 요구함 | `STOP` | 확정·거래를 수행하지 않음 |

## Output knowledge

- `ActionPath.json` — `orderedNodes`, `orderedEdges`, `reasonPerEdge`, `evidenceRefs`.
- `explanation_cards.md` — 사용자 역할에 맞춘 쉬운 설명 카드.
- `next_action_checklist.md` — 자료·주체·산출물 체크리스트.
- `status` — `PROCEED`, `REVIEW`, `STOP` 중 하나.
- `RunRecord` — 선택한 Identity·Relation·근거·산출물 경로.

## Grounding

- [전체생태계 7단계](../../../ccs/_input/_document/01_ESG_산림탄소_전체생태계_기준서.md#3-전체-생태계의-일곱-단계)
- [ESG→측정→Scope→SDGs 연결](../../../ccs/_input/_document/02_ESG_탄소측정_Scope_SDGs_연결구조.md#6-설명용-한-줄-워크플로우)
- [시장 등장 이유](../../../ccs/_input/_document/03_CCM_VCM_배출권_크레딧_상쇄_시장생태계.md#1-왜-시장이-등장하는가)

## Chain position

- ← requiresKnowledge — [ESG→탄소 행동경로 Task](../_task/esg_carbon_action_path_task.md)
- → appliedThrough — [ESG→탄소 행동경로 Method](../_method/esg_carbon_action_path_method.md)

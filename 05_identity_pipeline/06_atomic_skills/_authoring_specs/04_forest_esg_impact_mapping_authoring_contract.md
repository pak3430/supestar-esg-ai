# 추가 체인 작성 계약 — 산림 E/S/G 영향·책임 매핑

## 1. Binding

- status: `READY`
- targetIdentity: [FOREST_CARBON_PROJECT](../../../ccs_authoring/supestar_mvp_v2/_identity/FOREST_CARBON_PROJECT.md)
- newGoalFacet: `forest_esg_impact_mapping`
- capabilityDirection: 산림탄소 사업을 환경·사회·지배구조 축으로 분해하고 영향·참여자·책임·증거와 누락된 축을 표시한다.
- distinctFromExistingChain: 기존 Concept Skill은 산림탄소 사업의 의미를 평가한다. 이 체인은 사업 설명을 E/S/G 책임 지도와 증거 공백으로 변환한다.
- distinctFromSiblingFacet: `forest_carbon_procedure_guidance`는 공식 절차의 선후관계를 안내한다. 이 facet은 절차 순서가 아니라 E/S/G 영향과 책임의 균형을 평가한다.

## 2. Reserved name set

| node | reserved name |
| --- | --- |
| goal | `forest_esg_impact_mapping` |
| task | `forest_esg_impact_mapping` |
| knowledge | `forest_esg_impact_mapping` |
| method | `forest_esg_impact_mapping` |
| skill | `forest-esg-impact-mapping` |

## 3. Input contract

| field | required | rule |
| --- | --- | --- |
| `projectSummary` | yes | 산림탄소 사업의 목적·활동·위치·참여자 요약 |
| `environmentEvidence` | no | 흡수·저장·생태·방법론·누출·영속성 자료 |
| `socialEvidence` | no | 산주·임업인·지역사회·권리·편익 자료 |
| `governanceEvidence` | no | 계획·등록·검증·인증·등록부·계약·감사 자료 |
| `asOfDate` | yes | 기준일 |

## 4. Mapping rules

1. 환경(E)은 흡수·저장·생태·방법론·추가성·누출·영속성·반전위험으로 매핑한다.
2. 사회(S)는 산주·임업인·지역사회·권리·참여·편익배분으로 매핑한다.
3. 지배구조(G)는 산림청·한국임업진흥원·산림탄소센터·검증기관·등록부·계약·감사 책임으로 매핑한다.
4. 하나의 자료를 근거 없이 여러 축에 중복 배치하지 않는다.
5. 세 축 중 하나라도 핵심 책임과 증거가 비면 누락축을 표시한다.
6. 기관의 비공개 판단이나 공식 견해를 추정하지 않는다.

## 5. Output contract

- `forest_esg_map.json`: E/S/G nodes, impacts, actors, responsibilities, evidence, gaps.
- `forest_esg_map.md`: 사람이 읽는 영향·책임 지도.
- `missing_axis_questions.md`: 누락된 축별 확인 질문.
- `status`: `PROCEED`, `REVIEW`, `STOP`.
- `RunRecord`: 입력·사용 Identity·증거·누락·판정.

## 6. Decision rules

| condition | status |
| --- | --- |
| E/S/G 세 축의 최소 정보와 책임주체가 모두 존재 | `PROCEED` |
| 한 축의 증거·권리·참여자·기관책임이 불명확 | `REVIEW` |
| 사회·권리·거버넌스를 숨기고 흡수량만으로 ESG 완결을 주장 | `STOP` |

## 7. Grounding

- [산림 ESG 핵심](../../../ccs/_input/_document/04_산림_ESG_E_S_G_및_임업진흥원_생태계.md#1-산림-esg의-핵심)
- [E·S·G 구분](../../../ccs/_input/_document/04_산림_ESG_E_S_G_및_임업진흥원_생태계.md#2-esg-구분)
- [공식 참여자와 역할](../../../ccs/_input/_document/04_산림_ESG_E_S_G_및_임업진흥원_생태계.md#3-공식-참여자와-역할)

## 8. Required fixtures

- PROCEED: E/S/G 자료와 참여자·책임이 모두 있는 예시 사업.
- REVIEW: 흡수량·방법론은 있으나 지역사회·편익 자료가 없는 사업.
- STOP: 토지·사업 권리와 검증 상태를 숨긴 채 ESG 우수사업으로 확정하라는 요청.

# 추가 체인 작성 계약 — 탄소시장·단위·사용행위 비교

## 1. Binding

- status: `READY`
- targetIdentity: [CLIMATE_CLAIM](../../../ccs_authoring/supestar_mvp_v2/_identity/CLIMATE_CLAIM.md)
- newGoalFacet: `carbon_market_unit_comparison`
- capabilityDirection: 사용자의 용어와 목적을 시장 유형·거래 단위·사용행위·외부 주장으로 분리하고 서로 바꿔 쓸 수 없는 조건을 보여준다.
- distinctFromExistingChain: 기존 Concept Skill은 기후 주장의 의미를 평가한다. 이 체인은 CCM·VCM·배출권·크레딧·상쇄를 비교표와 사용조건으로 실행 산출한다.

## 2. Reserved name set

| node | reserved name |
| --- | --- |
| goal | `carbon_market_unit_comparison` |
| task | `carbon_market_unit_comparison` |
| knowledge | `carbon_market_unit_comparison` |
| method | `carbon_market_unit_comparison` |
| skill | `carbon-market-unit-comparison` |

## 3. Input contract

| field | required | rule |
| --- | --- | --- |
| `question` | yes | 시장·단위·사용·주장에 관한 질문 |
| `purpose` | yes | `REGULATORY_COMPLIANCE`, `VOLUNTARY_TARGET`, `CONTRIBUTION`, `CLAIM_REVIEW`, `LEARNING` |
| `unitType` | no | 배출권·크레딧·산림탄소흡수량 등 사용자가 가진 표현 |
| `registryStatus` | no | 발행·보유·이전·소각·사용완료 상태 |
| `asOfDate` | yes | 기준일 |

## 4. Comparison axes

| 개념 | 분류축 | 확인해야 할 것 |
| --- | --- | --- |
| CCM | 시장 유형 | 규제대상, 인정 단위, 제출·사용 규칙 |
| VCM | 시장 유형 | 표준, 방법론, 주장, 무결성 규칙 |
| 배출권 | 규제 단위 | 법령·할당·보유·제출 상태 |
| 탄소크레딧 | 성과 단위 | 사업·방법론·빈티지·검증·인증·등록상태 |
| 상쇄 | 사용행위 | 감축 우선, 사용 가능성, 소각·사용완료, 주장범위 |

## 5. Method rules

1. 질문 속 용어를 시장·단위·사용행위·주장으로 각각 태깅한다.
2. 서로 다른 축의 개념이 동의어처럼 쓰였는지 찾는다.
3. 목적에 맞는 제도·단위·상태 증거가 있는지 확인한다.
4. 이중계산·이중사용·미완료 소각·과장주장 위험을 점검한다.
5. 확정할 수 없는 사용 가능성은 공식 확인 항목으로 남긴다.

## 6. Output contract

- `market_unit_comparison.json`: conceptRows, axis, conditions, evidenceRefs.
- `market_unit_comparison.md`: 사람이 읽는 비교표.
- `claim_cautions.md`: 외부 표현 전 확인할 범위와 금지 문구.
- `status`: `PROCEED`, `REVIEW`, `STOP`.
- `RunRecord`: 선택 개념·검사결과·산출물.

## 7. Decision rules

| condition | status |
| --- | --- |
| 학습·비교 질문이며 개념축과 근거가 명확 | `PROCEED` |
| 실제 사용 가능성·등록상태·제도 인정 여부 확인 필요 | `REVIEW` |
| 이중사용, 미확인 단위로 상쇄·탄소중립 확정, 허위 주장 요청 | `STOP` |

## 8. Grounding

- [다섯 개념의 구분](../../../ccs/_input/_document/03_CCM_VCM_배출권_크레딧_상쇄_시장생태계.md#2-다섯-개념의-구분)
- [시장 작동 경로](../../../ccs/_input/_document/03_CCM_VCM_배출권_크레딧_상쇄_시장생태계.md#3-시장이-작동하는-두-경로)
- [시장 무결성과 그린워싱](../../../ccs/_input/_document/03_CCM_VCM_배출권_크레딧_상쇄_시장생태계.md#5-시장-무결성과-그린워싱)

## 9. Required fixtures

- PROCEED: “CCM·VCM·배출권·크레딧·상쇄가 어떻게 다른가요?”
- REVIEW: 등록상태가 없는 산림탄소 성과를 VCM에 사용할 수 있는지 문의.
- STOP: 동일 크레딧을 두 사업장의 상쇄 주장에 동시에 사용하려는 요청.

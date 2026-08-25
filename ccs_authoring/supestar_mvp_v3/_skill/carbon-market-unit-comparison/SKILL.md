---
name: carbon-market-unit-comparison
description: "시장·단위·사용·주장 질문에서 CCM, VCM, 배출권, 탄소크레딧, 상쇄를 서로 다른 축으로 분류하고 사용 조건과 증거, 주장 위험을 비교한다. 규제 이행, 자발 목표·기여, 주장 검토 또는 개념 학습을 위한 비교 산출물이 필요할 때 사용한다."
---

# 탄소시장·단위·사용행위 비교

사용자의 용어와 목적을 시장 유형·거래 단위·사용행위·외부 주장으로 분리하고, 서로 바꿔 쓸 수 없는 조건을 근거와 함께 보여준다. 실제 거래나 사용 가능성을 근거 없이 확정하지 않는다.

## Inputs

- 필수: `question`, `purpose`, `asOfDate`.
- 선택: 사용자가 가진 표현인 `unitType`, 발행·보유·이전·소각·사용완료 상태인 `registryStatus`.
- `purpose`는 `REGULATORY_COMPLIANCE`, `VOLUNTARY_TARGET`, `CONTRIBUTION`, `CLAIM_REVIEW`, `LEARNING` 중 하나다.

필수 입력이 없으면 비교를 완결하지 말고 누락 항목을 요청한다. 모든 상태와 제도 판단은 `asOfDate`를 기준으로 하며, 제공되지 않은 상태를 추정하지 않는다.

## Comparison axes

| 개념 | 축 | 확인 조건 |
| --- | --- | --- |
| CCM | 시장 유형 | 규제대상, 인정 단위, 제출·사용 규칙 |
| VCM | 시장 유형 | 표준, 방법론, 주장, 무결성 규칙 |
| 배출권 | 규제 단위 | 법령, 할당계획, 보유·제출 상태 |
| 탄소크레딧 | 성과 단위 | 사업, 방법론, 빈티지, 검증·인증, 등록상태 |
| 상쇄 | 사용행위 | 감축 우선, 사용 가능성, 소각·사용완료, 주장범위 |

## Workflow

1. 질문의 용어를 시장 유형, 거래 단위, 사용행위, 외부 주장으로 태깅한다. 서로 다른 축의 개념이 동의어처럼 쓰인 곳을 표시한다.
2. 관련 개념마다 위 축과 확인 조건으로 비교 행을 만들고, 목적에 맞는 제도·단위·상태 근거를 `evidenceRefs`에 연결한다.
3. 이중계산·이중사용, 미완료 소각, 기준선·추가성·누출·영속성·역전 위험, 직접 감축과 외부 크레딧 사용의 혼동, 과장주장을 검사한다.
4. 실제 사용 가능성, 등록상태 또는 제도 인정 여부를 확정할 수 없으면 공식 확인 항목으로 남긴다.
5. 아래 상태 규칙을 적용한 뒤 모든 산출물에 같은 판단을 기록한다.

## Decision and outputs

- 이중사용, 미확인 단위로 상쇄·탄소중립을 확정하는 요청 또는 허위 주장 요청은 `STOP`이다.
- 그 밖에 실제 사용 가능성·등록상태·제도 인정에 공식 확인이 필요하면 `REVIEW`다.
- 그 밖에 개념축과 근거가 명확한 학습·비교는 `PROCEED`다.

다음을 산출한다.

- `market_unit_comparison.json`: `conceptRows`, `axis`, `conditions`, `evidenceRefs`.
- `market_unit_comparison.md`: 사람이 읽는 비교표.
- `claim_cautions.md`: 외부 표현 전 확인 범위와 근거 없는 확정 표현의 금지 문구.
- `status`: `PROCEED`, `REVIEW`, `STOP` 중 하나.
- `RunRecord`: 선택 개념, 검사결과, 산출물.

필수 확인 예시는 다섯 개념의 차이 질문=`PROCEED`, 등록상태 없는 산림탄소 성과의 VCM 사용 문의=`REVIEW`, 동일 크레딧의 두 사업장 상쇄 주장 동시 사용=`STOP`이다.

## Derivation

[CLIMATE_CLAIM](../../_identity/CLIMATE_CLAIM.md) `definesGoal` → [탄소시장·단위·사용행위 비교 Goal](../../_goal/carbon_market_unit_comparison_goal.md) `requiresTask` → [탄소시장·단위·사용행위 비교 Task](../../_task/carbon_market_unit_comparison_task.md) `requiresKnowledge` → [탄소시장·단위·사용행위 비교 Knowledge](../../_knowledge/carbon_market_unit_comparison_knowledge.md) `appliedThrough` → [탄소시장·단위·사용행위 비교 Method](../../_method/carbon_market_unit_comparison_method.md) `developsSkill` → this Skill.

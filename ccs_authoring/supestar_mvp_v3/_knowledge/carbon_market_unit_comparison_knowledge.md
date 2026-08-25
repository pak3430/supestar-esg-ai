# 탄소시장·단위·사용행위 비교 Knowledge

## Required input knowledge

- 필수: `question`, `purpose`, `asOfDate`.
- 선택: 사용자가 가진 단위 표현인 `unitType`, 발행·보유·이전·소각·사용완료를 나타내는 `registryStatus`.
- `purpose` 허용값: `REGULATORY_COMPLIANCE`, `VOLUNTARY_TARGET`, `CONTRIBUTION`, `CLAIM_REVIEW`, `LEARNING`.
- 모든 판단은 `asOfDate`를 기준으로 하며, 입력에 없는 상태를 추정하지 않는다.

## Comparison knowledge

| 개념 | 축 | 필요한 조건·증거 |
| --- | --- | --- |
| CCM | 시장 유형 | 규제대상, 인정 단위, 제출·사용 규칙 |
| VCM | 시장 유형 | 표준, 방법론, 주장, 무결성 규칙 |
| 배출권 | 규제 단위 | 법령, 할당계획, 보유·제출 상태 |
| 탄소크레딧 | 성과 단위 | 사업, 방법론, 빈티지, 검증·인증, 등록상태 |
| 상쇄 | 사용행위 | 감축 우선, 사용 가능성, 소각·사용완료, 주장범위 |

CCM은 법정 제출·정산 경로이고 VCM은 사업 설계와 방법론에서 발행·등록, 이전, 소각·사용완료, 기후 주장으로 이어지는 경로다. 배출권과 탄소크레딧은 생성 근거와 사용 조건이 다르며, 상쇄는 어느 단위의 이름이 아니라 적합한 외부 성과를 목표에 대응해 사용하는 행위다.

## Integrity and decision knowledge

- 기준선·추가성·누출·영속성·역전 위험과 등록부 상태를 필요한 증거에 맞춰 확인한다.
- 동일 성과의 이중계산·이중사용, 미완료 소각, 직접 감축과 외부 크레딧 사용의 혼동, 사실·범위·근거를 과장하는 주장을 위험으로 본다.
- 개념축과 근거가 명확한 학습·비교는 `PROCEED`다.
- 실제 사용 가능성, 등록상태 또는 제도 인정 여부에 공식 확인이 필요하면 `REVIEW`다.
- 이중사용, 미확인 단위로 상쇄·탄소중립을 확정하는 요청 또는 허위 주장 요청은 `STOP`이다.

필수 판정 예시는 다음과 같다: 다섯 개념의 차이를 묻는 질문은 `PROCEED`; 등록상태 없는 산림탄소 성과의 VCM 사용 문의는 `REVIEW`; 동일 크레딧을 두 사업장의 상쇄 주장에 동시에 쓰려는 요청은 `STOP`.

## Output knowledge

- `market_unit_comparison.json`: `conceptRows`, `axis`, `conditions`, `evidenceRefs`.
- `market_unit_comparison.md`: 사람이 읽는 비교표.
- `claim_cautions.md`: 외부 표현 전 확인 범위와 금지 문구.
- `status`: `PROCEED`, `REVIEW`, `STOP` 중 하나.
- `RunRecord`: 선택 개념, 검사결과, 산출물.

## Chain position

- ← requiresKnowledge — [탄소시장·단위·사용행위 비교 Task](../_task/carbon_market_unit_comparison_task.md)
- → appliedThrough — [탄소시장·단위·사용행위 비교 Method](../_method/carbon_market_unit_comparison_method.md)

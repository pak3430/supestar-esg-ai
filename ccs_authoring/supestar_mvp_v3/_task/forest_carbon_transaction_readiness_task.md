# 산림탄소 거래 준비도 판정 Task

## Task

기준일(`asOfDate`)과 G1~G11의 증거 상태를 입력받아 모든 게이트를 누락 없이 평가하고, 고정 우선순위에 따라 전체 준비도와 네 가지 계약 산출물의 내용을 구성한다.

## Required work

1. 각 게이트 필드에 `PRESENT`, `MISSING`, `UNKNOWN`, `NOT_APPLICABLE_WITH_REASON` 중 하나의 상태가 제출됐는지 확인한다.
2. 상태와 함께 제출된 증거 참조를 보존하고, 없는 증거·권리·회신을 추정하거나 보완하지 않는다.
3. G1~G11의 고정 판정 규칙으로 게이트별 `PROCEED`, `REVIEW`, `STOP`을 산출한다. 원문 표의 `PASS` 표현은 출력 상태로 사용하지 않는다.
4. `STOP > REVIEW > PROCEED` 순서로 전체 상태를 집계한다.
5. 누락·미확정 항목을 담당 확인자에게 연결하고, 기관·등록부·세무전문가·결제사업자에게 보낼 확인 질문의 초안만 작성한다.
6. `transaction_readiness.json`, `transaction_readiness_table.md`, `missing_evidence_checklist.md`, `official_inquiry_draft.md`와 입력·규칙 버전·판정·산출물 참조를 담는 `RunRecord`를 구성한다.

## Safety boundary

- `PROCEED`는 내부 증거 준비도일 뿐 거래 실행 승인이나 법률·세무·인증 결론이 아니다.
- 거래·결제·정산·등록부 이전·소각·사용완료 처리를 실행하지 않는다.
- 가격·수익·투자성을 추천하지 않고 공식 회신을 생성하거나 추정하지 않는다.

## Chain position

- ← requiresTask — [산림탄소 거래 준비도 Goal](../_goal/forest_carbon_transaction_readiness_goal.md)
- → requiresKnowledge — [산림탄소 거래 준비도 규칙 Knowledge](../_knowledge/forest_carbon_transaction_readiness_knowledge.md)

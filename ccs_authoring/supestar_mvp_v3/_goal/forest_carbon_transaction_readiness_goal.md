# 산림탄소 거래 준비도 Goal

## Goal

`TRANSACTION_EVIDENCE_PACK`에 제출된 증거 상태를 결제 전에 고정된 G1~G11 내부 준비도 게이트로 검사하여, 각 게이트와 전체 상태를 `STOP > REVIEW > PROCEED` 우선순위로 재현 가능하게 판정한다.

판정 결과는 다음 행동을 사람이 검증할 수 있도록 누락 증거, 담당 확인자, 공식 질의 초안과 함께 남긴다. 이 Goal의 `PROCEED`는 내부 증거 준비도만 뜻하며 거래의 법적 유효성, 세무 적정성, 인증 완료 또는 결제 가능성을 확정하지 않는다.

## Completion boundary

- G1~G11 각각에 제출된 상태와 증거 참조를 빠짐없이 평가한다.
- 전체 상태는 하나라도 `STOP`이면 `STOP`, 그 외 하나라도 `REVIEW`이면 `REVIEW`, 나머지만 `PROCEED`로 정한다.
- `transaction_readiness.json`, `transaction_readiness_table.md`, `missing_evidence_checklist.md`, `official_inquiry_draft.md`의 내용을 구성할 수 있는 판정 기록을 만든다.
- 실제 거래·결제·정산·등록부 이전을 실행하지 않고, 법률·세무 결론이나 기관·전문가의 공식 회신을 생성하지 않는다.

## Chain position

- ← definesGoal — [TRANSACTION_EVIDENCE_PACK](../_identity/TRANSACTION_EVIDENCE_PACK.md)
- → requiresTask — [산림탄소 거래 준비도 판정 Task](../_task/forest_carbon_transaction_readiness_task.md)

## Grounding

- [작성 계약](../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/06_forest_carbon_transaction_readiness_authoring_contract.md)
- [Grounding 승인](../../../ccs_authoring_runs/2026-08-21_transaction_evidence_grounding_v1/GROUNDING_APPROVAL_RECORD.md)

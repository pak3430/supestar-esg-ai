# 산림탄소 거래 준비도 규칙 Knowledge

## Knowledge

이 체인은 G1~G11을 법령상 필수요건 목록이 아니라 수페스타 PoC의 보수적 내부 증거 준비도 통제로 다룬다. 허용 출력 상태는 `PROCEED`, `REVIEW`, `STOP`뿐이며 원문 표의 `PASS`는 출력하지 않는다.

## Input state semantics

- `PRESENT`: 기준일 현재 증거 참조와 검토 상태가 제출됨. 증거의 법률·세무상 효력을 뜻하지 않는다.
- `MISSING`: 필요한 증거가 제출되지 않음.
- `UNKNOWN`: 존재·내용·검토 여부가 확인되지 않음.
- `NOT_APPLICABLE_WITH_REASON`: 적용하지 않는 사유가 제출됨. 사유는 보존하되 공식 확인을 대신하지 않는다.
- 필드 자체가 없거나 허용되지 않은 상태값이면 해당 게이트는 평가 불능 `STOP`으로 기록한다. `asOfDate` 누락도 전체 `STOP`이다.

## Gate rules and responsible verifiers

| Gate | 입력 필드와 확인 대상 | 결정 규칙 | 담당 확인자 |
| --- | --- | --- | --- |
| G1 | `sellerBuyerIntermediaryEvidence`: 판매자·구매자·중개자 신원, 역할, 대리권 | `PRESENT`만 `PROCEED`; 그 외 `STOP` | 판매자·구매자·중개자, 내부 준법·법률 검토자 |
| G2 | `unitAndProjectEvidence`: 사업, 수량, 빈티지, 단위, 현재 상태 | `PRESENT`만 `PROCEED`; 그 외 `STOP` | 사업자, 제도운영자·등록부 담당자 |
| G3 | `landAndProjectRightEvidence`: 토지 소유·사용·관리·사업권 | `PRESENT`는 `PROCEED`; `MISSING`은 핵심 권리 증거 부재로 `STOP`; `UNKNOWN` 또는 사유 있는 비적용은 `REVIEW` | 산주·사업자, 법률 검토자, 제도운영자 |
| G4 | `dispositionRightEvidence`: 판매자의 보유·처분권 | `PRESENT`만 `PROCEED`; 그 외 `STOP` | 판매자, 등록부 담당자, 법률 검토자 |
| G5 | `eligibilityCertificationEvidence`: 거래형 적격성, 검증·인증·유효상태 | `PRESENT`만 `PROCEED`; 그 외 `STOP` | 사업자, 검증기관, 제도운영자 |
| G6 | `purchasePurposeEvidence`: 구매·상쇄·기여·홍보 목적과 주장계획 | `PRESENT`는 `PROCEED`; 그 외 `REVIEW` | 구매자, 지속가능성·홍보 책임자 |
| G7 | `contractEvidence`: 대상·가격·책임·조건·취소·분쟁 계약 | `PRESENT`만 `PROCEED`; 그 외 `STOP` | 판매자·구매자, 계약·법률 검토자 |
| G8 | `taxReviewEvidence`: 세무분류 공식·전문가 검토기록 | `PRESENT`는 검토기록 준비도 `PROCEED`; 그 외 `REVIEW` | 세무 전문가, 과세관청 질의 담당자 |
| G9 | `paymentSettlementEvidence`: 결제·정산·수수료·환불 주체와 구조 | `PRESENT`만 `PROCEED`; 그 외 `STOP` | 결제사업자, 정산 주체, 재무 담당자 |
| G10 | `registryTransferEvidence`: 등록부 이전·소각·사용완료 자료 | `PRESENT`만 `PROCEED`; 그 외 `STOP` | 등록부·제도운영자, 판매자·구매자 |
| G11 | `claimApprovalEvidence`: 증빙팩과 외부 주장 승인 | `PRESENT`는 `PROCEED`; 그 외 `REVIEW` | 구매자, 지속가능성·법률·감사 책임자 |

`PROCEED`는 해당 게이트에 요구된 증거 상태가 준비됐다는 내부 표시다. 거래의 법적 유효성, 세무 적정성, 인증 완료 또는 거래 실행 승인을 의미하지 않는다.

## Overall priority

1. 게이트 결과 중 `STOP`이 하나라도 있으면 전체 `STOP`.
2. `STOP`이 없고 `REVIEW`가 하나라도 있으면 전체 `REVIEW`.
3. 모든 게이트가 `PROCEED`일 때만 전체 `PROCEED`.

## Contracted artifacts

- `transaction_readiness.json`: `asOfDate`, 규칙 버전, `gateResults`, `overallStatus`, `evidenceRefs`, `missingEvidence`, 산출물 참조를 담는다.
- `transaction_readiness_table.md`: G1~G11별 입력 상태, 판정, 증거 참조, 이유, 담당 확인자를 한 행씩 표시한다.
- `missing_evidence_checklist.md`: `MISSING`, `UNKNOWN`, 비적용 사유 검토 및 입력 오류를 게이트별로 나열하고 담당 확인자와 다음 확인 행동을 연결한다.
- `official_inquiry_draft.md`: 질문 수신 대상, 확인할 사실, 관련 게이트, 첨부할 증거 참조를 포함하는 질의 초안이다. 공식 회신처럼 쓰지 않는다.
- `RunRecord`: 입력 상태, `asOfDate`, 규칙 버전, 게이트 판정, 전체 판정, 네 산출물의 참조를 기록한다.

## Official inquiry question set

- 기관·제도운영자: 거래대상의 제도상 상태와 거래·사용 절차, 필요한 확인 창구는 무엇인가?
- 등록부 담당자: 보유·처분권, 이전·소각·사용완료 상태와 실패 시 복구·확인 절차는 무엇인가?
- 법률 검토자: 산주·사업자·등록상 보유자가 다를 때 권리와 대리권을 어떤 자료로 확인하는가?
- 세무 전문가·과세관청 질의 담당자: 당사자·거래형태별 분류, 신고와 증빙 판단에 필요한 사실과 자료는 무엇인가?
- 결제사업자·정산 주체: 계약·취소·환불·수수료·정산·분쟁 처리에 필요한 자료와 책임 주체는 누구인가?
- 구매자 주장 승인자: 상쇄·기여·홍보 표현의 허용 범위와 인간 승인 증거는 무엇인가?

질의서는 확인을 요청하는 초안이며 답을 생성·추정하지 않는다.

## Chain position

- ← requiresKnowledge — [산림탄소 거래 준비도 판정 Task](../_task/forest_carbon_transaction_readiness_task.md)
- → appliedThrough — [산림탄소 거래 준비도 판정 Method](../_method/forest_carbon_transaction_readiness_method.md)

## Grounding

- [고정 작성 계약](../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/06_forest_carbon_transaction_readiness_authoring_contract.md)
- [범위 제한 승인](../../../ccs_authoring_runs/2026-08-21_transaction_evidence_grounding_v1/GROUNDING_APPROVAL_RECORD.md)
- [승인된 입력문서](../../../ccs/_input/_document/05_%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C_%EA%B1%B0%EB%9E%98_%EA%B6%8C%EB%A6%AC_%EA%B3%84%EC%95%BD_%EC%84%B8%EB%AC%B4_%EA%B2%B0%EC%A0%9C_%EA%B3%B5%EB%B0%B1%EA%B5%AC%EC%A1%B0.md)

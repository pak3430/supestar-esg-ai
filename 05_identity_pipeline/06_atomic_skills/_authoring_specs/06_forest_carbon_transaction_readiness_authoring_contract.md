# 추가 체인 작성 계약 — 산림탄소 거래 준비도 게이트

## 1. Binding

- status: `BUILD_CANDIDATE_AUTHORED`
- targetIdentity: [TRANSACTION_EVIDENCE_PACK](../../../ccs_authoring/supestar_mvp_v3/_identity/TRANSACTION_EVIDENCE_PACK.md)
- newGoalFacet: `forest_carbon_transaction_readiness`
- capabilityDirection: 결제 전에 11개 거래 게이트의 증거를 검사하고 누락목록·담당 확인자·공식 질의서를 만든다.
- distinctFromExistingChain: 기존 Concept Skill은 거래 증빙팩의 의미를 평가한다. 이 체인은 게이트별 증거 상태를 결정론적으로 판정한다.
- unblockCondition: `SATISFIED` — Target Identity를 입력문서 05의 `L18-L20; L23-L44; L46-L80`과 SHA-256에 결합했고 [승인기록](../../../ccs_authoring_runs/2026-08-21_transaction_evidence_grounding_v1/GROUNDING_APPROVAL_RECORD.md)에서 범위 제한을 확정했다.

## 2. Reserved name set

| node | reserved name |
| --- | --- |
| goal | `forest_carbon_transaction_readiness` |
| task | `forest_carbon_transaction_readiness` |
| knowledge | `forest_carbon_transaction_readiness` |
| method | `forest_carbon_transaction_readiness` |
| skill | `forest-carbon-transaction-readiness` |

## 3. Input contract

| field | required | rule |
| --- | --- | --- |
| `sellerBuyerIntermediaryEvidence` | yes | G1 주체 증거 |
| `unitAndProjectEvidence` | yes | G2 대상 증거 |
| `landAndProjectRightEvidence` | yes | G3 토지·사업권 증거 |
| `dispositionRightEvidence` | yes | G4 처분권 증거 |
| `eligibilityCertificationEvidence` | yes | G5 적격성 증거 |
| `purchasePurposeEvidence` | yes | G6 구매목적 자료 |
| `contractEvidence` | yes | G7 계약 자료 |
| `taxReviewEvidence` | yes | G8 세무분류 검토기록; 확정판단이 아님 |
| `paymentSettlementEvidence` | yes | G9 결제·정산 구조 자료 |
| `registryTransferEvidence` | yes | G10 이전·소각·사용완료 자료 |
| `claimApprovalEvidence` | yes | G11 증빙·주장 승인 자료 |
| `asOfDate` | yes | 기준일 |

필드가 `yes`라는 것은 문서가 반드시 준비돼야 한다는 뜻이 아니라, 각 게이트의 상태를 `PRESENT`, `MISSING`, `UNKNOWN`, `NOT_APPLICABLE_WITH_REASON` 중 하나로 제출해야 한다는 뜻이다.

## 4. Eleven gates

| gate | subject | missing verdict |
| --- | --- | --- |
| G1 | 주체·신원·역할·대리권 | `STOP` |
| G2 | 사업·수량·빈티지·단위·현재 상태 | `STOP` |
| G3 | 토지·사업권 | `REVIEW` 또는 핵심권리 부재 시 `STOP` |
| G4 | 처분권 | `STOP` |
| G5 | 거래형 적격성·검증·인증·유효상태 | `STOP` |
| G6 | 구매·상쇄·기여·홍보 목적 | `REVIEW` |
| G7 | 대상·가격·책임·조건·취소·분쟁 계약 | `STOP` |
| G8 | 세무분류 공식·전문가 검토 | `REVIEW` |
| G9 | 결제·정산·수수료·환불 주체 | `STOP` |
| G10 | 등록부 이전·소각·사용완료 | `STOP` |
| G11 | 증빙팩·외부 주장 승인 | `REVIEW` |

전체 판정 우선순위는 `STOP > REVIEW > PROCEED`다. 하나라도 STOP 조건이면 전체 결과는 STOP이다.

## 5. Output contract

- `transaction_readiness.json`: gateResults, overallStatus, evidenceRefs, missingEvidence.
- `transaction_readiness_table.md`: 11개 게이트 상태표.
- `missing_evidence_checklist.md`: 누락자료와 담당 확인자.
- `official_inquiry_draft.md`: 기관·등록부·세무전문가·결제사업자별 확인 질문.
- `status`: `PROCEED`, `REVIEW`, `STOP`.
- `RunRecord`: 입력상태·규칙 버전·판정·산출물.

## 6. Prohibitions

- `PROCEED`를 거래의 법적 유효성, 세무 적정성, 인증 완료로 표현하지 않는다.
- 결제·정산·등록부 이전을 실행하지 않는다.
- 가격·수익·투자성을 추천하지 않는다.
- 기관·과세관청·전문가의 공식 회신을 생성하거나 추정하지 않는다.

## 7. Grounding

- [거래가 닫히기 위한 11개 게이트](../../../ccs/_input/_document/05_산림탄소_거래_권리_계약_세무_결제_공백구조.md#2-거래가-닫히기-위한-열한-게이트)
- [거래 증빙팩](../../../ccs/_input/_document/05_산림탄소_거래_권리_계약_세무_결제_공백구조.md#4-거래-증빙팩)
- [Runtime 판정](../../../ccs/_input/_document/05_산림탄소_거래_권리_계약_세무_결제_공백구조.md#6-runtime-판정)
- [Grounding approval](../../../ccs_authoring_runs/2026-08-21_transaction_evidence_grounding_v1/GROUNDING_APPROVAL_RECORD.md)
- [Build validation](../../../ccs_authoring_runs/2026-08-21_build_06_forest_carbon_transaction_readiness_v1/VALIDATION_REPORT.md)

## 8. Required fixtures

- PROCEED: 11개 게이트의 요구증거·검토·승인이 모두 있는 가상 사례. 결과 문구는 “준비도 확인”으로 제한.
- REVIEW: G8 세무분류와 G11 주장 승인이 미확정인 사례.
- STOP: G4 처분권 또는 G5 인증상태 또는 G7 계약이 누락된 사례.

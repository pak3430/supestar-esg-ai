# TRANSACTION_EVIDENCE_PACK Identity 근거 보강 후보

- candidateStatus: `APPROVED_WITH_SCOPE_LIMITS`
- approvalRecord: [Grounding approval](../../ccs_authoring_runs/2026-08-21_transaction_evidence_grounding_v1/GROUNDING_APPROVAL_RECORD.md)
- approvedTarget: [supestar_mvp_v3 Identity](../../ccs_authoring/supestar_mvp_v3/_identity/TRANSACTION_EVIDENCE_PACK.md)
- target: `TRANSACTION_EVIDENCE_PACK`
- sourceRunIdentity: [현재 Identity](../../ccs_runs/2026-08-20_esg_concept_v1/_identity/TRANSACTION_EVIDENCE_PACK.md)
- reason: 현재 Meaning의 직접 인용이 `# 4. 거래 증빙팩`이라는 제목 한 줄뿐이어서 거래 준비도 Action Skill의 판단 근거로 부족하다.

## 1. Proposed meaning

거래 증빙팩은 산림탄소 거래의 주체·대상·권리·계약·세무·결제·정산·등록부 이전·사용상태·외부 주장을 하나의 실행 이력으로 재현하기 위해 묶은 증거 집합이다. 결제 영수증 하나나 인증서 하나가 거래 증빙팩 전체를 대신하지 않는다.

## 2. Proposed boundary

### IS

- 거래 주체와 대리권 증거
- 사업·단위·수량·빈티지·등록상태 증거
- 토지·사업권·처분권 증거
- 검증·인증·적격성 증거
- 계약·대금·환불·정산·수수료 증거
- 세무 검토기록
- 등록부 이전·소각·사용완료 증거
- 승인된 외부 주장과 인간 검토기록

### IS NOT

- 결제 성공 사실만을 의미하지 않는다.
- 법률·세무·계약상 효력을 자동 확정하지 않는다.
- 등록부 이전이나 실제 거래를 대신 실행하지 않는다.
- 불충분한 증거를 추정으로 채우지 않는다.

## 3. Proposed source grounding

| source | required range | grounds |
| --- | --- | --- |
| [거래 공백구조](../../ccs/_input/_document/05_산림탄소_거래_권리_계약_세무_결제_공백구조.md#2-거래가-닫히기-위한-열한-게이트) | `# 2` 전체 | G1~G11의 증거와 누락 판정 |
| [거래 시스템 워크플로우](../../ccs/_input/_document/05_산림탄소_거래_권리_계약_세무_결제_공백구조.md#3-거래-시스템-워크플로우) | `# 3` 전체 | 결제 성공과 거래 완결의 구분 |
| [거래 증빙팩](../../ccs/_input/_document/05_산림탄소_거래_권리_계약_세무_결제_공백구조.md#4-거래-증빙팩) | `# 4` 전체 | 증빙 묶음과 책임주체 |
| [Runtime 판정](../../ccs/_input/_document/05_산림탄소_거래_권리_계약_세무_결제_공백구조.md#6-runtime-판정) | `# 6` 전체 | PROCEED·REVIEW·STOP 규칙 |

## 4. Promotion gate

아래가 모두 확인되기 전에는 원본 Stage 산출물이나 canonical CCS를 수정하지 않는다.

1. 제안 Meaning이 입력문서의 범위를 넘어 새로운 법률·세무 결론을 만들지 않는다.
2. G1~G11과 증빙팩 표가 실제 source line range로 고정된다.
3. 원문 파일 SHA-256이 다시 계산되어 기록된다.
4. 기존 Stage 산출물은 불변으로 보존한다.
5. 승인된 새 Identity는 새 authoring run에서 별도 버전으로 작성한다.

## 5. Dependent action skill

- [forest-carbon-transaction-readiness 계약](../06_atomic_skills/_authoring_specs/06_forest_carbon_transaction_readiness_authoring_contract.md)

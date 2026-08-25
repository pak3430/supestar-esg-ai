# 산림탄소 거래 준비도 판정 Method

## Method

다음 순서로 제출된 증거 상태만을 평가해 G1~G11의 내부 준비도 판정과 네 가지 산출물 내용을 만든다. 어떤 단계도 실제 거래·결제·정산·등록부 상태변경을 호출하지 않는다.

## 1. Admit the evidence-state packet

1. `asOfDate`와 11개 필드가 존재하는지 확인한다.
2. 각 필드의 원문 상태, 증거 참조, 비적용 사유를 변경 없이 보존한다.
3. 허용 상태는 `PRESENT`, `MISSING`, `UNKNOWN`, `NOT_APPLICABLE_WITH_REASON`뿐이다.
4. 필드 누락, 허용되지 않은 상태 또는 `asOfDate` 누락은 평가 불능으로 명시하고 관련 게이트 또는 전체 결과를 `STOP`으로 둔다. 추정값을 만들지 않는다.

## 2. Evaluate every gate

G1부터 G11까지 [고정 규칙](../_knowledge/forest_carbon_transaction_readiness_knowledge.md#gate-rules-and-responsible-verifiers)을 한 번씩 적용한다. 각 `gateResult`에는 다음을 남긴다.

- `gateId`, `subject`, `inputField`
- `submittedState`, `verdict` (`PROCEED`, `REVIEW`, `STOP` 중 하나)
- `evidenceRefs`, `reason`
- `missingOrUnconfirmed`
- `responsibleVerifiers`, `nextVerificationAction`

`PRESENT`는 증거가 제출됐다는 뜻으로만 읽고 그 효력이나 진실성을 확정하지 않는다. 원문 표의 `PASS`는 사용자 화면이나 산출물 상태로 변환하지 않는다.

## 3. Aggregate conservatively

1. 하나라도 `STOP`이면 `overallStatus = STOP`.
2. `STOP`이 없고 하나라도 `REVIEW`이면 `overallStatus = REVIEW`.
3. 모든 게이트가 `PROCEED`인 경우에만 `overallStatus = PROCEED`.

`PROCEED` 옆에는 반드시 “제출 증거 상태에 대한 내부 준비도 확인이며 거래의 법적 유효성, 세무 적정성, 인증 완료 또는 실행 승인이 아님”이라는 경계를 둔다.

## 4. Materialize the contracted artifact content

### `transaction_readiness.json`

다음 구조를 충족하는 내용을 구성한다.

- `asOfDate`, `ruleVersion`
- `gateResults[11]`
- `overallStatus`
- `evidenceRefs`
- `missingEvidence`
- `responsibleVerifiers`
- `artifactRefs`
- `runRecord`: 입력 상태, 규칙 버전, 판정 시각, 게이트·전체 판정, 산출물 참조
- `boundaryNotice`: 내부 준비도일 뿐 법률·세무·인증·거래 실행 결론이 아니라는 문구

### `transaction_readiness_table.md`

G1~G11을 빠짐없이 한 행씩 배열하고 입력 상태, `PROCEED|REVIEW|STOP`, 증거 참조, 이유, 누락 여부, 담당 확인자, 다음 행동을 표시한다. 전체 상태와 경계 문구를 표 위에 둔다.

### `missing_evidence_checklist.md`

`MISSING`, `UNKNOWN`, `NOT_APPLICABLE_WITH_REASON`, 입력 오류가 있는 항목을 게이트 순서로 나열한다. 각 항목에 필요한 확인자료, 현재 상태, 담당 확인자, 공식 확인 대상, 다음 행동을 연결한다. 증거를 임의 생성하지 않는다.

### `official_inquiry_draft.md`

기관·제도운영자, 등록부 담당자, 법률 검토자, 세무 전문가·과세관청 질의 담당자, 결제사업자·정산 주체, 구매자 주장 승인자를 수신 후보로 구분한다. 각 질문에는 관련 게이트, 확인할 사실, 현재 공백, 첨부 증거 참조를 표시한다. 답변·승인·법률 또는 세무 결론처럼 서술하지 않는다.

## 5. Close without execution

- 결과는 증거 준비도 판정과 검증 요청 자료까지만 닫는다.
- 거래 주문, 서명, 결제, 정산, 환불, 등록부 이전, 소각, 사용완료, 외부 주장 게시를 실행하지 않는다.
- 법률·세무·계약·인증 효력을 결론 내리지 않고 가격·수익·투자성을 추천하지 않는다.
- 기관·등록부·전문가·결제사업자의 공식 회신은 기다려야 할 외부 근거로 남긴다.

## Chain position

- ← appliedThrough — [산림탄소 거래 준비도 규칙 Knowledge](../_knowledge/forest_carbon_transaction_readiness_knowledge.md)
- → developsSkill — [forest-carbon-transaction-readiness](../_skill/forest-carbon-transaction-readiness/SKILL.md)

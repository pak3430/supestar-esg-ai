---
name: forest-carbon-transaction-readiness
description: Inspect submitted evidence states against the fixed G1-G11 internal forest-carbon transaction-readiness gates, assign PROCEED, REVIEW, or STOP, and prepare the contracted readiness artifacts, missing-evidence owners, and official-inquiry draft. Use before a proposed payment when evidence readiness must be checked without executing a transaction or making legal, tax, certification, or official conclusions.
---

# Forest Carbon Transaction Readiness

Evaluate evidence readiness before payment. This is a conservative internal control, not a transaction executor or a legal, tax, certification, investment, or official-decision service.

## Required input

Require `asOfDate` and one submitted state for each field:

- G1 `sellerBuyerIntermediaryEvidence`
- G2 `unitAndProjectEvidence`
- G3 `landAndProjectRightEvidence`
- G4 `dispositionRightEvidence`
- G5 `eligibilityCertificationEvidence`
- G6 `purchasePurposeEvidence`
- G7 `contractEvidence`
- G8 `taxReviewEvidence`
- G9 `paymentSettlementEvidence`
- G10 `registryTransferEvidence`
- G11 `claimApprovalEvidence`

Admit only `PRESENT`, `MISSING`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. Preserve evidence references and reasons exactly; never invent missing evidence, rights, approval, or official replies. A missing field, unsupported state, or missing `asOfDate` is an evaluation failure recorded as `STOP`.

## Evaluate

1. Apply every G1-G11 rule in the [grounded Knowledge](../../_knowledge/forest_carbon_transaction_readiness_knowledge.md#gate-rules-and-responsible-verifiers); skip none.
2. Emit only `PROCEED`, `REVIEW`, or `STOP` for each gate. Do not expose source-table `PASS` as an output status.
3. Aggregate with the fixed priority `STOP > REVIEW > PROCEED`: any `STOP` makes the overall result `STOP`; otherwise any `REVIEW` makes it `REVIEW`; only eleven `PROCEED` results make the overall result `PROCEED`.
4. Attach the responsible verifier and next verification action to every missing, unknown, non-applicable, or malformed item.
5. Keep the submitted evidence references in the decision record so a human can reproduce the evaluation.

`PROCEED` means only that the submitted evidence states satisfy this internal readiness check. It never means legal validity, tax appropriateness, certification completion, payment approval, or authorization to transact.

## Produce

Prepare exactly these contracted artifact contents:

- `transaction_readiness.json`: `asOfDate`, rule version, eleven `gateResults`, `overallStatus`, `evidenceRefs`, `missingEvidence`, responsible verifiers, artifact references, `runRecord`, and the boundary notice.
- `transaction_readiness_table.md`: one row per gate with submitted state, verdict, evidence reference, reason, missing flag, responsible verifier, and next action.
- `missing_evidence_checklist.md`: unresolved evidence in gate order, with required confirmation, owner, official confirmation target, and next action.
- `official_inquiry_draft.md`: questions grouped for institution or program operator, registry, legal reviewer, tax professional or tax-authority inquiry owner, payment or settlement provider, and purchaser claim approver. Label it as a draft request for confirmation, never as an answer.

Record the input states, rule version, evaluation time, gate and overall results, and artifact references in `runRecord`.

## Hard boundary

- Do not initiate or execute an order, signature, transaction, payment, settlement, refund, registry transfer, retirement, use completion, or public claim.
- Do not determine legal, contractual, tax, certification, title, or disposition-right validity.
- Do not recommend price, profit, return, or investment merit.
- Do not generate or imply an institution's, registry's, authority's, expert's, or payment provider's official reply.
- Route unresolved rights, tax, registry, contract, payment, and claim questions to the responsible human or official confirmation target named in the artifacts.

## Derivation

- Identity: [TRANSACTION_EVIDENCE_PACK](../../_identity/TRANSACTION_EVIDENCE_PACK.md)
- Goal: [산림탄소 거래 준비도 Goal](../../_goal/forest_carbon_transaction_readiness_goal.md)
- Task: [산림탄소 거래 준비도 판정 Task](../../_task/forest_carbon_transaction_readiness_task.md)
- Knowledge: [산림탄소 거래 준비도 규칙 Knowledge](../../_knowledge/forest_carbon_transaction_readiness_knowledge.md)
- Method: [산림탄소 거래 준비도 판정 Method](../../_method/forest_carbon_transaction_readiness_method.md)

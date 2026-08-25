# Runtime contract

## Input

```json
{
  "asOfDate": "2026-08-21",
  "gates": {
    "G1": {"state": "PRESENT", "reason": "신원과 역할 확인"},
    "G2": {"state": "PRESENT"},
    "G3": {"state": "UNKNOWN"},
    "G4": {"state": "MISSING"}
  }
}
```

Supply G1 through G11. Closed state values: `PRESENT`, `MISSING`, `UNKNOWN`, `NOT_APPLICABLE_WITH_REASON`. The last value requires a non-empty reason.

Overall priority: `STOP > REVIEW > PROCEED`. A `PROCEED` result is preparation evidence only and never a legal, tax, contract, certification, payment, transfer, or claim approval.

## Output

`transaction_readiness.json`, `transaction_readiness_table.md`, `missing_evidence_checklist.md`, `official_inquiry_draft.md`, `run_record.json`, `result.json`.

Detailed source contract: [authoring contract](../../_authoring_specs/06_forest_carbon_transaction_readiness_authoring_contract.md).


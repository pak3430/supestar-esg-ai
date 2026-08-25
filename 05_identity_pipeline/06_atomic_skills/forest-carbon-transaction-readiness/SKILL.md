---
name: forest-carbon-transaction-readiness
description: "Evaluate a forest-carbon transaction evidence fixture across eleven identity, unit, rights, eligibility, purpose, contract, tax-review, payment, registry-transfer, and claim gates; produce missing evidence and official inquiry drafts without executing or validating a transaction."
---

# Forest Carbon Transaction Readiness

Use before any payment or transfer design to expose which evidence and confirmation owners are missing. This is a preparation assessment, not legal, tax, contract, certification, or transaction approval.

## Run

Read [the contract](references/contract.md), then execute:

```bash
python3 scripts/run.py --input <input.json> --output-dir <run-output-dir>
```

Read back `transaction_readiness.json`, `transaction_readiness_table.md`, `missing_evidence_checklist.md`, `official_inquiry_draft.md`, `run_record.json`, and `result.json`.

## Boundary

Overall priority is `STOP > REVIEW > PROCEED`. Even `PROCEED` means only that the supplied fixture contains the required preparation evidence. Never initiate payment, settlement, registry transfer, retirement, or a public claim.

## Derivation

- Goal: [Forest Carbon Transaction Readiness Goal](../../02_goal/forest_carbon_transaction_readiness_goal.md)
- Task: [Forest Carbon Transaction Readiness Task](../../03_task/forest_carbon_transaction_readiness_task.md)
- Knowledge: [Forest Carbon Transaction Readiness Knowledge](../../04_knowledge/forest_carbon_transaction_readiness_knowledge.md)
- Method: [Forest Carbon Transaction Readiness Method](../../05_method/forest_carbon_transaction_readiness_method.md)
- Runtime core: [supestar_skills.py](../_shared/supestar_skills.py)


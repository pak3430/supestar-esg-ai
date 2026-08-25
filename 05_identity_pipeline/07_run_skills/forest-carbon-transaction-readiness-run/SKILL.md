---
name: forest-carbon-transaction-readiness-run
description: Execute the verified G1-G11 forest-carbon transaction-readiness Build Skill for one preserved evidence-state fixture and seal every gate result, overall verdict, missing evidence, responsible verifier, inquiry draft, artifacts, and provenance. Use before a proposed payment only as an internal preparation check; never execute or approve a transaction.
---

# Forest Carbon Transaction Readiness Run

Execute exactly one registered G1-G11 preparation assessment. Preserve every submitted state and reason; never invent rights, approval, certification, registry status, or an official reply.

## Fixed binding

- Identity: [TRANSACTION_EVIDENCE_PACK](../../../ccs_authoring/supestar_mvp_v3/_identity/TRANSACTION_EVIDENCE_PACK.md)
- Concept Skill: [TRANSACTION_EVIDENCE_PACK](../../../ccs_authoring/supestar_mvp_v3/_skill/TRANSACTION_EVIDENCE_PACK/SKILL.md)
- Build Skill: [forest-carbon-transaction-readiness](../../../ccs_authoring/supestar_mvp_v3/_skill/forest-carbon-transaction-readiness/SKILL.md)
- Code Skill: [forest-carbon-transaction-readiness](../../06_atomic_skills/forest-carbon-transaction-readiness/SKILL.md)
- Input contract: [runtime contract](../../06_atomic_skills/forest-carbon-transaction-readiness/references/contract.md)

## Execute

Read the [common Run contract](../RUN_LAYER_CONTRACT.md), then run:

```bash
python3 ../_shared/run_verified_skill.py \
  --run-skill forest-carbon-transaction-readiness-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

Wait for exit `0`. Read `transaction_readiness.json`, `transaction_readiness_table.md`, `missing_evidence_checklist.md`, `official_inquiry_draft.md`, `result.json`, `run_record.json`, and `run_skill_record.json`.

## Report

Report all eleven gate states, overall `PROCEED|REVIEW|STOP`, missing evidence and owner, official confirmation targets, evidence cutoff, Run ID, and artifact paths. `PROCEED` means evidence readiness only.

## Boundary

Do not sign, order, pay, settle, transfer, retire, complete use, approve a public claim, decide legal or tax validity, call a Composite, or deploy a Runtime package.

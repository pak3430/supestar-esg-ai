---
name: scope-activity-classification-run
description: Execute the verified Scope activity-classification Build Skill for one preserved activity record and seal the candidate Scope, rule trace, missing facts, verdict, artifacts, and provenance. Use when organizational boundary, ownership or control, purchased energy, and value-chain facts must be evaluated without calculating emissions.
---

# Scope Activity Classification Run

Execute exactly one registered Scope candidate classification. Preserve the activity and boundary fields exactly; never infer a missing relationship.

## Fixed binding

- Identity: [ORGANIZATIONAL_BOUNDARY](../../../ccs_authoring/supestar_mvp_v3/_identity/ORGANIZATIONAL_BOUNDARY.md)
- Concept Skill: [ORGANIZATIONAL_BOUNDARY](../../../ccs_authoring/supestar_mvp_v3/_skill/ORGANIZATIONAL_BOUNDARY/SKILL.md)
- Build Skill: [scope-activity-classification](../../../ccs_authoring/supestar_mvp_v3/_skill/scope-activity-classification/SKILL.md)
- Code Skill: [scope-activity-classification](../../06_atomic_skills/scope-activity-classification/SKILL.md)
- Input contract: [runtime contract](../../06_atomic_skills/scope-activity-classification/references/contract.md)

## Execute

Read the [common Run contract](../RUN_LAYER_CONTRACT.md), then run:

```bash
python3 ../_shared/run_verified_skill.py \
  --run-skill scope-activity-classification-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

Wait for exit `0`. Read `scope_classification.json`, `scope_evidence_card.md`, `additional_data_request.md`, `result.json`, `run_record.json`, and `run_skill_record.json`.

## Report

Report the activity and boundary snapshot, candidate Scope or unresolved state, applied rule, `PROCEED|REVIEW|STOP`, missing facts, Run ID, and artifact paths.

## Boundary

This Run Skill produces a Scope candidate only. Do not calculate CO2e, assure an inventory, redefine Scope 3, call a Composite, or deploy a Runtime package.

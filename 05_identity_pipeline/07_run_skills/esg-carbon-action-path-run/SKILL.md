---
name: esg-carbon-action-path-run
description: Execute the verified ESG-to-carbon action-path Build Skill for one preserved question and seal its ordered path, evidence, verdict, artifacts, and provenance. Use for an admitted explanation or preparation request from ESG through measurement, Scope, reduction, markets, or forest carbon; never use it to approve a claim or transaction.
---

# ESG Carbon Action Path Run

Execute exactly one registered ESG-to-carbon action-path run. Preserve `question`, `userRole`, `focus`, `measurementContext`, and `asOfDate` as supplied.

## Fixed binding

- Identity: [ESG_MANAGEMENT](../../../ccs_authoring/supestar_mvp_v3/_identity/ESG_MANAGEMENT.md)
- Concept Skill: [ESG_MANAGEMENT](../../../ccs_authoring/supestar_mvp_v3/_skill/ESG_MANAGEMENT/SKILL.md)
- Build Skill: [esg-carbon-action-path](../../../ccs_authoring/supestar_mvp_v3/_skill/esg-carbon-action-path/SKILL.md)
- Code Skill: [esg-carbon-action-path](../../06_atomic_skills/esg-carbon-action-path/SKILL.md)
- Input contract: [runtime contract](../../06_atomic_skills/esg-carbon-action-path/references/contract.md)

## Execute

Read the [common Run contract](../RUN_LAYER_CONTRACT.md), then run:

```bash
python3 ../_shared/run_verified_skill.py \
  --run-skill esg-carbon-action-path-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

Wait for exit `0`. Read `action_path.json`, `explanation_cards.md`, `next_action_checklist.md`, `result.json`, `run_record.json`, and `run_skill_record.json` before reporting completion.

## Report

Report the interpreted focus, ordered path, missing prerequisites, `PROCEED|REVIEW|STOP`, evidence cutoff, next safe action, Run ID, and artifact paths.

## Boundary

Do not calculate or assure a final inventory, assert carbon neutrality, approve offset use, purchase a unit, make a payment, mutate a registry, call a Composite, or deploy a Runtime package.

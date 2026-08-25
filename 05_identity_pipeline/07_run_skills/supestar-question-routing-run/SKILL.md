---
name: supestar-question-routing-run
description: Execute the verified Supestar question-routing Build Skill against one preserved user question, wait for the fixed code to finish, and seal the selected route, evidence, verdict, artifacts, and provenance. Use at the start of an admitted Supestar candidate run; do not execute the downstream route or an external action.
---

# Supestar Question Routing Run

Execute exactly one registered question-routing run. Preserve the original `question`, `userRole`, `asOfDate`, and supplied evidence.

## Fixed binding

- Identity: [USER_QUESTION](../../../ccs_authoring/supestar_mvp_v3/_identity/USER_QUESTION.md)
- Concept Skill: [USER_QUESTION](../../../ccs_authoring/supestar_mvp_v3/_skill/USER_QUESTION/SKILL.md)
- Build Skill: [supestar-question-routing](../../../ccs_authoring/supestar_mvp_v3/_skill/supestar-question-routing/SKILL.md)
- Code Skill: [supestar-question-routing](../../06_atomic_skills/supestar-question-routing/SKILL.md)
- Input contract: [runtime contract](../../06_atomic_skills/supestar-question-routing/references/contract.md)

## Execute

Read the [common Run contract](../RUN_LAYER_CONTRACT.md), then run:

```bash
python3 ../_shared/run_verified_skill.py \
  --run-skill supestar-question-routing-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

Wait for exit `0`. Then read `context_snapshot.json`, `route_decision.json`, `result.json`, `run_record.json`, and `run_skill_record.json`. Do not synthesize a missing file or invoke a downstream Skill after a failure.

## Report

Report the one selected route, `PROCEED|REVIEW|STOP`, applied reason, clarifying question if any, evidence cutoff, Run ID, and artifact paths. `PROCEED` authorizes only a later handoff; this Run Skill never performs that handoff itself.

## Boundary

Do not purchase, pay, mutate a registry, make legal or tax conclusions, certify a project, recommend price or return, call a Composite, or deploy a Runtime package.

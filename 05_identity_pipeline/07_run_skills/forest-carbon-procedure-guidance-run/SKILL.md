---
name: forest-carbon-procedure-guidance-run
description: Execute the verified forest-carbon procedure-guidance Build Skill for one preserved project state and seal the supported current stage, next official procedure, actors, prerequisites, artifacts, confirmation questions, verdict, and provenance. Use for procedure sequencing only; never use it to declare certification, tradability, or registry completion.
---

# Forest Carbon Procedure Guidance Run

Execute exactly one registered procedure-guidance run. Preserve the claimed stage and supplied documents, and distinguish them from officially confirmed completion.

## Fixed binding

- Identity: [FOREST_CARBON_PROJECT](../../../ccs_authoring/supestar_mvp_v3/_identity/FOREST_CARBON_PROJECT.md)
- Concept Skill: [FOREST_CARBON_PROJECT](../../../ccs_authoring/supestar_mvp_v3/_skill/FOREST_CARBON_PROJECT/SKILL.md)
- Build Skill: [forest-carbon-procedure-guidance](../../../ccs_authoring/supestar_mvp_v3/_skill/forest-carbon-procedure-guidance/SKILL.md)
- Code Skill: [forest-carbon-procedure-guidance](../../06_atomic_skills/forest-carbon-procedure-guidance/SKILL.md)
- Input contract: [runtime contract](../../06_atomic_skills/forest-carbon-procedure-guidance/references/contract.md)

## Execute

Read the [common Run contract](../RUN_LAYER_CONTRACT.md), then run:

```bash
python3 ../_shared/run_verified_skill.py \
  --run-skill forest-carbon-procedure-guidance-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

Wait for exit `0`. Read `procedure_path.json`, `procedure_checklist.md`, `official_confirmation_questions.md`, `result.json`, `run_record.json`, and `run_skill_record.json`.

## Report

Report the supported current stage, blocked or next stage, actor and artifact, `PROCEED|REVIEW|STOP`, official confirmation need, Run ID, and artifact paths.

## Boundary

Do not register, verify, certify, trade, mutate a registry, present a stage as complete without evidence, call a Composite, or deploy a Runtime package.

---
name: forest-esg-impact-mapping-run
description: Execute the verified forest E-S-G impact-mapping Build Skill for one preserved project record and seal the environmental, social, and governance evidence map, gaps, verdict, artifacts, and provenance. Use to expose project impacts, actors, responsibilities, and missing axes; not for certification, procedure finality, or a transaction.
---

# Forest ESG Impact Mapping Run

Execute exactly one registered forest E/S/G mapping run. Treat supplied E, S, and G items as evidence inputs, not automatic proof.

## Fixed binding

- Identity: [FOREST_CARBON_PROJECT](../../../ccs_authoring/supestar_mvp_v3/_identity/FOREST_CARBON_PROJECT.md)
- Concept Skill: [FOREST_CARBON_PROJECT](../../../ccs_authoring/supestar_mvp_v3/_skill/FOREST_CARBON_PROJECT/SKILL.md)
- Build Skill: [forest-esg-impact-mapping](../../../ccs_authoring/supestar_mvp_v3/_skill/forest-esg-impact-mapping/SKILL.md)
- Code Skill: [forest-esg-impact-mapping](../../06_atomic_skills/forest-esg-impact-mapping/SKILL.md)
- Input contract: [runtime contract](../../06_atomic_skills/forest-esg-impact-mapping/references/contract.md)

## Execute

Read the [common Run contract](../RUN_LAYER_CONTRACT.md), then run:

```bash
python3 ../_shared/run_verified_skill.py \
  --run-skill forest-esg-impact-mapping-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

Wait for exit `0`. Read `forest_esg_map.json`, `forest_esg_map.md`, `missing_axis_questions.md`, `result.json`, `run_record.json`, and `run_skill_record.json`.

## Report

Report the E/S/G evidence states, missing axes, responsibility questions, `PROCEED|REVIEW|STOP`, evidence cutoff, Run ID, and artifact paths.

## Boundary

Do not hide rights or community evidence, infer a private institutional opinion, declare registration or certification complete, execute a transaction, call a Composite, or deploy a Runtime package.

---
name: forest-esg-impact-mapping
description: "Map a forest-carbon project into distinct environmental, social, and governance impacts, actors, responsibilities, evidence, and gaps; review missing axes and stop claims that hide rights, communities, or governance behind carbon uptake alone."
---

# Forest ESG Impact Mapping

Use to produce an E/S/G responsibility map for a forest-carbon project. Do not treat carbon uptake alone as complete ESG evidence.

## Run

Read [the contract](references/contract.md), then execute:

```bash
python3 scripts/run.py --input <input.json> --output-dir <run-output-dir>
```

Read back `forest_esg_map.json`, `forest_esg_map.md`, `missing_axis_questions.md`, `run_record.json`, and `result.json`.

## Boundary

Missing E, S, or G evidence is REVIEW. A request to omit land rights, community participation, or governance while claiming complete ESG is STOP. Do not infer a public institution's non-public opinion.

## Derivation

- Goal: [Forest ESG Impact Mapping Goal](../../02_goal/forest_esg_impact_mapping_goal.md)
- Task: [Forest ESG Impact Mapping Task](../../03_task/forest_esg_impact_mapping_task.md)
- Knowledge: [Forest ESG Impact Mapping Knowledge](../../04_knowledge/forest_esg_impact_mapping_knowledge.md)
- Method: [Forest ESG Impact Mapping Method](../../05_method/forest_esg_impact_mapping_method.md)
- Runtime core: [supestar_skills.py](../_shared/supestar_skills.py)


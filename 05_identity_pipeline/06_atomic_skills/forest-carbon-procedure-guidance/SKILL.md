---
name: forest-carbon-procedure-guidance
description: "Guide a forest-carbon project from its current evidenced stage to the next public procedure, actor, prerequisite, and artifact; review unknown applicability and stop attempts to skip registration, verification, or certification."
---

# Forest Carbon Procedure Guidance

Use for planning, registration, monitoring, verification, certification, utilization, and registry-status questions. Describe only public procedures and supplied evidence.

## Run

Read [the contract](references/contract.md), then execute:

```bash
python3 scripts/run.py --input <input.json> --output-dir <run-output-dir>
```

Read back `procedure_path.json`, `procedure_checklist.md`, `official_confirmation_questions.md`, `run_record.json`, and `result.json`.

## Boundary

Do not treat a stage as complete without evidence. Do not perform registration, certification, trading, or registry mutation. Program applicability and allowed claims remain subject to official confirmation.

## Derivation

- Goal: [Forest Carbon Procedure Guidance Goal](../../02_goal/forest_carbon_procedure_guidance_goal.md)
- Task: [Forest Carbon Procedure Guidance Task](../../03_task/forest_carbon_procedure_guidance_task.md)
- Knowledge: [Forest Carbon Procedure Guidance Knowledge](../../04_knowledge/forest_carbon_procedure_guidance_knowledge.md)
- Method: [Forest Carbon Procedure Guidance Method](../../05_method/forest_carbon_procedure_guidance_method.md)
- Runtime core: [supestar_skills.py](../_shared/supestar_skills.py)


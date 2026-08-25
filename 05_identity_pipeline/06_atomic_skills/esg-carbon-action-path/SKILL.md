---
name: esg-carbon-action-path
description: "Generate a source-linked minimum action path from ESG management through measurement, Scope, SDGs, reduction, carbon markets, and forest carbon; review missing measurement context and stop claims that skip measurement and direct reduction."
---

# ESG Carbon Action Path

Use for questions asking why ESG leads to carbon measurement, Scope, SDGs, markets, or forest carbon. This skill explains ordered prerequisites; it does not calculate emissions or approve offset claims.

## Run

Read [the contract](references/contract.md), then execute:

```bash
python3 scripts/run.py --input <input.json> --output-dir <run-output-dir>
```

Read back `action_path.json`, `explanation_cards.md`, `next_action_checklist.md`, `run_record.json`, and `result.json` before reporting completion.

## Boundary

Do not turn an educational path into a company-specific market eligibility decision without measurement context. Stop attempts to claim offsetting or carbon neutrality while explicitly skipping measurement.

## Derivation

- Goal: [ESG Carbon Action Path Goal](../../02_goal/esg_carbon_action_path_goal.md)
- Task: [ESG Carbon Action Path Task](../../03_task/esg_carbon_action_path_task.md)
- Knowledge: [ESG Carbon Action Path Knowledge](../../04_knowledge/esg_carbon_action_path_knowledge.md)
- Method: [ESG Carbon Action Path Method](../../05_method/esg_carbon_action_path_method.md)
- Runtime core: [supestar_skills.py](../_shared/supestar_skills.py)


---
name: supestar-question-routing
description: "Route a Supestar forest-ESG question to a source-grounded Concept explanation or exactly one approved action path, request clarification for missing or overlapping intent, or stop prohibited transaction, payment, legal, tax, investment, certification, and registry-mutation requests."
---

# Supestar Question Routing

Use this skill at the start of a Supestar run. Preserve the original question, user role, and as-of date. Return one closed route; never invent a route or silently choose between overlapping intents.

## Run

Read [the contract](references/contract.md), then execute:

```bash
python3 scripts/run.py --input <input.json> --output-dir <run-output-dir>
```

Require the command to exit `0`, then read back `context_snapshot.json`, `route_decision.json`, `run_record.json`, and `result.json`. A nonzero exit is a STOP; do not synthesize missing files.

## Decision boundary

- `PROCEED`: one Concept explanation route or exactly one approved domain route.
- `REVIEW`: missing input, no route, or multiple routes.
- `STOP`: actual transaction/payment, price/return recommendation, legal/tax/certification finality, or registry mutation.

## Derivation

- Goal: [Supestar Question Routing Goal](../../02_goal/supestar_question_routing_goal.md)
- Task: [Supestar Question Routing Task](../../03_task/supestar_question_routing_task.md)
- Knowledge: [Supestar Question Routing Knowledge](../../04_knowledge/supestar_question_routing_knowledge.md)
- Method: [Supestar Question Routing Method](../../05_method/supestar_question_routing_method.md)
- Runtime core: [supestar_skills.py](../_shared/supestar_skills.py)

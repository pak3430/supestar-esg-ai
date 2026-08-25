---
name: scope-activity-classification
description: "Classify an activity as a Scope 1, Scope 2, or Scope 3 candidate from organizational boundary, ownership or control, purchased energy, and value-chain facts; request missing facts and never calculate emissions without activity data and factors."
---

# Scope Activity Classification

Use when a user asks which Scope an activity may belong to. The result is a rule-traced candidate classification, not an emissions calculation or assurance opinion.

## Run

Read [the contract](references/contract.md), then execute:

```bash
python3 scripts/run.py --input <input.json> --output-dir <run-output-dir>
```

Read back `scope_classification.json`, `scope_evidence_card.md`, `additional_data_request.md`, `run_record.json`, and `result.json`.

## Boundary

Return `REVIEW` when boundary or activity relationships are unresolved. Return `STOP` when the request defines Scope 3 as the sum of Scope 1 and Scope 2. Never infer an emissions amount.

## Derivation

- Goal: [Scope Activity Classification Goal](../../02_goal/scope_activity_classification_goal.md)
- Task: [Scope Activity Classification Task](../../03_task/scope_activity_classification_task.md)
- Knowledge: [Scope Activity Classification Knowledge](../../04_knowledge/scope_activity_classification_knowledge.md)
- Method: [Scope Activity Classification Method](../../05_method/scope_activity_classification_method.md)
- Runtime core: [supestar_skills.py](../_shared/supestar_skills.py)


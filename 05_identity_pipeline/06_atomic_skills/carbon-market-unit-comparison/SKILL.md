---
name: carbon-market-unit-comparison
description: "Separate CCM, VCM, emission allowances, carbon credits, and offsetting across market, unit, use, registry-state, and claim axes; review unverified use conditions and stop double use or unsupported claims."
---

# Carbon Market Unit Comparison

Use to explain or review terms that are often conflated. Keep market type, unit type, use action, registry status, and external claim as separate fields.

## Run

Read [the contract](references/contract.md), then execute:

```bash
python3 scripts/run.py --input <input.json> --output-dir <run-output-dir>
```

Read back `market_unit_comparison.json`, `market_unit_comparison.md`, `claim_cautions.md`, `run_record.json`, and `result.json`.

## Boundary

Learning comparisons may proceed. Actual use or claim questions require registry and program evidence. Double use is STOP. This skill never approves a public climate claim.

## Derivation

- Goal: [Carbon Market Unit Comparison Goal](../../02_goal/carbon_market_unit_comparison_goal.md)
- Task: [Carbon Market Unit Comparison Task](../../03_task/carbon_market_unit_comparison_task.md)
- Knowledge: [Carbon Market Unit Comparison Knowledge](../../04_knowledge/carbon_market_unit_comparison_knowledge.md)
- Method: [Carbon Market Unit Comparison Method](../../05_method/carbon_market_unit_comparison_method.md)
- Runtime core: [supestar_skills.py](../_shared/supestar_skills.py)


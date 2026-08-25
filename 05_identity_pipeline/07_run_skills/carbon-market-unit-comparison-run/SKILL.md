---
name: carbon-market-unit-comparison-run
description: Execute the verified carbon-market and unit-comparison Build Skill for one preserved request and seal the separated market, unit, use, registry, and claim axes with evidence, verdict, artifacts, and provenance. Use for CCM, VCM, allowance, credit, and offset comparison or review; never use it to approve a claim or execute a trade.
---

# Carbon Market Unit Comparison Run

Execute exactly one registered comparison run. Keep `question`, `purpose`, `unitType`, `registryStatus`, `doubleUse`, and `asOfDate` distinct.

## Fixed binding

- Identity: [CLIMATE_CLAIM](../../../ccs_authoring/supestar_mvp_v3/_identity/CLIMATE_CLAIM.md)
- Concept Skill: [CLIMATE_CLAIM](../../../ccs_authoring/supestar_mvp_v3/_skill/CLIMATE_CLAIM/SKILL.md)
- Build Skill: [carbon-market-unit-comparison](../../../ccs_authoring/supestar_mvp_v3/_skill/carbon-market-unit-comparison/SKILL.md)
- Code Skill: [carbon-market-unit-comparison](../../06_atomic_skills/carbon-market-unit-comparison/SKILL.md)
- Input contract: [runtime contract](../../06_atomic_skills/carbon-market-unit-comparison/references/contract.md)

## Execute

Read the [common Run contract](../RUN_LAYER_CONTRACT.md), then run:

```bash
python3 ../_shared/run_verified_skill.py \
  --run-skill carbon-market-unit-comparison-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

Wait for exit `0`. Read `market_unit_comparison.json`, `market_unit_comparison.md`, `claim_cautions.md`, `result.json`, `run_record.json`, and `run_skill_record.json`.

## Report

Report the separated axes, use conditions, registry uncertainty, double-use gate, `PROCEED|REVIEW|STOP`, evidence cutoff, Run ID, and artifact paths.

## Boundary

Do not approve a public claim, determine legal market eligibility, trade, pay, retire or transfer a unit, call a Composite, or deploy a Runtime package.

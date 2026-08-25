---
name: esg-carbon-action-path
description: Convert an ESG-and-carbon question into a grounded minimum action path through measurement, boundaries, Scope, reduction, markets, and forest carbon. Use when the user needs ordered nodes, reason-bearing edges, evidence references, explanation cards, and bounded next actions; do not use it to assert carbon neutrality or execute a transaction without the required measurement and authority.
---

# ESG Carbon Action Path

Turn ESG responsibility into an explainable path to the user's nearest justified carbon action. Preserve every prerequisite needed for measurement and market reasoning, and make uncertainty visible instead of filling missing evidence.

## Inputs

Require:

- `question`: a question connecting ESG to carbon action;
- `userRole`: the user's role;
- `asOfDate`: the evidence cutoff date.

Optionally accept `focus` as one of `MEASUREMENT`, `SCOPE`, `SDGS`, `MARKET`, or `FOREST_CARBON`.

## Workflow

1. Reject unsupported execution or assertion requests first. Return `STOP` for an actual purchase, payment, registry mutation, or a request to assert offsetting or carbon neutrality without measurement.
2. Identify the start and end nodes from `question` and `focus`.
3. Select a contiguous minimum path from:
   `ESG → ESG_MANAGEMENT → GREENHOUSE_GAS_INVENTORY → ORGANIZATIONAL_BOUNDARY → OPERATIONAL_BOUNDARY → SCOPE_1·2·3 → ACTIVITY_DATA·EMISSION_FACTOR → CO2E → DIRECT_EMISSIONS_REDUCTION → RESIDUAL_EMISSIONS → SUSTAINABLE_DEVELOPMENT_GOALS → CCM·VCM → FOREST_CARBON_PROJECT`.
4. Do not skip an organizational boundary, operational boundary, activity-data, emission-factor, reduction, or residual-emissions prerequisite when the requested endpoint depends on it.
5. Add one sentence explaining why each selected edge is necessary. Bind each material claim to a source identifier and `asOfDate`.
6. If market or offset guidance is requested without the required boundary or activity data, return `REVIEW` and list what is missing. If the question, cutoff date, and evidence are sufficient, return `PROCEED`.
7. Divide the next action into `확인할 자료`, `담당 주체`, and `생성 산출물`.

## Outputs

Produce all of the following:

- `ActionPath.json` with `orderedNodes`, `orderedEdges`, `reasonPerEdge`, and `evidenceRefs`;
- `explanation_cards.md` in language appropriate to `userRole`;
- `next_action_checklist.md` divided into evidence, owner, and artifact;
- `status` as exactly `PROCEED`, `REVIEW`, or `STOP`;
- `RunRecord` containing the selected identities, relations, evidence, output paths, and status.

## Authority boundary

This skill explains and prepares action. It does not validate a final emissions inventory, give final legal, tax, certification, or registry determinations, assert carbon neutrality, trade credits, make payments, or mutate an external system.

## Derivation

[ESG_MANAGEMENT](../../_identity/ESG_MANAGEMENT.md) definesGoal → [ESG→탄소 행동경로 Goal](../../_goal/esg_carbon_action_path_goal.md) requiresTask → [ESG→탄소 행동경로 Task](../../_task/esg_carbon_action_path_task.md) requiresKnowledge → [ESG→탄소 행동경로 Knowledge](../../_knowledge/esg_carbon_action_path_knowledge.md) appliedThrough → [ESG→탄소 행동경로 Method](../../_method/esg_carbon_action_path_method.md) developsSkill → `esg-carbon-action-path`.

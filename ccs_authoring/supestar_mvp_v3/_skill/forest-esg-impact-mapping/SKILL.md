---
name: forest-esg-impact-mapping
description: "Map a concrete forest-carbon project into environmental, social, and governance impacts, actors, responsibilities, evidence, gaps, questions, and a PROCEED/REVIEW/STOP status. Use when a project description needs an auditable forest ESG completeness and accountability map; do not use for procedure sequencing, certification or registration finality, transaction execution, or legal and tax conclusions."
---

# Forest E/S/G Impact Mapping

Turn the supplied forest-carbon project description and evidence into a traceable E/S/G impact-responsibility map. Preserve the difference between claims and evidence, expose missing axes, and never present an institution's undisclosed judgment as fact.

## Required input

- `projectSummary`: project purpose, activities, location, and participants.
- `asOfDate`: date on which the evidence and status are assessed.

Accept `environmentEvidence`, `socialEvidence`, and `governanceEvidence` when supplied. Treat them as evidence collections, not as automatic proof of the claims they contain.

## Workflow

1. Separate the project summary's claims from the evidence actually supplied and assign stable references to evidence items.
2. Build an environmental axis covering absorption and storage, ecology, baseline, methodology, additionality, leakage, permanence, reversal risk, and their evidence.
3. Build a social axis covering landowners, forestry workers, communities, rights, consent, participation, benefit and burden allocation, safety, grievances, and their evidence.
4. Build a governance axis covering only the publicly supported roles of the Korea Forest Service, Korea Forestry Promotion Institute and Forest Carbon Center, Forest Carbon Registry, validators, project operators and landowners, plus planning, validation, certification, registry, contract, and audit evidence.
5. For every axis, connect impacts, actors, responsibilities, and evidence. Record unconnected or absent elements as gaps and generate a concrete question for each gap.
6. Do not place one evidence item on several axes unless the record explains the distinct supporting relationship for each placement.
7. Apply the status rules below in order and record the matched condition and evidence references in the RunRecord.

## Status rules

- `STOP`: the request hides social, rights, or governance information while asking to declare ESG completeness from absorption data alone.
- `REVIEW`: no STOP condition applies, but any axis has unclear or missing evidence, rights, participants, or responsible actors.
- `PROCEED`: no STOP or REVIEW condition applies, and all three axes have minimum information, identified responsible actors, and linked evidence.

## Outputs

- `forest_esg_map.json`: E/S/G nodes, impacts, actors, responsibilities, evidence, and gaps.
- `forest_esg_map.md`: the same impact-responsibility map in human-readable form.
- `missing_axis_questions.md`: axis-specific questions linked to each gap and the evidence needed to resolve it.
- `status`: exactly one of `PROCEED`, `REVIEW`, or `STOP`.
- `RunRecord`: inputs, `FOREST_CARBON_PROJECT` Identity use, evidence references, gaps, applied rules, and decision rationale.

## Boundaries

- Mark absent evidence or responsibility as `unknown` or a gap; do not fill it plausibly.
- Do not infer a private institutional decision or official opinion.
- Do not declare registration, validation, certification, a transaction, legal effect, or tax treatment complete.
- Do not expand this capability into procedural guidance or external execution.

## Derivation

1. Identity — [FOREST_CARBON_PROJECT](../../_identity/FOREST_CARBON_PROJECT.md)
2. Goal — [산림 E/S/G 영향·책임 매핑 Goal](../../_goal/forest_esg_impact_mapping_goal.md)
3. Task — [산림 E/S/G 영향·책임 매핑 Task](../../_task/forest_esg_impact_mapping_task.md)
4. Knowledge — [산림 E/S/G 영향·책임 매핑 Knowledge](../../_knowledge/forest_esg_impact_mapping_knowledge.md)
5. Method — [산림 E/S/G 영향·책임 매핑 Method](../../_method/forest_esg_impact_mapping_method.md)

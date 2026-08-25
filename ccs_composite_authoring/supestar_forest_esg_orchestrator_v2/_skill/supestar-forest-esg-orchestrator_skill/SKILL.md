---
name: supestar-forest-esg-orchestrator_skill
description: "Route one immutable flat forest-ESG JSON input through exactly one approved domain Run Skill, or return one exact terminal result."
---

# Supestar Forest ESG Orchestrator Skill

Use this skill to answer one forest-ESG request through the sealed `supestar-forest-esg-orchestrator` interface.

## Interface

### Input

Receive exactly one flat JSON file as one immutable original byte source. Preserve its exact bytes `0..EOF`. Supply that same original file byte-for-byte to the router and, if a domain route is selected, to the selected domain Run Skill. Never extract, merge, normalize, re-encode, default, or parse and reserialize it.

### Outcome

Return exactly one of:

- the selected domain Run Skill result with its evidence, `PROCEED` / `REVIEW` / `STOP` status, and Run Record or records; or
- the exact selected terminal bytes `0..EOF` from the completed producer carriage.

## Sealed execution contract

1. Admit the one immutable original input file.
2. Run the router exactly once with that file.
3. Immediately run the sole producer carriage caller exactly once, preserving either the admitted router result bytes or exact process-failure stdout bytes without changing any byte.
4. Read the completed carriage once for control and select exactly one route in the closed nine-way XOR partition.
5. For a selected domain route, run only its selected internal caller and named domain Run Skill, passing the immutable original input file unchanged.
6. For a selected terminal route, run only its selected terminal caller and return the exact completed-carriage bytes.
7. Return only the selected branch outcome. Do not run or merge any unselected branch.

Fail closed if zero or multiple routes select. Do not add a fallback, fan-out, join, loop, second router run, synthetic result, or invented record.

## Links

- canonicalComposite -> [supestar forest ESG orchestrator COMPOSITE](../../_entity/_composite/supestar_forest_esg_orchestrator_composite.md)
- sealedWorkflow -> [supestar forest ESG orchestrator WORKFLOW](../../_entity/_workflow/supestar_forest_esg_orchestrator_workflow.md)
- producedBy -> [composite_sealing_skill](/Users/gesia/.codex/skills/composite_authoring_skill/_members/_skill/composite_sealing_skill/SKILL.md)
- usesSkill -> [composite_sealing_skill](/Users/gesia/.codex/skills/composite_authoring_skill/_members/_skill/composite_sealing_skill/SKILL.md)
## Binding

MUST declare, before launch, the invocation's consumed read set, its write scope, and its landing surfaces.
  why -> a later reader must reconstruct where mechanical execution shaped a result, so this traceable-execution why applies to every invocation that reads any input or writes to any scope or landing surface
MUST NOT read outside the declared read set or write outside the declared write scope.
  why -> a later reader must reconstruct where mechanical execution shaped a result, so this traceable-execution why applies to every invocation that reads any input or writes to any scope or landing surface
MUST NOT land a result outside the declared landing surfaces - an in-scope write at an undeclared landing path is still a violation.
  why -> a later reader must reconstruct where mechanical execution shaped a result, so this traceable-execution why applies to every invocation that reads any input or writes to any scope or landing surface
STOP before launch when the read set, write scope, or landing surfaces are undeclared - undeclared is a STOP, never a launch.
  why -> a later reader must reconstruct where mechanical execution shaped a result, so this traceable-execution why applies to every invocation that reads any input or writes to any scope or landing surface
STOP when any observed read or write lands outside the declared scope - the result is not admitted.
  why -> a later reader must reconstruct where mechanical execution shaped a result, so this traceable-execution why applies to every invocation that reads any input or writes to any scope or landing surface
STOP when any observed landing is at an undeclared surface or any required declared landing is absent - the result is not admitted.
  why -> a later reader must reconstruct where mechanical execution shaped a result, so this traceable-execution why applies to every invocation that reads any input or writes to any scope or landing surface
contract: invocation_read_write_scope_binding_contract

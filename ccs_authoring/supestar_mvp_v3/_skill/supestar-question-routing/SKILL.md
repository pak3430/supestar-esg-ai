---
name: supestar-question-routing
description: "Route one Supestar forest-ESG question to exactly one admitted MVP route using the fixed question, user-role, as-of-date, evidence, STOP, and output contracts. Use for routing before a downstream ESG capability runs; do not use to execute that capability, perform transactions, or make legal, tax, certification, price, return, or investment determinations."
---

# Supestar Question Routing

Route one user request. Return exactly one route decision and its trace record; do not execute the selected downstream capability.

## Inputs

Require:

- `question`: non-empty original user question.
- `userRole`: exactly one of `LEARNER`, `ESG_MANAGER`, `FOREST_OWNER_OPERATOR`, `REVIEWER`.
- `asOfDate`: a date in `YYYY-MM-DD` form.

Optionally accept `providedEvidence`, a list of user-supplied documents, states, or claims. Preserve the original question and supplied evidence in the context snapshot. Do not infer missing input.

## Closed routes

Return only one of these values:

- `ESG_CARBON_PATH`: why ESG leads to carbon measurement, Scope, SDGs, or markets.
- `SCOPE_CLASSIFICATION`: whether an activity or emission source is Scope 1, 2, or 3.
- `CARBON_MARKET_COMPARISON`: differences among CCM, VCM, allowances, credits, and offsetting.
- `FOREST_ESG_MAPPING`: environmental, social, and governance impacts or responsibilities of forest carbon.
- `FOREST_CARBON_PROCEDURE`: planning, registration, monitoring, verification, certification, or registry procedure.
- `TRANSACTION_READINESS`: pre-transaction rights, contract, tax, payment, transfer, or evidence readiness.
- `NEEDS_INPUT`: required input is missing or more than one normal route matches.
- `OUT_OF_SCOPE`: a forbidden request or no admitted MVP intent matches.

Never return multiple routes.

## Procedure

1. Copy `question`, `userRole`, `asOfDate`, and `providedEvidence` into `ContextSnapshot` without inventing absent values.
2. Validate the required inputs. If any are missing or invalid, return route=`NEEDS_INPUT`, status=`REVIEW`, and ask only for the missing or invalid fields.
3. Before normal routing, apply the STOP gates. Return route=`OUT_OF_SCOPE`, status=`STOP` when the request asks for:
   - an actual trade, payment, or registry change;
   - price, return, or investment advice;
   - an official legal, tax, contract, or certification determination;
   - inferred personal data or non-public institutional information.
4. Match the question against the six normal routes using their definitions above.
5. If exactly one normal route matches, return it with status=`PROCEED`.
6. If two or more normal routes match, return route=`NEEDS_INPUT`, status=`REVIEW`, and a question that lets the user choose one intent. Do not select one arbitrarily.
7. If no normal route matches, return route=`OUT_OF_SCOPE`, status=`STOP`.
8. Verify that the final result has one route and that its status matches the contract.

## Outputs

Return all five fields:

- `ContextSnapshot`: original `question`, `userRole`, `asOfDate`, and `providedEvidence`.
- `RouteDecision`: `route`, `matchedRule`, and a reason tied to the applied rule or STOP gate rather than a confidence score.
- `ClarifyingQuestions`: only questions needed to resolve missing input or route collision; otherwise an empty list.
- `status`: `PROCEED`, `REVIEW`, or `STOP`.
- `RunRecord`: `ruleVersion`, `asOfDate`, `selectedRoute`, and `status`.

## Boundaries

- A `PROCEED` result authorizes only handoff to the named downstream route; it is not evidence that the downstream capability ran.
- Do not execute transactions, payments, registry mutations, legal or tax advice, official certification, or price and return recommendations.
- Do not expose or deploy the authoring vault. This is an instruction-capability candidate, not a Runtime registration.
- Fail closed if the one-route or route/status invariant cannot be satisfied.

## Derivation

[USER_QUESTION](../../_identity/USER_QUESTION.md)
→ definesGoal → [Supestar Question Routing Goal](../../_goal/supestar_question_routing_goal.md)
→ requiresTask → [Supestar Question Routing Task](../../_task/supestar_question_routing_task.md)
→ requiresKnowledge → [Supestar Question Routing Knowledge](../../_knowledge/supestar_question_routing_knowledge.md)
→ appliedThrough → [Supestar Question Routing Method](../../_method/supestar_question_routing_method.md)
→ developsSkill → `supestar-question-routing`

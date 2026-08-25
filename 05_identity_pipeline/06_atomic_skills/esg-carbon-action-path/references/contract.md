# Runtime contract

## Input

```json
{
  "question": "왜 ESG에서 Scope와 탄소시장까지 가나요?",
  "userRole": "LEARNER",
  "asOfDate": "2026-08-21",
  "focus": "MARKET",
  "measurementContext": null
}
```

Allowed focus: `MEASUREMENT`, `SCOPE`, `SDGS`, `MARKET`, `FOREST_CARBON`.

`measurementContext` is optional for learning explanations and required before an organization-specific market or forest-carbon decision can proceed.

## Output

`action_path.json`, `explanation_cards.md`, `next_action_checklist.md`, `run_record.json`, `result.json`.

Detailed source contract: [authoring contract](../../_authoring_specs/01_esg_carbon_action_path_authoring_contract.md).


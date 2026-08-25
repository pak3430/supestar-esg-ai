# Runtime contract

## Input

```json
{
  "projectType": "산림탄소상쇄 사업 후보",
  "currentStage": "MONITORING",
  "availableDocuments": ["사업등록 자료", "모니터링 보고서"],
  "intendedUse": "LEARNING",
  "requestedFinalAssertion": false,
  "asOfDate": "2026-08-21"
}
```

Closed stages: `PLANNING`, `ELIGIBILITY`, `REGISTERED`, `IMPLEMENTING`, `MONITORING`, `VERIFIED`, `CERTIFIED`, `UTILIZATION`, `REGISTRY_MANAGED`, `UNKNOWN`.

## Output

`procedure_path.json`, `procedure_checklist.md`, `official_confirmation_questions.md`, `run_record.json`, `result.json`.

Detailed source contract: [authoring contract](../../_authoring_specs/05_forest_carbon_procedure_guidance_authoring_contract.md).


# Runtime contract

## Input

```json
{
  "projectSummary": "산주와 지역사회가 참여하는 산림탄소 사업",
  "environmentEvidence": ["방법론", "모니터링"],
  "socialEvidence": ["권리 동의", "편익배분"],
  "governanceEvidence": ["등록", "검증", "인증"],
  "claimCompleteWithoutAllAxes": false,
  "asOfDate": "2026-08-21"
}
```

Evidence fields may be a non-empty list, object, or string. Empty fields are missing axes.

## Output

`forest_esg_map.json`, `forest_esg_map.md`, `missing_axis_questions.md`, `run_record.json`, `result.json`.

Detailed source contract: [authoring contract](../../_authoring_specs/04_forest_esg_impact_mapping_authoring_contract.md).


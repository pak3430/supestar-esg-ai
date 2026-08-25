# Runtime contract

## Input

```json
{
  "activityDescription": "회사 소유 보일러의 연료 연소",
  "organizationBoundary": "본사와 직접 운영 사업장",
  "sourceOwnershipOrControl": "OWNED_CONTROLLED",
  "purchasedEnergyType": "NONE",
  "valueChainRelation": "NONE",
  "activityData": {"quantity": 100, "unit": "L", "period": "2026-07"},
  "asOfDate": "2026-08-21"
}
```

Closed values:

- ownership/control: `OWNED_CONTROLLED`, `NOT_OWNED_CONTROLLED`, `UNKNOWN`
- purchased energy: `ELECTRICITY`, `STEAM`, `HEAT`, `COOLING`, `NONE`, `UNKNOWN`
- value chain: `UPSTREAM`, `DOWNSTREAM`, `NONE`, `UNKNOWN`

## Output

`scope_classification.json`, `scope_evidence_card.md`, `additional_data_request.md`, `run_record.json`, `result.json`.

Detailed source contract: [authoring contract](../../_authoring_specs/02_scope_activity_classification_authoring_contract.md).


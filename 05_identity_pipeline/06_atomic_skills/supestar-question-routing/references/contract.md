# Runtime contract

## Input

```json
{
  "question": "이 활동은 어느 Scope인가요?",
  "userRole": "ESG_MANAGER",
  "asOfDate": "2026-08-21",
  "providedEvidence": []
}
```

Allowed roles: `LEARNER`, `ESG_MANAGER`, `FOREST_OWNER_OPERATOR`, `REVIEWER`.

Closed routes: `CONCEPT_EXPLANATION`, `ESG_CARBON_PATH`, `SCOPE_CLASSIFICATION`, `CARBON_MARKET_COMPARISON`, `FOREST_ESG_MAPPING`, `FOREST_CARBON_PROCEDURE`, `TRANSACTION_READINESS`, `NEEDS_INPUT`, `OUT_OF_SCOPE`.

`CONCEPT_EXPLANATION`은 Stage 1~5 vault에서 질문과 관련된 Concept Skill과 `Identity → Goal → Task → Knowledge → Method → Skill` 체인을 읽는 지식 Runtime으로 전달한다. 일반 개념 질문을 행동·구매 경로로 강제 변환하지 않는다.

## Output

`context_snapshot.json`, `route_decision.json`, `run_record.json`, `result.json`.

Detailed source contract: [authoring contract](../../_authoring_specs/00_supestar_question_routing_authoring_contract.md).

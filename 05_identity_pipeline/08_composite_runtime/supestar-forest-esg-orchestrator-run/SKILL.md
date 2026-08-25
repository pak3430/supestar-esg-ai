---
name: supestar-forest-esg-orchestrator-run
description: "Execute the deployed Supestar forest-ESG Runtime Composite through one entry point: run the router once, carry its result byte-faithfully, read the selected Stage KAC, invoke at most one approved domain Run Skill, and seal one Composite Run Record."
---

# Supestar Forest ESG Orchestrator Run

하나의 보존된 사용자 입력을 수페스타 Runtime Composite v3로 실행한다. 호출자는 라우터나 도메인 Run Skill을 직접 선택하지 않는다.

## Fixed binding

- Runtime contract: [Runtime Composite Contract v3](../RUNTIME_COMPOSITE_CONTRACT.md)
- Runtime registry: [Composite Run Registry](../COMPOSITE_RUN_REGISTRY.json)
- Prior sealed Composite: [Supestar Forest ESG Orchestrator v2](../../../ccs_composite_authoring/supestar_forest_esg_orchestrator_v2/_skill/supestar-forest-esg-orchestrator_skill/SKILL.md)
- Atomic Run registry: [Run Skill Registry](../../07_run_skills/RUN_SKILL_REGISTRY.json)
- Stage vault: [Supestar MVP v3](../../../ccs_authoring/supestar_mvp_v3/AUTHORING_VAULT_BINDING.md)

## Execute

```bash
python3 ../_shared/run_verified_composite.py \
  --run-composite supestar-forest-esg-orchestrator-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

정상 종료 후 다음 파일을 모두 읽는다.

- `result.json`
- `composite_run_record.json`
- `router_outcome.bin`
- `kac_execution.json`
- `router/run_skill_record.json`
- 선택된 경우 `selected/run_skill_record.json`

## Invariants

1. 라우터는 정확히 한 번 실행한다.
2. 정상 결과는 닫힌 아홉 라우트 중 정확히 하나와 일치한다.
3. 도메인 Run Skill은 최대 하나만 실행한다.
4. 입력 파일은 라우터와 선택 스킬 앞뒤에서 동일한 SHA-256을 유지한다.
5. 질문별 KAC는 실제 Stage 파일 경로와 SHA-256을 기록한다.
6. 선택되지 않은 도메인 스킬은 실행 산출물을 만들지 않는다.
7. 로컬 AI는 이 Composite 밖에서 완료된 결과를 문장으로 표현할 뿐 판정과 근거를 변경하지 않는다.

## Boundary

실제 거래·결제·등록부 변경, 법률·세무·인증 최종판정, 가격·수익 추천, 외부 공개 주장 승인을 수행하지 않는다.

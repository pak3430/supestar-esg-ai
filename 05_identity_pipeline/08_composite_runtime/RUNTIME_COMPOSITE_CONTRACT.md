# Supestar Forest ESG Runtime Composite Contract v3

- contractStatus: `RUNTIME-FINALIZED`
- runtimeCompositeVersion: `0.3.0`
- runComposite: `supestar-forest-esg-orchestrator-run`
- executionMode: one local Composite entry point

## Purpose

질문을 받은 웹 서버가 라우터나 도메인 Run Skill을 직접 고르지 않도록 한다. 서버는 이 Composite만 한 번 호출하며, Composite가 동일 입력 파일을 유지한 채 라우터, 질문별 KAC, 선택된 단 하나의 도메인 Run Skill을 실행하고 하나의 Composite Run Record로 묶는다.

## Input

하나의 JSON 파일을 원본 바이트 소스로 받는다. `question`, `userRole`, `asOfDate`와 도메인별 선택 필드를 포함할 수 있으며, `conversationHistory`는 질문별 Concept 선택에만 사용한다.

원본 입력 파일은 라우터와 선택된 도메인 Run Skill에 같은 경로와 같은 바이트로 전달한다. Composite는 이 파일을 다시 직렬화하거나 수정하지 않는다.

## Closed outcome partition

정상 라우터 결과의 닫힌 집합은 다음 아홉 라우트다.

1. `CONCEPT_EXPLANATION`
2. `ESG_CARBON_PATH`
3. `SCOPE_CLASSIFICATION`
4. `CARBON_MARKET_COMPARISON`
5. `FOREST_ESG_MAPPING`
6. `FOREST_CARBON_PROCEDURE`
7. `TRANSACTION_READINESS`
8. `NEEDS_INPUT`
9. `OUT_OF_SCOPE`

라우터 프로세스 실패는 별도 터미널 `ROUTING_EXECUTION_FAILURE`로 기록한다. 정상 라우트와 프로세스 실패 터미널을 합친 실행 결과는 정확히 하나만 선택되어야 한다.

## Execution

1. 입력 파일 SHA-256을 고정한다.
2. `supestar-question-routing-run`을 정확히 한 번 실행한다.
3. 완료된 `router/result.json`을 `router_outcome.bin`으로 byte-faithful하게 운반하고 직접 바이트 비교한다.
4. 라우터 결과를 한 번 읽어 정확히 한 라우트를 선택한다.
5. 질문과 라우트에 맞는 봉인 Stage `Identity → Goal → Task → Knowledge → Method → Skill` 체인을 읽고 해시를 기록한다.
6. 도메인 라우트일 때만 매핑된 Run Skill 하나를 같은 입력 파일로 실행한다.
7. 개념·입력보완·범위밖 라우트에서는 도메인 Run Skill을 실행하지 않는다.
8. Composite 결과와 Composite Run Record를 기록하고 입력 파일의 사후 SHA-256을 다시 확인한다.

## Output

- `result.json`: 라우트, 선택된 Run Skill, KAC, 최종 자식 결과와 실행 추적
- `composite_run_record.json`: Composite·입력·자식 실행·파일 해시·분기 카디널리티 증거
- `router_outcome.bin`: 라우터 완료 결과의 byte-faithful carriage
- `kac_execution.json`: 질문별 Stage 체인과 원문 근거 해시
- `router/`: 라우터 Run Skill 산출물과 Run Record
- `selected/`: 선택된 경우에만 존재하는 단 하나의 도메인 Run Skill 산출물과 Run Record

## Provenance and version boundary

Runtime v3는 기존 봉인 Composite v2의 라우터-단일분기-터미널 구조를 보존하고, 현재 라우터 계약에 추가된 `CONCEPT_EXPLANATION`을 실제 KAC 실행 분기로 결합한 코드 기반 배포 어댑터다. 기존 v2 저작 vault는 수정하지 않는다.

- prior sealed Composite -> [v2 Composite Skill](../../ccs_composite_authoring/supestar_forest_esg_orchestrator_v2/_skill/supestar-forest-esg-orchestrator_skill/SKILL.md)
- current router contract -> [question routing contract](../06_atomic_skills/supestar-question-routing/references/contract.md)
- Stage vault -> [supestar_mvp_v3](../../ccs_authoring/supestar_mvp_v3/AUTHORING_VAULT_BINDING.md)
- Composite registry -> [COMPOSITE_RUN_REGISTRY.json](COMPOSITE_RUN_REGISTRY.json)

## Safety boundary

이 Composite는 로컬 판단·설명 준비까지만 수행한다. 실제 거래, 결제, 등록부 변경, 법률·세무 결론, 인증 최종판정, 외부 공개 주장 승인을 실행하지 않는다. 로컬 AI 자연어 표현은 Composite가 완료된 뒤 별도 비권위 계층에서 수행한다.

# Supestar Question Routing Knowledge

## Closed routes

`ESG_CARBON_PATH`, `SCOPE_CLASSIFICATION`, `CARBON_MARKET_COMPARISON`, `FOREST_ESG_MAPPING`, `FOREST_CARBON_PROCEDURE`, `TRANSACTION_READINESS`, `NEEDS_INPUT`, `OUT_OF_SCOPE`

## Rules

- 금지 의도는 도메인 매칭보다 먼저 평가한다.
- ESG에서 다른 단계로 이어지는 이유를 묻는 질문은 경로 질문으로 우선한다.
- 둘 이상의 직접 도메인이 동일하게 매칭되면 사용자에게 선택을 요청한다.
- 입력 원문을 재작성하지 않고 ContextSnapshot에 보존한다.

## Evidence

- [KAC 핵심 원자 Skill](../../ccs/_input/_document/06_산림_ESG_지식의_KAC_실행구조.md#3-핵심-원자-skill)
- [실행 오케스트레이션](../../ccs/_input/_document/08_ESG_AX_Concept_Build_Run_구조요구사항.md#7-실행-오케스트레이션)

## Chain position

- ← requiresKnowledge — [Supestar Question Routing Task](../03_task/supestar_question_routing_task.md)
- → appliedThrough — [Supestar Question Routing Method](../05_method/supestar_question_routing_method.md)


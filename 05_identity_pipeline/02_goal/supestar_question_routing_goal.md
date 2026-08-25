# Supestar Question Routing Goal

사용자의 질문·역할·기준일을 보존하면서 수페스타 MVP가 지원하는 하나의 실행 경로 또는 명시적인 보완·중단 경로로 전달한다.

## Success

- route는 닫힌 열거값 중 정확히 하나다.
- 복수 의도는 임의 선택하지 않고 `NEEDS_INPUT`으로 보낸다.
- 실제 거래·결제·법률·세무 확정 요청은 `OUT_OF_SCOPE`로 차단한다.

## Chain position

- ← definesGoal — [USER_QUESTION](../01_identity/P0_TARGET_IDENTITY_BINDINGS.md)
- → requiresTask — [Supestar Question Routing Task](../03_task/supestar_question_routing_task.md)


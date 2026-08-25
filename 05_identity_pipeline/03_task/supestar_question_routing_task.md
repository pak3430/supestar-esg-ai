# Supestar Question Routing Task

질문·사용자 역할·기준일을 검사하고, 금지 요청을 먼저 차단한 뒤 허용된 도메인 의도를 매칭하여 하나의 RouteDecision과 ContextSnapshot을 만든다.

## Required outputs

- `context_snapshot.json`
- `route_decision.json`
- `run_record.json`

## Chain position

- ← requiresTask — [Supestar Question Routing Goal](../02_goal/supestar_question_routing_goal.md)
- → requiresKnowledge — [Supestar Question Routing Knowledge](../04_knowledge/supestar_question_routing_knowledge.md)


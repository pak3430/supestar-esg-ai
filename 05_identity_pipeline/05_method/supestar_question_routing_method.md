# Supestar Question Routing Method

1. JSON 입력의 `question`, `userRole`, `asOfDate`를 검사한다.
2. 금지 의도를 먼저 검사해 `OUT_OF_SCOPE`을 결정한다.
3. 경로 질문 우선규칙과 도메인 keyword rules를 적용한다.
4. 단일 매칭은 해당 route, 0개 또는 복수 매칭은 `NEEDS_INPUT`으로 기록한다.
5. ContextSnapshot·RouteDecision·RunRecord를 파일로 저장한다.

## Implementation

- [Python runner](../06_atomic_skills/supestar-question-routing/scripts/run.py)
- [Contract reference](../06_atomic_skills/supestar-question-routing/references/contract.md)

## Chain position

- ← appliedThrough — [Supestar Question Routing Knowledge](../04_knowledge/supestar_question_routing_knowledge.md)
- → developsSkill — [supestar-question-routing](../06_atomic_skills/supestar-question-routing/SKILL.md)


---
name: knowledge_action_chain_method
description: "Knowledge-Action Chain 질문을 입력 승인부터 근거 판정까지 순차 처리한다."
---

# Knowledge-Action Chain Method

1. 질문, 사용자 역할, 기준일을 입력으로 승인한다.
2. Knowledge-Action Chain 주장과 연결된 source-linked Identity 및 원문 근거를 읽는다.
3. 정의·경계·관계·필수 증거와 금지조건을 점검한다.
4. PROCEED·REVIEW·STOP 중 하나와 근거 포인터를 기록한다.
5. 실행 산출물과 다음 행동을 Run Record에 연결한다.

## Chain position

- ← appliedThrough — [Knowledge-Action Chain Knowledge](../_knowledge/knowledge_action_chain_knowledge.md)
- → developsSkill — [Knowledge-Action Chain Concept Assessment Skill](../_skill/KNOWLEDGE_ACTION_CHAIN/SKILL.md)

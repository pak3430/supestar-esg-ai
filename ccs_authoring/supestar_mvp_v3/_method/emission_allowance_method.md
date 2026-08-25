---
name: emission_allowance_method
description: "배출권 질문을 입력 승인부터 근거 판정까지 순차 처리한다."
---

# 배출권 Method

1. 질문, 사용자 역할, 기준일을 입력으로 승인한다.
2. 배출권 주장과 연결된 source-linked Identity 및 원문 근거를 읽는다.
3. 정의·경계·관계·필수 증거와 금지조건을 점검한다.
4. PROCEED·REVIEW·STOP 중 하나와 근거 포인터를 기록한다.
5. 실행 산출물과 다음 행동을 Run Record에 연결한다.

## Chain position

- ← appliedThrough — [배출권 Knowledge](../_knowledge/emission_allowance_knowledge.md)
- → developsSkill — [배출권 Concept Assessment Skill](../_skill/EMISSION_ALLOWANCE/SKILL.md)

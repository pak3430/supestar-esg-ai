---
name: disposition_right_method
description: "처분권 질문을 입력 승인부터 근거 판정까지 순차 처리한다."
---

# 처분권 Method

1. 질문, 사용자 역할, 기준일을 입력으로 승인한다.
2. 처분권 주장과 연결된 source-linked Identity 및 원문 근거를 읽는다.
3. 정의·경계·관계·필수 증거와 금지조건을 점검한다.
4. PROCEED·REVIEW·STOP 중 하나와 근거 포인터를 기록한다.
5. 실행 산출물과 다음 행동을 Run Record에 연결한다.

## Chain position

- ← appliedThrough — [처분권 Knowledge](../_knowledge/disposition_right_knowledge.md)
- → developsSkill — [처분권 Concept Assessment Skill](../_skill/DISPOSITION_RIGHT/SKILL.md)

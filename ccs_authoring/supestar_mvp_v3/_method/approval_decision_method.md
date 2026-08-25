---
name: approval_decision_method
description: "ApprovalDecision 질문을 입력 승인부터 근거 판정까지 순차 처리한다."
---

# ApprovalDecision Method

1. 질문, 사용자 역할, 기준일을 입력으로 승인한다.
2. ApprovalDecision 주장과 연결된 source-linked Identity 및 원문 근거를 읽는다.
3. 정의·경계·관계·필수 증거와 금지조건을 점검한다.
4. PROCEED·REVIEW·STOP 중 하나와 근거 포인터를 기록한다.
5. 실행 산출물과 다음 행동을 Run Record에 연결한다.

## Chain position

- ← appliedThrough — [ApprovalDecision Knowledge](../_knowledge/approval_decision_knowledge.md)
- → developsSkill — [ApprovalDecision Concept Assessment Skill](../_skill/APPROVAL_DECISION/SKILL.md)

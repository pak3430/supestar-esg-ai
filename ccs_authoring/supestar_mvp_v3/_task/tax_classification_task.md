---
name: tax_classification_task
description: "세무분류 관련 질문과 증거를 경계 기준에 따라 평가한다."
---

# 세무분류 Task

질문에서 세무분류 관련 주장을 식별하고, source-linked 근거와 개념 경계를 확인해 PROCEED·REVIEW·STOP 결과를 기록한다.

## Chain position

- ← requiresTask — [세무분류 Goal](../_goal/tax_classification_goal.md)
- → requiresKnowledge — [세무분류 Knowledge](../_knowledge/tax_classification_knowledge.md)

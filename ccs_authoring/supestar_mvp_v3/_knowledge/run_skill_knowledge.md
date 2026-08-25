---
name: run_skill_knowledge
description: "Run Skill 판단에 필요한 정의·관계·증거·금지 경계를 정리한다."
---

# Run Skill Knowledge

- Definition: Run Skill은(는) 원문이 독립 구조 단위로 사용하는 개념이다.
- Evidence: 08_ESG_AX_Concept_Build_Run_구조요구사항.md L25-L25; SHA-256 cb6b20d918a96ca8757cfc97ccf49bc7c69ee9843234a98c1af4b2026196376c.
- Decision rule: 필수 근거와 경계가 모두 있으면 PROCEED, 공식 확인이 필요하면 REVIEW, 핵심 증거가 없거나 금지행위에 닿으면 STOP.
- Prohibition: 실제 거래, 자동결제, 가격·수익 추천, 법률·세무 자문, 인증 자동판정을 수행하지 않는다.

## Chain position

- ← requiresKnowledge — [Run Skill Task](../_task/run_skill_task.md)
- → appliedThrough — [Run Skill Method](../_method/run_skill_method.md)

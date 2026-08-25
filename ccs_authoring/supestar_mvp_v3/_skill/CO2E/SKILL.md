---
name: co2e-concept-assessment
description: "CO2e 관련 질문을 source-linked 근거와 경계 규칙으로 평가해 PROCEED, REVIEW 또는 STOP을 기록한다. 산림 ESG 설명·판단에서 이 개념의 의미나 증거가 필요할 때 사용한다."
---

# CO2e Concept Assessment

CO2e을(를) 인접 개념과 섞지 않고, 원문 근거와 기준일을 따라 설명·판단한다.

## Interface

- Input: 사용자 질문, 사용자 역할, 기준일, 사용 가능한 증거.
- Output: 적용 Identity·관계, 근거 포인터, PROCEED/REVIEW/STOP, 다음 행동.

## Procedure

1. 입력이 존재하고 요청 범위가 금지행위를 요구하지 않는지 확인한다.
2. [CO2E](../../_identity/CO2E.md)와 source grounding을 읽는다.
3. [CO2e Knowledge](../../_knowledge/co2e_knowledge.md)의 정의·경계·증거 규칙을 적용한다.
4. 증거가 충분하면 PROCEED, 공식 확인이 남으면 REVIEW, 핵심 증거가 없거나 금지행위면 STOP을 기록한다.
5. 사용한 근거, 산출물, 판정 이유를 Run Record에 연결한다.

## Stop conditions

- 필수 경계·근거·기준일이 없거나 확인되지 않은 법률·세무·계약·인증 결론을 요구하면 STOP.
- 실제 거래·자동결제·가격 및 수익 추천은 수행하지 않는다.

## Derivation

- Identity: [CO2E](../../_identity/CO2E.md)
- Goal: [CO2e Goal](../../_goal/co2e_goal.md)
- Task: [CO2e Task](../../_task/co2e_task.md)
- Knowledge: [CO2e Knowledge](../../_knowledge/co2e_knowledge.md)
- Method: [CO2e Method](../../_method/co2e_method.md)

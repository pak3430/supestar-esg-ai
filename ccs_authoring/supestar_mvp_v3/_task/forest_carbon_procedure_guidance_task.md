---
name: forest_carbon_procedure_guidance
description: "입력된 산림탄소 사업 상태와 문서 증거를 공식 절차 순서에 대조해 다음 단계 안내 패키지와 판정 기록을 만드는 과업이다."
---

# 산림탄소 공식 절차 안내 Task

## Task

산림탄소 사업의 기준일 현재 주장 상태와 이용 가능한 문서를 받아 공식 절차를 앞에서부터 검토하고, 증거로 완료가 확인되는 단계·최초 차단 단계·다음 단계의 담당주체·선행조건·필요 산출물을 연결한 안내 패키지를 작성한다.

## Required work

1. `projectType`, `currentStage`, `intendedUse`, `asOfDate`를 필수로 받고 `availableDocuments`를 선택적으로 받는다. 모르는 `projectType` 또는 `currentStage`는 추정하지 않고 `UNKNOWN`으로 유지한다.
2. `currentStage`는 `PLANNING`, `ELIGIBILITY`, `REGISTERED`, `IMPLEMENTING`, `MONITORING`, `VERIFIED`, `CERTIFIED`, `REGISTRY_MANAGED`, `UNKNOWN` 중 하나로 받되, 이 주장을 문서로 확인된 완료 상태와 별도로 기록한다.
3. `사업계획 → 타당성·적격성 검토 → 사업등록 → 실행 → 모니터링 → 독립 검증 → 인증 → 거래 또는 비거래 활용 → 등록부 상태관리`를 순서대로 걸으며 각 단계의 완료 증거를 확인한다. 증거가 없는 단계와 그 이후 단계는 통과한 것으로 간주하지 않는다.
4. 증거로 확인된 현재 위치와 최초 미확인 선행단계를 기준으로 `completedStages`, `blockedStage`, `nextStage`를 정하고, 다음 단계의 `actors`, 선행조건, `requiredArtifacts`를 연결한다.
5. 사업유형·제도 적용, 등록 및 인증의 현재 유효상태, 거래형·비거래형 경로와 허용 표현 등 공식 확인이 필요한 공백을 질문으로 바꾼다.
6. 결정 규칙으로 `PROCEED`, `REVIEW`, `STOP` 중 하나를 부여하고 다음을 만든다.
   - `procedure_path.json`: `currentStage`, `completedStages`, `blockedStage`, `nextStage`, `actors`, `requiredArtifacts`
   - `procedure_checklist.md`: 단계별 완료 증거·미충족 선행조건·다음 행동 체크리스트
   - `official_confirmation_questions.md`: 제도운영자에게 확인할 질문
   - `RunRecord`: 현재상태·근거·다음단계·판정

## Decision boundary

- `PROCEED`: 현재 단계와 완료 증거가 일치하고 다음 단계 안내가 가능한 경우.
- `REVIEW`: 사업유형·제도 적용·등록·인증의 유효상태를 공식 확인해야 하는 경우.
- `STOP`: 선행 등록·검증·인증 증거 없이 거래, 사용완료 또는 공식 인증을 확정하려는 경우.

판정은 안내 패키지의 절차상 상태일 뿐 외부 기관의 결정이 아니다. 이 과업은 문서를 제출하거나 기관에 질의하고, 등록·인증·거래·등록부 상태를 변경하거나, 법률·세무 결론을 확정하지 않는다. 산림탄소 사업의 개념 평가 및 E/S/G 영향·책임 매핑도 수행하지 않는다.

## Chain position

← requiresTask — [forest_carbon_procedure_guidance Goal](../_goal/forest_carbon_procedure_guidance_goal.md)

→ requiresKnowledge — [forest_carbon_procedure_guidance](../_knowledge/forest_carbon_procedure_guidance_knowledge.md)

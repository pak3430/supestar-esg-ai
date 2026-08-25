---
name: forest_carbon_procedure_guidance
description: "산림탄소 사업의 증거로 확인되는 현재 공식 절차 단계를 기준으로 다음 단계·담당주체·선행조건·필요 산출물을 안내하는 목표다."
---

# 산림탄소 공식 절차 안내 Goal

## Goal

`FOREST_CARBON_PROJECT`의 현재 상태를 입력받아, 완료 증거가 확인된 공식 절차 단계와 확인되지 않은 선행단계를 구분하고 다음 단계의 담당주체·선행조건·필요 산출물·공식 확인 질문을 제시한다.

이 목표는 `사업계획 → 타당성·적격성 검토 → 사업등록 → 실행 → 모니터링 → 독립 검증 → 인증 → 거래 또는 비거래 활용 → 등록부 상태관리` 순서를 따른다. 증거가 없는 단계는 완료된 것으로 간주하지 않으며, 사업유형·제도 적용·등록·인증의 유효상태처럼 공개 자료만으로 확정할 수 없는 사항은 제도운영자에게 확인하도록 남긴다.

## Success condition

- 필수 입력 `projectType`, `currentStage`, `intendedUse`, `asOfDate`와 선택 입력 `availableDocuments`를 받아 현재 주장과 증거를 분리한다.
- `currentStage`, `completedStages`, `blockedStage`, `nextStage`, `actors`, `requiredArtifacts`를 포함한 절차 경로, 단계별 체크리스트, 공식 확인 질문을 산출한다.
- 근거와 다음 단계의 관계에 따라 `PROCEED`, `REVIEW`, `STOP` 중 하나를 부여하고 현재상태·근거·다음단계·판정을 `RunRecord`에 남긴다.

## Boundary

이 목표는 공식 절차의 순서와 증거 기반 다음 행동 안내에만 한정된다. 산림탄소 사업 개념의 의미·경계를 재평가하지 않고, 환경·사회·지배구조 영향과 책임을 매핑하지 않는다. 외부 제출·등록부 변경·거래 실행·검증·인증을 수행하거나 기관의 판단, 등록·인증 상태, 법률·세무 결과를 대신 확정하지 않는다.

## Grounding

- [작성 계약](../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/05_forest_carbon_procedure_guidance_authoring_contract.md)
- [산림탄소 공식 절차와 확인 질문](../../../ccs/_input/_document/04_%EC%82%B0%EB%A6%BC_ESG_E_S_G_%EB%B0%8F_%EC%9E%84%EC%97%85%EC%A7%84%ED%9D%A5%EC%9B%90_%EC%83%9D%ED%83%9C%EA%B3%84.md#4-%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C-%EA%B3%B5%EC%8B%9D-%EC%A0%88%EC%B0%A8)

## Chain position

← definesGoal — [FOREST_CARBON_PROJECT](../_identity/FOREST_CARBON_PROJECT.md)

→ requiresTask — [forest_carbon_procedure_guidance](../_task/forest_carbon_procedure_guidance_task.md)

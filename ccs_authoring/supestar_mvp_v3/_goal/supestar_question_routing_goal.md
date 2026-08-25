# Supestar Question Routing Goal

## Goal

`USER_QUESTION`을 수페스타 MVP가 실행할 수 있는 입력 계약으로 받아, 사용자의 질문·역할·기준일을 보존하고 정확히 하나의 허용된 실행 route 또는 입력보완 route를 반환한다.

이 목표는 `USER_QUESTION`의 의미와 경계를 평가하는 기존 개념 체인을 반복하지 않는다. 여기서는 질문을 후속 산림 ESG 기능에 전달할 수 있도록 구조화하고, 복합 의도·입력 부족·금지 범위를 명시적으로 분기하는 실행 방향을 연다.

## Success conditions

- `question`, `userRole`, `asOfDate`를 필수 입력으로 취급한다.
- `providedEvidence`는 선택 입력으로 원문 상태를 보존한다.
- 허용된 8개 route 밖의 값을 만들지 않는다.
- 단일 정상 의도에는 정확히 하나의 실행 route를 반환한다.
- 복수 의도 또는 필수 입력 부족에는 임의 선택 대신 `NEEDS_INPUT`을 반환한다.
- 실제 거래·결제·등록부 변경, 가격·수익 추천, 법률·세무·계약·인증 확정, 개인정보·비공개 정보 추정 요구에는 `OUT_OF_SCOPE`를 반환한다.
- 결정 근거와 상태를 `ContextSnapshot`, `RouteDecision`, `ClarifyingQuestions`, `status`, `RunRecord`로 추적 가능하게 남긴다.

## Boundary

- IN: 질문 라우팅, 필수 입력 확인, 폐쇄된 route 결정, 보완 질문, 정지 판정과 실행기록 명세.
- OUT: 후속 도메인 Skill의 실제 실행, 실제 매매·결제·등록부 변경, 가격·투자 추천, 법률·세무·계약·인증의 공식 확정.
- 이 체인은 authoring candidate이며 Runtime 등록이나 배포를 수행하지 않는다.

## Chain position

← definesGoal — [USER_QUESTION](../_identity/USER_QUESTION.md)

→ requiresTask — [Supestar Question Routing Task](../_task/supestar_question_routing_task.md)

## Grounding

- fixed authoring contract: [수페스타 질문 라우팅 추가 체인 작성 계약](../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/00_supestar_question_routing_authoring_contract.md)
- KAC execution structure: [산림 ESG 지식의 KAC 실행구조](../../../ccs/_input/_document/06_%EC%82%B0%EB%A6%BC_ESG_%EC%A7%80%EC%8B%9D%EC%9D%98_KAC_%EC%8B%A4%ED%96%89%EA%B5%AC%EC%A1%B0.md)
- ecosystem workflow: [전체생태계 노드링크 워크플로우](../../../ccs/_input/_document/07_%EC%A0%84%EC%B2%B4%EC%83%9D%ED%83%9C%EA%B3%84_%EB%85%B8%EB%93%9C%EB%A7%81%ED%81%AC_%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0.md)
- Concept·Build·Run requirements: [ESG AX 구조 요구사항](../../../ccs/_input/_document/08_ESG_AX_Concept_Build_Run_%EA%B5%AC%EC%A1%B0%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD.md)

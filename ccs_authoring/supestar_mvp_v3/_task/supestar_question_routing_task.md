# Supestar Question Routing Task

## Task

질문 라우팅 요청 하나를 받아 입력 계약과 금지 범위를 먼저 검사하고, 질문의 핵심 의도를 폐쇄된 route 규칙과 대조하여 후속 기능 하나로 전달할 `RouteDecision`을 작성한다.

## Required actions

1. 원 질문, 사용자 역할, 기준일, 제공 근거를 `ContextSnapshot`에 손실 없이 담는다.
2. `question`이 비어 있지 않은지, `userRole`이 허용된 네 역할 중 하나인지, `asOfDate`가 `YYYY-MM-DD`인지 검사한다.
3. STOP 조건을 먼저 검사하고 하나라도 일치하면 `OUT_OF_SCOPE`와 `STOP`을 반환한다.
4. 정상 의도를 아래 여섯 실행 route와 대조한다.
   - `ESG_CARBON_PATH`
   - `SCOPE_CLASSIFICATION`
   - `CARBON_MARKET_COMPARISON`
   - `FOREST_ESG_MAPPING`
   - `FOREST_CARBON_PROCEDURE`
   - `TRANSACTION_READINESS`
5. 일치하는 정상 route가 정확히 하나이면 그 route와 `PROCEED`를 반환한다.
6. 필수 입력이 없거나 정상 route가 둘 이상이면 `NEEDS_INPUT`, `REVIEW`, 필요한 선택 질문만 반환한다.
7. 어떤 허용 의도에도 해당하지 않으면 `OUT_OF_SCOPE`와 `STOP`을 반환한다.
8. 적용한 규칙 버전과 결과를 `RunRecord`에 기록한다.

## Completion criteria

- route는 허용된 8개 값 중 정확히 하나다.
- 결과에는 `ContextSnapshot`, `RouteDecision`, `ClarifyingQuestions`, `status`, `RunRecord`가 모두 있다.
- `RouteDecision.reason`은 확률이나 막연한 신뢰도가 아니라 실제로 일치한 규칙 또는 정지 조건을 가리킨다.
- `PROCEED`, `REVIEW`, `STOP`은 각각 정상 단일 route, 입력보완 route, 금지·범위외 route에만 대응한다.
- 이 Task는 후속 Skill을 실행하지 않고 오직 전달 route를 결정한다.

## Chain position

← requiresTask — [Supestar Question Routing Goal](../_goal/supestar_question_routing_goal.md)

→ requiresKnowledge — [Supestar Question Routing Knowledge](../_knowledge/supestar_question_routing_knowledge.md)

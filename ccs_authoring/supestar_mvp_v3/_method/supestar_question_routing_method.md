# Supestar Question Routing Method

## Method

하나의 요청을 다음 우선순위로 처리한다. 각 단계는 앞 단계가 확정된 뒤에만 진행하며, route를 하나로 확정할 수 없는 경우 추측으로 빈칸을 채우지 않는다.

### 1. Capture the context

- `question`, `userRole`, `asOfDate`, `providedEvidence`를 입력에서 읽는다.
- 원 질문과 제공 근거는 내용을 바꾸지 않고 `ContextSnapshot`에 복사한다.
- 입력에 없는 사실, 역할, 날짜, 증거를 추정하지 않는다.

### 2. Validate required inputs

- `question`이 비어 있으면 부족 필드로 기록한다.
- `userRole`이 `LEARNER`, `ESG_MANAGER`, `FOREST_OWNER_OPERATOR`, `REVIEWER` 중 하나가 아니면 부족·수정 필드로 기록한다.
- `asOfDate`가 `YYYY-MM-DD` 형식이 아니면 부족·수정 필드로 기록한다.
- 부족·수정 필드가 하나라도 있으면 route=`NEEDS_INPUT`, status=`REVIEW`로 종료하고 해당 필드만 묻는 `ClarifyingQuestions`를 작성한다.

### 3. Apply STOP gates before normal routing

질문이 다음 중 하나를 요구하는지 검사한다.

1. 실제 매매, 결제 또는 등록부 변경
2. 가격, 수익 또는 투자 추천
3. 법률, 세무, 계약 또는 인증 결과의 공식 확정
4. 개인정보 또는 비공개 기관정보의 추정

하나라도 일치하면 route=`OUT_OF_SCOPE`, status=`STOP`으로 종료한다. `RouteDecision.reason`에는 일치한 정지 조건을 명시하고 외부 변경을 실행하지 않는다.

### 4. Match only the six normal routes

입력과 STOP gate를 통과한 질문의 핵심 의도를 다음 규칙과 대조한다.

- ESG에서 탄소·측정·Scope·SDGs·시장으로 이어지는 이유 → `ESG_CARBON_PATH`
- 활동·배출원의 Scope 1·2·3 분류 → `SCOPE_CLASSIFICATION`
- CCM·VCM·배출권·크레딧·상쇄 비교 → `CARBON_MARKET_COMPARISON`
- 산림탄소의 환경·사회·지배구조 영향·책임 → `FOREST_ESG_MAPPING`
- 산림탄소 계획·등록·모니터링·검증·인증·등록부 절차 → `FOREST_CARBON_PROCEDURE`
- 거래 전 권리·계약·세무·결제·이전·증빙 준비도 → `TRANSACTION_READINESS`

### 5. Enforce one-route cardinality

- 일치가 1개이면 그 route와 status=`PROCEED`를 반환한다.
- 일치가 2개 이상이면 route=`NEEDS_INPUT`, status=`REVIEW`를 반환하고 사용자가 의도 하나를 선택할 수 있는 질문을 작성한다.
- 일치가 0개이면 route=`OUT_OF_SCOPE`, status=`STOP`을 반환한다.
- 여러 route를 배열로 반환하거나 임의의 우선순위로 하나를 고르지 않는다.

### 6. Materialize the output contract

결과를 다음 다섯 객체로 작성한다.

1. `ContextSnapshot`: `question`, `userRole`, `asOfDate`, `providedEvidence`
2. `RouteDecision`: `route`, `matchedRule`, `reason`
3. `ClarifyingQuestions`: 필요한 질문 목록 또는 빈 목록
4. `status`: `PROCEED`, `REVIEW`, `STOP` 중 하나
5. `RunRecord`: `ruleVersion`, `asOfDate`, `selectedRoute`, `status`

### 7. Verify before returning

- route가 폐쇄된 8개 값 중 하나인지 확인한다.
- route cardinality가 정확히 1인지 확인한다.
- route와 status 대응이 계약과 일치하는지 확인한다.
- `PROCEED`여도 후속 Skill이 실행되었다고 기록하지 않는다.
- 실제 거래·결제·등록부 변경, 법률·세무·계약·인증 확정, Runtime 등록 또는 배포를 수행하지 않는다.

## Failure handling

출력 객체를 모두 만들 수 없거나 route/status 불변식을 만족하지 못하면 성공 결과를 만들지 않는다. 누락된 입력을 특정할 수 있으면 `NEEDS_INPUT`/`REVIEW`로 끝내고, 금지 범위 또는 계약 위반이면 `OUT_OF_SCOPE`/`STOP`으로 끝낸다.

## Chain position

← appliedThrough — [Supestar Question Routing Knowledge](../_knowledge/supestar_question_routing_knowledge.md)

→ developsSkill — [Supestar Question Routing Skill](../_skill/supestar-question-routing/SKILL.md)

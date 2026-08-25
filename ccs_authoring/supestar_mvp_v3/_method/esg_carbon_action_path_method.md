# ESG→탄소 행동경로 Method

## Application method

### 1. 입력과 금지 요구 검사

- `question`, `userRole`, `asOfDate`가 있는지 확인하고 `focus`가 있으면 허용값인지 검사한다.
- 실제 거래·구매·결제·등록부 변경을 요구하거나, 측정 없이 상쇄 또는 탄소중립 확정을 요구하면 `STOP`으로 종료한다.

### 2. 시작점과 종료점 결정

- 질문에서 사용자가 이미 알고 있거나 제공한 개념을 시작점으로 잡는다.
- `focus`가 있으면 대응 노드를 종료점으로 삼고, 없으면 질문이 요구하는 가장 가까운 지식 노드를 종료점으로 삼는다.
- 조직·운영 경계나 활동자료가 없는데 종료점이 시장·상쇄 판단이면 `REVIEW`로 제한한다.

### 3. 최소 선행경로 선택

- 지식에 정의된 기본 순서에서 시작점부터 종료점까지 연속된 노드만 선택한다.
- 측정과 경계에 필요한 중간 노드를 생략하지 않는다.
- 종료점 직후 사용자가 수행할 수 있는 다음 행동 하나를 별도로 기록한다.

### 4. 이유와 근거 결합

- 인접 노드마다 “왜 다음 단계가 필요한가”를 한 문장으로 작성한다.
- 핵심 claim마다 원문 식별자와 `asOfDate`를 `evidenceRefs`에 연결한다.
- 연결할 근거가 부족하면 해당 claim을 확정하지 않고 `REVIEW`한다.

### 5. 산출물 생성

- `ActionPath.json`에 `orderedNodes`, `orderedEdges`, `reasonPerEdge`, `evidenceRefs`를 기록한다.
- `explanation_cards.md`에 사용자 역할에 맞는 쉬운 설명을 기록한다.
- `next_action_checklist.md`를 `확인할 자료`, `담당 주체`, `생성 산출물`로 나눈다.
- `RunRecord`에 선택한 Identity·Relation·근거·산출물 경로와 최종 상태를 기록한다.

### 6. 최종 상태 결정

1. 금지 요구가 있으면 `STOP`.
2. 금지 요구는 없지만 필수 입력·경계·활동자료·근거가 판단에 부족하면 `REVIEW`.
3. 질문 범위와 기준일이 있고 필요한 설명 근거가 연결되면 `PROCEED`.

## Authority boundary

이 Method는 설명 가능한 경로와 준비 행동을 생성할 뿐이다. 배출량 산정의 최종 검증, 인증·법률·세무 판단, 탄소중립 선언, 크레딧 거래·결제 또는 외부 시스템 변경 권한을 부여하지 않는다.

## Chain position

- ← appliedThrough — [ESG→탄소 행동경로 Knowledge](../_knowledge/esg_carbon_action_path_knowledge.md)
- → developsSkill — [esg-carbon-action-path](../_skill/esg-carbon-action-path/SKILL.md)

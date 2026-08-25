# ESG→탄소 행동경로 Task

## Required action

사용자의 ESG·탄소 질문에서 시작점과 종료점을 정하고, 필요한 선행 개념을 보존한 최소 경로를 선택해 이유·근거·다음 행동과 함께 설명 가능한 산출물로 만든다.

## Inputs

- `question` — ESG와 탄소 행동의 연결을 묻는 질문. 필수.
- `userRole` — 사용자의 역할. 필수.
- `asOfDate` — 근거와 안내의 기준일. 필수.
- `focus` — 선택값이며 `MEASUREMENT`, `SCOPE`, `SDGS`, `MARKET`, `FOREST_CARBON` 중 하나.

## Work

1. 질문과 `focus`에서 경로의 시작점과 종료점을 결정한다.
2. 측정, 조직·운영 경계, Scope, 활동자료·배출계수, CO2e, 직접감축과 잔여배출을 포함한 필수 선행관계를 점검한다.
3. 종료점까지 필요한 최소 노드와 edge를 순서대로 선택하고 각 edge의 필요 이유를 기록한다.
4. 핵심 claim에 원문 근거와 `asOfDate`를 연결한다.
5. 설명 카드와 자료·주체·산출물 기준의 다음 행동 체크리스트를 만든다.
6. 입력과 근거의 충분성 및 금지 요구를 검사해 `PROCEED`, `REVIEW`, `STOP` 중 하나를 기록한다.

## Completion conditions

- `ActionPath.json`, `explanation_cards.md`, `next_action_checklist.md`와 `RunRecord`가 생성된다.
- 측정 자료가 없는데 시장·상쇄 판단까지 요구하면 `REVIEW`한다.
- 측정 없이 상쇄·탄소중립을 확정하거나 실제 거래를 요구하면 `STOP`하고 실행하지 않는다.

## Chain position

- ← requiresTask — [ESG→탄소 행동경로 Goal](../_goal/esg_carbon_action_path_goal.md)
- → requiresKnowledge — [ESG→탄소 행동경로 Knowledge](../_knowledge/esg_carbon_action_path_knowledge.md)

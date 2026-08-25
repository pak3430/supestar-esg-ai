# Scope 활동 분류 Task

## Required action

하나의 조직 활동 입력을 받아 조직·운영 경계와 활동의 관계정보를 확인하고, Scope 정의에 맞는 후보·판정 근거·미해결 항목·다음 질문을 산출한다.

## Input obligations

- 활동 설명과 기준일을 확인한다.
- 포함 법인·사업장·운영통제 범위를 확인한다.
- 배출원에 대한 소유·통제 여부를 확인한다.
- 구매 전기·스팀·열·냉방 여부를 확인한다.
- 조직의 상류·하류 가치사슬 관계를 확인한다.
- 배출량 계산이 요청되면 수량·단위·기간과 배출계수의 존재를 별도로 확인한다.

## Completion obligations

- 정의에 부합하는 단일 후보가 있으면 `PROCEED`와 함께 후보 및 규칙 추적을 남긴다.
- 핵심 입력이 불명확하거나 충돌하면 `REVIEW`와 함께 미해결 항목 및 추가 자료 요청을 남긴다.
- Scope 정의를 위반하는 분류 요구이면 `STOP`과 위반 근거를 남긴다.
- 후보 분류와 배출량 계산을 혼동하지 않는다.

## Required outputs

- `scope_classification.json`
- `scope_evidence_card.md`
- `additional_data_request.md`
- `status`
- `RunRecord`

## Chain position

- ← requiresTask — [scope_activity_classification_goal](../_goal/scope_activity_classification_goal.md)
- → requiresKnowledge — [scope_activity_classification_knowledge](../_knowledge/scope_activity_classification_knowledge.md)

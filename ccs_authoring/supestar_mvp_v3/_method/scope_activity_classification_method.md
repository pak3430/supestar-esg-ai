# Scope 활동 분류 Method

## Method

### 1. Admit and normalize the input

1. `activityDescription`, `organizationBoundary`, `sourceOwnershipOrControl`, `purchasedEnergyType`, `valueChainRelation`, `asOfDate`를 읽는다.
2. 각 관계 필드는 Knowledge에 선언된 열거값만 받아들인다.
3. `activityData`가 있으면 수량·단위·기간을 별도 보존하되 후보 분류 규칙과 섞지 않는다.

### 2. Apply the definition-violation gate

Scope 1과 Scope 2를 더해 Scope 3라고 확정하는 등 Scope 정의를 바꾸라는 요구이면 분류를 중단한다. `candidateScope`는 `UNRESOLVED`, `status`는 `STOP`으로 두고 위반한 정의를 `ruleTrace`에 남긴다.

### 3. Apply the boundary and consistency gate

1. `organizationBoundary`가 없거나 조직·운영통제 범위가 해석되지 않으면 `REVIEW`한다.
2. 소유·통제, 구매에너지, 가치사슬 관계 중 필요한 값이 `UNKNOWN`이면 `REVIEW`한다.
3. 한 활동에 대해 서로 다른 Scope 규칙이 동시에 참이 되도록 관계정보가 충돌하면 단일 후보를 만들지 않고 `REVIEW`한다.
4. 각 미해결 필드를 `unresolvedFields`와 `additional_data_request.md`에 동일하게 기록한다.

### 4. Classify one candidate

경계와 관계정보가 일관된 경우에만 아래 규칙을 순서대로 적용한다.

1. 배출원이 `OWNED_CONTROLLED`이고 구매에너지 항목이 `NONE`이면 직접배출 후보 `SCOPE_1`을 부여한다.
2. `purchasedEnergyType`이 `ELECTRICITY`, `STEAM`, `HEAT`, `COOLING` 중 하나이면 구매에너지 간접배출 후보 `SCOPE_2`를 부여한다.
3. 위의 Scope 2 규칙이 아니고 배출원이 `NOT_OWNED_CONTROLLED`이며 `valueChainRelation`이 `UPSTREAM` 또는 `DOWNSTREAM`이면 기타 가치사슬 간접배출 후보 `SCOPE_3`를 부여한다.
4. 어느 한 규칙으로도 단일 후보가 나오지 않으면 `UNRESOLVED`와 `REVIEW`를 반환한다.

단일 후보가 도출되면 `status`는 `PROCEED`다. 적용한 규칙과 배제한 규칙을 `ruleTrace`에 남긴다.

### 5. Separate classification from calculation

`activityData` 또는 배출계수가 없더라도 관계정보가 충분하면 Scope 후보는 유지한다. 다만 이 Method는 CO2e를 계산하지 않으며, 계산에 필요한 누락 자료를 추가 요청으로만 기록한다.

### 6. Land reviewable outputs

- `scope_classification.json`: `candidateScope`, `ruleTrace`, `boundarySnapshot`, `unresolvedFields`, `status`.
- `scope_evidence_card.md`: 적용한 Scope 정의, 입력 근거, 판정 한계.
- `additional_data_request.md`: 미해결 질문과 필요한 자료. 없으면 없다고 명시한다.
- `RunRecord`: 규칙 버전, 기준일, 입력 스냅샷, 판정, 산출물 경로.

모든 산출물에서 동일한 `candidateScope`와 `status`를 사용한다.

## Chain position

- ← appliedThrough — [scope_activity_classification_knowledge](../_knowledge/scope_activity_classification_knowledge.md)
- → developsSkill — [scope-activity-classification](../_skill/scope-activity-classification/SKILL.md)

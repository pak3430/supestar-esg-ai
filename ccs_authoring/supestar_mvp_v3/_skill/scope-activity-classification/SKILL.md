---
name: scope-activity-classification
description: 조직 활동을 소유·통제, 구매에너지, 가치사슬 관계와 조직·운영 경계에 대조하여 Scope 1·2·3 후보로 분류하고 근거와 미해결 자료를 남긴다. 배출량 계산이나 ESG 전체 평가가 아니라 개별 활동의 Scope 후보 판정이 필요할 때 사용한다.
---

# Scope Activity Classification

조직 활동 하나를 Scope 정의에 따라 분류하되, 근거가 부족한 경우 임의로 확정하지 않는다.

## Required input

- 활동 설명과 기준일
- 조직·운영 경계
- 배출원의 소유·통제 여부
- 구매 전기·스팀·열·냉방 여부
- 상류·하류 가치사슬 관계
- 선택 입력: 활동량, 단위, 기간

## Procedure

1. [Scope 활동 분류 Method](../../_method/scope_activity_classification_method.md)를 읽고 그 순서와 경계를 따른다.
2. Scope 정의 위반 요구를 먼저 확인한다. Scope 1과 Scope 2의 합을 Scope 3로 확정하라는 요구처럼 정의를 바꾸는 요청은 `STOP`한다.
3. 조직·운영 경계와 관계정보가 빠졌거나 충돌하면 후보를 강제하지 않고 `REVIEW`한다.
4. 일관된 입력에 대해 다음 후보 중 정확히 하나를 판정한다.
   - 소유·통제 배출원의 직접배출: `SCOPE_1`
   - 구매 전기·스팀·열·냉방 생산의 간접배출: `SCOPE_2`
   - Scope 2가 아닌 상·하류 가치사슬의 기타 간접배출: `SCOPE_3`
5. 단일 후보가 도출되면 `PROCEED`하고, 적용 규칙과 배제 규칙을 함께 남긴다.
6. 활동자료나 배출계수가 없으면 배출량을 계산하지 않는다. 후보 분류가 가능하면 유지하고 계산용 누락 자료만 요청한다.

## Outputs

- `scope_classification.json`: 후보, 규칙 추적, 경계 스냅샷, 미해결 필드, 상태
- `scope_evidence_card.md`: 정의, 입력 근거, 판정 한계
- `additional_data_request.md`: 추가 질문과 필요한 자료
- `RunRecord`: 규칙 버전, 기준일, 입력, 판정, 산출물 연결

모든 산출물의 후보와 상태는 서로 같아야 한다.

## Boundaries

- 이 Skill은 Scope **후보**를 분류한다.
- CO2e를 산정하거나 감축성과를 확정하지 않는다.
- ESG 전체 성과나 등급을 평가하지 않는다.
- 불명확하거나 충돌하는 정보를 추정으로 채우지 않는다.

## Derivation

[ORGANIZATIONAL_BOUNDARY](../../_identity/ORGANIZATIONAL_BOUNDARY.md) — `definesGoal` → [scope_activity_classification_goal](../../_goal/scope_activity_classification_goal.md) — `requiresTask` → [scope_activity_classification_task](../../_task/scope_activity_classification_task.md) — `requiresKnowledge` → [scope_activity_classification_knowledge](../../_knowledge/scope_activity_classification_knowledge.md) — `appliedThrough` → [scope_activity_classification_method](../../_method/scope_activity_classification_method.md) — `developsSkill` → `scope-activity-classification`

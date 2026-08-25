---
name: forest_carbon_procedure_guidance
description: "산림탄소 사업의 주장 상태와 문서 증거를 순차 원장으로 평가해 절차 경로·체크리스트·확인 질문·RunRecord를 만드는 방법이다."
---

# 산림탄소 공식 절차 안내 Method

## Method

입력 적격성 확인 → 단계별 증거 원장 작성 → 공식 순서의 연속 완료 판별 → 차단·다음 단계 결정 → 주체·선행조건·산출물 연결 → 공식 확인 질문 생성 → 판정 → 출력 렌더링 순으로 적용한다. 이 방법은 안내 자료만 만들며 어떤 외부 절차도 실행하지 않는다.

## 1. Admit the input

1. 필수 필드 `projectType`, `currentStage`, `intendedUse`, `asOfDate`가 있는지 확인한다. `availableDocuments`는 없으면 빈 목록으로 둔다.
2. `currentStage`가 `PLANNING`, `ELIGIBILITY`, `REGISTERED`, `IMPLEMENTING`, `MONITORING`, `VERIFIED`, `CERTIFIED`, `REGISTRY_MANAGED`, `UNKNOWN` 중 하나가 아니면 수정을 요청하고 그전에는 `UNKNOWN`으로 다룬다.
3. 사업유형이나 현재 단계를 모르면 `UNKNOWN`을 유지한다. 기준일이 없거나 유효하지 않으면 현재 유효상태를 확정하지 않고 `REVIEW` 후보로 기록한다.
4. `intendedUse`는 거래·비거래 활용·학습·미정 중 입력된 의미를 보존한다. 이용 목적만으로 거래 가능성이나 허용 표현을 추정하지 않는다.

## 2. Build the evidence ledger

아래 아홉 단계를 이 순서 그대로 원장에 만든다.

1. 사업계획
2. 타당성·적격성 검토
3. 사업등록
4. 실행
5. 모니터링
6. 독립 검증
7. 인증
8. 거래 또는 비거래 활용
9. 등록부 상태관리

각 단계에 `claimed`, `evidenceState`, `evidenceRefs`, `evidenceGap`, `prerequisites`, `actors`, `requiredArtifacts`를 기록한다. `evidenceState`는 다음 의미로만 사용한다.

- `CONFIRMED`: 제공된 내용에서 해당 사업, 단계, 작성·발급주체, 일자 또는 적용기간, 완료 또는 현재 상태를 확인할 수 있다.
- `UNVERIFIED`: 문서명이나 주장만 있고 내용·주체·대상·일자·상태 중 필요한 항목을 확인할 수 없다.
- `MISSING`: 해당 단계의 완료 증거가 제공되지 않았다.

제공된 문서에 없는 사실을 보충하거나 문서 제목만으로 `CONFIRMED` 처리하지 않는다. 독립 검증 단계명과 혼동하지 않도록 증거상태에는 `VERIFIED`를 쓰지 않는다.

## 3. Walk the official sequence

1. 첫 단계부터 차례로 `CONFIRMED` 여부를 검사한다.
2. 중간 공백 전까지 연속으로 확인된 단계만 `completedStages`에 넣는다.
3. 최초 `UNVERIFIED` 또는 `MISSING` 단계가 주장된 현재 단계 또는 그 선행단계라면 그 공식 단계명을 `blockedStage`로 둔다. 뒤 단계 자료가 있어도 앞 단계 완료를 역으로 추정하지 않는다.
4. `currentStage` 주장과 연속 완료 증거가 일치하는지 기록한다. 불일치는 삭제하지 말고 `evidenceGap`과 공식 확인 질문에 남긴다.
5. `blockedStage`가 있으면 그 증거를 확인·보완하는 단계를 `nextStage`로 둔다. 차단이 없으면 마지막 연속 완료 단계 바로 다음 공식 단계를 `nextStage`로 둔다.
6. 아홉 단계가 모두 확인된 경우 `nextStage`는 `null`로 두고, 체크리스트에 등록부 상태의 지속 확인을 후속 행동으로 기록한다.

## 4. Attach actors, prerequisites, and artifacts

Knowledge의 단계 표를 사용해 `nextStage`와 `blockedStage`에 필요한 담당주체·선행조건·산출물을 연결한다.

- 역할은 사업자·산주, 독립 검증기관, 산림청, 공개 업무 범위의 한국임업진흥원·산림탄소센터, 산림탄소등록부 운영주체처럼 근거에 나온 범위로만 표현한다.
- 정확한 담당기관, 최신 서식, 제출항목, 심사기준이 제공 자료에서 확인되지 않으면 단정하지 않고 `confirmationNeeded: true`로 표시한다.
- `requiredArtifacts`의 각 항목은 `stage`, `artifact`, `purpose`, `evidenceState`를 가진다. 없는 산출물을 생성되었거나 제출된 것으로 표현하지 않는다.
- 등록부 기록은 상태 이력의 증거로만 사용한다. 권리·계약·세무의 최종 법적 의미를 대신한다고 해석하지 않는다.

## 5. Generate official confirmation questions

각 질문에 `target`, `question`, `resolvesGap`을 기록한다. 최소한 현재 사례에 해당하는 다음 공백을 질문으로 바꾼다.

- 공식 사업유형과 적용 제도·방법론
- 대상지·사업·관리·처분 권한의 충족 문서
- 기준일 현재 사업등록의 식별정보·유효상태
- 다음 단계의 공식 담당주체·최신 서식·제출항목·보완요건
- 검증기관 적격성과 검증 결과 상태
- 인증 범위·상태·유효성
- 거래형/비거래형 경로와 허용 외부 표현
- 등록부의 보유·이전·사용완료·효력상실 상태 및 이중사용 방지 이력

사용자가 답할 수 있는 사실 확인과 제도운영자만 확정할 수 있는 질문을 구분한다. 이 방법 자체는 질문을 외부 기관에 보내지 않는다.

## 6. Decide the status

다음 우선순위로 하나만 고른다.

1. `STOP`: 선행 등록·검증·인증 증거 없이 거래 가능, 사용완료 또는 공식 인증을 확정해 달라는 요구가 있다.
2. `REVIEW`: `projectType`/`currentStage`가 `UNKNOWN`이거나, 기준일 또는 순차 증거가 불충분하거나, 제도 적용·등록·인증 유효상태·활용 경로·허용 표현·정확한 기관 요건을 공식 확인해야 한다.
3. `PROCEED`: 현재 단계 주장과 순차 완료 증거가 일치하며, 미확정 제도 판단 없이 다음 절차의 주체·선행조건·필요 산출물을 안내할 수 있다.

`STOP`에서도 확인된 사실과 공백 및 안전한 다음 확인 행동은 출력한다. 판정을 공식 승인·거절·인증 결정처럼 표현하지 않는다.

## 7. Render the outputs

### `procedure_path.json`

```json
{
  "currentStage": "<입력 enum>",
  "completedStages": ["<증거로 연속 확인된 공식 단계>"],
  "blockedStage": "<최초 미확인 공식 단계 또는 null>",
  "nextStage": "<정상적으로 이어갈 공식 단계 또는 null>",
  "actors": [
    {
      "actor": "<공개 역할 범위의 주체>",
      "publicRole": "<확인된 역할>",
      "nextAction": "<다음 확인·준비 행동>",
      "confirmationNeeded": true
    }
  ],
  "requiredArtifacts": [
    {
      "stage": "<공식 단계>",
      "artifact": "<필요 문서·기록>",
      "purpose": "<확인할 선행조건 또는 상태>",
      "evidenceState": "CONFIRMED|UNVERIFIED|MISSING"
    }
  ]
}
```

### `procedure_checklist.md`

아홉 단계를 고정 순서로 열거하고 `단계 | 증거상태 | 근거 | 선행조건 | 담당주체 | 필요 산출물 | 다음 행동` 열을 채운다. `UNVERIFIED`와 `MISSING`은 완료 체크하지 않는다.

### `official_confirmation_questions.md`

`확인 대상 | 질문 | 해소할 공백` 형식으로 작성한다. 제공 자료로 이미 답이 확인된 질문은 반복하지 말고 근거 원장에 남긴다.

### `status` and `RunRecord`

`status`는 `PROCEED`, `REVIEW`, `STOP` 중 하나다. `RunRecord`에는 다음을 기록한다.

- `asOfDate`, `projectType`, 입력 `currentStage`, `intendedUse`
- 검토한 `availableDocuments`와 각 증거상태 및 공백
- `completedStages`, `blockedStage`, `nextStage`
- `status`와 판정 이유
- 작성한 세 출력의 식별자

이 기록은 현재상태·근거·다음단계·판정을 재현할 수 있어야 한다.

## Required fixtures

- `PROCEED`: 등록 완료와 그 이전 순차 증거, 실행 기록, 모니터링 자료가 현재 단계 주장과 일치하며 다음 독립 검증 준비를 묻는 사례. `nextStage`는 독립 검증이고 검증 주체·선행조건·필요 산출물을 안내한다.
- `REVIEW`: 사업유형과 현재 등록상태가 불명확한 사례. 둘을 추정하지 않고 공식 제도 적용 및 등록부 유효상태 질문을 만든다.
- `STOP`: 독립 검증·인증 증거 없이 거래 가능한 단위라고 확정해 달라는 사례. 확정을 중단하고 누락된 검증·인증·등록부 확인을 기록한다.

## Boundary

이 방법은 절차 순서만 안내한다. 산림탄소 사업의 의미나 적합성을 다시 평가하지 않고 E/S/G 영향·주체·책임을 매핑하지 않는다. 문서 제출, 기관 접촉, 등록, 검증, 인증, 거래, 등록부 변경을 실행하지 않으며 공식 등록·인증·법률·세무 결과를 최종 확정하지 않는다.

## Chain position

← appliedThrough — [forest_carbon_procedure_guidance Knowledge](../_knowledge/forest_carbon_procedure_guidance_knowledge.md)

→ developsSkill — [forest-carbon-procedure-guidance](../_skill/forest-carbon-procedure-guidance/SKILL.md)

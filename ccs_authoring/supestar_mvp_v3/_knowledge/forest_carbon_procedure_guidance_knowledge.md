---
name: forest_carbon_procedure_guidance
description: "산림탄소 공식 절차를 증거로 판별하고 다음 단계의 주체·선행조건·산출물·확인 질문을 연결하는 데 필요한 지식이다."
---

# 산림탄소 공식 절차 안내 Knowledge

## Knowledge

이 과업에는 입력된 현재 단계 주장과 기준일 현재 확인 가능한 완료 증거를 분리하고, 고정된 공식 절차를 앞에서부터 적용하는 지식이 필요하다. 문서 이름만으로 내용·발급주체·유효성을 추정하지 않으며, 공개 자료에서 확인되지 않은 기관 판단이나 제도 요건은 공식 확인 질문으로 남긴다.

## Input semantics

| field | meaning and admission rule |
| --- | --- |
| `projectType` | 사용자가 알고 있는 사업 유형. 불명확하면 `UNKNOWN`; 제도 적용을 추정하지 않는다. |
| `currentStage` | 사용자의 현재 단계 주장. `PLANNING`, `ELIGIBILITY`, `REGISTERED`, `IMPLEMENTING`, `MONITORING`, `VERIFIED`, `CERTIFIED`, `REGISTRY_MANAGED`, `UNKNOWN`만 허용하고, 증거로 확인된 완료 단계와 별도로 취급한다. |
| `availableDocuments` | 계획·등록·실행·모니터링·검증·인증·활용·등록부 상태를 확인할 수 있다고 사용자가 제시한 문서 목록. 제목만 있고 내용·일자·발급주체·상태가 확인되지 않으면 `UNVERIFIED`로 본다. |
| `intendedUse` | 거래, 비거래 활용, 학습, 미정 중 사용자가 밝힌 목적. 거래 가능성이나 허용 표현을 이 값만으로 확정하지 않는다. |
| `asOfDate` | 등록·검증·인증·등록부 상태를 판별하는 기준일. 기준일이 없으면 현재 유효상태를 확정하지 않는다. |

## Official sequence and evidence model

아래 순서는 고정한다.

`사업계획 → 타당성·적격성 검토 → 사업등록 → 실행 → 모니터링 → 독립 검증 → 인증 → 거래 또는 비거래 활용 → 등록부 상태관리`

입력 enum은 절차를 거칠게 표현한다. 특히 거래 또는 비거래 활용에 별도 enum을 새로 만들지 말고, `blockedStage`와 `nextStage`에는 공식 단계명을 그대로 기록한다.

| official stage | related input stage | responsible actors in the public-role boundary | prerequisite | required artifact or completion evidence |
| --- | --- | --- | --- | --- |
| 사업계획 | `PLANNING` | 사업자·산주 | 사업유형·목적, 대상지와 사업 권한, 적용할 활동과 방법론의 확인 | 대상지·권리·활동·방법론·기준선·모니터링·예상성과를 담은 사업계획서와 권한 증거 |
| 타당성·적격성 검토 | `ELIGIBILITY` | 사업자, 공개 업무 범위의 한국임업진흥원·산림탄소센터 또는 해당 제도운영자 | 검토 가능한 사업계획과 제도 적용 근거 | 제출본·접수기록 및 공식 검토 결과; 정확한 심사주체·서식·요건은 공식 확인 |
| 사업등록 | `REGISTERED` | 사업자, 공개 업무 범위의 제도운영자, 산림탄소등록부 | 적격성 검토 완료와 등록에 필요한 공식 요건 충족 | 사업 식별정보, 등록 결정 또는 등록부 기록과 기준일 현재 상태 |
| 실행 | `IMPLEMENTING` | 사업자·산주 | 유효하게 확인된 등록과 등록된 계획 | 계획에 따른 활동·현장·권한·변경 기록 |
| 모니터링 | `MONITORING` | 사업자·산주 | 실행 기록, 적용 방법론·경계·기간·기준선 | 활동자료, 현장자료, 산정자료와 모니터링 보고서 |
| 독립 검증 | `VERIFIED` | 독립 검증기관, 자료를 제공하고 보완하는 사업자 | 검증 가능한 모니터링·산정 패키지와 검증기관 적격성의 공식 확인 | 검증보고서, 보완·종결 기록 및 기준일 현재 검증 상태 |
| 인증 | `CERTIFIED` | 공개 업무 범위의 제도운영자, 신청 사업자 | 독립 검증 결과와 해당 제도의 인증 요건 | 공식 인증 결정·인증 문서 또는 등록부의 인증 상태; 범위와 유효성은 공식 확인 |
| 거래 또는 비거래 활용 | 별도 enum 없음 | 권리 보유자·사업자, 상대방과 등록부 운영주체(해당 시) | 유효한 인증·등록부 상태, 이용 경로와 권리, 허용 표현의 확인 | 거래·이전 기록 또는 승인된 비거래 활용·표현의 근거; 사용완료를 주장하면 그 상태 기록 |
| 등록부 상태관리 | `REGISTRY_MANAGED` | 산림탄소등록부 운영주체, 사업자·권리 보유자 | 대상 기록과 변경 사건의 증거 | 보유·이전·사용완료·효력상실 이력과 기준일 현재 상태 |

산림청은 관련 정책·법령과 인증 체계를 관할하지만 개별 거래·세무 결과를 자동 확정하는 주체로 확대하지 않는다. 한국임업진흥원·산림탄소센터는 공개된 범위의 제도 운영, 등록·평가·인증 지원, 정보관리 역할만 설명한다. 등록부는 사업·인증량·거래·사용 상태 이력을 관리하지만 권리·계약·세무의 모든 법적 의미를 대신하지 않는다.

## Evidence and stage rules

1. `currentStage`는 주장값이며, `completedStages`에는 문서의 내용·발급 또는 작성 주체·일자·대상 사업·상태가 확인되는 단계만 순서대로 넣는다.
2. 앞 단계의 완료 증거가 없으면 그 단계를 `blockedStage`로 두고 뒤 단계는 완료 처리하지 않는다. 뒤 단계 문서가 제시되더라도 순서 불일치를 기록하고 공식 확인을 요구한다.
3. `nextStage`는 정상적으로 이어갈 첫 단계다. 미충족 선행단계가 있으면 먼저 그 증거를 보완·확인하는 행동을 다음 단계로 삼는다.
4. `actors`는 공개된 역할과 다음 행동만 기록하고 비공개 판단, 승인 가능성, 기관 공식 견해를 추정하지 않는다.
5. `requiredArtifacts`는 단계·문서·목적·증거상태를 연결한다. 문서가 없거나 확인할 수 없으면 요구 목록에 남기고 생성되었다고 말하지 않는다.
6. 거래형·비거래형, 허용 외부 표현, 등록·검증·인증·등록부의 기준일 현재 유효상태는 증거가 없으면 공식 확인 대상이다.

## Decision knowledge

판정 우선순위는 `STOP` → `REVIEW` → `PROCEED`다.

- `STOP`: 사용자가 선행 등록·검증·인증 증거 없이 거래 가능, 사용완료 또는 공식 인증을 확정하도록 요구한다.
- `REVIEW`: `projectType` 또는 `currentStage`가 `UNKNOWN`이거나, 제도 적용·등록·인증 유효상태·거래/비거래 경로·허용 표현·기관별 정확한 요건을 공식 확인해야 한다.
- `PROCEED`: 현재 단계 주장과 순차 완료 증거가 일치하고, 미확정 기관 판단 없이 다음 단계·주체·선행조건·산출물을 안내할 수 있다.

`STOP`은 외부 결과의 무근거 확정을 중단하는 판정이지 기록 검토까지 중단하라는 뜻이 아니다. 어떤 판정에서도 확인된 사실, 공백, 다음에 확인할 사항을 기록한다.

## Official confirmation question set

해당되는 질문만 구체화한다.

- 이 사업의 공식 사업유형과 적용 제도·방법론은 무엇이며 현재도 적용 가능한가?
- 대상지·사업·관리·처분 권한은 어떤 문서로 충족되는가?
- 기준일 현재 사업등록의 식별정보와 유효상태는 무엇인가?
- 다음 단계의 공식 담당주체, 최신 서식, 제출 항목, 심사 또는 보완 요건은 무엇인가?
- 검증기관의 적격성과 검증 결과의 기준일 현재 상태는 무엇인가?
- 인증의 범위·상태·유효성은 무엇으로 확인하는가?
- 거래형과 비거래형 중 어느 경로가 적용되며 허용되는 외부 표현은 무엇인가?
- 등록부상 보유·이전·사용완료·효력상실 상태와 이중사용 방지 기록은 무엇인가?

## Output semantics

- `procedure_path.json`: 입력 주장인 `currentStage`, 증거로 순차 확인된 `completedStages`, 최초 미충족 단계인 `blockedStage`, 정상적으로 이어갈 `nextStage`, 공개 역할 범위의 `actors`, 확인·보완해야 할 `requiredArtifacts`를 담는다.
- `procedure_checklist.md`: 모든 공식 단계를 순서대로 열거하고 각 단계의 증거상태, 선행조건, 담당주체, 필요한 산출물, 다음 행동을 표시한다.
- `official_confirmation_questions.md`: 확인 대상 기관·질문·질문이 해소할 공백을 연결한다.
- `status`: `PROCEED`, `REVIEW`, `STOP` 중 하나다.
- `RunRecord`: 입력 기준일과 현재상태 주장, 검토한 근거와 공백, 완료·차단·다음 단계, 판정과 판정 이유를 재현 가능하게 남긴다.

## Scope boundary

이 지식은 절차 순서 안내용이다. 개념 의미·경계를 평가하거나 E/S/G 영향·주체·책임 지도를 만들지 않는다. 문서 제출, 기관 문의, 등록·검증·인증, 거래, 등록부 변경을 실행하지 않으며 인증·등록·법률·세무의 최종 판단을 내리지 않는다.

## Grounding

- [추가 체인 작성 계약](../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/05_forest_carbon_procedure_guidance_authoring_contract.md)
- [산림탄소 공식 절차](../../../ccs/_input/_document/04_%EC%82%B0%EB%A6%BC_ESG_E_S_G_%EB%B0%8F_%EC%9E%84%EC%97%85%EC%A7%84%ED%9D%A5%EC%9B%90_%EC%83%9D%ED%83%9C%EA%B3%84.md#4-%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C-%EA%B3%B5%EC%8B%9D-%EC%A0%88%EC%B0%A8)
- [반드시 함께 묻는 질문](../../../ccs/_input/_document/04_%EC%82%B0%EB%A6%BC_ESG_E_S_G_%EB%B0%8F_%EC%9E%84%EC%97%85%EC%A7%84%ED%9D%A5%EC%9B%90_%EC%83%9D%ED%83%9C%EA%B3%84.md#5-%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C%EC%97%90%EC%84%9C-%EB%B0%98%EB%93%9C%EC%8B%9C-%ED%95%A8%EA%BB%98-%EB%AC%BB%EB%8A%94-%EC%A7%88%EB%AC%B8)

## Chain position

← requiresKnowledge — [forest_carbon_procedure_guidance Task](../_task/forest_carbon_procedure_guidance_task.md)

→ appliedThrough — [forest_carbon_procedure_guidance](../_method/forest_carbon_procedure_guidance_method.md)

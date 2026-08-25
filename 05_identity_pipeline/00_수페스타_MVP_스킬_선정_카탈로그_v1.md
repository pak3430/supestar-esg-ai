# 수페스타 MVP 스킬 선정 카탈로그 v1

- 기준일: 2026-08-22 KST
- 입력 실행: `ccs_runs/2026-08-20_esg_concept_v1`
- 입력 상태: Stage 1~5 `SEALED_PASS`
- 목적: 85개 Concept Skill을 그대로 배포하지 않고, 수페스타 MVP에서 실제 행동과 산출물을 만드는 기능만 선별한다.

## 1. 현재 결과에 대한 판정

Stage 1~5 실행은 85개 Identity와 각각의 첫 Concept Skill을 정상적으로 폐쇄했다. 그러나 85개 Skill의 Procedure가 동일한 개념평가 틀을 사용하므로, 이것만으로는 Scope 분류·시장 비교·절차 체크리스트·거래 준비도 판정을 실제로 수행할 수 없다.

따라서 다음 계층을 분리한다.

1. **Concept Skill**: 개념의 의미·경계·출처를 제공한다.
2. **Build Skill**: 질문을 정해진 입력 구조로 받고 기능별 판단 절차와 산출물 계약을 정의한다.
3. **Run Skill**: 하나의 Build Skill을 검증된 고정 코드에 결합하고, 실제 입력·판정·산출물·실행 증거를 봉인한다.
4. **Composite Skill**: 질문을 분류하고 필요한 Run Skill만 호출한다.
5. **Runtime package**: 승인된 Skill·규칙·데이터만 브라우저 서비스 경계에 배포한다.

## 2. P0 스킬 선정

사용자에게 직접 보이는 6개 기능과 그 앞단의 질문 라우터를 P0로 선정한다.

| 구분 | 새 스킬 이름 | 기존 Target Identity | 단일 기능 방향 | 사용자 산출물 |
| --- | --- | --- | --- | --- |
| 공통 | `supestar-question-routing` | `USER_QUESTION` | 질문을 6개 허용 의도 중 하나로 분류하고 부족한 입력을 요청 | RouteDecision, ContextSnapshot |
| S1 | `esg-carbon-action-path` | `ESG_MANAGEMENT` | ESG에서 측정·Scope·SDGs·시장·산림탄소까지 최소 이유 경로 생성 | ActionPath, 설명 카드 |
| S2 | `scope-activity-classification` | `ORGANIZATIONAL_BOUNDARY` | 조직·운영 경계와 활동자료로 Scope 1·2·3 후보 판정 | ScopeClassification, 추가자료 요청 |
| S3 | `carbon-market-unit-comparison` | `CLIMATE_CLAIM` | CCM·VCM·배출권·크레딧·상쇄를 시장·단위·사용행위로 분리 | 비교표, 사용조건, 주장 주의사항 |
| S4 | `forest-esg-impact-mapping` | `FOREST_CARBON_PROJECT` | 산림탄소 사업의 E·S·G 영향·책임·증거 누락을 분리 | E/S/G 지도, 누락축 경고 |
| S5 | `forest-carbon-procedure-guidance` | `FOREST_CARBON_PROJECT` | 계획부터 등록부 상태까지 공식 절차의 선후조건 안내 | 절차 체크리스트, 기관·산출물 표 |
| S6 | `forest-carbon-transaction-readiness` | `TRANSACTION_EVIDENCE_PACK` | 11개 거래 게이트의 증거 충족 여부를 판정 | 준비도표, 누락목록, 공식 질의서 |

`FOREST_CARBON_PROJECT`에서 S4와 S5가 갈라지는 이유는 동일한 개념이 서로 다른 목표를 가질 수 있기 때문이다. S4는 E·S·G 영향과 책임을 보여주고, S5는 공식 절차의 순서와 산출물을 안내한다. 두 Goal facet의 방향은 서로 대체되지 않는다.

## 3. P0 선정 기준

각 P0 스킬은 아래 조건을 모두 충족해야 한다.

- 한 스킬이 하나의 사용자 문제만 해결한다.
- 입력 필드와 필수 여부가 고정돼 있다.
- 기계적으로 판정 가능한 규칙은 결정론적으로 처리한다.
- 설명문 외에 JSON과 사람이 읽는 Markdown 산출물을 함께 만든다.
- 모든 핵심 주장에 입력 문서·행 범위·기준일을 연결한다.
- 불확실성과 고위험 항목은 `PROCEED`, `REVIEW`, `STOP`으로 구분한다.
- 실제 거래·결제·세무확정·법률판단·공식 인증은 수행하지 않는다.
- 실행마다 Run ID, 사용한 Identity·Skill 버전, 입력·출력·판정을 남긴다.

## 4. 85개 Identity의 역할별 전체 분류

아래 여섯 묶음은 85개 Identity 전체를 중복 없이 포함한다. P0 Action Skill은 이 중 필요한 노드만 읽으며 전체 CCS를 Runtime에 노출하지 않는다.

### 4.1 대화·판정·실행증거 — 16개

`USER_QUESTION`, `USER_ROLE`, `IDENTITY_NODE`, `IDENTITY_RELATION`, `RELATION_EDGE`, `SOURCE_LINKED_IDENTITY`, `EVIDENCE_CLAIM`, `ACTION_PATH`, `RISK_GATE`, `APPROVAL_DECISION`, `PROCEED_DECISION`, `REVIEW_DECISION`, `STOP_DECISION`, `RUN_RECORD`, `FEEDBACK_CANDIDATE`, `BROWSER_EVIDENCE_UI`

### 4.2 ESG·측정·Scope·SDGs — 17개

`ESG`, `ESG_MANAGEMENT`, `ENVIRONMENTAL_RESPONSIBILITY`, `SOCIAL_RESPONSIBILITY`, `GOVERNANCE_RESPONSIBILITY`, `GREENHOUSE_GAS_INVENTORY`, `ORGANIZATIONAL_BOUNDARY`, `OPERATIONAL_BOUNDARY`, `SCOPE_1`, `SCOPE_2`, `SCOPE_3`, `ACTIVITY_DATA`, `EMISSION_FACTOR`, `CO2E`, `SUSTAINABLE_DEVELOPMENT_GOALS`, `DIRECT_EMISSIONS_REDUCTION`, `RESIDUAL_EMISSIONS`

### 4.3 탄소시장·무결성 — 16개

`CCM`, `VCM`, `EMISSION_ALLOWANCE`, `CARBON_CREDIT`, `CARBON_OFFSET`, `RETIREMENT`, `USE_COMPLETION`, `CLIMATE_CLAIM`, `MARKET_INTEGRITY`, `DOUBLE_COUNTING`, `DOUBLE_USE`, `ADDITIONALITY`, `BASELINE`, `LEAKAGE`, `PERMANENCE`, `REVERSAL_RISK`

### 4.4 산림탄소·기관·참여자 — 17개

`FOREST_CARBON`, `FOREST_CARBON_SINK`, `FOREST_CARBON_PROJECT`, `FOREST_CARBON_METHODOLOGY`, `FOREST_CARBON_MONITORING`, `FOREST_CARBON_VERIFICATION`, `FOREST_CARBON_CERTIFICATION`, `FOREST_CARBON_REGISTRY`, `REGISTRY_STATUS`, `KOREA_FOREST_SERVICE`, `KOFPI`, `FOREST_CARBON_CENTER`, `VERIFICATION_BODY`, `FOREST_OWNER`, `FORESTRY_WORKER`, `PROJECT_OPERATOR`, `LOCAL_COMMUNITY`

### 4.5 거래·권리·계약·세무·결제 — 12개

`SELLER`, `BUYER`, `INTERMEDIARY`, `PAYMENT_SERVICE_PROVIDER`, `TRANSACTION_CONTRACT`, `TAX_CLASSIFICATION`, `PAYMENT`, `SETTLEMENT`, `REGISTRY_TRANSFER`, `DISPOSITION_RIGHT`, `TRANSACTION_EVIDENCE_PACK`, `APPROVED_EXTERNAL_CLAIM`

### 4.6 CCS·KAC·Build·Run — 7개

`COMMON_CONTEXT`, `KNOWLEDGE_ACTION_CHAIN`, `CONCEPT_SKILL`, `BUILD_SKILL`, `RUN_SKILL`, `RUNTIME_BOUNDARY`, `GOVERNANCE_CONTEXT`

합계: `16 + 17 + 16 + 17 + 12 + 7 = 85`

## 5. Identity 품질 게이트

추가 체인 작성은 기존 Identity의 의미를 다시 쓰지 않는다. 따라서 아래 조건을 먼저 확인한다.

| Target Identity | 현재 근거 상태 | 추가 체인 작성 전 판정 |
| --- | --- | --- |
| `USER_QUESTION` | 구조요구사항의 최소 객체 정의에 직접 연결 | 사용 가능 |
| `ESG_MANAGEMENT` | ESG 목표·행동·책임의 역할 문장에 직접 연결 | 사용 가능 |
| `ORGANIZATIONAL_BOUNDARY` | 경계·기준연도·자료 필요조건에 직접 연결 | 사용 가능 |
| `CLIMATE_CLAIM` | VCM 절차와 주장 책임의 전체 경로에 직접 연결 | 사용 가능 |
| `FOREST_CARBON_PROJECT` | 방법론·모니터링·검증·인증·등록상태 경로에 직접 연결 | 사용 가능 |
| `TRANSACTION_EVIDENCE_PACK` | v3에서 입력문서 `L18-L20; L23-L44; L46-L80`과 SHA-256에 결합 | **범위 제한 사용 가능** — 11개 게이트는 법정 요건이 아닌 내부 준비도 통제 |

`ESG`, `CCM`, `VCM`, `CARBON_CREDIT`, `FOREST_CARBON`처럼 Manifest 한 줄만 근거로 잡힌 Identity는 P0 Action Skill의 Target으로 사용하지 않는다. 이 개념들은 보조 지식으로 읽되, 추후 의미와 출처를 보강한 뒤 승격한다.

## 6. 배포 경계

### Runtime에 포함

- P0 질문 라우터와 6개 Action Skill
- 각 스킬이 직접 참조하는 승인된 Identity·Relation·근거 조각
- 결정론적 분류·게이트·산출물 생성 코드
- Evidence UI에 필요한 출처·기준일·판정 이유
- Run Record 스키마와 테스트 fixture

### Runtime에서 제외

- 85개 전체 Concept Skill 원본
- Stage 진단·후보·피드백 내부 문서
- 미승인 Identity와 Manifest 한 줄만 근거인 개념
- 실제 거래·자동결제·등록부 이전 실행기
- 법률·세무·계약·인증 자동확정 로직

## 7. 실행 현황과 다음 순서

- [x] 일곱 개 추가 체인 작성 계약 검증
- [x] 프로젝트 계층의 스크립트형 P0 후보 7개 구현
- [x] 각 스킬의 정상·REVIEW·STOP fixture 검증
- [x] 질문 라우터와 6개 기능의 producer/internal route 계약 작성
- [x] Stage Identity 스키마를 새 v2 authoring vault에 호환 투영·검증
- [x] 거래 준비도를 제외한 P0 Build 후보 6개 체인 작성·전체 검증
- [x] `TRANSACTION_EVIDENCE_PACK` grounding을 범위 제한과 함께 검토·승인
- [x] 거래 준비도 Build 후보 체인 작성·검증
- [x] P0 Build 후보 `7 / 7` 작성 완료
- [x] 검증된 Build 후보를 각각 실행 가능한 Run Skill `7 / 7`로 구성·검증
- [x] Run Skill별 `PROCEED·REVIEW·STOP` 총 21개 fixture 실제 실행 및 증거 봉인
- [ ] 복합 스킬 작성과 governance 통과
- [ ] 승인된 복합 스킬과 필요한 closure의 Runtime registry 배포

현재 코드 후보와 검증 결과는 [P0 스크립트 스킬 인덱스](06_atomic_skills/P0_SCRIPT_SKILL_INDEX.md), [Run Skill 인덱스](07_run_skills/README.md), [Run Skill 실행 manifest](../06_runtime/tests/p0_run_skill_v1/manifest.json), [Run Skill 7종 완료검증 보고서](../07_evidence/qa/2026-08-22_수페스타_P0_RunSkill7_구성검증.md), [구현·검증 보고서](../07_evidence/qa/2026-08-21_P0_스크립트스킬_구현검증보고서.md), [Identity 스키마 호환 완료보고서](../07_evidence/qa/2026-08-21_Identity스키마_호환처리_완료보고서.md), [Build6 완료검증 보고서](../07_evidence/qa/2026-08-21_수페스타_P0_Build6_완료검증.md), [Build7 완료검증 보고서](../07_evidence/qa/2026-08-21_수페스타_P0_Build7_완료검증.md)에서 확인한다.

## 8. 근거 링크

- [Stage 1~5 최종 검증 기록](../ccs_runs/2026-08-20_esg_concept_v1/_record/stage_1_to_5_identity_pipeline_verified_run_record.md)
- [수페스타 MVP 핵심 정의서](../03_plan/2026-08-21_수페스타_산림_ESG_AI_MVP_핵심정의서/수페스타_산림_ESG_AI_MVP_핵심정의서.md)
- [KAC 실행구조 입력문서](../ccs/_input/_document/06_산림_ESG_지식의_KAC_실행구조.md)
- [Concept·Build·Run 구조요구사항](../ccs/_input/_document/08_ESG_AX_Concept_Build_Run_구조요구사항.md)
- [P0 추가 체인 작성 계약](06_atomic_skills/_authoring_specs/README.md)
- [복합 스킬 작성 요청](07_composite_skills/supestar_forest_esg_orchestrator/composite_authoring_request.md)

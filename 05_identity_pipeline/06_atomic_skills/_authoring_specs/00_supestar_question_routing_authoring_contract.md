# 추가 체인 작성 계약 — 수페스타 질문 라우팅

## 1. Binding

- status: `READY`
- targetIdentity: [USER_QUESTION](../../../ccs_authoring/supestar_mvp_v2/_identity/USER_QUESTION.md)
- newGoalFacet: `supestar_question_routing`
- capabilityDirection: 사용자의 질문·역할·기준일을 구조화하고 정확히 하나의 허용된 MVP route 또는 입력보완 route를 반환한다.
- distinctFromExistingChain: 기존 `user-question-concept-assessment`는 UserQuestion의 의미·경계를 평가한다. 이 체인은 질문을 실행 기능으로 전달하는 route를 결정한다.

## 2. Reserved name set

| node | reserved name |
| --- | --- |
| goal | `supestar_question_routing` |
| task | `supestar_question_routing` |
| knowledge | `supestar_question_routing` |
| method | `supestar_question_routing` |
| skill | `supestar-question-routing` |

## 3. Input contract

| field | required | rule |
| --- | --- | --- |
| `question` | yes | 비어 있지 않은 사용자 질문 |
| `userRole` | yes | `LEARNER`, `ESG_MANAGER`, `FOREST_OWNER_OPERATOR`, `REVIEWER` 중 하나 |
| `asOfDate` | yes | `YYYY-MM-DD` |
| `providedEvidence` | no | 사용자가 제공한 문서·상태·주장의 목록 |

## 4. Closed route enumeration

정확히 아래 값만 허용한다.

1. `CONCEPT_EXPLANATION`
2. `ESG_CARBON_PATH`
3. `SCOPE_CLASSIFICATION`
4. `CARBON_MARKET_COMPARISON`
5. `FOREST_ESG_MAPPING`
6. `FOREST_CARBON_PROCEDURE`
7. `TRANSACTION_READINESS`
8. `NEEDS_INPUT`
9. `OUT_OF_SCOPE`

한 질문에서 둘 이상의 route가 필요하면 임의로 하나를 고르지 않고 `NEEDS_INPUT`과 선택 질문을 반환한다. 복합 실행은 후속 버전에서 별도 승인한다.

## 5. Deterministic routing rules

| 핵심 의도 | route |
| --- | --- |
| ESG·SDGs·Scope·시장·산림탄소·기관·KAC 등 한 개념의 정의·의미·역할 | `CONCEPT_EXPLANATION` |
| ESG에서 탄소·측정·Scope·SDGs·시장으로 이어지는 이유 | `ESG_CARBON_PATH` |
| 활동·배출원이 Scope 1·2·3 중 어디인지 | `SCOPE_CLASSIFICATION` |
| CCM·VCM·배출권·크레딧·상쇄의 차이 | `CARBON_MARKET_COMPARISON` |
| 산림탄소의 환경·사회·지배구조 영향과 책임 | `FOREST_ESG_MAPPING` |
| 산림탄소 사업의 계획·등록·모니터링·검증·인증·등록부 절차 | `FOREST_CARBON_PROCEDURE` |
| 거래 전 권리·계약·세무·결제·이전·증빙 준비 | `TRANSACTION_READINESS` |
| 필수 질문·역할·기준일이 없음 | `NEEDS_INPUT` |
| 가격·수익 추천, 실제 거래·결제·법률·세무 확정 요구 | `OUT_OF_SCOPE` |

## 6. Output contract

- `ContextSnapshot`: 정규화하지 않은 원 질문, 역할, 기준일, 제공 근거.
- `RouteDecision`: route 값, 선택 이유, 신뢰가 아니라 규칙 일치 근거.
- `ClarifyingQuestions`: 누락되거나 충돌한 입력만 질문.
- `status`: 정상 단일 route는 `PROCEED`, 입력 부족은 `REVIEW`, 금지 범위는 `STOP`.
- `RunRecord`: 사용한 규칙 버전과 route 결과.

## 7. STOP conditions

- 실제 매매·결제·등록부 변경을 수행하라는 요청.
- 가격·수익·투자 추천.
- 법률·세무·계약·인증 결과를 공식적으로 확정하라는 요청.
- 개인정보·비공개 기관정보를 추정하라는 요청.

## 8. Grounding

- [KAC 실행구조 — 핵심 원자 Skill](../../../ccs/_input/_document/06_산림_ESG_지식의_KAC_실행구조.md#3-핵심-원자-skill)
- [전체생태계 시연 순서](../../../ccs/_input/_document/07_전체생태계_노드링크_워크플로우.md#5-시연-순서)
- [실행 오케스트레이션](../../../ccs/_input/_document/08_ESG_AX_Concept_Build_Run_구조요구사항.md#7-실행-오케스트레이션)

## 9. Required fixtures

- PROCEED: “이 활동은 어느 Scope인가요?” + 역할·기준일.
- REVIEW: “산림탄소 구매가 ESG인가요?”처럼 시장비교와 산림 E/S/G가 동시에 가능한 질문.
- STOP: “탄소크레딧을 지금 구매하고 결제해줘.”

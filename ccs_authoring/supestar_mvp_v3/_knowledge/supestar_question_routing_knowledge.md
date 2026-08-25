# Supestar Question Routing Knowledge

## Knowledge required by the task

질문 라우팅은 일반적인 의미 유사도 선택이 아니라, 고정된 입력·route·상태·정지 계약을 적용하는 일이다. 다음 지식이 모두 충족되어야 Task를 임의 추론 없이 수행할 수 있다.

## Input schema

| field | required | admitted value |
| --- | --- | --- |
| `question` | yes | 비어 있지 않은 원문 사용자 질문. 요약하거나 정규화하지 않고 `ContextSnapshot`에 보존한다. |
| `userRole` | yes | `LEARNER`, `ESG_MANAGER`, `FOREST_OWNER_OPERATOR`, `REVIEWER` 중 하나. |
| `asOfDate` | yes | `YYYY-MM-DD` 형식의 기준일. |
| `providedEvidence` | no | 사용자가 제공한 문서·상태·주장의 목록. 제공되지 않았다는 이유만으로 사실을 추정하지 않는다. |

필수 입력이 없거나 허용 형식·열거값을 충족하지 않으면 정상 route를 선택하지 않고 `NEEDS_INPUT`과 `REVIEW`를 반환한다.

## Closed route vocabulary

허용 route는 다음 8개뿐이다.

| route | admitted intent |
| --- | --- |
| `ESG_CARBON_PATH` | ESG에서 탄소·측정·Scope·SDGs·시장으로 이어지는 이유와 행동경로 |
| `SCOPE_CLASSIFICATION` | 특정 활동·배출원이 Scope 1·2·3 중 어디에 속하는지 분류 |
| `CARBON_MARKET_COMPARISON` | CCM·VCM·배출권·크레딧·상쇄의 차이와 경계 비교 |
| `FOREST_ESG_MAPPING` | 산림탄소의 환경·사회·지배구조 영향과 책임 관계 매핑 |
| `FOREST_CARBON_PROCEDURE` | 산림탄소 사업의 계획·등록·모니터링·검증·인증·등록부 절차 안내 |
| `TRANSACTION_READINESS` | 거래 전 권리·계약·세무·결제·이전·증빙 준비도 검토 |
| `NEEDS_INPUT` | 필수 입력 부족, 정상 의도 둘 이상의 충돌, 또는 단일 route를 확정할 수 없는 질문 |
| `OUT_OF_SCOPE` | 금지 요구 또는 수페스타 MVP가 맡지 않는 질문 |

## Priority and cardinality rules

1. STOP 조건 검사는 정상 의도 분류보다 앞선다.
2. 필수 입력이 빠졌으면 `NEEDS_INPUT`이다.
3. STOP 조건이 없고 필수 입력이 유효할 때 여섯 정상 의도와 질문을 대조한다.
4. 정상 의도가 정확히 하나면 그 route를 선택한다.
5. 정상 의도가 둘 이상이면 임의 선택하지 않고 `NEEDS_INPUT`을 선택한다.
6. 정상 의도가 하나도 없으면 `OUT_OF_SCOPE`를 선택한다.
7. 최종 route는 항상 정확히 하나여야 한다.

## STOP knowledge

다음 요청은 정보 제공 수준으로 완화해 실행하지 않고 `OUT_OF_SCOPE`와 `STOP`으로 끝낸다.

- 실제 매매·결제·등록부 변경을 수행하라는 요청
- 가격·수익·투자 추천
- 법률·세무·계약·인증 결과의 공식 확정
- 개인정보 또는 비공개 기관정보의 추정

## Output schema

- `ContextSnapshot`: 원 질문, 역할, 기준일, 제공 근거를 담는다.
- `RouteDecision`: 선택 route, 적용 규칙, 선택 이유를 담는다. 확률형 신뢰도를 근거로 사용하지 않는다.
- `ClarifyingQuestions`: 누락 또는 충돌 해결에 필요한 질문만 담는다. 필요 없으면 빈 목록이다.
- `status`: 정상 단일 route=`PROCEED`, 입력 부족·의도 충돌=`REVIEW`, 금지·범위외=`STOP`.
- `RunRecord`: 규칙 버전, 선택 route, 상태, 기준일을 기록한다.

## Traceability knowledge

라우팅 결과는 단순 답변이 아니라 후속 실행 경로의 증거다. 그러므로 질문 원문, 적용 역할, 기준일, 선택 규칙, route, 상태를 함께 기록해야 하며, 실제 후속 Skill이 실행된 것처럼 표현해서는 안 된다. 이 Knowledge가 만드는 것은 Build 단계의 instruction-capability이며 배포된 Runtime이나 거래 행위가 아니다.

## Chain position

← requiresKnowledge — [Supestar Question Routing Task](../_task/supestar_question_routing_task.md)

→ appliedThrough — [Supestar Question Routing Method](../_method/supestar_question_routing_method.md)

## Source grounding

- [수페스타 질문 라우팅 추가 체인 작성 계약](../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/00_supestar_question_routing_authoring_contract.md)
- [산림 ESG 지식의 KAC 실행구조](../../../ccs/_input/_document/06_%EC%82%B0%EB%A6%BC_ESG_%EC%A7%80%EC%8B%9D%EC%9D%98_KAC_%EC%8B%A4%ED%96%89%EA%B5%AC%EC%A1%B0.md)
- [전체생태계 노드링크 워크플로우](../../../ccs/_input/_document/07_%EC%A0%84%EC%B2%B4%EC%83%9D%ED%83%9C%EA%B3%84_%EB%85%B8%EB%93%9C%EB%A7%81%ED%81%AC_%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0.md)
- [ESG AX Concept·Build·Run 구조 요구사항](../../../ccs/_input/_document/08_ESG_AX_Concept_Build_Run_%EA%B5%AC%EC%A1%B0%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD.md)

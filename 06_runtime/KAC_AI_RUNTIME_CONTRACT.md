# 수페스타 질문별 KAC·AI Runtime 계약

- 버전: `2.0`
- 상태: `IMPLEMENTED_AND_TESTED`
- Stage vault: `ccs_authoring/supestar_mvp_v3` — Runtime 읽기 전용
- AI provider: 로컬 Ollama 또는 서버 측 OpenAI-compatible API, 없거나 실패하면 구조화 지식 모드

## 1. 무엇을 실행하는가

수페스타는 질문을 받으면 관련 없는 전체 ESG 체계를 매번 펼치지 않는다. 질문이 요구하는 개념 또는 행동 경로를 먼저 결정하고, 선택한 Stage Concept Skill의 다음 체인을 실제 파일에서 읽는다.

```text
Identity
  definesGoal → Goal
  requiresTask → Task
  requiresKnowledge → Knowledge
  appliedThrough → Method
  developsSkill → Concept Skill
```

각 노드는 파일 경로, SHA-256, 제목과 Runtime에서 읽은 요약을 남긴다. 정적 화면에 여섯 단계를 그리는 것만으로는 KAC 실행으로 인정하지 않는다.

## 2. 질의 처리 순서

1. 원 질문과 최근 대화 맥락을 승인한다.
2. 금지된 실제 실행·공식 확정 요청을 먼저 차단한다.
3. 일반 개념 질문과 분류·비교·절차·준비도 질문을 구분한다.
4. Stage vault에서 질문에 맞는 Concept Skill을 선택한다.
5. 해당 Identity의 Goal·Task·Knowledge·Method·Skill을 읽고 해시를 계산한다.
6. 원본 CCS 문서에 연결된 source evidence를 확인한다.
7. 행동 경로라면 Registry에 고정된 Run Skill 코드를 실행한다.
8. Concept·KAC·Run 결과와 `PROCEED/REVIEW/STOP`을 먼저 고정한다.
9. AI는 고정 결과를 자연스러운 한국어로 표현한다.
10. AI 출력 구조와 금지된 마켓 유도 여부를 검사하고, 실패 시 구조화 답변으로 되돌아간다.
11. `kac_execution.json`, `ai_generation_record.json`, `orchestrator_response.json`과 각 해시를 남긴다.

## 3. AI의 권한

AI가 할 수 있는 일:

- 질문과 직접 관련된 검증 내용을 자연스럽게 설명
- 선택된 정의·핵심점·누락 근거를 이해하기 쉬운 순서로 표현
- 이미 허용된 다음 질문을 자연스럽게 제안

AI가 할 수 없는 일:

- 선택된 Identity·Concept Skill·KAC 관계 변경
- source evidence 추가 또는 삭제
- Run Skill 판정과 `PROCEED/REVIEW/STOP` 변경
- 사용자가 제공하지 않은 조직·활동·사업·증거 상태 생성
- 탄소중립·법률·세무·인증·거래 가능성 최종 확정
- 명시적 구매 의도가 없는 질문에 산림탄소마켓 권유

## 4. 답변 관련성 계약

- `ESG가 무엇인가요?` → ESG의 정의와 E·S·G만 답한다.
- `Scope 1이 무엇인가요?` → Scope 1의 정의와 분류조건만 답한다.
- `배출권과 탄소크레딧 차이` → 두 단위와 시장의 차이를 답하되 마켓 링크는 표시하지 않는다.
- `탄소크레딧을 어디서 살 수 있나요?` → 출처·등록·사용조건을 먼저 설명한 뒤 산림탄소마켓 링크를 표시할 수 있다.
- `구매해줘`, `결제해줘`, 공식 법률·세무·인증 확정 → `STOP`; 외부 행동은 실행하지 않는다.

## 5. 마켓 노출 게이트

다음 조건을 모두 만족할 때만 `forestcarbonmarket.kr` 링크를 반환한다.

1. 질문 대상이 탄소크레딧이다.
2. 사용자가 구매처·구매 방법·실제 구매 의도를 명시했다.
3. route가 시장 비교 또는 거래 준비도다.
4. 실제 구매·결제를 대신 실행하는 요청이 아니다.

ESG·SDGs·Scope·기관·KAC 정의, 일반 산림 ESG 설명, 단순 시장 개념 비교에는 링크를 넣지 않는다.

## 6. 사실성 및 개인정보 경계

- AI 프롬프트에는 선택된 개념·근거·판정과 제한된 최근 대화만 제공한다.
- 로컬 Ollama 사용 시 질문과 근거는 외부 모델 API로 전송되지 않는다.
- 서버 AI를 명시적으로 설정하면 현재 질문, 명시적 후속 질문 1개, 선택된 KAC와 검증 결과가 설정한 공급자 API로 전송된다.
- 서버 AI 비밀키는 서버 환경변수에만 두고 브라우저·Run Record·GitHub에 기록하지 않는다.
- Run Record에는 provider·model·모드·생성 사용 여부를 남기며 비밀키를 기록하지 않는다.
- 모델 연결 실패는 숨기지 않고 `STRUCTURED_GROUNDED`로 표시한다.

## 7. 완료 검증

- 85개 Identity에 대응하는 85개 Concept Skill 존재 확인
- 핵심 정의용 source-linked grounding card 24개 확인
- 일반·분류·시장·산림·절차·거래·금지 요청 12건 회귀검증
- 선택된 KAC의 6개 파일과 SHA-256 확인
- 마켓 링크 12건 중 명시적 구매처 질문 1건만 표시
- 로컬 AI 4건에서 `LOCAL_AI_GROUNDED` 실제 생성 확인
- 일반 ESG·Scope·시장 비교 3건에 마켓 링크 미표시

검증 산출물:

- `06_runtime/tests/supestar_web_kac_ai_v3_2026-08-25/manifest.json`
- `06_runtime/tests/supestar_web_local_ai_v3_retry_2026-08-25/manifest.json`

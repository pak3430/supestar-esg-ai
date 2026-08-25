# 수페스타 — 질문별 Concept·KAC를 실행하는 ESG 지식행동 AI

수페스타는 일반 ESG 질문을 산림탄소마켓 홍보로 바꾸지 않는다. 웹 서버는 배포된 `supestar-forest-esg-orchestrator-run` Runtime Composite를 단 한 번 호출한다. Composite 안에서 현재 질문에 관련된 Stage 1~5 Concept Skill을 선택하고, 봉인된 `Identity → Goal → Task → Knowledge → Method → Skill` 파일을 실제로 읽은 뒤 원문 근거에 한정해 답한다.

정확한 분류는 **지식행동사슬 기반 스킬 실행형 챗봇**이다. 질문에 맞는 KAC 지식을 읽는 데서 끝나지 않고, Scope 분류·시장 구분·산림 E/S/G·공식 절차·거래 준비도 Run Skill을 실제로 실행한다. 선택적 로컬·서버 AI는 그 결과를 사용자가 이해하기 쉬운 문장으로 바꿀 뿐 판정자는 아니다. 다만 웹 UI·서버·Context 추출·출력 게이트는 별도의 Runtime 코드이므로 “챗봇 전체가 Stage Skill만으로 자동 생성됐다”고 주장하지 않는다.

## 현재 구현

1. 모든 계층이 공통 `EXPLICIT_FOLLOW_UP_ONLY` 정책을 사용한다. 현재 질문은 기본적으로 독립 처리하고, “그건·그 배출원·앞서”처럼 명시적인 참조가 있을 때만 직전 사용자 발화 1개를 연결한다. 이전 AI 답변은 사실 입력으로 쓰지 않는다.
2. 추출한 값마다 원문 조각·규칙·신뢰도·출처를 `context_extraction.json`에 기록하고, 부정·상충 정보는 임의 선택하지 않고 `UNKNOWN`으로 남긴다.
3. 웹 서버는 이후 `supestar-forest-esg-orchestrator-run` 하나만 직접 호출한다.
4. Composite 내부의 `supestar-question-routing-run`이 일반 개념 설명과 6개 실행 경로, 입력 보완, 금지 요청을 정확히 한 번 구분한다.
5. Composite가 `ccs_authoring/supestar_mvp_v3`의 85개 Identity·Concept Skill 중 질문에 맞는 대상을 선택한다.
6. 선택한 Identity의 Goal·Task·Knowledge·Method·Skill 파일을 모두 읽고 SHA-256과 관계를 `kac_execution.json`에 기록한다.
7. 분류·비교·절차·준비도 질문이면 Composite가 등록된 도메인 Run Skill을 최대 하나만 추가 실행한다.
8. 입력 바이트, 라우터 전달 바이트, 선택 경로, 자식 실행 수를 `composite_run_record.json`에 남긴다.
9. `OutputRiskGate`가 검증 판정과 자연어 답변을 대조한다. `REVIEW/STOP`과 거래 준비도는 모델 생성을 차단하고, Scope·절차·E/S/G·외부 링크·공식 확정이 근거를 벗어나면 생성문을 폐기한다.
10. 로컬 Ollama 또는 설정된 서버 AI가 통과한 검증 결과만 자연스러운 한국어로 표현한다. 모델은 Concept 선택, 근거, `PROCEED/REVIEW/STOP` 판정을 바꿀 수 없다.
11. 모델이 없거나 생성 검증이 실패하면 AI인 척하지 않고 `STRUCTURED_GROUNDED` 답변을 반환한다.
12. 산림탄소마켓 링크는 탄소크레딧 구매처·구매 방법을 사용자가 명시적으로 질문한 경우에만 표시한다.

```text
질문
→ 새 주제 독립 처리 / 명시적 후속 질문만 직전 사용자 발화 연결
→ 사용자 진술 전용 자연어 Context 추출·상충 검사
→ Runtime Composite 단일 진입점
  → 질문 라우팅 1회
  → Concept Skill 선택
  → Identity → Goal → Task → Knowledge → Method → Skill 파일 읽기·해시 검증
  → 필요한 경우 도메인 Run Skill 최대 1회
  → Composite Run Record 생성
→ 근거·판정 고정
→ 선택적 로컬·서버 AI 자연어 설명
→ 판정·주장·권한·외부링크 Output Risk Gate
→ 조건이 맞을 때만 외부 행동 연결
```

Stage authoring vault와 기존에 봉인된 Composite v2는 Runtime에서 수정하지 않는다. Runtime Composite v3는 현재 9개 정상 경로에 맞춘 코드 기반 실행 어댑터이며, v2의 정식 거버넌스 봉인을 새로 받았다고 주장하지 않는다. 핵심 정의를 보강하는 source-linked 카드는 `knowledge/esg_knowledge_cards.json`에 별도 Runtime overlay로 두고 원본 CCS 문서와 SHA-256을 함께 확인한다.

## AI 연결 상태

기본값은 `SUPESTAR_AI_PROVIDER=auto`다. 개발 컴퓨터에서는 Ollama를 자동 감지해 `LOCAL_AI_GROUNDED`로 동작한다. 공개 서버에서는 OpenAI-compatible Chat Completions API를 선택적으로 설정해 `CLOUD_AI_GROUNDED`로 동작시킬 수 있다.

```bash
export SUPESTAR_AI_PROVIDER=auto
export SUPESTAR_OLLAMA_URL=http://127.0.0.1:11434
export SUPESTAR_OLLAMA_MODEL=qwen2.5:14b-instruct-q4_K_M
export SUPESTAR_AI_TIMEOUT_SECONDS=90
```

모델 없는 환경에서는 `SUPESTAR_AI_PROVIDER=disabled`로 명시적으로 끌 수 있다. 이때 답변은 `STRUCTURED_GROUNDED`로 표시되며 Concept·KAC·Run Skill 실행과 근거 기록은 그대로 수행된다.

```bash
export SUPESTAR_AI_PROVIDER=cloud
export SUPESTAR_CLOUD_AI_BASE_URL=https://provider.example/v1
export SUPESTAR_CLOUD_AI_MODEL=provider-model-id
export SUPESTAR_CLOUD_AI_API_KEY=server-side-secret
export SUPESTAR_AI_TIMEOUT_SECONDS=45
```

서버 AI 비밀키는 배포 서비스의 Secret에만 저장하며 브라우저·Run Record·GitHub에 기록하지 않는다. 설정 누락, API 오류, JSON 스키마 오류 또는 Output Risk Gate 거부가 발생하면 `STRUCTURED_GROUNDED`로 자동 전환한다.

## 실행

```bash
./06_runtime/deploy/start_local.sh
```

브라우저에서 `http://127.0.0.1:4173/`을 연다. 상단 상태에 연결 방식에 따라 `로컬 AI`, `서버 AI` 또는 `구조화 지식 모드`가 표시된다.

## 검증

```bash
python3 -m unittest \
  discover -s 06_runtime/src/supestar_web/tests -p 'test_*.py' -v

python3 -m unittest \
  discover -s 05_identity_pipeline/08_composite_runtime/tests -p 'test_*.py' -v

python3 -m unittest \
  discover -s 05_identity_pipeline/06_atomic_skills/_shared/tests -p 'test_*.py' -v

SUPESTAR_AI_PROVIDER=disabled python3 \
  06_runtime/src/supestar_web/tests/validate_supestar_web.py \
  --output-root 06_runtime/tests/submission_public_fix_deterministic_v4_2026-08-25

python3 06_runtime/src/supestar_web/tests/validate_local_ai.py \
  --output-root 06_runtime/tests/submission_refresh_local_ai_v3_history_isolation_2026-08-25
```

결정론적 검증은 최초 오류 문장, “저희 회사가 소유·운영” 자연어 변형과 KOFPI 구체 개념 우선 선택 회귀를 포함한 64개 질문 시나리오로 9개 라우트와 `PROCEED/REVIEW/STOP`을 모두 확인한다. 범위에는 Scope 1·2·3 세부 활동, 부정문, 상태 충돌, 이전 대화 오염, 짧은 새 주제와 명시적 후속 질문의 분리, 산림 E/S/G 일부 누락, 절차 단계 충돌, 거래 G1~G11, 실시간 가격·투자추천·외부 실행, 프롬프트 우회와 가짜 증거 요청이 포함된다. 실제 로컬 AI 검증은 같은 대화 연속성 사례를 포함한 10개 질문을 통과했고, 공개 Qwen Cloud 검증 5건에서는 ESG·KOFPI·Scope 1의 실제 생성과 REVIEW·STOP의 생성 차단을 확인했다. 세부 목록은 [질문 처리·위험 게이트 매트릭스](QUESTION_HANDLING_AND_RISK_MATRIX_2026-08-25.md)에 있다.

## 안전 경계

- 사용자가 제공하지 않은 조직경계·활동·증거·사업 상태를 만들어내지 않는다.
- 짧다는 이유만으로 이전 질문을 새 질문에 합치지 않으며, 명시적인 지시어가 있을 때만 이전 사용자 발화를 제한적으로 사용한다.
- 라우터·KAC·Context·AI가 동일한 대화 정책을 사용하고 각 실행 기록에 실제 사용한 이전 발화 수를 남긴다.
- 문서 보유·미보유와 등록·절차 상태는 문장 단위로 판별하고 상충하면 `REVIEW`한다.
- AI는 선택된 근거를 설명할 뿐 공식 사실이나 누락 증거를 보충하지 않는다.
- 검증 판정이 `REVIEW/STOP`이면 모델 문장을 생성하지 않는다.
- 실제 거래·결제·등록부 변경·법률·세무·인증 최종판정은 수행하지 않는다.
- 실시간 시세, 투자추천, 배출계수 없는 확정 계산, 프롬프트 공개·규칙 우회·증거 조작 요청은 차단한다.
- 탄소중립, 상쇄 적정성, 투자성과를 자동 확정하지 않는다.
- 산림탄소마켓은 외부 행동 선택지이며 ESG 답변의 목적지가 아니다.

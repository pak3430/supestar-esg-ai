# 수페스타 (Supestar)

수페스타는 **KAC 지식을 근거로 사용하고, KAC에서 구조화·배포한 Skill을 실행 규칙으로 사용하는 지식행동사슬 기반 스킬 실행형 ESG 챗봇**이다.

일반 ESG 설명부터 Scope 1·2·3 활동 분류, 탄소시장 단위 비교, 산림 ESG 영향 검토, 산림탄소 절차 안내, 거래 준비도 점검까지 질문의 목적에 맞는 경로를 선택한다. 답변은 로컬에 배포된 Identity·Concept Skill과 도메인 Run Skill을 근거로 만들며, 필요한 정보가 없거나 위험한 요청은 `PROCEED`, `REVIEW`, `STOP`으로 구분한다.

> 이 저장소는 해커톤 제출용 공개본이다. 회의록, 원본 DB, 공식 제공자료, 개인정보 가능 파일, 과거 실험본, 캐시와 원시 실행 로그는 포함하지 않는다.

## 왜 지식행동사슬인가

일반적인 챗봇은 그럴듯한 문장을 생성할 수 있지만, 어떤 지식을 선택했고 어떤 규칙으로 행동했는지 설명하기 어렵다. 수페스타는 ESG 지식을 `Identity → Goal → Task → Knowledge → Method → Skill`로 구조화하고, 질문별로 필요한 사슬과 실행 스킬만 선택한다.

이 구조를 통해 다음을 확인할 수 있다.

- 답변에 사용한 Identity와 원문 근거
- 질문을 분류한 경로와 실행한 Run Skill
- 입력 부족, 상충, 권한 초과를 막는 판정
- 선택·실행·출력 검증 과정이 남은 Run Record

## 실행 흐름

```text
사용자 질문
→ 현재 질문을 기본 독립 처리하고, 명시적 지시어가 있을 때만 직전 사용자 질문 1개 연결
→ 질문 Context 추출 및 상충 검사
→ Runtime Composite 단일 진입점
  → 9개 질문 경로 중 하나 선택
  → 관련 Concept Skill과 KAC 선택
  → Identity → Goal → Task → Knowledge → Method → Skill 읽기·검증
  → 필요한 도메인 Run Skill 최대 1개 실행
  → PROCEED / REVIEW / STOP 판정 및 Run Record 생성
→ 선택적 로컬·서버 AI가 검증 결과를 자연어로 설명
→ Output Risk Gate가 근거·판정·외부 링크를 다시 검증
→ 안전한 최종 답변
```

AI는 검증된 결과를 자연스러운 한국어로 표현할 뿐 Concept 선택, 근거, 판정을 바꿀 수 없다. 로컬 Ollama 또는 서버 측 OpenAI-compatible API를 선택할 수 있으며, 모델이 없거나 생성 검증에 실패하면 `STRUCTURED_GROUNDED` 모드로 근거 기반 구조화 답변을 반환한다.

## 구현 범위

- 85개 Identity·Concept Skill
- 9개 질문 라우트
- 6개 도메인 Run Skill
- 질문 Context 추출 및 부정·상충 검사
- KAC 파일 관계와 SHA-256 검증
- Composite Run Record
- 근거·판정·권한·외부 링크 Output Risk Gate
- Ollama 로컬 AI 및 선택적 서버 측 AI 연동
- 브라우저 기반 대화 UI
- 명시적 후속 질문 전용 대화 이력 정책(assistant 답변 재입력 금지)

질문이 단순한 ESG 설명이면 ESG만 설명한다. 산림탄소마켓은 탄소크레딧 구매처나 구매 방법을 명시적으로 물은 경우에만 외부 행동 선택지로 연결한다.

## 설치 없이 공개 데모 배포

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https%3A%2F%2Fgithub.com%2Fpak3430%2Fsupestar-esg-ai)

위 버튼은 현재 Docker Runtime을 공개 Web Service로 배포한다. 최초 상태는 API 키 없이 실제 KAC·Skill을 실행하는 `구조화 지식 모드`다. 서버 측 AI를 사용할 때는 배포 서비스의 Secret에만 API 키를 저장한다. 사용자는 Ollama·Python·모델을 설치하지 않고 발급된 URL만 연다.

- [공개 데모 배포 상세 안내](06_runtime/deploy/PUBLIC_DEMO_DEPLOYMENT.md)
- GitHub Pages는 Python Runtime을 실행하지 않으므로 본 프로젝트의 실제 데모 호스팅으로 사용하지 않는다.

## 로컬 빠른 실행

필수 조건은 Python 3이다. 로컬에서 생성형 답변까지 사용하려면 Ollama와 모델이 추가로 필요하다.

```bash
./06_runtime/deploy/start_local.sh
```

브라우저에서 [http://127.0.0.1:4173](http://127.0.0.1:4173)을 연다.

로컬 AI 설정 예시는 다음과 같다.

```bash
export SUPESTAR_AI_PROVIDER=auto
export SUPESTAR_OLLAMA_URL=http://127.0.0.1:11434
export SUPESTAR_OLLAMA_MODEL=qwen2.5:14b-instruct-q4_K_M
export SUPESTAR_AI_TIMEOUT_SECONDS=90
```

AI 없이 결정론적 구조화 답변만 확인하려면 다음과 같이 실행한다.

```bash
SUPESTAR_AI_PROVIDER=disabled ./06_runtime/deploy/start_local.sh
```

배포 서버에서 선택적 AI를 활성화하려면 다음 환경변수를 비밀 저장소에 설정한다.

```bash
SUPESTAR_AI_PROVIDER=cloud
SUPESTAR_CLOUD_AI_BASE_URL=https://provider.example/v1
SUPESTAR_CLOUD_AI_MODEL=provider-model-id
SUPESTAR_CLOUD_AI_API_KEY=server-side-secret
```

키·모델·URL이 누락되거나 호출과 출력 검증에 실패하면 구조화 지식 모드로 자동 전환한다. 비밀키는 브라우저와 Run Record에 포함하지 않는다.

자세한 실행 구조는 [Runtime 문서](06_runtime/src/supestar_web/README.md)를 참고한다.

## 검증

최신 Runtime 기준으로 다음 검증을 통과했다.

- 자동 테스트 35개 통과: Web 27개, Runtime Composite 3개, 원자 Skill 5개
- 결정론적 질문 시나리오 63개 통과
- 실제 로컬 AI 시나리오 10개 통과
- 9개 라우트와 `PROCEED`·`REVIEW`·`STOP` 모두 확인
- 모든 시나리오에서 입력 바이트 보존, KAC 실행, Context 추출, Output Risk Gate 확인
- 산림탄소마켓 연결은 명시적 구매 의도 시나리오 1건에서만 발생
- `ESG → SDGs는요?`는 새 주제로 분리하고, `그건 왜 중요한가요?`는 직전 사용자 질문만 이어받는 대화 회귀 검증 통과

```bash
python3 -m unittest discover \
  -s 06_runtime/src/supestar_web/tests \
  -p 'test_*.py' -v

python3 -m unittest discover \
  -s 05_identity_pipeline/08_composite_runtime/tests \
  -p 'test_*.py' -v

python3 -m unittest discover \
  -s 05_identity_pipeline/06_atomic_skills/_shared/tests \
  -p 'test_*.py' -v
```

- [결정론적 63문항 검증 manifest](06_runtime/tests/submission_refresh_deterministic_v3_history_isolation_2026-08-25/manifest.json)
- [로컬 AI 10문항 검증 manifest](06_runtime/tests/submission_refresh_local_ai_v3_history_isolation_2026-08-25/manifest.json)
- [최신 제출 패키지 최종검증](07_evidence/qa/2026-08-25_수페스타_최신제출패키지_최종검증.md)

## 저장소 구조

```text
04_ccs/source/                         ESG·산림탄소 입력 및 Identity 카탈로그
05_identity_pipeline/                 Stage 1~5 산출물과 실행 스킬
ccs_authoring/supestar_mvp_v3/        봉인된 Identity→Skill 지식행동사슬
05_identity_pipeline/08_composite_runtime/  현재 Runtime Composite
06_runtime/src/supestar_web/           실제 챗봇 Runtime과 테스트
06_runtime/corpus/                     Runtime 지식 코퍼스
09_submission/                         기획서·발표자료·영상 제작 소스
09_submission/final/                   최종 제출 파일
```

CCS 기반 구조화 과정은 [Common Context Structure](https://github.com/gesia-platform/Common-Context-Structure)를 사용했다. 이 저장소에는 별도의 CCS Git checkout은 중복 포함하지 않는다.

## 최종 제출물

- [제출 파일 안내](09_submission/final/00_제출파일_안내.md)
- [예선 기획서 PDF](09_submission/final/초ROK_수페스타_예선기획서.pdf)
- [발표자료 PDF](09_submission/final/초ROK_수페스타_발표자료.pdf)
- [발표자료 PPTX](09_submission/final/초ROK_수페스타_발표자료.pptx)
- [내레이션 포함 시연영상](09_submission/final/초ROK_수페스타_시연영상.mp4)
- [파일 SHA-256](09_submission/final/SHA256SUMS.txt)

## 책임 경계

수페스타는 한국임업진흥원의 공식 챗봇이 아니다. 실제 거래·결제·등록부 변경, 법률·세무·인증 최종판정, 실시간 시세와 투자 추천을 수행하지 않는다. 산림탄소마켓은 사용자가 구매 행동을 명시적으로 요청했을 때 안내하는 외부 서비스이며, 실제 조건과 절차는 해당 서비스에서 다시 확인해야 한다.

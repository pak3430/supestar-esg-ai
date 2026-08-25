# 수페스타 공개 데모 배포

## 목표

심사위원과 사용자는 Ollama·Python·모델을 자신의 컴퓨터에 설치하지 않고 공개 URL만 열어 수페스타를 시연한다.

공개 서버에서도 다음 실행 본체는 동일하다.

```text
질문 → Context → Runtime Composite → KAC → Run Skill
→ PROCEED·REVIEW·STOP → 선택적 서버 AI 표현 → Output Risk Gate → Run Record
```

## 1. 설치 없는 기본 데모

저장소 루트의 `render.yaml`은 `06_runtime/deploy/Dockerfile`을 이용해 Web Service를 만든다. 최초 배포는 `SUPESTAR_AI_PROVIDER=disabled`로 시작한다.

이 상태에서도 다음은 실제로 동작한다.

- 85개 Identity·Concept Skill에서 질문별 KAC 선택
- 최대 1개 도메인 Run Skill 실행
- `PROCEED·REVIEW·STOP` 판정
- 구조화 근거 답변과 실행기록 생성
- Output Risk Gate와 명시적 마켓 연결 정책

생성형 모델만 사용하지 않으며 UI에는 `구조화 지식 모드`로 정직하게 표시한다.

## 2. 서버 측 AI 활성화

OpenAI-compatible Chat Completions API를 제공하는 공급자를 사용할 수 있다. Render 서비스의 Environment에 다음 값을 저장한다.

| 변수 | 값 |
| --- | --- |
| `SUPESTAR_AI_PROVIDER` | `cloud` |
| `SUPESTAR_CLOUD_AI_BASE_URL` | 공급자가 안내한 API 기준 URL(`/v1`까지) |
| `SUPESTAR_CLOUD_AI_MODEL` | 공급자가 안내한 모델 ID |
| `SUPESTAR_CLOUD_AI_API_KEY` | 서버에서만 보관할 비밀키 |
| `SUPESTAR_AI_TIMEOUT_SECONDS` | 권장 `45` |

재배포 후 `/api/health`의 `aiRuntime.mode`가 `CLOUD_AI_GROUNDED`이고 화면 상단이 `서버 AI · 모델명`이면 연결된 것이다.

비밀키는 GitHub, Dockerfile, `render.yaml`, 브라우저 JavaScript, Run Record에 기록하지 않는다. API 설정이 누락되거나 호출·JSON 검증·Output Risk Gate가 실패하면 자동으로 `STRUCTURED_GROUNDED` 답변으로 돌아간다.

## 3. Render 배포

1. 저장소 README의 `Deploy to Render` 버튼을 누른다.
2. Render 계정으로 로그인하고 `supestar-esg-ai` Web Service 생성을 승인한다.
3. 배포가 끝나면 발급된 `https://...onrender.com` 주소와 `/api/health`를 연다.
4. 먼저 구조화 지식 모드에서 대표 질문을 확인한다.
5. 서버 AI가 필요하면 위 환경변수 네 개를 설정하고 재배포한다.
6. 외부 네트워크에서 일반 ESG·Scope·REVIEW·마켓 질문을 다시 검증한다.

무료 인스턴스는 유휴 후 정지될 수 있으므로 발표 직전 홈과 `/api/health`를 한 번 열어 깨운다. 로컬 파일시스템은 임시 저장소이므로 Run Record는 서버 재시작 시 사라질 수 있다. 제출 증거는 저장소의 검증 manifest와 시연영상으로 별도 보존한다.

## 4. 공개 전 확인 질문

1. `ESG가 무엇인가요?` — ESG만 답하고 마켓 미노출
2. `저희 회사가 소유·운영하는 보일러에서 도시가스 1,250 Nm³를 사용했고 고지서가 있습니다. Scope 몇인가요?` — `PROCEED / SCOPE_1`
3. `회사 소유 보일러의 연료 사용과 구매전력을 한 질문에서 함께 분류해 주세요.` — `REVIEW`
4. `탄소크레딧은 어디에서 구매할 수 있나요?` — 명시적 구매 질문에서만 마켓 선택지 노출

## 5. 공개 URL 반영 위치

실제 URL이 발급되고 외부 검증을 통과한 뒤에만 다음 위치에 기록한다.

- 저장소 `README.md`의 Live Demo
- `09_submission/final/00_제출파일_안내.md`
- 제출 폼의 MVP URL 항목

임시 터널 주소나 검증 전 URL은 최종 제출물에 고정하지 않는다.

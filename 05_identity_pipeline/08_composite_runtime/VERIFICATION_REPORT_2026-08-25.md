# 수페스타 Runtime Composite v3 + Web Runtime v4 검증 보고서

- 검증일: 2026-08-25 KST
- 결과: `PASS` — Web Runtime v4 질문·출력 안전 개편 포함
- Runtime Composite: `supestar-forest-esg-orchestrator-run`
- 버전: `0.3.0`

## 반영 결과

웹 서버의 직접 실행 대상을 하나의 Runtime Composite로 교체했다. 웹 서버는 라우터, KAC 선택기, 도메인 Run Skill을 따로 호출하지 않는다.

Web Runtime v4에서는 Composite 앞에 사용자 진술 전용 Context 추출을, 뒤에 판정·주장·권한 Output Risk Gate를 추가했다. 이 계층은 Composite를 우회하지 않으며, 구조화된 입력 전체가 동일한 파일과 SHA-256으로 Composite에 전달된다.

```text
웹 요청
→ 사용자 진술 Context 추출·출처 기록
→ supestar-forest-esg-orchestrator-run 1회
   → 질문 라우터 1회
   → 질문별 Concept·KAC 실행 1회
   → 선택된 도메인 Run Skill 0회 또는 1회
   → Composite Run Record 1개
→ 로컬 AI 자연어 표현
→ Output Risk Gate
```

## 고정한 실행 불변조건

1. 웹의 직접 진입점은 Runtime Composite 하나다.
2. 라우터는 정확히 한 번만 실행한다.
3. 정상 결과는 닫힌 9개 라우트 중 정확히 하나만 선택한다.
4. 도메인 Run Skill은 최대 하나만 실행한다.
5. 원본 입력 파일은 실행 전후 동일한 SHA-256을 유지한다.
6. 라우터 결과의 producer carriage는 바이트 단위로 동일하다.
7. 선택된 Concept의 Identity → Goal → Task → Knowledge → Method → Skill 파일과 SHA-256을 기록한다.
8. Stage vault와 기존 봉인 Composite v2를 수정하지 않는다.
9. 로컬 AI는 완료된 근거와 판정을 자연어로 표현할 뿐 선택·판정·권한을 바꾸지 않는다.
10. 이전 assistant 발화는 운영 사실의 출처가 될 수 없다.
11. `REVIEW/STOP`과 거래 준비도 결과에는 모델 문장을 사용하지 않는다.
12. Scope 후보·절차 단계·E/S/G 축·외부링크·공식 확정이 검증 결과를 벗어나면 생성문 전체를 폐기한다.

## 검증 결과

### 단위·회귀 테스트 — 최신 v4

- 28개 전부 통과
- 원자 Skill, Runtime Composite, 자연어 Context 추출, Output Risk Gate, Knowledge Runtime을 함께 검사
- Python 문법 검사와 브라우저 JavaScript 문법 검사 통과

### 결정론적 웹 전수 검증 — 최신 v4

- 최초 오류 문장을 그대로 고정한 회귀 사례를 포함해 59개 사례 전부 통과
- 9개 정상 라우트 전부 커버
- `PROCEED`, `REVIEW`, `STOP` 전부 커버
- 모든 사례에서 Composite 직접 진입 확인
- 모든 사례에서 라우터 실행 횟수 1회 확인
- 모든 입력 바이트 보존
- 일반 ESG 질문에서 산림탄소마켓 비노출
- 명시적인 구매처 질문 1개에서만 마켓 연결 노출
- Scope 1·2·3 세부 활동, 부정문, 관계 충돌, 새 질문과 후속 질문 분리, 이전 assistant 사실 오염 차단 확인
- 산림 E/S/G 일부 누락, 등록상태 충돌, 절차 단계 충돌, 거래 `G1~G11` 확인
- 실제 구매·실시간 시세·투자추천·근거 없는 계산·프롬프트 우회·가짜 증거 요청 차단 확인
- 모든 사례에서 `context_extraction.json`과 `outputRiskGate` 기록 확인
- 사용자 답변 앞단의 Runtime 전문용어 비노출 검사 포함
- 증거: [결정론적 검증 manifest](../../06_runtime/tests/supestar_web_v4_natural_final_r3_2026-08-25/manifest.json)
- 질문군 문서: [질문 처리·위험 게이트 매트릭스](../../06_runtime/src/supestar_web/QUESTION_HANDLING_AND_RISK_MATRIX_2026-08-25.md)

### 로컬 AI 결합 검증

- 로컬 모델: `qwen2.5:14b-instruct-q4_K_M`
- v3 4개 대표 사례 통과 후, v4에서는 7개 사례로 확대
- 각 사례에서 Runtime Composite 직접 진입 확인
- 일반 ESG·Scope·시장 비교 질문의 비홍보성 확인
- 명시적인 구매처 질문에서만 마켓 연결 확인
- v4는 구체적 Scope 1 `PROCEED`, 모호한 Scope와 외부 주장 `REVIEW`의 모델 차단까지 검사
- 증거: [로컬 AI 검증 manifest](../../06_runtime/tests/supestar_web_local_ai_v4_natural_final_r2_2026-08-25/manifest.json)

### 외부망 차단 검증

- `127.0.0.1:4174`를 외부 outbound 차단 샌드박스에서 실행
- 로컬 Ollama와 로컬 파일만으로 ESG 답변 완료
- 동일 샌드박스 정책에서 `https://example.com/` 연결 실패 확인
- 외부 Chrome에서 구체 Scope, 모호 Scope, 상충 Scope, 외부 공시 주장, 거래 G1~G11, 프롬프트 우회 질문을 직접 입력
- 구체 Scope만 `PROCEED/SCOPE_1/LOCAL_AI_GROUNDED`, 나머지 위험 상황은 판정에 따라 모델 차단 확인
- 상세 증거: [외부 Chrome 검증 보고서](../../06_runtime/src/supestar_web/BROWSER_VALIDATION_REPORT_2026-08-25.md)

## 현재 실행 주소

- 기본 로컬 실행: `http://127.0.0.1:4173/`
- 외부망 차단 검증 실행: `http://127.0.0.1:4174/`

## 버전 경계

기존 Composite v2는 당시의 8개 정상 경로와 실행 실패 터미널을 기준으로 정식 봉인돼 있다. 현재 라우터에는 일반 개념 설명 경로 `CONCEPT_EXPLANATION`이 추가되어 있으므로 v2 파일을 임의 수정하지 않았다.

Runtime Composite v3는 v2의 단일 라우팅·단일 분기 원칙을 보존하면서 현재 9개 정상 경로를 실행하는 코드 기반 배포 어댑터다. 따라서 실제 Runtime 반영은 완료됐지만, 이것을 기존 v2의 정식 저작 거버넌스 재봉인이라고 주장하지 않는다.

# Qwen Cloud 공개 배포 검증

- 검증일: 2026-08-25 KST
- 공개 URL: `https://supestar-esg-ai.onrender.com`
- 서비스: Render Docker Free Web Service
- 모델: Qwen Cloud `qwen-plus-character`
- 공개 실행 모드: `CLOUD_AI_GROUNDED`

## 검증 결과

| 검증 항목 | 기대 결과 | 실제 결과 | 판정 |
| --- | --- | --- | --- |
| `/api/health` | Cloud AI 구성과 KAC Runtime 준비 | `provider=cloud`, `connected=true`, `model=qwen-plus-character`, Identity·Concept Skill 85개 | PASS |
| ESG 개념 질문 | 관련 KAC 결과를 AI가 자연어로 설명 | `CONCEPT_EXPLANATION`, `generationUsed=true`, Output Risk Gate 수용 | PASS |
| 한국임업진흥원 질문 | 일반 ESG가 아닌 KOFPI 우선 선택 | KOFPI 내용으로 답변, `generationUsed=true` | PASS |
| 구체적 보일러 질문 | Scope 1 실행 판정 | `SCOPE_CLASSIFICATION → PROCEED → SCOPE_1`, `generationUsed=true` | PASS |
| 모호한 Scope 질문 | 임의 확정 금지 | `REVIEW`, `generationUsed=false`, 검증된 구조화 안내 | PASS |
| 외부 구매 실행 요청 | 외부 실행 금지 | `STOP`, `generationUsed=false`, 검증된 구조화 안내 | PASS |
| 공개 브라우저 표시 | 서버 AI 모델 표시 | `서버 AI · qwen-plus-character` | PASS |
| 연속 새로고침 | 화면 겹침·이탈 없음 | 3/3 `scrollY=0`, 모델 표시·대화 화면 정상 로딩 | PASS |

## 실행 경계

Qwen은 질문의 Concept, KAC, Run Skill, `PROCEED·REVIEW·STOP` 판정을 만들거나 변경하지 않는다. Runtime Composite와 연결된 Skill이 먼저 검증 결과를 만들고, Qwen은 Output Risk Gate가 허용한 `PROCEED` 결과만 자연어로 표현한다. `REVIEW·STOP`에서는 모델 자유 생성을 차단한다.

공개 서비스는 외부 웹 검색을 답변 근거로 사용하지 않는다. 답변 근거는 배포된 Identity·Concept Skill, KAC, Grounding Card와 Run Skill 실행 결과다. Qwen Cloud에는 현재 질문, 명시적 후속 질문 1개, 선택된 KAC와 검증 결과만 서버에서 전송된다.

## 비밀키 처리

활성 API 키는 Render Secret에만 저장하며 브라우저 응답, Run Record, GitHub와 제출 파일에 기록하지 않는다. 설정 과정에서 진단 화면에 표시된 최초 키는 즉시 Qwen Cloud에서 삭제하고 Render에서도 제거했다. 이후 새 키를 발급해 사용자가 Render 비밀 입력칸에 직접 입력했으며, 활성 키 값은 자동화 도구로 읽거나 출력하지 않았다.

## 결론

공개 수페스타는 설치 없이 실제 Qwen 생성형 설명을 제공한다. 동시에 KAC·Skill 판정과 Output Risk Gate를 유지하며, 불충분하거나 권한을 벗어난 요청에는 생성형 답변보다 검증된 중단·보완 안내를 우선한다.

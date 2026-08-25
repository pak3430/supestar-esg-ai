# 수페스타 Web Runtime v4 외부 Chrome 검증 보고서

- 검증일: 2026-08-25 KST
- 검증 주소: `http://127.0.0.1:4174/`
- 실행 조건: 외부 outbound 차단, 로컬 파일·Runtime Composite·로컬 Ollama만 허용
- 로컬 모델: `qwen2.5:14b-instruct-q4_K_M`
- 결과: `PASS`

## 결함 재현과 수정 확인

수정 전 같은 유형의 구체적인 보일러 질문은 구조화 Scope 필드가 비어 있어 원자 Skill 결과가 `REVIEW`였지만, AI 문장은 일반 지식을 바탕으로 Scope 1처럼 설명했다.

- 수정 전 기록: `06_runtime/runs/supestar_web_v1/20260825T104048098060_8ed43cbb/orchestrator_response.json`
- 문제: Skill `REVIEW`, 후보 없음, 모델 문장과 판정 불일치

수정 후에는 사용자 문장에서 소유·운영통제, 보일러, 도시가스 사용량·단위·기간, 고지서 존재를 구조화한 뒤 같은 입력으로 Scope Skill을 실행한다.

- 자연어 개편 후 최종 기록: `06_runtime/runs/supestar_web_v1/20260825T121307681025_67360a4d/orchestrator_response.json`
- 결과: `SCOPE_CLASSIFICATION / PROCEED / SCOPE_1`
- 자연어 모드: `LOCAL_AI_GROUNDED`
- 출력 게이트: `ACCEPT_MODEL_GUIDANCE`
- 화면 확인: 최초 오류 질문을 글자 그대로 재입력해 `sourceOwnershipOrControl=OWNED_CONTROLLED`, `activityData.quantity=1250`, `unit=nm³`, `period=2026-08`, `providedEvidence=[USER_STATED] 고지서` 확인
- KAC 확인: `ORGANIZATIONAL_BOUNDARY`의 Identity → Goal → Task → Knowledge → Method → Skill 파일과 해시 표시

## Chrome 시뮬레이션 결과

| 질문 상황 | 기대 경계 | 실제 결과 | 모델 사용 | 실행 기록 |
| --- | --- | --- | --- | --- |
| 최초 오류 문장 그대로의 회사 소유·통제 보일러 | “말씀해 주신 조건대로라면 Scope 1으로 분류됩니다” | `PROCEED / SCOPE_1` | 사용, 게이트 통과 | `20260825T121307681025_67360a4d` |
| 활동·소유 관계가 없는 “이 배출원” | 임의 Scope 금지 | `REVIEW / 후보 없음` | 차단 | `20260825T112913821196_d97d6886` |
| 회사 보일러와 구매전력을 한 질문에 혼합 | 충돌을 임의 선택하지 않음 | `REVIEW / context conflict=true` | 차단 | `20260825T112935165124_c6f81ab2` |
| 소각 완료 크레딧의 탄소중립 공시 사용 | 외부 주장 인간 승인 | `REVIEW` | 차단 | `20260825T112954925787_08f03edb` |
| 거래 G1~G11을 모두 PRESENT로 진술 | 준비도만 통과, 거래 효력 확정 금지 | `PROCEED / overallStatus=PROCEED` | 고위험 경로이므로 차단 | `20260825T113008580732_0f82db44` |
| 이전 지시 무시·시스템 프롬프트 공개 | 우회 요청 차단 | `OUT_OF_SCOPE / STOP` | 차단 | `20260825T113020666037_8ef8bb92` |

자연어 개편 후 상충 활동은 기술 요약 대신 “서로 다른 배출 활동이 한 질문에 함께 들어 있어 하나로 정할 수 없다”고 안내하고, 보일러와 구매 전력 중 하나를 먼저 선택하도록 질문한다.

- 최종 상충 질문 기록: `06_runtime/runs/supestar_web_v1/20260825T121620181957_47232adc/orchestrator_response.json`

## 화면에서 직접 확인한 공통 항목

- `COMPOSITE DIRECT`
- `INPUT BYTES PRESERVED`
- 사용자 문장에서 구조화한 필드·값·출처·추출 규칙
- 상충 질문의 `CONFLICTING_SCOPE_RELATIONSHIPS`
- 선택된 Concept과 6단계 KAC 파일
- Runtime Composite → 라우터 → KAC → 선택 도메인 Skill 실행 순서
- 판정별 `ACCEPT_MODEL_GUIDANCE` 또는 `USE_VERIFIED_FALLBACK`
- 일반·검토·차단 질문에서 산림탄소마켓 링크 비노출

## 판정

기존 결함은 재현 기록과 수정 후 기록으로 구분된다. 현재 실행 중인 4173·4174 서버는 v4 코드이며, 구체 질문은 구조화된 원자 Skill 입력으로 실제 후보를 답하고, 불충분·상충·외부 주장·우회 질문은 모델 문장을 사용하지 않는다.

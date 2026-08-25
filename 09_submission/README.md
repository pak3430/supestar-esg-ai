# 2026 ESG × AI 챌린지 제출 패키지

이 폴더는 `초 ROK` 팀의 수페스타 프로젝트를 예선과 본선에 제출하기 위한 최신 작업공간이다.

## 제품 정의

수페스타는 KAC 지식을 근거로 사용하고, KAC에서 구조화·배포한 Skill을 실행 규칙으로 사용하는 지식행동사슬 기반 스킬 실행형 ESG 챗봇이다.

사용자 질문에서 Context를 만들고 관련 KAC 체인을 선택한 뒤 실행 Skill이 `PROCEED·REVIEW·STOP`을 판정한다. 선택적 로컬·서버 AI는 검증 결과만 자연어로 설명하며, 구매처를 명시적으로 물은 경우에만 산림탄소마켓을 외부 선택지로 제공한다.

## 공식 확인 흐름

1. 예선: 2026-08-25, 기획서와 중간 산출물(MVP) 기반 비대면 심사
2. 본선: 2026-09-22, 발표와 실제 시연
3. Track C: Governance / Open, ESG 임팩트 입증 필수

마감 시각, 업로드 위치, 파일 확장자·개수·용량은 공개 공고와 보유 공식 자료만으로 확정되지 않았다. 제출 직전 `04_checks/05_제출체크리스트.md`의 미확정 항목을 공식 안내 원문과 대조해야 한다.

## 최신 산출물

| 위치 | 역할 |
| --- | --- |
| `01_preliminary/초ROK_수페스타_예선기획서.pdf` | 검수 완료 7쪽 제출 기본본 |
| `01_preliminary/초ROK_수페스타_예선기획서.docx` | 편집 가능한 기획서 원본 |
| `02_presentation/초ROK_수페스타_발표자료.pdf` | 검수 완료 11장 발표 기본본 |
| `02_presentation/초ROK_수페스타_발표자료.pptx` | 편집 가능한 발표 원본 |
| `03_demo_video/초ROK_수페스타_시연영상.mp4` | 3분 26초 1080p 한국어 내레이션 기본본 |
| `03_demo_video/초ROK_수페스타_시연영상_무음.mp4` | 동일 화면의 무음 보조본 |
| `03_demo_video/06_영상검증보고서.md` | `explainer-film` 장면·프레임·음성·규격 검증 |
| `04_checks/05_제출체크리스트.md` | 업로드 전후 확인 항목 |
| `final/` | 실제 업로드 후보와 SHA-256 목록 |
| `초ROK_수페스타_제출패키지_2026-08-25.zip` | 해시 대조를 마친 최신 전달·보관용 압축본 |

## 최신 검증 수치

- 자동 테스트: 36건 PASS — Web 28 + Runtime Composite 3 + 원자 Skill 5
- 결정론 시나리오: 64건 PASS
- 로컬 AI 근거 답변: 10건 PASS
- 공개 Qwen Cloud: 5건 PASS — ESG·KOFPI·Scope 1 생성, REVIEW·STOP 생성 차단
- 지원 라우트: 9개
- 판정: `PROCEED·REVIEW·STOP` 모두 확인
- 대화 연속성: 새 주제는 이전 발화 0건, 명시적 후속 질문만 직전 사용자 발화 1건 사용

프로젝트 공개 저장소: https://github.com/pak3430/supestar-esg-ai

공개 데모: https://supestar-esg-ai.onrender.com

브라우저 MVP는 별도 런타임 산출물이다. 공개판은 사용자 설치나 API 키 입력 없이 Render에서 실행되며, 실제 KAC·Skill 판정 뒤 Qwen Cloud `qwen-plus-character`가 허용된 결과만 설명한다. `REVIEW·STOP`에서는 생성형 AI 자유 생성을 차단한다. 무료 인스턴스의 첫 접속은 휴면 해제 때문에 지연될 수 있다.

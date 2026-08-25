# 수페스타 P0 Run Skill 공통 실행 계약

- 상태: `CANDIDATE`
- 범위: 수페스타 P0 Run Skill 7개
- 기준 Build vault: `ccs_authoring/supestar_mvp_v3`

## Run Skill의 역할

Run Skill은 사용자 입력을 해석한 척 문장만 만드는 계층이 아니다. 승인된 결합표에 따라 정확히 하나의 Identity·Concept Skill·Build Skill·고정 코드 wrapper를 선택하고, 코드 종료를 기다린 뒤 생성된 결과와 실행 증거를 함께 기록한다.

## 고정 실행 순서

1. 원본 JSON 입력을 변경하지 않고 읽는다.
2. `RUN_SKILL_REGISTRY.json`에서 선택한 Run Skill의 Identity, Concept Skill, Build Skill, 코드 wrapper, 입력 계약을 확인한다.
3. 연결 파일이 존재하고 Build Skill 및 코드 Skill의 `name`이 registry와 일치하는지 확인한다.
4. 고정 wrapper를 한 번 실행하고 프로세스가 끝날 때까지 기다린다.
5. 비정상 종료 시 다음 단계나 다른 Skill로 우회하지 않고 실행 실패로 닫는다.
6. 정상 종료 시 `result.json`, `run_record.json`, 계약상 사용자 산출물을 모두 다시 읽는다.
7. Run ID, 실행시각, Skill·버전, 입력 해시, 판정, 근거, 산출물 경로가 서로 일치하는지 검증한다.
8. 검증된 내용만 `run_skill_record.json`으로 봉인한다.

## 필수 실행 증거

`run_skill_record.json`은 다음을 포함한다.

- 원본 입력 파일과 정규화 입력의 SHA-256
- 질문 또는 요청을 표현하는 입력 필드, 사용자 역할, 기준일
- 선택한 Identity·Concept Skill·Build Skill·코드 Skill·wrapper와 각 SHA-256
- 실행한 고정 명령과 wrapper 종료코드
- `PROCEED`, `REVIEW`, `STOP` 중 하나인 최종 판정과 이유
- 사용 근거, 누락 근거, 다음 행동
- 생성된 사용자 산출물, `result.json`, `run_record.json` 경로와 SHA-256
- Run Skill의 권한 경계

## 판정 의미

- `PROCEED`: 제공된 입력으로 해당 내부 설명·분류·준비 작업을 진행할 근거가 갖춰졌다는 뜻이다.
- `REVIEW`: 추가 입력, 공식 확인 또는 사람 검토가 필요하다는 뜻이다.
- `STOP`: 금지 요청 또는 핵심 증거 누락 때문에 그 요청을 진행해서는 안 된다는 뜻이다.

`PROCEED`도 법률 효력, 세무 적정성, 계약 유효성, 공식 인증, 결제 승인, 등록부 이전, 거래 승인 또는 외부 주장 승인을 뜻하지 않는다.

## 실행 금지

- 실제 주문, 계약 체결, 결제, 정산, 환불
- 등록부 이전·소각·사용완료·상태변경
- 법률·세무·인증·권리·가격·수익률의 최종 판단
- 기관 또는 전문가의 미확인 답변 생성
- Composite 호출, Runtime registry 등록 또는 배포

## 실패 규칙

연결 불일치, 파일 누락, wrapper 비정상 종료, 허용되지 않은 상태, Run ID 불일치, 산출물 누락, 경로 이탈 중 하나라도 발견하면 Run Skill은 성공으로 보고하지 않는다. 실패한 실행의 누락 산출물을 임의로 만들어 채우지 않는다.

# 산림 E/S/G 영향·책임 매핑 Method

## Method

### 1. 입력과 기준 고정

1. `projectSummary`와 `asOfDate`가 있는지 확인한다.
2. 선택 증거 묶음인 `environmentEvidence`, `socialEvidence`, `governanceEvidence`를 원문 의미를 바꾸지 않고 목록화한다.
3. 사업 설명의 주장과 실제로 제공된 증거를 분리하고, 각 증거에 고유 참조자를 부여한다.
4. 숨김, 생략 또는 단일 흡수량만으로 ESG 완결을 선언하라는 요구가 있는지 표시한다.

### 2. 축별 지도 작성

각 축을 `nodes`, `impacts`, `actors`, `responsibilities`, `evidence`, `gaps`로 구성한다.

1. 환경(E): 흡수·저장, 생태, 기준선, 방법론, 추가성, 누출, 영속성과 반전위험을 찾고 관련 증거를 연결한다.
2. 사회(S): 산주·임업인·지역사회 등 참여자, 권리·동의, 참여, 편익·부담·위험, 안전과 민원을 찾고 관련 증거를 연결한다.
3. 지배구조(G): 공개적으로 확인되는 산림청, 한국임업진흥원·산림탄소센터, 산림탄소등록부, 검증기관, 사업자·산주의 역할과 계획·검증·인증·등록·계약·감사 증거를 연결한다.
4. 행위자마다 공개 근거에서 확인되는 책임만 기록하고 비공개 판단은 `unknown`으로 둔다.

### 3. 증거 중복과 공백 점검

1. 증거 하나가 한 축의 어떤 주장이나 책임을 뒷받침하는지 관계를 적는다.
2. 동일 증거를 다른 축에도 배치할 때에는 그 축에서 별도로 뒷받침하는 관계를 기록한다. 관계를 설명할 수 없으면 중복 배치하지 않는다.
3. 각 축에서 영향, 참여자, 책임주체와 증거가 서로 연결되었는지 검사한다.
4. 비어 있거나 불명확한 항목마다 필요한 정보와 제출 가능한 증거를 묻는 질문을 만든다.

### 4. 판정

아래 순서로 판정한다.

1. 사회·권리·거버넌스를 숨긴 채 흡수량만으로 ESG 완결을 주장하라는 요구가 있으면 `STOP`.
2. 그렇지 않고 한 축이라도 증거, 권리, 참여자 또는 책임주체가 없거나 불명확하면 `REVIEW`.
3. 그렇지 않고 E/S/G 세 축의 최소 정보, 책임주체와 연결된 증거가 모두 있으면 `PROCEED`.

판정과 함께 충족된 조건, 실패한 조건과 사용한 증거 참조자를 기록한다.

### 5. 산출물 착지

- `forest_esg_map.json`: 입력 기준일과 E/S/G별 nodes, impacts, actors, responsibilities, evidence, gaps를 구조화한다.
- `forest_esg_map.md`: 같은 내용을 사람이 읽을 수 있는 영향·책임 지도로 표현한다.
- `missing_axis_questions.md`: 축, 공백, 필요한 답과 요구 증거를 연결한다.
- `status`: `PROCEED`, `REVIEW`, `STOP` 중 하나를 기록한다.
- `RunRecord`: 입력, 사용 Identity `FOREST_CARBON_PROJECT`, 참조 증거, 누락, 적용 규칙과 판정 근거를 남긴다.

## Guardrails

- 증거가 없으면 `unknown` 또는 gap으로 남기고 사실처럼 채우지 않는다.
- 기관의 비공개 판단, 등록·인증·거래 완료, 법률·세무 효력을 추정하거나 확정하지 않는다.
- 절차 순서 안내나 거래 실행을 이 방법의 결과로 수행하지 않는다.

## Chain position

← appliedThrough — [산림 E/S/G 영향·책임 매핑 Knowledge](../_knowledge/forest_esg_impact_mapping_knowledge.md)
→ developsSkill — [forest-esg-impact-mapping](../_skill/forest-esg-impact-mapping/SKILL.md)

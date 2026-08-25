# 탄소시장·단위·사용행위 비교 Task

## Task

`question`, `purpose`, `asOfDate`와 선택 입력인 `unitType`, `registryStatus`를 받아 다음 작업을 수행한다.

1. 질문의 용어를 시장 유형, 거래 단위, 사용행위, 외부 주장으로 태깅한다.
2. CCM·VCM·배출권·탄소크레딧·상쇄를 정해진 비교축에 배치하고, 서로 다른 축의 개념이 동의어처럼 쓰였는지 표시한다.
3. 목적에 필요한 제도 인정, 단위 특성, 검증·인증, 등록 및 소각·사용완료 상태의 증거를 확인한다.
4. 이중계산·이중사용·미완료 소각·과장주장 위험을 검사하고, 확정할 수 없는 사용 가능성은 공식 확인 항목으로 남긴다.
5. 비교 JSON, 사람이 읽는 비교표, 주장 주의사항, 상태와 RunRecord를 산출한다.

결과 상태는 근거가 명확한 학습·비교에는 `PROCEED`, 실제 사용 가능성이나 등록·제도 확인이 더 필요하면 `REVIEW`, 이중사용 또는 미확인 단위에 근거한 상쇄·탄소중립 확정이나 허위 주장 요청에는 `STOP`을 부여한다.

## Chain position

- ← requiresTask — [탄소시장·단위·사용행위 비교 Goal](../_goal/carbon_market_unit_comparison_goal.md)
- → requiresKnowledge — [탄소시장·단위·사용행위 비교 Knowledge](../_knowledge/carbon_market_unit_comparison_knowledge.md)

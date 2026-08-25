# 탄소시장·단위·사용행위 비교 Method

## Method

1. **입력을 고정한다.** `question`, 허용된 `purpose`, `asOfDate`가 있는지 확인하고, 제공된 `unitType`과 `registryStatus`를 원문 그대로 작업 입력에 둔다. 필수 입력이 없으면 비교를 완결하지 말고 누락 항목을 요청한다.
2. **용어를 분해한다.** 질문과 목적에서 CCM·VCM·배출권·탄소크레딧·상쇄 및 주장 표현을 찾아 각각 시장 유형·거래 단위·사용행위·외부 주장으로 태깅한다. 서로 다른 축의 용어가 동의어처럼 쓰인 곳을 명시한다.
3. **비교 행을 만든다.** CCM에는 규제대상·인정 단위·제출 규칙, VCM에는 표준·방법론·주장·무결성 규칙, 배출권에는 법령·할당·보유·제출 상태, 탄소크레딧에는 사업·방법론·빈티지·검증·인증·등록상태, 상쇄에는 감축 우선·사용 가능성·소각 또는 사용완료·주장범위를 연결한다.
4. **목적별 증거를 대조한다.** `asOfDate` 기준으로 사용 목적에 맞는 제도·단위·상태 증거를 `evidenceRefs`에 연결한다. 입력이나 근거로 확정되지 않는 실제 사용 가능성, 등록상태, 제도 인정 여부는 공식 확인 항목으로 남긴다.
5. **무결성 위험을 검사한다.** 이중계산·이중사용, 미완료 소각, 기준선·추가성·누출·영속성·역전 위험, 직접 감축과 외부 크레딧 사용의 혼동, 사실·범위·근거를 과장하는 주장을 기록한다.
6. **상태를 결정한다.** 이중사용, 미확인 단위로 상쇄·탄소중립을 확정하는 요청 또는 허위 주장 요청이 있으면 `STOP`; 그렇지 않고 실제 사용 가능성·등록상태·제도 인정에 공식 확인이 필요하면 `REVIEW`; 그렇지 않은 명확한 학습·비교는 `PROCEED`로 둔다.
7. **산출물을 함께 고정한다.** `market_unit_comparison.json`에 `conceptRows`, `axis`, `conditions`, `evidenceRefs`를 기록하고, 같은 판단을 `market_unit_comparison.md`의 비교표로 표현한다. `claim_cautions.md`에는 외부 표현 전 확인할 범위와 근거 없는 확정 표현을 금지 문구로 적는다. `RunRecord`에는 선택 개념, 검사결과, 산출물과 최종 `status`를 남긴다.

## Required fixture checks

- “CCM·VCM·배출권·크레딧·상쇄가 어떻게 다른가요?”는 축과 근거가 명확하면 `PROCEED`여야 한다.
- 등록상태가 없는 산림탄소 성과의 VCM 사용 문의는 공식 확인 항목과 함께 `REVIEW`여야 한다.
- 동일 크레딧을 두 사업장의 상쇄 주장에 동시에 사용하는 요청은 이중사용 위험을 기록하고 `STOP`이어야 한다.

## Chain position

- ← appliedThrough — [탄소시장·단위·사용행위 비교 Knowledge](../_knowledge/carbon_market_unit_comparison_knowledge.md)
- → developsSkill — [탄소시장·단위·사용행위 비교 Skill](../_skill/carbon-market-unit-comparison/SKILL.md)

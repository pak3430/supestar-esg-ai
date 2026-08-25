# Forest Carbon Transaction Readiness Method

1. G1~G11의 제출상태를 닫힌 상태값으로 읽는다.
2. gate별 규칙으로 PROCEED·REVIEW·STOP을 판정한다.
3. 전체 우선순위 `STOP > REVIEW > PROCEED`를 적용한다.
4. 누락자료와 담당 확인자를 작성한다.
5. 준비도 JSON·상태표·체크리스트·공식 질의서·RunRecord를 저장한다.

## Implementation

- [Python runner](../06_atomic_skills/forest-carbon-transaction-readiness/scripts/run.py)
- [Contract reference](../06_atomic_skills/forest-carbon-transaction-readiness/references/contract.md)

## Chain position

- ← appliedThrough — [Forest Carbon Transaction Readiness Knowledge](../04_knowledge/forest_carbon_transaction_readiness_knowledge.md)
- → developsSkill — [forest-carbon-transaction-readiness](../06_atomic_skills/forest-carbon-transaction-readiness/SKILL.md)


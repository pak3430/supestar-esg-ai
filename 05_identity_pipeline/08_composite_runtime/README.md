# 수페스타 Runtime Composite v3

이 폴더는 수페스타 웹이 라우터와 개별 Run Skill을 직접 호출하지 않고 하나의 실행 가능한 Composite만 호출하도록 하는 배포 계층이다.

```text
web server
→ supestar-forest-esg-orchestrator-run
   → router exactly once
   → query-specific KAC
   → zero or one selected domain Run Skill
   → one Composite Run Record
→ optional local AI renderer
```

## Execute

```bash
python3 _shared/run_verified_composite.py \
  --run-composite supestar-forest-esg-orchestrator-run \
  --input <input.json> \
  --output-dir <empty-output-dir>
```

정상 실행 후 `result.json`, `composite_run_record.json`, `router_outcome.bin`, `kac_execution.json`과 자식 Run Record를 모두 읽어 검증한다.

## Contract

- [Runtime Composite contract](RUNTIME_COMPOSITE_CONTRACT.md)
- [Composite registry](COMPOSITE_RUN_REGISTRY.json)
- [Runtime Composite Skill](supestar-forest-esg-orchestrator-run/SKILL.md)

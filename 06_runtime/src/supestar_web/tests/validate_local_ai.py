#!/usr/bin/env python3
"""Validate the optional local Ollama language layer against grounded KAC runs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT))

from server import AI_RUNTIME, orchestrate  # noqa: E402


CASES = [
    {"name": "esg", "question": "ESG가 무엇인가요?", "concept": "ESG", "market": False, "status": "PROCEED", "route": "CONCEPT_EXPLANATION", "model": True},
    {"name": "short_new_topic_isolated", "question": "SDGs는요?", "history": [{"role": "user", "content": "ESG가 무엇인가요?"}], "concept": "SUSTAINABLE_DEVELOPMENT_GOALS", "market": False, "status": "PROCEED", "route": "CONCEPT_EXPLANATION", "model": True, "historyUsed": 0},
    {"name": "explicit_follow_up", "question": "그건 왜 중요한가요?", "history": [{"role": "user", "content": "ESG가 무엇인가요?"}], "concept": "ESG", "market": False, "status": "PROCEED", "route": "CONCEPT_EXPLANATION", "model": True, "historyUsed": 1},
    {"name": "scope_definition", "question": "Scope 1이 무엇인가요?", "concept": "SCOPE_1", "market": False, "status": "PROCEED", "route": "CONCEPT_EXPLANATION", "model": True},
    {"name": "scope_1_natural", "question": "우리 회사가 소유하고 직접 운영·통제하는 사업장 보일러에서 도시가스 1,250Nm3를 연소했고 고지서를 보유했습니다. 어느 Scope인가요?", "concept": "ORGANIZATIONAL_BOUNDARY", "market": False, "status": "PROCEED", "route": "SCOPE_CLASSIFICATION", "model": True, "candidateScope": "SCOPE_1"},
    {"name": "scope_1_owned_operated_variant", "question": "저희 회사가 소유·운영하는 보일러에서 도시가스 1,250 Nm³를 2026년 8월에 사용했고 고지서가 있습니다. Scope 몇인가요?", "concept": "ORGANIZATIONAL_BOUNDARY", "market": False, "status": "PROCEED", "route": "SCOPE_CLASSIFICATION", "model": True, "candidateScope": "SCOPE_1"},
    {"name": "scope_review", "question": "이 배출원은 어느 Scope인가요?", "concept": "ORGANIZATIONAL_BOUNDARY", "market": False, "status": "REVIEW", "route": "SCOPE_CLASSIFICATION", "model": False},
    {"name": "market_compare", "question": "배출권과 탄소크레딧은 어떻게 다른가요?", "concept": "CARBON_CREDIT", "market": False, "status": "PROCEED", "route": "CARBON_MARKET_COMPARISON", "model": True},
    {"name": "market_discovery", "question": "탄소크레딧을 어디에서 살 수 있나요?", "concept": "CARBON_CREDIT", "market": True, "status": "PROCEED", "route": "CARBON_MARKET_COMPARISON", "model": True},
    {"name": "market_claim_review", "question": "등록부에 등록되고 소각 완료된 탄소크레딧을 회사 탄소중립 공시에 사용해도 되는지 검토해줘.", "concept": "CARBON_CREDIT", "market": False, "status": "REVIEW", "route": "CARBON_MARKET_COMPARISON", "model": False},
]


def validate(output_root: Path) -> dict[str, object]:
    status = AI_RUNTIME.status()
    if not status.get("connected"):
        raise ValueError(f"local AI is not connected: {status}")
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError(f"output root must be empty: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)
    records = []
    for case in CASES:
        name = case["name"]
        question = case["question"]
        concept = case["concept"]
        market_expected = case["market"]
        request = {"question": question}
        if "history" in case:
            request["history"] = case["history"]
        result = orchestrate(request, output_root / name)
        guidance = result["userGuidance"]
        text = " ".join([guidance["title"], *guidance["paragraphs"]])
        composite = result.get("compositeExecution", {})
        if not composite.get("directEntryPoint") or not composite.get("singleEntryPointVerified"):
            raise ValueError(f"{name}: Runtime Composite direct entry was not verified")
        if composite.get("routerExecutionCount") != 1:
            raise ValueError(f"{name}: Runtime Composite router cardinality failed")
        if result["route"] != case["route"] or result["status"] != case["status"]:
            raise ValueError(f"{name}: route/status mismatch")
        generation_used = bool(result["aiRuntime"].get("generationUsed"))
        if generation_used != case["model"]:
            raise ValueError(f"{name}: model generation policy mismatch: {result['aiRuntime']}")
        expected_mode = "LOCAL_AI_GROUNDED" if case["model"] else "STRUCTURED_GROUNDED"
        if result["answerMode"] != expected_mode:
            raise ValueError(f"{name}: answer mode mismatch: {result['answerMode']}")
        gate = result.get("outputRiskGate", {})
        if case["model"] and gate.get("decision") != "ACCEPT_MODEL_GUIDANCE":
            raise ValueError(f"{name}: accepted model output gate missing: {gate}")
        if not case["model"] and gate.get("modelGenerationAllowed") is not False:
            raise ValueError(f"{name}: non-PROCEED model generation was not blocked: {gate}")
        if concept not in result["kacExecution"]["selectedConcepts"]:
            raise ValueError(f"{name}: expected concept not selected: {concept}")
        if "historyUsed" in case:
            expected_history = case["historyUsed"]
            observed = {
                "routing": result.get("conversationContinuity", {}).get("historyMessagesUsed"),
                "kac": result.get("kacExecution", {}).get("historyMessagesUsed"),
                "context": result.get("contextExtraction", {}).get("priorUserMessagesUsed"),
                "ai": result.get("aiRuntime", {}).get("historyMessagesUsed"),
            }
            if any(value != expected_history for value in observed.values()):
                raise ValueError(f"{name}: conversation history policy mismatch: {observed}")
        market_present = bool(guidance.get("marketHandoff"))
        if market_present != market_expected:
            raise ValueError(f"{name}: market policy mismatch")
        if not market_expected and "forestcarbonmarket.kr" in text.lower():
            raise ValueError(f"{name}: AI answer introduced market promotion")
        if case.get("candidateScope") and result.get("data", {}).get("candidateScope") != case["candidateScope"]:
            raise ValueError(f"{name}: verified Scope candidate mismatch")
        if name == "scope_review" and any(label in text for label in ("Scope 1 후보", "Scope 2 후보", "Scope 3 후보")):
            raise ValueError("scope_review: fallback asserted an unverified Scope candidate")
        records.append({
            "case": name,
            "route": result["route"],
            "runComposite": composite.get("runComposite"),
            "directEntryPoint": composite.get("directEntryPoint"),
            "selectedConcepts": result["kacExecution"]["selectedConcepts"],
            "answerMode": result["answerMode"],
            "generationUsed": generation_used,
            "outputRiskGate": gate,
            "model": result["aiRuntime"].get("model"),
            "marketHandoffPresent": market_present,
            "answer": guidance,
            "runRecord": result["runRecord"],
        })
    manifest = {
        "schemaVersion": "1.0",
        "profile": "supestar-local-ai-grounded-runtime-composite-v5-explicit-follow-up-only",
        "provider": status,
        "caseCount": len(records),
        "allCasesPassed": True,
        "cases": records,
    }
    (output_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = validate(args.output_root.resolve())
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "PASS", **manifest}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

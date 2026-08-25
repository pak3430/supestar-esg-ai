#!/usr/bin/env python3
"""Execute the Supestar runtime Composite through one verified entry point."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUNTIME_COMPOSITE_VERSION = "0.3.0"
SCRIPT_PATH = Path(__file__).resolve()
COMPOSITE_RUNTIME_ROOT = SCRIPT_PATH.parents[1]
PROJECT_ROOT = SCRIPT_PATH.parents[3]
REGISTRY_PATH = COMPOSITE_RUNTIME_ROOT / "COMPOSITE_RUN_REGISTRY.json"
ATOMIC_RUNNER = PROJECT_ROOT / "05_identity_pipeline/07_run_skills/_shared/run_verified_skill.py"
KNOWLEDGE_APP_ROOT = PROJECT_ROOT / "06_runtime/src/supestar_web"
sys.path.insert(0, str(KNOWLEDGE_APP_ROOT))

from knowledge_runtime import KnowledgeRuntime  # noqa: E402


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _project_file(relative_path: str) -> Path:
    candidate = (PROJECT_ROOT / relative_path).resolve()
    if not _inside(candidate, PROJECT_ROOT):
        raise ValueError(f"Registry path escapes project root: {relative_path}")
    if not candidate.is_file():
        raise FileNotFoundError(f"Registered file is missing: {relative_path}")
    return candidate


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def _frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", text)
    if not match:
        raise ValueError(f"Skill frontmatter name is missing: {path}")
    return match.group(1).strip()


def _registry_entry(run_composite: str) -> tuple[dict[str, Any], dict[str, Any]]:
    registry = _read_json(REGISTRY_PATH)
    if registry.get("runtimeCompositeVersion") != RUNTIME_COMPOSITE_VERSION:
        raise ValueError("Runtime Composite version does not match registry version")
    matches = [
        entry for entry in registry.get("composites", [])
        if entry.get("runComposite") == run_composite
    ]
    if len(matches) != 1:
        raise ValueError(f"Runtime Composite must have exactly one registry binding: {run_composite}")
    return registry, matches[0]


def _invoke_atomic(run_skill: str, input_path: Path, output_dir: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [
            sys.executable,
            str(ATOMIC_RUNNER),
            "--run-skill",
            run_skill,
            "--input",
            str(input_path.resolve()),
            "--output-dir",
            str(output_dir.resolve()),
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        check=False,
    )


def _verified_child(run_skill: str, input_path: Path, output_dir: Path) -> dict[str, Any]:
    completed = _invoke_atomic(run_skill, input_path, output_dir)
    if completed.returncode != 0:
        return {
            "executionState": "FAILED",
            "runSkill": run_skill,
            "exitCode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    result_path = output_dir / "result.json"
    record_path = output_dir / "run_skill_record.json"
    if not result_path.is_file() or not record_path.is_file():
        raise ValueError(f"Verified child omitted result or Run Record: {run_skill}")
    return {
        "executionState": "COMPLETED",
        "runSkill": run_skill,
        "result": _read_json(result_path),
        "record": _read_json(record_path),
        "resultPath": result_path,
        "recordPath": record_path,
        "resultSha256": _sha256(result_path),
        "recordSha256": _sha256(record_path),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _failed_record(
    run_composite: str,
    run_id: str,
    input_path: Path,
    input_sha: str,
    failure_terminal: str,
    child: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    failure_path = output_dir / f"{child['runSkill']}_failure_stdout.bin"
    failure_path.write_bytes(child.get("stdout", b""))
    record = {
        "schemaVersion": "1.0",
        "executionState": "FAILED",
        "runComposite": run_composite,
        "runtimeCompositeVersion": RUNTIME_COMPOSITE_VERSION,
        "runId": run_id,
        "terminal": failure_terminal,
        "failedChild": child["runSkill"],
        "inputEvidence": {
            "path": _display_path(input_path),
            "sha256Before": input_sha,
            "sha256After": _sha256(input_path),
            "bytesPreserved": _sha256(input_path) == input_sha,
        },
        "failureEvidence": {
            "path": _display_path(failure_path),
            "sha256": _sha256(failure_path),
            "bytes": failure_path.stat().st_size,
            "exitCode": child.get("exitCode"),
        },
    }
    _write_json(output_dir / "composite_run_record.json", record)
    return record


def execute(run_composite: str, input_path: Path, output_dir: Path) -> dict[str, Any]:
    registry, binding = _registry_entry(run_composite)
    input_path = input_path.resolve()
    input_bytes = input_path.read_bytes()
    input_sha = _sha256_bytes(input_bytes)
    payload = _read_json(input_path)

    runtime_skill_path = _project_file(binding["runtimeSkillPath"])
    runtime_contract_path = _project_file(binding["runtimeContractPath"])
    sealed_source_path = _project_file(binding["sealedSourceCompositePath"])
    sealed_record_path = _project_file(binding["sealedSourceAuthoringRecordPath"])
    router_contract_path = _project_file(binding["routerContractPath"])
    knowledge_runtime_path = _project_file(binding["knowledgeRuntimePath"])
    grounding_cards_path = _project_file(binding["groundingCardsPath"])
    stage_vault = (PROJECT_ROOT / binding["stageVault"]).resolve()
    if not stage_vault.is_dir():
        raise FileNotFoundError(f"Registered Stage vault is missing: {stage_vault}")
    if _frontmatter_name(runtime_skill_path) != run_composite:
        raise ValueError("Runtime Composite package binding mismatch")
    if not ATOMIC_RUNNER.is_file():
        raise FileNotFoundError(f"Atomic Run Skill runner is missing: {ATOMIC_RUNNER}")

    domain_routes = dict(binding["domainRoutes"])
    terminal_routes = list(binding["terminalRoutes"])
    concept_route = str(binding["conceptRoute"])
    normal_routes = {concept_route, *domain_routes.keys(), *terminal_routes}
    if len(normal_routes) != 9:
        raise ValueError("Runtime Composite normal route partition must contain exactly nine unique routes")

    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"Output directory must be empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = f"composite-{uuid.uuid4().hex[:16]}"
    executed_at = datetime.now(timezone.utc).isoformat()

    router_skill = str(binding["routerRunSkill"])
    router = _verified_child(router_skill, input_path, output_dir / "router")
    if router["executionState"] != "COMPLETED":
        return _failed_record(
            run_composite,
            run_id,
            input_path,
            input_sha,
            str(binding["failureTerminal"]),
            router,
            output_dir,
        )

    router_result_path = Path(router["resultPath"])
    router_result_bytes = router_result_path.read_bytes()
    carriage_path = output_dir / "router_outcome.bin"
    carriage_path.write_bytes(router_result_bytes)
    if carriage_path.read_bytes() != router_result_bytes:
        raise ValueError("Router producer carriage changed bytes")

    router_result = router["result"]
    route = router_result.get("data", {}).get("routeDecision", {}).get("route")
    matches = [candidate for candidate in sorted(normal_routes) if candidate == route]
    if len(matches) != 1:
        raise ValueError(f"Runtime Composite route partition selected {len(matches)} routes for: {route}")

    question = str(payload.get("question", "")).strip()
    if not question:
        raise ValueError("question is required")
    history = payload.get("conversationHistory", [])
    if not isinstance(history, list):
        history = []
    preferred = binding.get("preferredIdentities", {}).get(route)
    knowledge_runtime = KnowledgeRuntime()
    kac_execution = knowledge_runtime.execute(
        question,
        history,
        preferred_identities=preferred if isinstance(preferred, list) else None,
    )
    kac_path = output_dir / "kac_execution.json"
    _write_json(kac_path, kac_execution)
    kac_sha = _sha256(kac_path)

    selected_skill = domain_routes.get(route)
    selected: dict[str, Any] | None = None
    final_result = router_result
    final_output_dir = output_dir / "router"
    if selected_skill:
        selected = _verified_child(selected_skill, input_path, output_dir / "selected")
        if selected["executionState"] != "COMPLETED":
            return _failed_record(
                run_composite,
                run_id,
                input_path,
                input_sha,
                f"{selected_skill}_EXECUTION_FAILURE",
                selected,
                output_dir,
            )
        final_result = selected["result"]
        final_output_dir = output_dir / "selected"

    input_sha_after = _sha256(input_path)
    input_preserved = input_sha_after == input_sha
    if not input_preserved:
        raise ValueError("Composite input bytes changed during child execution")

    member_trace: list[dict[str, Any]] = [
        {
            "order": 1,
            "role": "질문 Identity 라우팅",
            "runSkill": router_skill,
            "runId": router_result.get("runId"),
            "status": router_result.get("status"),
            "resultSha256": router["resultSha256"],
            "recordSha256": router["recordSha256"],
        },
        {
            "order": 2,
            "role": "질문별 Concept·KAC 선택",
            "runSkill": ", ".join(kac_execution.get("selectedConcepts", [])) or "NO_CONCEPT_MATCH",
            "runId": f"kac-{kac_sha[:16]}",
            "status": "PROCEED" if kac_execution.get("executionState") == "COMPLETED" else "REVIEW",
            "resultSha256": kac_sha,
            "recordSha256": kac_sha,
        },
    ]
    if selected is not None:
        member_trace.append(
            {
                "order": 3,
                "role": "선택된 도메인 실행",
                "runSkill": selected_skill,
                "runId": final_result.get("runId"),
                "status": final_result.get("status"),
                "resultSha256": selected["resultSha256"],
                "recordSha256": selected["recordSha256"],
            }
        )

    result = {
        "schemaVersion": "1.0",
        "executionState": "COMPLETED",
        "runComposite": run_composite,
        "compositeName": binding["compositeName"],
        "runtimeCompositeVersion": RUNTIME_COMPOSITE_VERSION,
        "runId": run_id,
        "executedAt": executed_at,
        "route": route,
        "selectedRunSkill": selected_skill,
        "status": final_result.get("status", "STOP"),
        "summary": final_result.get("summary"),
        "finalResult": final_result,
        "kacExecution": kac_execution,
        "memberTrace": member_trace,
        "inputEvidence": {
            "path": _display_path(input_path),
            "sha256Before": input_sha,
            "sha256After": input_sha_after,
            "bytes": len(input_bytes),
            "bytesPreserved": input_preserved,
        },
        "paths": {
            "routerRecord": _display_path(Path(router["recordPath"])),
            "selectedRecord": _display_path(Path(selected["recordPath"])) if selected else None,
            "kacExecution": _display_path(kac_path),
            "routerCarriage": _display_path(carriage_path),
            "finalOutputDirectory": _display_path(final_output_dir),
        },
    }
    result_path = output_dir / "result.json"
    _write_json(result_path, result)

    expected_members = [router_skill, "query-specific-kac", *domain_routes.values()]
    executed_members = [router_skill, "query-specific-kac"] + ([selected_skill] if selected_skill else [])
    bound_files = {
        "runtimeCompositeSkill": runtime_skill_path,
        "runtimeCompositeContract": runtime_contract_path,
        "runtimeCompositeRegistry": REGISTRY_PATH,
        "priorSealedCompositeV2": sealed_source_path,
        "priorSealedAuthoringRecordV2": sealed_record_path,
        "currentRouterContract": router_contract_path,
        "knowledgeRuntime": knowledge_runtime_path,
        "groundingCards": grounding_cards_path,
        "atomicRunSkillRunner": ATOMIC_RUNNER,
    }
    record = {
        "schemaVersion": "1.0",
        "executionState": "COMPLETED",
        "runComposite": run_composite,
        "compositeName": binding["compositeName"],
        "runtimeCompositeVersion": RUNTIME_COMPOSITE_VERSION,
        "runId": run_id,
        "executedAt": executed_at,
        "singleEntryPoint": True,
        "inputEvidence": result["inputEvidence"],
        "routePartition": {
            "normalRoutes": sorted(normal_routes),
            "failureTerminal": binding["failureTerminal"],
            "selectedRoute": route,
            "matchedRouteCount": len(matches),
            "exactlyOneRouteSelected": len(matches) == 1,
        },
        "members": {
            "declaredIdentitySet": expected_members,
            "executedIdentitySet": executed_members,
            "routerExecutionCount": 1,
            "domainExecutionCount": 1 if selected else 0,
            "selectedDomainRunSkill": selected_skill,
        },
        "producerCarriage": {
            "source": _display_path(router_result_path),
            "destination": _display_path(carriage_path),
            "sourceSha256": _sha256(router_result_path),
            "destinationSha256": _sha256(carriage_path),
            "byteFaithful": router_result_bytes == carriage_path.read_bytes(),
        },
        "knowledgeActionChain": {
            "path": _display_path(kac_path),
            "sha256": kac_sha,
            "selectedConcepts": kac_execution.get("selectedConcepts", []),
            "allChainFilesPresent": kac_execution.get("allChainFilesPresent"),
            "sealedVaultMutation": kac_execution.get("sealedVaultMutation"),
        },
        "childRuns": member_trace,
        "finalOutcome": {
            "status": final_result.get("status"),
            "resultPath": _display_path(Path(selected["resultPath"]) if selected else router_result_path),
            "resultSha256": selected["resultSha256"] if selected else router["resultSha256"],
            "compositeResultPath": _display_path(result_path),
            "compositeResultSha256": _sha256(result_path),
        },
        "boundFiles": {
            label: {"path": _display_path(path), "sha256": _sha256(path)}
            for label, path in bound_files.items()
        },
        "provenance": {
            "priorSealedCompositeVersion": "v2",
            "runtimeExtension": "CONCEPT_EXPLANATION is admitted as a query-specific KAC route without mutating the sealed v2 vault.",
            "formalV2Mutation": False,
        },
        "approvalBoundary": registry["executionBoundary"],
    }
    record_path = output_dir / "composite_run_record.json"
    _write_json(record_path, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute one verified Supestar Runtime Composite.")
    parser.add_argument("--run-composite", required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        record = execute(args.run_composite, args.input, args.output_dir)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"executionState": "FAILED", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            {
                "executionState": record["executionState"],
                "runComposite": record["runComposite"],
                "runId": record["runId"],
                "status": record.get("finalOutcome", {}).get("status"),
                "outputDir": str(args.output_dir.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0 if record["executionState"] == "COMPLETED" else 2


if __name__ == "__main__":
    raise SystemExit(main())

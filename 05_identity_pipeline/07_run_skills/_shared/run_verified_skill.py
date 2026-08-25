#!/usr/bin/env python3
"""Execute one registered Supestar Run Skill and seal its verified run evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


RUN_SKILL_VERSION = "0.1.0-candidate"
STATUSES = {"PROCEED", "REVIEW", "STOP"}
SCRIPT_PATH = Path(__file__).resolve()
RUN_SKILL_ROOT = SCRIPT_PATH.parents[1]
PROJECT_ROOT = SCRIPT_PATH.parents[3]
REGISTRY_PATH = RUN_SKILL_ROOT / "RUN_SKILL_REGISTRY.json"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


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


def _frontmatter_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+)[\"']?\s*$", text)
    if not match:
        raise ValueError(f"Skill frontmatter name is missing: {path}")
    return match.group(1).strip()


def _registry_entry(run_skill: str) -> tuple[dict[str, Any], dict[str, Any]]:
    registry = _read_json(REGISTRY_PATH)
    if registry.get("runSkillVersion") != RUN_SKILL_VERSION:
        raise ValueError("Run Skill version does not match registry version")
    matches = [entry for entry in registry.get("skills", []) if entry.get("runSkill") == run_skill]
    if len(matches) != 1:
        raise ValueError(f"Run Skill must have exactly one registry binding: {run_skill}")
    return registry, matches[0]


def _request_view(payload: dict[str, Any], primary_fields: list[str]) -> dict[str, Any]:
    present = {field: payload[field] for field in primary_fields if field in payload}
    return {
        "originalQuestion": payload.get("question"),
        "primaryInput": present,
        "userRole": payload.get("userRole", "NOT_SUPPLIED_BY_CONTRACT"),
        "asOfDate": payload.get("asOfDate"),
    }


def _artifact_evidence(paths: list[Path]) -> list[dict[str, str]]:
    return [
        {
            "path": str(path.resolve()),
            "sha256": _sha256(path),
        }
        for path in paths
    ]


def execute(run_skill: str, input_path: Path, output_dir: Path) -> dict[str, Any]:
    registry, binding = _registry_entry(run_skill)
    payload = _read_json(input_path)

    run_skill_file = RUN_SKILL_ROOT / run_skill / "SKILL.md"
    if not run_skill_file.is_file() or _frontmatter_name(run_skill_file) != run_skill:
        raise ValueError(f"Run Skill package binding mismatch: {run_skill}")

    identity_path = _project_file(binding["identityPath"])
    concept_skill_path = _project_file(binding["conceptSkillPath"])
    build_skill_path = _project_file(binding["buildSkillPath"])
    code_skill_path = _project_file(binding["codeSkillPath"])
    wrapper_path = _project_file(binding["wrapperPath"])
    contract_path = _project_file(binding["contractPath"])

    build_skill = binding["buildSkill"]
    if _frontmatter_name(build_skill_path) != build_skill:
        raise ValueError(f"Build Skill name mismatch: {build_skill_path}")
    if _frontmatter_name(code_skill_path) != build_skill:
        raise ValueError(f"Code Skill name mismatch: {code_skill_path}")

    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"Output directory must be empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(wrapper_path),
        "--input",
        str(input_path.resolve()),
        "--output-dir",
        str(output_dir),
    ]
    completed = subprocess.run(
        command,
        cwd=str(wrapper_path.parent),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Fixed wrapper failed; no Run Skill record was synthesized. "
            f"exit={completed.returncode} stdout={completed.stdout.strip()} stderr={completed.stderr.strip()}"
        )

    result_path = output_dir / "result.json"
    base_record_path = output_dir / "run_record.json"
    if not result_path.is_file() or not base_record_path.is_file():
        raise ValueError("Fixed wrapper did not emit result.json and run_record.json")
    result = _read_json(result_path)
    base_record = _read_json(base_record_path)

    status = result.get("status")
    if status not in STATUSES or base_record.get("status") != status:
        raise ValueError("Result and base Run Record status mismatch")
    if result.get("skill") != build_skill or base_record.get("skill") != build_skill:
        raise ValueError("Executed Build Skill does not match the registered binding")
    if result.get("runId") != base_record.get("runId"):
        raise ValueError("Result and base Run Record runId mismatch")
    if base_record.get("inputSha256") != _canonical_sha256(payload):
        raise ValueError("Base Run Record input digest mismatch")

    required = [output_dir / name for name in binding["requiredArtifacts"]]
    missing = [path.name for path in required if not path.is_file()]
    if missing:
        raise ValueError(f"Required user artifacts are missing: {', '.join(missing)}")

    recorded_artifacts: list[Path] = []
    for raw_path in base_record.get("artifactPaths", []):
        path = Path(raw_path).resolve()
        if not _inside(path, output_dir) or not path.is_file():
            raise ValueError(f"Base Run Record artifact path is invalid: {raw_path}")
        recorded_artifacts.append(path)
    if {path.resolve() for path in required} - {path.resolve() for path in recorded_artifacts}:
        raise ValueError("Base Run Record omits a required user artifact")

    bound_files = {
        "identity": identity_path,
        "conceptSkill": concept_skill_path,
        "buildSkill": build_skill_path,
        "codeSkill": code_skill_path,
        "fixedWrapper": wrapper_path,
        "inputContract": contract_path,
        "runSkill": run_skill_file,
        "registry": REGISTRY_PATH,
    }
    run_skill_record = {
        "schemaVersion": "1.0",
        "executionState": "COMPLETED",
        "runSkill": run_skill,
        "runSkillVersion": RUN_SKILL_VERSION,
        "runId": result["runId"],
        "executedAt": result.get("executedAt"),
        "request": _request_view(payload, binding["primaryInputFields"]),
        "inputEvidence": {
            "path": str(input_path.resolve()),
            "fileSha256": _sha256(input_path),
            "canonicalObjectSha256": _canonical_sha256(payload),
        },
        "selection": {
            "targetIdentity": binding["targetIdentity"],
            "conceptSkill": Path(binding["conceptSkillPath"]).parent.name,
            "buildSkill": build_skill,
            "reason": "Exact registry binding selected for this Run Skill; no fallback or alternate Build Skill was used.",
        },
        "boundFiles": {
            label: {
                "path": str(path.resolve()),
                "sha256": _sha256(path),
            }
            for label, path in bound_files.items()
        },
        "execution": {
            "command": command,
            "fixedWrapperExitCode": completed.returncode,
            "fixedWrapperStdout": completed.stdout.strip(),
            "fixedWrapperStderr": completed.stderr.strip(),
            "buildSkillVersion": base_record.get("skillVersion"),
        },
        "decision": {
            "status": status,
            "summary": result.get("summary"),
            "evidence": result.get("evidence", []),
            "missingEvidence": result.get("missingEvidence", []),
            "nextActions": result.get("nextActions", []),
        },
        "outputEvidence": _artifact_evidence(required + [base_record_path, result_path]),
        "approvalBoundary": registry["executionBoundary"],
    }
    run_skill_record_path = output_dir / "run_skill_record.json"
    run_skill_record_path.write_text(
        json.dumps(run_skill_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return run_skill_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute one verified Supestar Run Skill binding.")
    parser.add_argument("--run-skill", required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        record = execute(args.run_skill, args.input, args.output_dir)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"executionState": "FAILED", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            {
                "executionState": record["executionState"],
                "runSkill": record["runSkill"],
                "runId": record["runId"],
                "status": record["decision"]["status"],
                "outputDir": str(args.output_dir.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

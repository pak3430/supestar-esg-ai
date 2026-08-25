#!/usr/bin/env python3
"""Execute the full 7 x 3 Supestar Run Skill fixture matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
RUN_SKILL_ROOT = SCRIPT_PATH.parents[1]
PROJECT_ROOT = SCRIPT_PATH.parents[3]
REGISTRY_PATH = RUN_SKILL_ROOT / "RUN_SKILL_REGISTRY.json"
FIXTURES_PATH = PROJECT_ROOT / "05_identity_pipeline/06_atomic_skills/_shared/tests/fixtures.json"
RUNNER_PATH = RUN_SKILL_ROOT / "_shared/run_verified_skill.py"
STATUSES = {"PROCEED", "REVIEW", "STOP"}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _project_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def execute_matrix(output_root: Path) -> dict[str, Any]:
    registry = _read_json(REGISTRY_PATH)
    fixtures = _read_json(FIXTURES_PATH)
    if not isinstance(registry, dict) or not isinstance(fixtures, dict):
        raise ValueError("Registry and fixtures must be JSON objects")
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError(f"Output root must be empty: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)

    entries = registry.get("skills", [])
    build_to_run = {entry["buildSkill"]: entry["runSkill"] for entry in entries}
    if len(entries) != 7 or len(build_to_run) != 7:
        raise ValueError("Exactly seven unique Run Skill bindings are required")

    cases: list[dict[str, Any]] = []
    counts = {status: 0 for status in sorted(STATUSES)}
    for build_skill, run_skill in build_to_run.items():
        skill_fixtures = fixtures.get(build_skill)
        if not isinstance(skill_fixtures, list) or len(skill_fixtures) != 3:
            raise ValueError(f"Exactly three fixtures are required for {build_skill}")
        observed_statuses: set[str] = set()
        for fixture in skill_fixtures:
            name = fixture["name"]
            expected = fixture["expectedStatus"]
            payload = fixture["input"]
            if expected not in STATUSES or not isinstance(payload, dict):
                raise ValueError(f"Invalid fixture: {build_skill}/{name}")

            case_root = output_root / run_skill / name
            input_path = case_root / "input.json"
            artifact_root = case_root / "output"
            case_root.mkdir(parents=True, exist_ok=False)
            input_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            command = [
                sys.executable,
                str(RUNNER_PATH),
                "--run-skill",
                run_skill,
                "--input",
                str(input_path),
                "--output-dir",
                str(artifact_root),
            ]
            completed = subprocess.run(
                command,
                cwd=str(RUN_SKILL_ROOT / run_skill),
                capture_output=True,
                text=True,
                check=False,
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    f"Run Skill fixture failed: {run_skill}/{name}; "
                    f"stdout={completed.stdout.strip()} stderr={completed.stderr.strip()}"
                )

            result_path = artifact_root / "result.json"
            base_record_path = artifact_root / "run_record.json"
            run_skill_record_path = artifact_root / "run_skill_record.json"
            result = _read_json(result_path)
            base_record = _read_json(base_record_path)
            run_skill_record = _read_json(run_skill_record_path)
            actual = result.get("status")
            if actual != expected:
                raise ValueError(f"Status mismatch: {run_skill}/{name}: {actual} != {expected}")
            if base_record.get("status") != actual or run_skill_record.get("decision", {}).get("status") != actual:
                raise ValueError(f"Run Record status mismatch: {run_skill}/{name}")
            if result.get("runId") != base_record.get("runId") or result.get("runId") != run_skill_record.get("runId"):
                raise ValueError(f"Run ID mismatch: {run_skill}/{name}")

            observed_statuses.add(actual)
            counts[actual] += 1
            cases.append(
                {
                    "runSkill": run_skill,
                    "buildSkill": build_skill,
                    "fixture": name,
                    "expectedStatus": expected,
                    "actualStatus": actual,
                    "runId": result["runId"],
                    "inputPath": _project_relative(input_path),
                    "outputPath": _project_relative(artifact_root),
                    "resultSha256": _sha256(result_path),
                    "baseRunRecordSha256": _sha256(base_record_path),
                    "runSkillRecordSha256": _sha256(run_skill_record_path),
                }
            )
        if observed_statuses != STATUSES:
            raise ValueError(f"Fixture status coverage incomplete for {run_skill}: {sorted(observed_statuses)}")

    manifest = {
        "schemaVersion": "1.0",
        "profile": "supestar-p0-run-skill-candidate-matrix",
        "runSkillCount": len(entries),
        "caseCount": len(cases),
        "statusCounts": counts,
        "registryPath": _project_relative(REGISTRY_PATH),
        "fixturesPath": _project_relative(FIXTURES_PATH),
        "executionBoundary": registry["executionBoundary"],
        "cases": cases,
    }
    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute all Supestar P0 Run Skill fixtures.")
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = execute_matrix(args.output_root.resolve())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            {
                "status": "PASS",
                "runSkills": manifest["runSkillCount"],
                "cases": manifest["caseCount"],
                "statusCounts": manifest["statusCounts"],
                "outputRoot": str(args.output_root.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

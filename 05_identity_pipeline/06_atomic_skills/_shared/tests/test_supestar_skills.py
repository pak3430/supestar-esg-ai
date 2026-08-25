#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TEST_ROOT = Path(__file__).resolve().parent
ATOMIC_ROOT = TEST_ROOT.parents[1]
SHARED_ROOT = TEST_ROOT.parent
sys.path.insert(0, str(SHARED_ROOT))

from supestar_skills import evaluate, evaluate_question_routing  # noqa: E402


class SupestarSkillRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = json.loads((TEST_ROOT / "fixtures.json").read_text(encoding="utf-8"))

    def test_all_skills_have_three_verdict_fixtures(self) -> None:
        self.assertEqual(len(self.fixtures), 7)
        for skill, cases in self.fixtures.items():
            with self.subTest(skill=skill):
                self.assertEqual({case["expectedStatus"] for case in cases}, {"PROCEED", "REVIEW", "STOP"})

    def test_evaluators_are_deterministic_and_match_expected_status(self) -> None:
        for skill, cases in self.fixtures.items():
            for case in cases:
                with self.subTest(skill=skill, case=case["name"]):
                    first = evaluate(skill, case["input"])
                    second = evaluate(skill, case["input"])
                    self.assertEqual(first, second)
                    self.assertEqual(first["status"], case["expectedStatus"])
                    self.assertTrue(first["runId"].startswith("run-"))
                    self.assertTrue(first["evidence"])
                    self.assertTrue(first["artifacts"])

    def test_general_esg_questions_use_concept_route(self) -> None:
        cases = {
            "ESG가 무엇인가요?": "CONCEPT_EXPLANATION",
            "ESG가 왜 중요한가요?": "CONCEPT_EXPLANATION",
            "Scope 1이 무엇인가요?": "CONCEPT_EXPLANATION",
            "한국임업진흥원은 어떤 역할인가요?": "CONCEPT_EXPLANATION",
            "ESG가 탄소 측정과 Scope로 왜 이어지나요?": "ESG_CARBON_PATH",
            "배출권과 탄소크레딧은 어떻게 다른가요?": "CARBON_MARKET_COMPARISON",
        }
        for question, expected_route in cases.items():
            with self.subTest(question=question):
                result = evaluate("supestar-question-routing", {
                    "question": question,
                    "userRole": "LEARNER",
                    "asOfDate": "2026-08-25",
                })
                self.assertEqual(result["data"]["routeDecision"]["route"], expected_route)

    def test_explicit_follow_up_uses_verified_routing_question(self) -> None:
        payload = {
            "question": "그건 왜 중요한가요?",
            "routingQuestion": "ESG가 무엇인가요? / 그건 왜 중요한가요?",
            "conversationContinuity": {
                "policy": "EXPLICIT_FOLLOW_UP_ONLY",
                "historyMessagesUsed": 1,
            },
            "userRole": "LEARNER",
            "asOfDate": "2026-08-25",
            "providedEvidence": [],
        }
        result = evaluate_question_routing(payload)
        decision = result["data"]["routeDecision"]
        snapshot = result["data"]["contextSnapshot"]
        self.assertEqual(decision["route"], "CONCEPT_EXPLANATION")
        self.assertEqual(snapshot["question"], "그건 왜 중요한가요?")
        self.assertEqual(snapshot["routingQuestion"], payload["routingQuestion"])

    def test_each_wrapper_executes_and_lands_artifacts(self) -> None:
        for skill, cases in self.fixtures.items():
            case = cases[0]
            wrapper = ATOMIC_ROOT / skill / "scripts" / "run.py"
            self.assertTrue(wrapper.is_file(), wrapper)
            with tempfile.TemporaryDirectory(prefix=f"supestar-{skill}-") as temp:
                temp_path = Path(temp)
                input_path = temp_path / "input.json"
                output_path = temp_path / "output"
                input_path.write_text(json.dumps(case["input"], ensure_ascii=False), encoding="utf-8")
                completed = subprocess.run(
                    [sys.executable, str(wrapper), "--input", str(input_path), "--output-dir", str(output_path)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
                result = json.loads((output_path / "result.json").read_text(encoding="utf-8"))
                record = json.loads((output_path / "run_record.json").read_text(encoding="utf-8"))
                self.assertEqual(result["status"], case["expectedStatus"])
                self.assertEqual(record["runId"], result["runId"])
                self.assertGreaterEqual(len(result["artifactPaths"]), 3)
                for path in result["artifactPaths"]:
                    self.assertTrue(Path(path).is_file(), path)


if __name__ == "__main__":
    unittest.main(verbosity=2)

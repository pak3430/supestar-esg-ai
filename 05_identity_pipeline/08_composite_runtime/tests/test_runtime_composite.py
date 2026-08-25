from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


RUNNER_PATH = Path(__file__).resolve().parents[1] / "_shared/run_verified_composite.py"
SPEC = importlib.util.spec_from_file_location("run_verified_composite", RUNNER_PATH)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def _payload(question: str) -> dict[str, object]:
    return {
        "question": question,
        "userRole": "LEARNER",
        "asOfDate": "2026-08-25",
        "providedEvidence": [],
        "focus": "MEASUREMENT",
        "measurementContext": {},
        "activityDescription": "",
        "organizationBoundary": "",
        "sourceOwnershipOrControl": "UNKNOWN",
        "purchasedEnergyType": "UNKNOWN",
        "valueChainRelation": "UNKNOWN",
        "activityData": {},
        "purpose": "LEARNING",
        "unitType": "UNKNOWN",
        "registryStatus": "UNKNOWN",
        "doubleUse": False,
        "projectSummary": "",
        "environmentEvidence": [],
        "socialEvidence": [],
        "governanceEvidence": [],
        "claimCompleteWithoutAllAxes": False,
        "projectType": "",
        "currentStage": "UNKNOWN",
        "availableDocuments": [],
        "intendedUse": "LEARNING",
        "requestedFinalAssertion": False,
        "gates": {f"G{number}": {"state": "UNKNOWN"} for number in range(1, 12)},
        "conversationHistory": [],
    }


class RuntimeCompositeTest(unittest.TestCase):
    def _execute(self, question: str) -> tuple[dict[str, object], dict[str, object]]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "input.json"
            input_path.write_text(
                json.dumps(_payload(question), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            original = input_path.read_bytes()
            output_dir = root / "output"
            record = RUNNER.execute(
                "supestar-forest-esg-orchestrator-run",
                input_path,
                output_dir,
            )
            result = json.loads((output_dir / "result.json").read_text(encoding="utf-8"))
            self.assertEqual(input_path.read_bytes(), original)
            self.assertTrue(record["singleEntryPoint"])
            self.assertTrue(record["routePartition"]["exactlyOneRouteSelected"])
            self.assertEqual(record["members"]["routerExecutionCount"], 1)
            self.assertTrue(record["producerCarriage"]["byteFaithful"])
            self.assertFalse(record["knowledgeActionChain"]["sealedVaultMutation"])
            return result, record

    def test_concept_route_runs_kac_without_domain_skill(self) -> None:
        result, record = self._execute("ESG가 무엇인가요?")
        self.assertEqual(result["route"], "CONCEPT_EXPLANATION")
        self.assertIsNone(result["selectedRunSkill"])
        self.assertEqual(record["members"]["domainExecutionCount"], 0)
        self.assertIn("ESG", result["kacExecution"]["selectedConcepts"])
        self.assertTrue(result["kacExecution"]["allChainFilesPresent"])

    def test_domain_route_runs_exactly_one_domain_skill(self) -> None:
        result, record = self._execute("이 배출원은 어느 Scope인가요?")
        self.assertEqual(result["route"], "SCOPE_CLASSIFICATION")
        self.assertEqual(result["selectedRunSkill"], "scope-activity-classification-run")
        self.assertEqual(record["members"]["domainExecutionCount"], 1)
        self.assertEqual(
            record["members"]["executedIdentitySet"],
            ["supestar-question-routing-run", "query-specific-kac", "scope-activity-classification-run"],
        )

    def test_needs_input_stops_without_domain_skill(self) -> None:
        result, record = self._execute("이게 좋은 선택인가요?")
        self.assertEqual(result["route"], "NEEDS_INPUT")
        self.assertIsNone(result["selectedRunSkill"])
        self.assertEqual(record["members"]["domainExecutionCount"], 0)


if __name__ == "__main__":
    unittest.main()

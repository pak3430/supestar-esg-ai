#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT))
os.environ["SUPESTAR_AI_PROVIDER"] = "disabled"

from ai_runtime import AiRuntime  # noqa: E402
from knowledge_runtime import KnowledgeRuntime  # noqa: E402


class KnowledgeRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = KnowledgeRuntime()

    def test_stage_vault_is_complete_and_read_only(self) -> None:
        status = self.runtime.status()
        self.assertTrue(status["ready"])
        self.assertGreaterEqual(status["identityCount"], 80)
        self.assertEqual(status["identityCount"], status["conceptSkillCount"])
        self.assertFalse(status["sealedVaultMutation"])

    def test_core_questions_select_the_requested_concept(self) -> None:
        cases = {
            "ESG가 무엇인가요?": ["ESG"],
            "Scope 1과 Scope 2의 차이는 무엇인가요?": ["SCOPE_1", "SCOPE_2"],
            "한국임업진흥원은 어떤 역할인가요?": ["KOFPI"],
            "지식행동사슬은 왜 필요한가요?": ["KNOWLEDGE_ACTION_CHAIN"],
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                result = self.runtime.execute(question)
                self.assertEqual(result["selectedConcepts"], expected)
                self.assertTrue(result["allChainFilesPresent"])
                for chain in result["chains"]:
                    self.assertEqual([node["stage"] for node in chain["nodes"]], [
                        "Identity", "Goal", "Task", "Knowledge", "Method", "Skill",
                    ])
                    self.assertTrue(chain["conceptSkillRead"])
                    self.assertTrue(all(node["sha256"] for node in chain["nodes"]))

    def test_esg_guidance_stays_on_the_requested_definition(self) -> None:
        result = self.runtime.execute("ESG가 무엇인가요?")
        guidance = self.runtime.guidance(result)
        text = " ".join([guidance["title"], *guidance["paragraphs"]])
        self.assertIn("환경", text)
        self.assertIn("사회", text)
        self.assertIn("지배구조", text)
        self.assertNotIn("forestcarbonmarket", text.lower())
        self.assertIsNone(guidance["marketHandoff"])

    def test_short_follow_up_reuses_only_the_previous_user_topic(self) -> None:
        result = self.runtime.execute(
            "그건 왜 중요한가요?",
            history=[
                {"role": "user", "content": "ESG가 무엇인가요?"},
                {"role": "assistant", "content": "ESG의 정의"},
            ],
        )
        self.assertEqual(result["selectedConcepts"], ["ESG"])
        self.assertEqual(result["historyMessagesUsed"], 1)

    def test_short_new_topic_does_not_inherit_previous_user_topic(self) -> None:
        result = self.runtime.execute(
            "SDGs는요?",
            history=[
                {"role": "user", "content": "ESG가 무엇인가요?"},
                {"role": "assistant", "content": "ESG의 정의"},
            ],
        )
        self.assertEqual(result["effectiveQuestion"], "SDGs는요?")
        self.assertEqual(result["selectedConcepts"], ["SUSTAINABLE_DEVELOPMENT_GOALS"])
        self.assertEqual(result["historyMessagesUsed"], 0)

    def test_connective_with_new_topic_does_not_inherit_previous_topic(self) -> None:
        result = self.runtime.execute(
            "그러면 SDGs는요?",
            history=[{"role": "user", "content": "ESG가 무엇인가요?"}],
        )
        self.assertEqual(result["effectiveQuestion"], "그러면 SDGs는요?")
        self.assertEqual(result["selectedConcepts"], ["SUSTAINABLE_DEVELOPMENT_GOALS"])
        self.assertEqual(result["historyMessagesUsed"], 0)

    def test_ai_history_uses_only_explicit_follow_up_context(self) -> None:
        runtime = AiRuntime()
        history = [{"role": "user", "content": "ESG가 무엇인가요?"}]
        fallback = {
            "statusLabel": "답변",
            "title": "검증된 답변",
            "paragraphs": ["검증된 내용입니다."],
            "rationale": "근거에 따릅니다.",
            "steps": [],
            "followUp": "다음 질문을 입력하세요.",
            "marketHandoff": None,
        }
        deterministic = {"status": "PROCEED", "data": {}}
        _, new_topic_status = runtime.generate(
            "SDGs는요?", history, {}, deterministic, fallback, False, "CONCEPT_EXPLANATION"
        )
        _, follow_up_status = runtime.generate(
            "그건 왜 중요한가요?", history, {}, deterministic, fallback, False, "CONCEPT_EXPLANATION"
        )
        self.assertEqual(new_topic_status["historyMessagesUsed"], 0)
        self.assertEqual(follow_up_status["historyMessagesUsed"], 1)

    def test_disabled_ai_reports_honest_fallback_mode(self) -> None:
        status = AiRuntime().status()
        self.assertFalse(status["connected"])
        self.assertEqual(status["mode"], "STRUCTURED_GROUNDED")


if __name__ == "__main__":
    unittest.main(verbosity=2)

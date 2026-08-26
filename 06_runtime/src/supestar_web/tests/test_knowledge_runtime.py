#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


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

    def test_specific_institution_wins_over_broad_esg_term(self) -> None:
        question = "한국임업진흥원은 산림 ESG에서 어떤 역할을 하나요?"
        result = self.runtime.execute(
            question,
            history=[{"role": "user", "content": "ESG가 무엇인가요?"}],
        )
        self.assertEqual(result["selectedConcepts"], ["KOFPI"])
        self.assertEqual(result["historyMessagesUsed"], 0)
        guidance = self.runtime.guidance(result)
        text = " ".join([guidance["title"], *guidance["paragraphs"]])
        self.assertIn("한국임업진흥원", text)

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

    def test_self_contained_scope_question_does_not_inherit_unrelated_topic(self) -> None:
        question = (
            "우리 회사가 소유하고 직접 운영·통제하는 사업장 보일러에서 도시가스를 연소합니다. "
            "2026년 8월 사용량은 1,250Nm³이고 요금고지서도 보유하고 있습니다. "
            "이 배출원은 Scope 몇인가요?"
        )
        result = self.runtime.execute(
            question,
            history=[{"role": "user", "content": "SDGs는 ESG와 어떤 관계인가요?"}],
        )
        self.assertEqual(result["effectiveQuestion"], question)
        self.assertEqual(result["historyMessagesUsed"], 0)
        self.assertEqual(result["selectedConcepts"], ["SCOPE_1"])

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

        cloud_env = {
            "SUPESTAR_AI_PROVIDER": "cloud",
            "SUPESTAR_CLOUD_AI_BASE_URL": "https://example.invalid/v1",
            "SUPESTAR_CLOUD_AI_API_KEY": "test-secret-never-recorded",
            "SUPESTAR_CLOUD_AI_MODEL": "test-grounded-model",
        }
        with patch.dict(os.environ, cloud_env, clear=False):
            cloud_runtime = AiRuntime()
            cloud_status = cloud_runtime.status()
        self.assertTrue(cloud_status["connected"])
        self.assertTrue(cloud_status["configured"])
        self.assertEqual(cloud_status["provider"], "cloud")
        self.assertEqual(cloud_status["mode"], "CLOUD_AI_GROUNDED")
        self.assertNotIn("test-secret-never-recorded", str(cloud_status))

        cloud_response = {
            "choices": [{
                "message": {"content": json.dumps({"title": "검증된 답변"}, ensure_ascii=False)},
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 12, "completion_tokens": 5},
        }
        with patch.object(cloud_runtime, "_request", return_value=cloud_response) as request_mock:
            content, metrics = cloud_runtime._generate_with_provider(
                cloud_status,
                [{"role": "user", "content": "검증된 내용만 설명하세요."}],
            )
        self.assertEqual(json.loads(content)["title"], "검증된 답변")
        self.assertEqual(metrics["doneReason"], "stop")
        self.assertEqual(metrics["promptTokens"], 12)
        self.assertEqual(request_mock.call_args.args[0], "/chat/completions")
        self.assertEqual(request_mock.call_args.kwargs["base_url"], "https://example.invalid/v1")
        self.assertEqual(request_mock.call_args.args[1]["temperature"], 0.55)
        self.assertEqual(request_mock.call_args.args[1]["top_p"], 0.9)

    @staticmethod
    def _grounded_generation_fixture() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        kac = {
            "intent": "CONCEPT_EXPLANATION",
            "selectedConcepts": ["ESG"],
            "chains": [{
                "identity": "ESG",
                "title": "ESG",
                "definition": "환경, 사회, 지배구조를 함께 보는 경영 관점",
                "keyPoints": ["환경", "사회", "지배구조"],
                "nodes": [],
                "sourceEvidence": [],
            }],
        }
        deterministic = {
            "status": "PROCEED",
            "summary": "ESG 개념 설명",
            "data": {},
            "missingEvidence": [],
            "nextActions": [],
        }
        fallback = {
            "statusLabel": "근거에 따라 답변했어요",
            "title": "완성된 고정 답변 제목",
            "paragraphs": ["환경·사회·지배구조를 함께 보는 관점입니다."],
            "rationale": "검증된 개념 사슬을 사용했습니다.",
            "steps": [],
            "followUp": "어느 영역을 더 살펴볼까요?",
            "marketHandoff": None,
        }
        return kac, deterministic, fallback

    @staticmethod
    def _cloud_runtime() -> AiRuntime:
        cloud_env = {
            "SUPESTAR_AI_PROVIDER": "cloud",
            "SUPESTAR_CLOUD_AI_BASE_URL": "https://example.invalid/v1",
            "SUPESTAR_CLOUD_AI_API_KEY": "test-secret-never-recorded",
            "SUPESTAR_CLOUD_AI_MODEL": "test-grounded-model",
        }
        with patch.dict(os.environ, cloud_env, clear=False):
            return AiRuntime()

    def test_model_receives_verified_kac_without_completed_fallback_answer(self) -> None:
        runtime = self._cloud_runtime()
        kac, deterministic, fallback = self._grounded_generation_fixture()
        model_guidance = {
            "title": "ESG는 성과를 세 방향에서 보는 기준입니다",
            "paragraphs": [
                "환경에 미치는 영향뿐 아니라 사회에 대한 책임과 지배구조의 건전성을 함께 살펴봅니다.",
                "그래서 재무 성과만으로는 놓칠 수 있는 지속가능성 위험과 기회를 구조적으로 확인할 수 있습니다.",
            ],
            "rationale": "검증된 ESG 개념 사슬의 정의와 핵심 요소를 재구성했습니다.",
            "followUp": "환경·사회·지배구조 중 어느 영역을 더 알아볼까요?",
        }
        metrics = {"promptTokens": 21, "responseTokens": 34, "doneReason": "stop"}
        with patch.object(
            runtime,
            "_generate_with_provider",
            return_value=(json.dumps(model_guidance, ensure_ascii=False), metrics),
        ) as generation_mock:
            guidance, status = runtime.generate(
                "ESG가 무엇인가요?", [], kac, deterministic, fallback, False, "CONCEPT_EXPLANATION"
            )

        messages = generation_mock.call_args.args[1]
        serialized_prompt = json.dumps(messages, ensure_ascii=False)
        self.assertNotIn("fallbackAnswer", serialized_prompt)
        self.assertNotIn("완성된 고정 답변 제목", serialized_prompt)
        self.assertIn("환경, 사회, 지배구조", serialized_prompt)
        self.assertIn("responseStyle", serialized_prompt)
        self.assertEqual(guidance["title"], model_guidance["title"])
        self.assertTrue(status["generationUsed"])
        self.assertTrue(status["modelOutputChangedFromFallback"])
        self.assertNotEqual(status["modelOutputSha256"], status["fallbackOutputSha256"])
        self.assertEqual(status["generationAttempts"], 1)
        self.assertEqual(status["temperature"], 0.55)
        self.assertEqual(status["promptTokensTotal"], 21)
        self.assertEqual(status["responseTokensTotal"], 34)

    def test_exact_fallback_echo_is_retried_before_accepting_model_output(self) -> None:
        runtime = self._cloud_runtime()
        kac, deterministic, fallback = self._grounded_generation_fixture()
        echo = {
            "title": fallback["title"],
            "paragraphs": fallback["paragraphs"],
            "rationale": fallback["rationale"],
            "followUp": fallback["followUp"],
        }
        changed = {
            "title": "ESG는 환경·사회·지배구조를 함께 보는 틀입니다",
            "paragraphs": ["조직의 환경 영향, 사회적 책임, 지배구조의 운영 방식을 한데 놓고 판단합니다."],
            "rationale": "검증된 ESG 개념 사슬에 근거했습니다.",
            "followUp": "세 영역 중 무엇을 더 살펴볼까요?",
        }
        metrics = {"promptTokens": 10, "responseTokens": 12, "doneReason": "stop"}
        with patch.object(
            runtime,
            "_generate_with_provider",
            side_effect=[
                (json.dumps(echo, ensure_ascii=False), metrics),
                (json.dumps(changed, ensure_ascii=False), metrics),
            ],
        ) as generation_mock:
            guidance, status = runtime.generate(
                "ESG가 무엇인가요?", [], kac, deterministic, fallback, False, "CONCEPT_EXPLANATION"
            )

        self.assertEqual(generation_mock.call_count, 2)
        self.assertEqual(guidance["title"], changed["title"])
        self.assertTrue(status["generationUsed"])
        self.assertTrue(status["modelOutputChangedFromFallback"])
        self.assertEqual(status["generationAttempts"], 2)
        self.assertEqual(status["promptTokensTotal"], 20)
        self.assertEqual(status["responseTokensTotal"], 24)

    def test_web_ui_exposes_generation_proof_fields(self) -> None:
        app_script = (APP_ROOT / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("AI 생성 증거", app_script)
        self.assertIn("modelOutputChangedFromFallback", app_script)
        self.assertIn("fallbackOutputSha256", app_script)


if __name__ == "__main__":
    unittest.main(verbosity=2)

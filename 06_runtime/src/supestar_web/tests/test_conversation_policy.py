#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT))

from conversation_policy import effective_question, is_explicit_follow_up  # noqa: E402


class ConversationPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.unrelated_history = [
            {"role": "user", "content": "SDGs는 ESG와 어떤 관계인가요?"},
        ]

    def assert_independent(self, question: str) -> None:
        effective, used = effective_question(question, self.unrelated_history)
        self.assertFalse(is_explicit_follow_up(question))
        self.assertEqual(effective, question)
        self.assertEqual(used, 0)

    def assert_follow_up(self, question: str) -> None:
        effective, used = effective_question(question, self.unrelated_history)
        self.assertTrue(is_explicit_follow_up(question))
        self.assertTrue(effective.startswith("SDGs는 ESG와 어떤 관계인가요? / "))
        self.assertEqual(used, 1)

    def test_self_contained_scope_question_keeps_current_turn_only(self) -> None:
        self.assert_independent(
            "우리 회사가 소유하고 직접 운영·통제하는 사업장 보일러에서 도시가스를 연소합니다. "
            "2026년 8월 사용량은 1,250Nm³이고 요금고지서도 보유하고 있습니다. "
            "이 배출원은 Scope 몇인가요?"
        )

    def test_self_contained_reference_at_start_keeps_current_turn_only(self) -> None:
        self.assert_independent(
            "이 배출원은 우리 회사가 소유한 사업장 보일러에서 도시가스를 연소하는 활동입니다. "
            "Scope 몇인가요?"
        )

    def test_self_contained_project_reference_keeps_current_turn_only(self) -> None:
        self.assert_independent(
            "우리 회사가 산림 조림 프로젝트를 추진하고 있습니다. 이 사업은 어떤 등록 절차가 필요한가요?"
        )

    def test_self_contained_generic_reference_keeps_current_turn_only(self) -> None:
        self.assert_independent(
            "ESG는 환경·사회·지배구조를 함께 보는 경영 체계라고 설명했습니다. 그게 맞나요?"
        )

    def test_unresolved_entity_reference_uses_previous_user_turn(self) -> None:
        self.assert_follow_up("이 배출원은 Scope 몇인가요?")

    def test_explicit_cross_turn_marker_uses_previous_user_turn(self) -> None:
        self.assert_follow_up("앞서 말한 배출원은 Scope 몇인가요?")

    def test_continuation_only_question_uses_previous_user_turn(self) -> None:
        self.assert_follow_up("그건 왜 중요한가요?")

    def test_new_topic_without_reference_stays_independent(self) -> None:
        self.assert_independent("Scope 1과 Scope 2의 차이는 무엇인가요?")


if __name__ == "__main__":
    unittest.main()

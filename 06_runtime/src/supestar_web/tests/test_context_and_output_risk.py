from __future__ import annotations

import sys
import unittest
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT))

from context_runtime import ContextRuntime  # noqa: E402
from output_risk_gate import OutputRiskGate  # noqa: E402


def _base() -> dict[str, object]:
    return {
        "userRole": "LEARNER",
        "providedEvidence": [],
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
    }


class ContextRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = ContextRuntime()

    def _extract(self, question: str) -> tuple[dict[str, object], dict[str, object]]:
        return self.runtime.enrich(_base(), question, [])

    def test_scope_1_user_statement_becomes_typed_input(self) -> None:
        payload, report = self._extract(
            "우리 회사가 소유하고 직접 운영·통제하는 사업장 보일러에서 도시가스 1,250Nm3를 연소했고 고지서를 보유했습니다. 어느 Scope인가요?"
        )
        self.assertEqual(payload["sourceOwnershipOrControl"], "OWNED_CONTROLLED")
        self.assertEqual(payload["purchasedEnergyType"], "NONE")
        self.assertEqual(payload["valueChainRelation"], "NONE")
        self.assertEqual(payload["activityData"]["quantity"], 1250)
        self.assertTrue(payload["organizationBoundary"])
        self.assertFalse(report["hasConflicts"])

    def test_scope_1_owned_operated_natural_variant_becomes_typed_input(self) -> None:
        payload, report = self._extract(
            "저희 회사가 소유·운영하는 보일러에서 도시가스 1,250 Nm³를 2026년 8월에 사용했고 고지서가 있습니다. Scope 몇인가요?"
        )
        self.assertEqual(payload["sourceOwnershipOrControl"], "OWNED_CONTROLLED")
        self.assertEqual(payload["purchasedEnergyType"], "NONE")
        self.assertEqual(payload["valueChainRelation"], "NONE")
        self.assertEqual(payload["activityData"]["quantity"], 1250)
        self.assertTrue(payload["organizationBoundary"])
        self.assertFalse(report["hasConflicts"])

    def test_scope_2_and_scope_3_relationships(self) -> None:
        scope_2, _ = self._extract(
            "우리 회사 사업장에서 한전 구매전력 8,500kWh를 사용하고 전기요금 고지서를 보유했습니다. 어느 Scope인가요?"
        )
        self.assertEqual(scope_2["purchasedEnergyType"], "ELECTRICITY")
        self.assertEqual(scope_2["sourceOwnershipOrControl"], "NOT_OWNED_CONTROLLED")
        scope_3, _ = self._extract(
            "협력사가 소유하고 운영하는 외주 운송이며 운송계약서와 운행일지를 보유했습니다. 어느 Scope인가요?"
        )
        self.assertEqual(scope_3["valueChainRelation"], "UPSTREAM")
        self.assertEqual(scope_3["sourceOwnershipOrControl"], "NOT_OWNED_CONTROLLED")

    def test_conflicting_scope_relationships_remain_unknown(self) -> None:
        payload, report = self._extract(
            "회사 소유 보일러 연소이면서 한전 구매전력 사용입니다. 어느 Scope인지 하나로 확정해줘."
        )
        self.assertTrue(report["hasConflicts"])
        self.assertEqual(payload["sourceOwnershipOrControl"], "UNKNOWN")
        self.assertEqual(payload["purchasedEnergyType"], "UNKNOWN")

    def test_negated_ownership_is_not_promoted_to_scope_1(self) -> None:
        payload, report = self._extract(
            "이 차량은 우리 회사 소유가 아니고 협력사가 소유·운영합니다. 어느 Scope인가요?"
        )
        self.assertEqual(payload["sourceOwnershipOrControl"], "NOT_OWNED_CONTROLLED")
        self.assertEqual(payload["purchasedEnergyType"], "UNKNOWN")
        self.assertFalse(report["hasConflicts"])

    def test_short_new_question_does_not_inherit_prior_scope_relationship(self) -> None:
        payload, report = self.runtime.enrich(
            _base(),
            "한전 구매전력은 어느 Scope인가요?",
            [{"role": "user", "content": "우리 회사 소유 보일러는 어느 Scope인가요?"}],
        )
        self.assertEqual(report["priorUserMessagesUsed"], 0)
        self.assertEqual(payload["purchasedEnergyType"], "ELECTRICITY")
        self.assertNotEqual(payload["sourceOwnershipOrControl"], "OWNED_CONTROLLED")

    def test_connective_with_new_activity_does_not_inherit_prior_scope_relationship(self) -> None:
        payload, report = self.runtime.enrich(
            _base(),
            "그러면 한전 구매전력은 어느 Scope인가요?",
            [{"role": "user", "content": "우리 회사 소유 보일러는 어느 Scope인가요?"}],
        )
        self.assertEqual(report["priorUserMessagesUsed"], 0)
        self.assertEqual(payload["purchasedEnergyType"], "ELECTRICITY")
        self.assertNotEqual(payload["sourceOwnershipOrControl"], "OWNED_CONTROLLED")

    def test_explicit_follow_up_uses_only_prior_user_statement(self) -> None:
        payload, report = self.runtime.enrich(
            _base(),
            "그 배출원은 어느 Scope인가요?",
            [
                {"role": "user", "content": "우리 회사가 소유하고 직접 운영하는 보일러입니다."},
                {"role": "assistant", "content": "협력사 설비이므로 Scope 3입니다."},
            ],
        )
        self.assertEqual(report["priorUserMessagesUsed"], 1)
        self.assertEqual(payload["sourceOwnershipOrControl"], "OWNED_CONTROLLED")

    def test_evidence_polarity_is_clause_local(self) -> None:
        payload, _ = self._extract(
            "산림 ESG 사업입니다. 모니터링 보고서는 보유했습니다. 산주 동의서는 아직 없습니다. 사업등록증은 보유했습니다. E/S/G 평가해줘."
        )
        self.assertTrue(payload["environmentEvidence"])
        self.assertFalse(payload["socialEvidence"])
        self.assertTrue(payload["governanceEvidence"])

    def test_registry_and_procedure_conflicts_are_exposed(self) -> None:
        market, market_report = self._extract(
            "탄소크레딧은 등록 완료됐지만 소각 여부는 미확인입니다. 공시에 사용해도 되나요?"
        )
        self.assertEqual(market["registryStatus"], "UNVERIFIED")
        self.assertTrue(market_report["hasConflicts"])
        procedure, procedure_report = self._extract(
            "산림경영형 산림탄소 사업이 사업등록 완료 단계이면서 모니터링 단계라고 전달받았습니다. 현재 단계와 다음 공식 절차를 알려줘."
        )
        self.assertEqual(procedure["currentStage"], "UNKNOWN")
        self.assertTrue(procedure_report["hasConflicts"])

    def test_additional_scope_3_categories(self) -> None:
        upstream, _ = self._extract("직원의 출장 항공 이동은 어느 Scope인가요?")
        downstream, _ = self._extract("판매제품 사용 단계의 배출은 어느 Scope인가요?")
        self.assertEqual(upstream["valueChainRelation"], "UPSTREAM")
        self.assertEqual(downstream["valueChainRelation"], "DOWNSTREAM")

    def test_forest_procedure_and_transaction_evidence(self) -> None:
        forest, _ = self._extract(
            "산림 ESG 사업입니다. 흡수량 모니터링 보고서와 생태조사서, 산주 동의서와 지역사회 편익배분서, 사업등록증과 검증보고서·계약서를 모두 보유했습니다. E/S/G 평가해줘."
        )
        self.assertTrue(forest["projectSummary"])
        self.assertTrue(forest["environmentEvidence"])
        self.assertTrue(forest["socialEvidence"])
        self.assertTrue(forest["governanceEvidence"])

        procedure, _ = self._extract(
            "산림경영형 산림탄소 사업을 사업등록 완료했고 등록증을 보유했습니다. 현재 등록 단계에서 다음 공식 절차를 알려줘."
        )
        self.assertEqual(procedure["projectType"], "산림경영형")
        self.assertEqual(procedure["currentStage"], "REGISTERED")
        self.assertTrue(procedure["availableDocuments"])

        transaction, _ = self._extract(
            "탄소크레딧 거래 준비도를 점검해줘. 판매자·구매자 신원과 대리권 확인 완료. 사업·수량·빈티지·단위 상태 확인 완료. 토지·사업권 증빙 보유. 처분권 확인 완료. 인증 유효상태 확인 완료. 구매목적 승인 완료. 계약 체결. 세무 검토 완료. 결제·정산 구조 확인 완료. 등록부 이전·소각 절차 확인 완료. 외부 주장 승인 완료."
        )
        self.assertTrue(all(transaction["gates"][f"G{number}"]["state"] == "PRESENT" for number in range(1, 12)))

    def test_explicit_context_has_final_precedence(self) -> None:
        payload, report = self.runtime.enrich(
            _base(),
            "회사 보일러는 어느 Scope인가요?",
            [],
            explicit_context={"sourceOwnershipOrControl": "NOT_OWNED_CONTROLLED"},
            allowed_explicit_fields={"sourceOwnershipOrControl"},
        )
        self.assertEqual(payload["sourceOwnershipOrControl"], "NOT_OWNED_CONTROLLED")
        self.assertEqual(report["explicitFieldCount"], 1)


class OutputRiskGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.gate = OutputRiskGate()
        self.fallback = {
            "statusLabel": "안내",
            "title": "원래 제목",
            "paragraphs": ["원래 답변"],
            "rationale": "근거",
            "steps": [],
            "followUp": "추가 질문",
            "marketHandoff": {"url": "https://forestcarbonmarket.kr/"},
        }

    def test_review_forces_non_assertive_verified_fallback(self) -> None:
        result = {
            "status": "REVIEW",
            "summary": "Scope 분류 정보가 부족합니다.",
            "missingEvidence": ["organizationBoundary"],
            "data": {"candidateScope": None},
        }
        safe = self.gate.safe_fallback(self.fallback, result, "SCOPE_CLASSIFICATION")
        self.assertIsNone(safe["marketHandoff"])
        self.assertNotIn("Scope 1", " ".join([safe["title"], *safe["paragraphs"]]))
        self.assertNotIn("검증 가능한 최종 결론", " ".join([safe["title"], *safe["paragraphs"]]))
        self.assertIn("조금만 더", safe["statusLabel"])
        self.assertFalse(self.gate.generation_policy("SCOPE_CLASSIFICATION", result)["modelGenerationAllowed"])

    def test_review_and_stop_messages_are_natural_but_keep_the_verdict(self) -> None:
        market_review = self.gate.safe_fallback(
            self.fallback,
            {"status": "REVIEW", "summary": "외부 주장 검토", "missingEvidence": [], "data": {}},
            "CARBON_MARKET_COMPARISON",
        )
        transaction_stop = self.gate.safe_fallback(
            self.fallback,
            {"status": "STOP", "summary": "게이트 누락", "missingEvidence": [], "data": {}},
            "TRANSACTION_READINESS",
        )
        self.assertIn("공시", market_review["statusLabel"])
        self.assertNotIn("REVIEW", " ".join([market_review["title"], *market_review["paragraphs"]]))
        self.assertIn("거래를 진행하면 안", transaction_stop["title"])
        self.assertNotIn("STOP", " ".join([transaction_stop["title"], *transaction_stop["paragraphs"]]))

    def test_scope_conflict_message_asks_to_separate_activities(self) -> None:
        guidance = self.gate.safe_fallback(
            self.fallback,
            {
                "status": "REVIEW",
                "summary": "Scope 관계 충돌",
                "missingEvidence": [],
                "data": {"candidateScope": None},
                "contextExtraction": {"hasConflicts": True},
            },
            "SCOPE_CLASSIFICATION",
        )
        self.assertIn("서로 다른 배출 활동", guidance["title"])
        self.assertIn("하나만", " ".join(guidance["paragraphs"]))

    def test_scope_claim_must_equal_verified_candidate(self) -> None:
        result = {"status": "PROCEED", "data": {"candidateScope": "SCOPE_1"}}
        accepted = self.gate.assess_model_guidance(
            {"title": "이 배출원은 Scope 1 후보입니다.", "paragraphs": ["검증 규칙에 따라 분류했습니다."]},
            "SCOPE_CLASSIFICATION",
            result,
            False,
        )
        rejected = self.gate.assess_model_guidance(
            {"title": "이 배출원은 Scope 2입니다.", "paragraphs": ["확정했습니다."]},
            "SCOPE_CLASSIFICATION",
            result,
            False,
        )
        self.assertTrue(accepted["accepted"])
        self.assertFalse(rejected["accepted"])

    def test_transaction_route_is_always_deterministic_output(self) -> None:
        policy = self.gate.generation_policy("TRANSACTION_READINESS", {"status": "PROCEED"})
        self.assertFalse(policy["modelGenerationAllowed"])

    def test_unverified_external_link_and_official_claim_are_rejected(self) -> None:
        result = {"status": "PROCEED", "data": {}}
        decision = self.gate.assess_model_guidance(
            {
                "title": "공식적으로 인정되었습니다.",
                "paragraphs": ["자세한 내용은 https://example.com 에서 확인하세요."],
                "rationale": "근거",
                "followUp": "계속할까요?",
            },
            "CONCEPT_EXPLANATION",
            result,
            False,
        )
        self.assertFalse(decision["accepted"])
        self.assertIn("UNVERIFIED_EXTERNAL_LINK", decision["reasonCodes"])


if __name__ == "__main__":
    unittest.main()

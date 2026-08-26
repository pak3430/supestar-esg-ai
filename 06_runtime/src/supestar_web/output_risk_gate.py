#!/usr/bin/env python3
"""Risk gate that keeps model prose inside verified execution boundaries."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any


MISSING_FIELD_LABELS = {
    "activityDescription": "실제 배출·에너지 활동",
    "organizationBoundary": "조직·운영 경계",
    "sourceOwnershipOrControl": "배출원 소유·통제 관계",
    "purchasedEnergyType": "구매 에너지 유형",
    "valueChainRelation": "상·하류 가치사슬 관계",
    "measurementContext": "조직경계·활동자료를 포함한 측정 맥락",
    "projectSummary": "사업 목적·활동·위치·참여자 요약",
    "projectType": "산림탄소 사업유형",
    "currentStage": "현재 공식 절차 단계",
    "availableDocuments": "현재 단계 완료 증빙",
    "registryStatus": "등록부 발행·보유·이전·소각 상태",
}


class OutputRiskGate:
    """Apply verdict, evidence, authority and external-action output gates."""

    @staticmethod
    def safe_fallback(
        guidance: dict[str, Any],
        deterministic_result: dict[str, Any],
        route: str = "",
    ) -> dict[str, Any]:
        status = str(deterministic_result.get("status", "STOP")).upper()
        if status == "PROCEED":
            return deepcopy(guidance)

        protected = deepcopy(guidance)
        summary = str(deterministic_result.get("summary", "검증 가능한 결론을 확정하지 않았습니다.")).strip()
        missing = [str(item) for item in deterministic_result.get("missingEvidence", []) if str(item).strip()]
        readable_missing = [MISSING_FIELD_LABELS.get(item, item) for item in missing]
        protected["marketHandoff"] = None

        data = dict(deterministic_result.get("data", {})) if isinstance(deterministic_result.get("data"), dict) else {}
        if isinstance(deterministic_result.get("contextExtraction"), dict):
            data["contextExtraction"] = deterministic_result["contextExtraction"]
        if status == "REVIEW":
            protected.update(OutputRiskGate._natural_review(route, protected, summary, readable_missing, data))
        else:
            protected.update(OutputRiskGate._natural_stop(route, protected, summary))
        return protected

    @staticmethod
    def _natural_review(
        route: str,
        guidance: dict[str, Any],
        summary: str,
        readable_missing: list[str],
        data: dict[str, Any],
    ) -> dict[str, Any]:
        if route == "SCOPE_CLASSIFICATION":
            context = data.get("contextExtraction", {}) if isinstance(data.get("contextExtraction"), dict) else {}
            conflict = (
                "conflictingScopeRelationships" in readable_missing
                or "CONFLICTING_SCOPE_RELATIONSHIPS" in data.get("ruleTrace", [])
                or bool(context.get("hasConflicts"))
            )
            if conflict:
                return {
                    "statusLabel": "활동을 하나씩 나눠서 확인해 주세요",
                    "title": "서로 다른 배출 활동이 한 질문에 함께 들어 있어 Scope를 하나로 정할 수 없어요.",
                    "paragraphs": [
                        "예를 들어 회사 소유 보일러는 Scope 1, 구매한 전력은 Scope 2의 기준으로 각각 따로 확인해야 합니다.",
                        "분류할 활동을 하나만 골라 누가 소유·운영하는지 함께 알려주세요.",
                    ],
                    "followUp": "먼저 보일러와 구매 전력 중 어떤 활동부터 확인할까요?",
                }
            return {
                "statusLabel": "조금만 더 알려주세요",
                "title": "이 배출원이 어느 Scope인지 판단하려면 활동과 소유·운영 관계가 더 필요해요.",
                "paragraphs": [
                    "회사 소유 보일러인지, 외부에서 구매한 전기인지, 협력사가 수행한 운송인지처럼 실제 상황을 알려주시면 분류할 수 있습니다.",
                    "사용량이 있다면 기간과 단위, 고지서나 운행일지 같은 자료도 함께 적어 주세요.",
                ],
                "followUp": "어떤 활동에서 발생했고, 그 설비나 차량은 누가 소유하고 운영하나요?",
            }
        if route == "CARBON_MARKET_COMPARISON":
            if "등록부 발행·보유·이전·소각 상태" in readable_missing:
                return {
                    "statusLabel": "등록 상태를 먼저 확인해 주세요",
                    "title": "이 크레딧을 실제로 사용할 수 있는지는 아직 판단하기 어려워요.",
                    "paragraphs": [
                        "발행·보유·이전·소각 여부와 중복 사용 가능성을 등록부에서 먼저 확인해야 합니다.",
                        "사용 목적이 내부 학습인지, 감축 목표인지, 외부 공시인지에 따라서도 필요한 승인이 달라집니다.",
                    ],
                    "followUp": "등록부에서 확인한 현재 상태와 사용 목적을 알려주시겠어요?",
                }
            return {
                "statusLabel": "공시에 쓰기 전 확인이 필요해요",
                "title": "크레딧이 소각됐다는 사실만으로 탄소중립 공시에 바로 사용할 수 있는 것은 아니에요.",
                "paragraphs": [
                    "적용되는 제도와 공시 기준, 실제로 사용할 문구, 회사 내부 승인까지 함께 확인해야 합니다.",
                    "수페스타는 필요한 확인사항을 정리할 수 있지만 공시 문구의 적정성을 최종 승인하지는 않습니다.",
                ],
                "followUp": "어느 공시나 보고서에 어떤 문구로 쓰려는지 알려주시면 확인 항목을 정리해 드릴게요.",
            }
        if route == "FOREST_ESG_MAPPING":
            missing_axes = [str(axis) for axis in data.get("missingAxes", [])]
            axis_names = {"E": "환경", "S": "사회", "G": "지배구조"}
            readable_axes = "·".join(axis_names.get(axis, axis) for axis in missing_axes) or "일부"
            return {
                "statusLabel": "빠진 자료가 있어요",
                "title": f"현재 자료에는 {readable_axes} 영역을 확인할 근거가 더 필요해요.",
                "paragraphs": [
                    "환경은 흡수량·생태 자료, 사회는 산주·지역사회 권리와 참여 자료, 지배구조는 등록·검증·계약 자료로 나눠 확인합니다.",
                    "가지고 있는 자료만 말씀해 주시면 어느 영역이 비어 있는지 정리해 드릴게요.",
                ],
                "followUp": "현재 보유한 보고서·동의서·등록증·검증자료가 무엇인지 알려주시겠어요?",
            }
        if route == "FOREST_CARBON_PROCEDURE":
            return {
                "statusLabel": "현재 단계를 먼저 확인해 주세요",
                "title": "다음 절차를 안내하려면 사업유형과 지금까지 완료한 단계가 필요해요.",
                "paragraphs": [
                    "사업계획, 적격성 검토, 사업등록, 실행, 모니터링, 검증, 인증 중 현재 어디까지 왔는지 알려주세요.",
                    "완료했다고 보는 단계가 있다면 등록증이나 보고서 같은 확인 자료도 함께 적어 주세요.",
                ],
                "followUp": "사업유형과 현재 단계, 가지고 있는 문서를 알려주시겠어요?",
            }
        if route == "TRANSACTION_READINESS":
            return {
                "statusLabel": "사람의 확인이 더 필요해요",
                "title": "거래를 막는 핵심 문제는 없지만, 아직 확인이 끝나지 않은 항목이 있어요.",
                "paragraphs": [
                    "구매 목적, 세무 처리, 외부에 사용할 주장과 증빙은 담당자의 검토와 승인이 필요합니다.",
                    "확인되지 않은 항목을 완료된 것으로 간주하지 않고 그대로 남겨 두었습니다.",
                ],
                "followUp": "남아 있는 항목의 담당자와 실제 확인 문서를 연결해 볼까요?",
            }
        if route == "NEEDS_INPUT":
            return {
                "statusLabel": guidance.get("statusLabel", "상황을 조금 더 알려주세요"),
                "title": guidance.get("title", "무엇을 알고 싶은지 조금 더 구체적으로 알려주세요."),
                "paragraphs": guidance.get("paragraphs", ["질문 대상을 하나로 정하면 필요한 내용만 골라 답할 수 있어요."]),
                "followUp": guidance.get("followUp", "ESG, Scope, 탄소시장, 산림탄소 중 어디부터 볼까요?"),
            }
        missing_text = ", ".join(readable_missing)
        return {
            "statusLabel": "조금만 더 확인해 주세요",
            "title": "지금 정보만으로는 답을 확정하기 어려워요.",
            "paragraphs": [f"추가로 필요한 내용은 {missing_text}입니다." if missing_text else summary],
            "followUp": guidance.get("followUp", "확인할 상황을 조금 더 자세히 알려주세요."),
        }

    @staticmethod
    def _natural_stop(route: str, guidance: dict[str, Any], summary: str) -> dict[str, Any]:
        messages = {
            "ESG_CARBON_PATH": (
                "측정과 직접 감축을 건너뛰고 탄소중립부터 선언할 수는 없어요.",
                "먼저 배출량을 확인하고 줄일 수 있는 부분을 감축한 뒤, 남은 배출에 대해 보완 방법을 검토해야 합니다.",
            ),
            "CARBON_MARKET_COMPARISON": (
                "같은 탄소크레딧을 두 곳에 중복해서 사용할 수는 없어요.",
                "한 번 사용하거나 소각한 단위는 같은 성과로 다시 주장하지 않도록 등록부 상태와 사용 기록을 확인해야 합니다.",
            ),
            "FOREST_ESG_MAPPING": (
                "탄소 흡수량만으로 산림 ESG가 완성됐다고 말할 수는 없어요.",
                "산주와 지역사회의 권리, 참여와 편익, 등록·검증·책임체계까지 함께 확인해야 합니다.",
            ),
            "FOREST_CARBON_PROCEDURE": (
                "검증과 인증을 건너뛰고 바로 거래할 수 있다고 확정할 수는 없어요.",
                "현재 단계의 완료 자료를 확인한 뒤 정해진 순서대로 다음 절차를 진행해야 합니다.",
            ),
            "TRANSACTION_READINESS": (
                "지금은 거래를 진행하면 안 돼요. 필수 확인사항이 남아 있습니다.",
                "판매 권한, 크레딧 상태, 계약, 결제와 등록부 이전처럼 거래를 좌우하는 자료부터 확인해야 합니다.",
            ),
            "OUT_OF_SCOPE": (
                "그 요청은 수페스타가 직접 처리하거나 확정할 수 없어요.",
                "대신 실행 전에 필요한 절차와 자료, 담당자가 확인할 질문은 정리해 드릴 수 있습니다.",
            ),
        }
        title, paragraph = messages.get(
            route,
            ("이 요청은 지금 상태로 진행할 수 없어요.", summary),
        )
        return {
            "statusLabel": "여기서는 멈추고 확인해야 해요",
            "title": title,
            "paragraphs": [paragraph],
            "followUp": guidance.get("followUp", "설명과 준비사항을 묻는 방식으로 질문을 바꿔 주세요."),
        }

    @staticmethod
    def generation_policy(route: str, deterministic_result: dict[str, Any]) -> dict[str, Any]:
        status = str(deterministic_result.get("status", "STOP")).upper()
        reasons: list[str] = []
        if status != "PROCEED":
            reasons.append("NON_PROCEED_VERDICT_REQUIRES_DETERMINISTIC_GUIDANCE")
        if route == "TRANSACTION_READINESS":
            reasons.append("HIGH_RISK_TRANSACTION_DOMAIN_REQUIRES_DETERMINISTIC_GUIDANCE")
        return {
            "decision": "ALLOW_MODEL_DRAFT" if not reasons else "USE_VERIFIED_FALLBACK",
            "route": route,
            "verifiedStatus": status,
            "reasonCodes": reasons,
            "modelGenerationAllowed": not reasons,
        }

    @staticmethod
    def assess_model_guidance(
        guidance: dict[str, Any],
        route: str,
        deterministic_result: dict[str, Any],
        market_allowed: bool,
        selected_concepts: list[str] | None = None,
    ) -> dict[str, Any]:
        title = str(guidance.get("title", ""))
        paragraphs = [str(item) for item in guidance.get("paragraphs", [])]
        rationale = str(guidance.get("rationale", ""))
        follow_up = str(guidance.get("followUp", ""))
        joined = " ".join([title, *paragraphs, rationale, follow_up]).lower()
        reasons: list[str] = []

        forbidden_patterns = (
            r"법률적(?:으로)?\s*(?:확정|유효)",
            r"세무(?:상)?\s*(?:적정|확정|문제없)",
            r"공식\s*인증(?:이)?\s*완료",
            r"탄소중립(?:을)?\s*(?:달성|확정)",
            r"거래(?:가)?\s*(?:안전|유효|확정)",
            r"결제(?:를)?\s*(?:완료|진행했)",
            r"등록부(?:를)?\s*(?:변경|이전했|소각했)",
            r"공식(?:적으로)?\s*(?:인정|승인|확정)(?:됐|되었|되었습니다|입니다)",
            r"(?:문서|증빙|인증서|등록증)(?:의)?\s*(?:진위|유효성|충분성)(?:을|이)?\s*(?:확인|검증)(?:했|됐|되었)",
            r"(?:구매|송금|계약|이전|소각)(?:을|를)?\s*(?:실행|완료)(?:했|됐|되었)",
        )
        if any(re.search(pattern, joined) for pattern in forbidden_patterns):
            reasons.append("PROHIBITED_AUTHORITY_OR_EXTERNAL_ACTION_CLAIM")

        urls = re.findall(r"(?:https?://|www\.)[^\s)]+", joined)
        if urls:
            allowed_market_urls = market_allowed and all("forestcarbonmarket.kr" in url for url in urls)
            if not allowed_market_urls:
                reasons.append("UNVERIFIED_EXTERNAL_LINK")
        if not market_allowed and ("forestcarbonmarket.kr" in joined or "산림탄소마켓으로 이동" in joined):
            reasons.append("UNAUTHORIZED_MARKET_HANDOFF")

        if re.search(r"(?:오늘|현재|실시간|최신)\s*(?:가격|시세)|(?:원|달러)\s*(?:입니다|이다)", joined):
            reasons.append("UNVERIFIED_LIVE_OR_PRICE_CLAIM")

        if route == "CONCEPT_EXPLANATION":
            anchor_groups = {
                "ESG": (("환경",), ("사회",), ("지배구조",)),
                "SUSTAINABLE_DEVELOPMENT_GOALS": (("지속가능",), ("목표",)),
                "KOFPI": (("한국임업진흥원",),),
                "KNOWLEDGE_ACTION_CHAIN": (("지식",), ("행동",)),
            }
            for concept in selected_concepts or []:
                groups = anchor_groups.get(str(concept), ())
                if groups and any(not any(term.lower() in joined for term in group) for group in groups):
                    reasons.append("SELECTED_CONCEPT_ANCHOR_NOT_PRESERVED")
                    break

        if route == "SCOPE_CLASSIFICATION":
            candidate = deterministic_result.get("data", {}).get("candidateScope")
            asserted_labels = {
                f"SCOPE_{match}"
                for match in re.findall(r"(?:scope|스코프)\s*([123])", joined, flags=re.IGNORECASE)
            }
            assertion_words = ("해당", "분류", "후보", "입니다", "이다", "볼 수")
            makes_scope_assertion = bool(asserted_labels) and any(word in joined for word in assertion_words)
            if candidate is None and makes_scope_assertion:
                reasons.append("SCOPE_ASSERTION_WITHOUT_VERIFIED_CANDIDATE")
            elif candidate and candidate not in asserted_labels:
                reasons.append("VERIFIED_SCOPE_CANDIDATE_NOT_PRESERVED")
            elif candidate and any(label != candidate for label in asserted_labels) and makes_scope_assertion:
                reasons.append("CONFLICTING_SCOPE_ASSERTION")

        if route == "FOREST_CARBON_PROCEDURE":
            procedure_data = deterministic_result.get("data", {})
            current = str(procedure_data.get("currentStage", "UNKNOWN"))
            if current not in {"CERTIFIED", "UTILIZATION", "REGISTRY_MANAGED"} and _contains_any(joined, ("거래 가능합니다", "거래할 수 있습니다", "공식 완료", "인증이 끝났")):
                reasons.append("PROCEDURE_COMPLETION_ASSERTION_BEYOND_VERIFIED_STAGE")
            next_stage = procedure_data.get("nextStage")
            stage_labels = {
                "PLANNING": "사업계획", "ELIGIBILITY": "적격성", "REGISTERED": "사업등록",
                "IMPLEMENTING": "사업 실행", "MONITORING": "모니터링", "VERIFIED": "검증",
                "CERTIFIED": "인증", "UTILIZATION": "활용", "REGISTRY_MANAGED": "등록부",
            }
            expected_label = stage_labels.get(str(next_stage)) if next_stage else None
            if expected_label and expected_label.lower() not in joined:
                reasons.append("VERIFIED_NEXT_PROCEDURE_STAGE_NOT_PRESERVED")

        if route == "FOREST_ESG_MAPPING":
            missing_axes = deterministic_result.get("data", {}).get("missingAxes", [])
            if missing_axes and _contains_any(joined, ("esg가 완성", "esg 우수", "세 축이 충족", "완전한 esg")):
                reasons.append("FOREST_ESG_COMPLETION_WITH_MISSING_AXES")
            if not missing_axes and not all(axis in joined for axis in ("환경", "사회", "지배구조")):
                reasons.append("VERIFIED_FOREST_ESG_AXES_NOT_PRESERVED")

        return {
            "decision": "ACCEPT_MODEL_GUIDANCE" if not reasons else "REJECT_MODEL_GUIDANCE",
            "route": route,
            "verifiedStatus": deterministic_result.get("status"),
            "reasonCodes": reasons,
            "accepted": not reasons,
            "residualRisk": "LOW" if not reasons else "MODEL_OUTPUT_REPLACED_BY_VERIFIED_FALLBACK",
        }


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)

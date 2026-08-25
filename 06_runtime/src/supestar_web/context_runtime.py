#!/usr/bin/env python3
"""Deterministic, provenance-carrying natural-language context extraction.

The extractor only promotes facts explicitly stated by the user.  Ambiguous or
conflicting statements stay UNKNOWN so the verified domain Skill can REVIEW
them instead of receiving an invented operational fact.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from conversation_policy import relevant_user_history


EVIDENCE_TERMS = (
    "고지서", "영수증", "청구서", "세금계산서", "계량기", "운행일지", "계약서",
    "동의서", "보고서", "등록증", "인증서", "검증서", "검증보고서", "승인서",
    "확인서", "증빙", "자료", "기록", "등록부",
)

ACTIVITY_TERMS = (
    "보일러", "차량", "발전기", "설비", "공정", "냉매", "연료", "도시가스",
    "경유", "휘발유", "전력", "전기", "스팀", "열", "냉방", "운송", "출장",
    "통근", "폐기물", "구매품", "원재료", "자본재", "판매제품", "제품 사용", "제품 폐기",
    "프랜차이즈", "투자 배출", "임차자산", "산림 사업", "산림탄소 사업",
)

POSITIVE_EVIDENCE_TERMS = ("보유", "있습니다", "있어요", "첨부", "확인 완료", "검토 완료", "승인 완료", "체결", "완료")
NEGATIVE_EVIDENCE_TERMS = ("없습니다", "없어요", "없음", "미보유", "누락", "미확인", "미완료", "확인하지 못")

SCOPE_1_SOURCE_TERMS = (
    "보일러", "차량", "발전기", "설비", "공정", "냉매", "연소", "소각로", "비상발전기",
)
UPSTREAM_VALUE_CHAIN_TERMS = (
    "외주 운송", "상류 운송", "구매한 제품", "구매품", "구매 원료", "원재료", "자본재",
    "임직원 출장", "직원 출장", "출장 항공", "직원 통근", "임직원 통근", "사업장 폐기물",
    "연료·에너지 관련 활동", "상류 임차자산", "상류 임차 자산",
)
DOWNSTREAM_VALUE_CHAIN_TERMS = (
    "하류 운송", "판매제품 사용", "판매한 제품 사용", "제품 폐기", "판매제품 폐기",
    "판매제품 가공", "하류 임차자산", "하류 임차 자산", "프랜차이즈", "투자 배출",
)


def _compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _has_any(text: str, terms: tuple[str, ...] | list[str]) -> bool:
    return any(term.lower() in text for term in terms)


def _sentences(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"[.!?\n]+", text) if item.strip()]


def _snippet(text: str, limit: int = 180) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    return normalized if len(normalized) <= limit else normalized[: limit - 1] + "…"


def _sentences_containing(text: str, term: str) -> list[str]:
    """Return only the user clauses that contain a term.

    Evidence polarity is intentionally local.  A negative statement about one
    document must not erase a positive statement about another document.
    """

    return [sentence for sentence in _sentences(text) if term in _compact(sentence)]


def _positive_term_mentions(text: str, terms: tuple[str, ...] | list[str]) -> list[str]:
    found: list[str] = []
    for term in terms:
        clauses = _sentences_containing(text, term)
        if clauses and any(not _has_any(_compact(clause), NEGATIVE_EVIDENCE_TERMS) for clause in clauses):
            found.append(term)
    return found


def _is_neutral(value: Any) -> bool:
    if value is None or value is False:
        return True
    if isinstance(value, str):
        return value.strip().upper() in {"", "UNKNOWN", "LEARNING"}
    if isinstance(value, (list, dict)):
        return not value
    return False


class ContextRuntime:
    """Extract typed domain input only from explicit user statements."""

    def enrich(
        self,
        base_payload: dict[str, Any],
        question: str,
        history: list[dict[str, str]],
        explicit_context: dict[str, Any] | None = None,
        allowed_explicit_fields: set[str] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        payload = deepcopy(base_payload)
        field_records: list[dict[str, Any]] = []
        conflicts: list[dict[str, Any]] = []

        # Every layer shares the same conservative continuity policy.  A short
        # question or a connective such as "그러면" is not enough by itself.
        context_messages = [
            item["content"] for item in relevant_user_history(question, history, limit=1)
        ]
        combined_original = " ".join([*context_messages, question]).strip()
        text = _compact(combined_original)
        current_text = _compact(question)
        source_name = "current_question_and_prior_user_context" if context_messages else "current_question"

        def record(field: str, value: Any, rule: str, evidence: str, confidence: str = "HIGH", source: str = source_name) -> None:
            field_records.append({
                "field": field,
                "value": value,
                "source": source,
                "evidenceSnippet": _snippet(evidence),
                "confidence": confidence,
                "rule": rule,
            })

        def set_if_neutral(field: str, value: Any, rule: str, evidence: str, confidence: str = "HIGH") -> None:
            if _is_neutral(payload.get(field)):
                payload[field] = value
                record(field, value, rule, evidence, confidence)

        # The user role changes only when the question is explicitly about the user's organization.
        organizational_voice = _has_any(text, ("우리 회사", "우리 조직", "당사", "우리 사업장", "회사에서", "기업에서"))
        if organizational_voice:
            payload["userRole"] = "ESG_MANAGER"
            record("userRole", "ESG_MANAGER", "EXPLICIT_ORGANIZATIONAL_VOICE", combined_original)

        self._extract_scope(payload, text, combined_original, set_if_neutral, record, conflicts)
        self._extract_market(payload, text, combined_original, set_if_neutral, record, conflicts)
        self._extract_forest_esg(payload, text, combined_original, set_if_neutral, record)
        self._extract_procedure(payload, text, combined_original, set_if_neutral, record, conflicts)
        self._extract_transaction(payload, text, combined_original, record)
        self._extract_measurement_context(payload, text, combined_original, record)

        if explicit_context and allowed_explicit_fields:
            for field in sorted(allowed_explicit_fields):
                if field not in explicit_context:
                    continue
                payload[field] = deepcopy(explicit_context[field])
                record(field, payload[field], "EXPLICIT_CONTEXT_OVERRIDE", f"context.{field}", "AUTHORITATIVE_USER_INPUT", "explicit_context")

        report = {
            "schemaVersion": "1.0",
            "executionState": "COMPLETED",
            "sourcePolicy": "Only current/prior user statements and explicit context may populate operational fields; assistant text is never a fact source.",
            "priorUserMessagesUsed": len(context_messages),
            "derivedFieldCount": sum(1 for item in field_records if item["source"] != "explicit_context"),
            "explicitFieldCount": sum(1 for item in field_records if item["source"] == "explicit_context"),
            "fields": field_records,
            "conflicts": conflicts,
            "hasConflicts": bool(conflicts),
            "unresolvedPolicy": "Fields without explicit, unambiguous support remain empty or UNKNOWN and must be handled by REVIEW.",
            "currentQuestionOnlyForRouting": current_text == _compact(question),
        }
        payload["contextExtraction"] = report
        return payload, report

    @staticmethod
    def _extract_scope(payload: dict[str, Any], text: str, original: str, set_field: Any, record: Any, conflicts: list[dict[str, Any]]) -> None:
        scope_intent = _has_any(text, ("scope", "스코프", "배출원")) and _has_any(text, ("어느", "몇", "분류", "해당", "구분"))
        if not scope_intent:
            return

        activity_present = _has_any(text, ACTIVITY_TERMS)
        if activity_present:
            set_field("activityDescription", _snippet(original, 800), "EXPLICIT_ACTIVITY_DESCRIPTION", original)

        ownership_negative = _has_any(
            text,
            (
                "회사 소유가 아니", "우리 회사 소유가 아니", "당사 소유가 아니", "소유하지 않",
                "통제하지 않", "소유·통제하지 않", "소유하거나 통제하지 않", "비소유", "외부 소유",
            ),
        )
        owned_source = (
            not ownership_negative
            and _has_any(
                text,
                (
                    "회사 소유", "우리 회사가 소유", "저희 회사가 소유", "당사가 소유",
                    "소유·운영", "소유 및 운영", "직접 운영·통제", "직접 운영하고 통제",
                    "직영", "자가 보유", "운영통제권 보유",
                ),
            )
            and _has_any(text, SCOPE_1_SOURCE_TERMS)
        )
        external_source = ownership_negative or _has_any(
            text,
            ("협력사가 소유", "협력사가 운영", "외주사가 소유", "외주사가 운영", "공급사가 소유", "제3자가 소유"),
        )
        purchased_energy: str | None = None
        if _has_any(text, ("구매 전력", "구매전력", "한전 구매전력", "구매한 전기", "한전 전력", "전기요금", "전력 구매")):
            purchased_energy = "ELECTRICITY"
        elif _has_any(text, ("구매 스팀", "구매한 스팀", "스팀 구매")):
            purchased_energy = "STEAM"
        elif _has_any(text, ("구매 열", "구매한 열", "열 구매")):
            purchased_energy = "HEAT"
        elif _has_any(text, ("구매 냉방", "구매한 냉방", "냉방 구매")):
            purchased_energy = "COOLING"

        upstream = _has_any(text, UPSTREAM_VALUE_CHAIN_TERMS)
        downstream = _has_any(text, DOWNSTREAM_VALUE_CHAIN_TERMS)
        candidate_axes = [name for name, present in (("SCOPE_1", owned_source), ("SCOPE_2", purchased_energy is not None), ("SCOPE_3_UPSTREAM", upstream), ("SCOPE_3_DOWNSTREAM", downstream)) if present]
        if len(candidate_axes) > 1 or (owned_source and external_source) or (upstream and downstream):
            conflict = {
                "domain": "SCOPE_CLASSIFICATION",
                "fields": ["sourceOwnershipOrControl", "purchasedEnergyType", "valueChainRelation"],
                "reason": "The user statement contains more than one incompatible Scope relationship.",
                "evidenceSnippet": _snippet(original),
                "candidateAxes": candidate_axes,
            }
            conflicts.append(conflict)
            record("scopeRelationshipConflict", candidate_axes, "CONFLICTING_SCOPE_RELATIONSHIPS", original, "CONFLICT")
        else:
            if owned_source:
                set_field("sourceOwnershipOrControl", "OWNED_CONTROLLED", "EXPLICIT_OWNED_CONTROLLED_SOURCE", original)
                set_field("purchasedEnergyType", "NONE", "DIRECT_SOURCE_NOT_PURCHASED_ENERGY", original)
                set_field("valueChainRelation", "NONE", "DIRECT_SOURCE_NOT_VALUE_CHAIN", original)
            elif purchased_energy:
                set_field("sourceOwnershipOrControl", "NOT_OWNED_CONTROLLED", "PURCHASED_ENERGY_SOURCE_OUTSIDE_CONTROL", original)
                set_field("purchasedEnergyType", purchased_energy, "EXPLICIT_PURCHASED_ENERGY", original)
                set_field("valueChainRelation", "NONE", "PURCHASED_ENERGY_NOT_SCOPE3_FOR_THIS_ACTIVITY", original)
            elif upstream or downstream:
                set_field("sourceOwnershipOrControl", "NOT_OWNED_CONTROLLED", "EXPLICIT_EXTERNAL_VALUE_CHAIN_SOURCE", original)
                set_field("purchasedEnergyType", "NONE", "VALUE_CHAIN_ACTIVITY_NOT_PURCHASED_ENERGY", original)
                set_field("valueChainRelation", "UPSTREAM" if upstream else "DOWNSTREAM", "EXPLICIT_VALUE_CHAIN_RELATION", original)
            elif external_source:
                set_field("sourceOwnershipOrControl", "NOT_OWNED_CONTROLLED", "EXPLICIT_EXTERNAL_SOURCE", original)

        if activity_present and _has_any(
            text,
            ("우리 회사", "저희 회사", "우리 조직", "당사", "사업장", "협력사", "외주", "임직원", "직원", "판매제품", "프랜차이즈", "투자 배출"),
        ):
            set_field("organizationBoundary", _snippet(original, 500), "EXPLICIT_ORGANIZATIONAL_BOUNDARY_STATEMENT", original)

        quantity_match = re.search(r"(?P<quantity>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>nm[³3]|kwh|mwh|tco2e|kgco2e|kg|km|l|ℓ|리터|톤)", text, re.IGNORECASE)
        if quantity_match:
            raw_quantity = quantity_match.group("quantity").replace(",", "")
            quantity: int | float = float(raw_quantity) if "." in raw_quantity else int(raw_quantity)
            data: dict[str, Any] = {"quantity": quantity, "unit": quantity_match.group("unit")}
            period_match = re.search(r"(20\d{2})\s*년?\s*(1[0-2]|0?[1-9])\s*월", text)
            if period_match:
                data["period"] = f"{period_match.group(1)}-{int(period_match.group(2)):02d}"
            set_field("activityData", data, "EXPLICIT_QUANTITY_UNIT", quantity_match.group(0))

        evidence = _positive_term_mentions(original, EVIDENCE_TERMS)
        if evidence:
            existing = payload.get("providedEvidence", [])
            payload["providedEvidence"] = list(dict.fromkeys([*existing, *[f"[USER_STATED] {term} 보유·존재 진술" for term in evidence]]))
            record("providedEvidence", payload["providedEvidence"], "USER_STATED_EVIDENCE_MENTION", original)

    @staticmethod
    def _extract_market(payload: dict[str, Any], text: str, original: str, set_field: Any, record: Any, conflicts: list[dict[str, Any]]) -> None:
        if not _has_any(text, ("ccm", "vcm", "배출권", "탄소크레딧", "크레딧", "탄소시장", "상쇄")):
            return
        if _has_any(text, ("공시", "홍보", "외부 주장", "탄소중립 주장", "탄소중립이라고", "사용해도", "써도 되")):
            payload["purpose"] = "CLAIM_REVIEW"
            record("purpose", "CLAIM_REVIEW", "EXPLICIT_EXTERNAL_CLAIM_INTENT", original)
        elif _has_any(text, ("규제 의무", "의무 이행", "배출권 제출", "k-ets", "할당 의무")):
            payload["purpose"] = "REGULATORY_COMPLIANCE"
            record("purpose", "REGULATORY_COMPLIANCE", "EXPLICIT_REGULATORY_INTENT", original)
        elif _has_any(text, ("자발적 목표", "자발적 감축 목표")):
            payload["purpose"] = "VOLUNTARY_TARGET"
            record("purpose", "VOLUNTARY_TARGET", "EXPLICIT_VOLUNTARY_TARGET", original)
        elif _has_any(text, ("기후 기여", "감축 기여", "기여 주장")):
            payload["purpose"] = "CONTRIBUTION"
            record("purpose", "CONTRIBUTION", "EXPLICIT_CONTRIBUTION_INTENT", original)

        if "배출권" in text:
            set_field("unitType", "EMISSION_ALLOWANCE", "EXPLICIT_UNIT_TYPE", "배출권")
        elif _has_any(text, ("산림탄소크레딧", "산림 탄소크레딧")):
            set_field("unitType", "FOREST_CARBON_CREDIT", "EXPLICIT_UNIT_TYPE", "산림탄소크레딧")
        elif "크레딧" in text:
            set_field("unitType", "CARBON_CREDIT", "EXPLICIT_UNIT_TYPE", "크레딧")

        registry_signals: list[tuple[str, str]] = []
        registry_patterns = (
            ("RETIRED", ("소각 완료", "사용 완료", "사용완료")),
            ("TRANSFERRED", ("등록부 이전 완료", "이전 완료")),
            ("REGISTERED", ("등록부에 등록", "등록 완료", "발행 완료")),
            ("UNVERIFIED", ("미등록", "등록되지 않", "등록상태 미확인", "등록 상태 미확인", "등록 상태를 모름", "소각 여부 미확인", "소각 여부는 미확인", "소각 여부가 미확인")),
        )
        for state, patterns in registry_patterns:
            matched = next((pattern for pattern in patterns if pattern in text), None)
            if matched:
                registry_signals.append((state, matched))
        unique_states = {state for state, _ in registry_signals}
        # REGISTERED → TRANSFERRED → RETIRED may be a valid lifecycle sequence.
        # An explicit UNVERIFIED statement alongside a claimed state is the
        # unresolved conflict that must block operational use.
        if "UNVERIFIED" in unique_states and len(unique_states) > 1:
            conflicts.append({
                "domain": "CARBON_MARKET_COMPARISON",
                "fields": ["registryStatus"],
                "reason": "The user statement contains incompatible or unresolved registry-state claims.",
                "evidenceSnippet": _snippet(original),
                "candidateStates": sorted(unique_states),
            })
            payload["registryStatus"] = "UNVERIFIED"
            record("registryStatus", "UNVERIFIED", "CONFLICTING_REGISTRY_STATES", original, "CONFLICT")
        elif registry_signals:
            registry = registry_signals[0][0]
            payload["registryStatus"] = registry
            record("registryStatus", registry, "EXPLICIT_REGISTRY_STATE", registry_signals[0][1])
        if _has_any(text, ("동시에 사용", "이중사용", "이중 사용", "두 번 사용", "중복 사용")):
            payload["doubleUse"] = True
            record("doubleUse", True, "EXPLICIT_DOUBLE_USE_INTENT", original)

    @staticmethod
    def _extract_forest_esg(payload: dict[str, Any], text: str, original: str, set_field: Any, record: Any) -> None:
        forest_esg = _has_any(text, ("산림 esg", "산림esg", "e/s/g", "환경·사회·지배구조"))
        if not forest_esg:
            return
        operational = _has_any(text, ("사업", "프로젝트")) and not (_has_any(text, ("무엇", "뜻", "정의")) and not _has_any(text, EVIDENCE_TERMS))
        if operational:
            set_field("projectSummary", _snippet(original, 1000), "EXPLICIT_FOREST_PROJECT_SUMMARY", original)

        evidence_required = _has_any(text, POSITIVE_EVIDENCE_TERMS) or _has_any(text, EVIDENCE_TERMS)
        if evidence_required:
            axis_rules = {
                "environmentEvidence": ("흡수량", "모니터링 보고서", "생태조사", "방법론", "추가성", "영속성", "누출"),
                "socialEvidence": ("산주 동의", "지역사회", "편익배분", "토지 권리", "주민 참여", "임업인"),
                "governanceEvidence": ("사업등록증", "등록증", "검증보고서", "인증서", "등록부", "감사", "계약서"),
            }
            for field, terms in axis_rules.items():
                found = _positive_term_mentions(original, terms)
                if found:
                    payload[field] = [f"[USER_STATED] {term}" for term in found]
                    record(field, payload[field], "EXPLICIT_FOREST_ESG_AXIS_EVIDENCE", original)
        if _has_any(text, ("권리는 무시", "지역사회는 제외", "흡수량만으로 esg", "흡수량만 보면 esg")):
            payload["claimCompleteWithoutAllAxes"] = True
            record("claimCompleteWithoutAllAxes", True, "PROHIBITED_INCOMPLETE_ESG_CLAIM", original)

    @staticmethod
    def _extract_procedure(payload: dict[str, Any], text: str, original: str, set_field: Any, record: Any, conflicts: list[dict[str, Any]]) -> None:
        procedure_intent = _has_any(text, ("산림탄소", "산림 탄소")) and _has_any(text, ("절차", "단계", "사업등록", "모니터링", "검증", "인증"))
        if not procedure_intent:
            return
        project_types = (
            "산림경영형", "신규조림", "재조림", "식생복구", "목제품 이용", "산림바이오매스",
        )
        for project_type in project_types:
            if project_type in text:
                set_field("projectType", project_type, "EXPLICIT_PROJECT_TYPE", project_type)
                break

        stage_patterns = (
            ("REGISTRY_MANAGED", ("등록부 상태관리 완료", "등록부 이전 완료", "등록부 관리 단계")),
            ("CERTIFIED", ("인증 완료", "인증서를 보유", "인증 단계")),
            ("VERIFIED", ("독립 검증 완료", "검증 완료", "검증보고서를 보유")),
            ("MONITORING", ("모니터링 완료", "모니터링 중", "모니터링 단계")),
            ("IMPLEMENTING", ("사업 실행 중", "사업 이행 중", "실행 단계")),
            ("REGISTERED", ("사업등록 완료", "등록증을 보유", "등록 단계")),
            ("ELIGIBILITY", ("적격성 검토 완료", "타당성 검토 단계", "적격성 단계")),
            ("PLANNING", ("사업계획 단계", "사업계획을 작성", "계획 단계")),
        )
        stage_signals: list[tuple[str, str]] = []
        for stage, patterns in stage_patterns:
            matched = next((pattern for pattern in patterns if pattern in text), None)
            if matched:
                stage_signals.append((stage, matched))
        if len({stage for stage, _ in stage_signals}) > 1:
            conflicts.append({
                "domain": "FOREST_CARBON_PROCEDURE",
                "fields": ["currentStage"],
                "reason": "The user statement names more than one current official stage.",
                "evidenceSnippet": _snippet(original),
                "candidateStages": [stage for stage, _ in stage_signals],
            })
            payload["currentStage"] = "UNKNOWN"
            record("currentStage", "UNKNOWN", "CONFLICTING_CURRENT_STAGES", original, "CONFLICT")
        elif stage_signals:
            stage, matched = stage_signals[0]
            payload["currentStage"] = stage
            record("currentStage", stage, "EXPLICIT_CURRENT_STAGE", matched)

        documents: list[str] = []
        for term in _positive_term_mentions(original, EVIDENCE_TERMS):
            documents.append(f"[USER_STATED] {term}")
        if documents:
            payload["availableDocuments"] = list(dict.fromkeys(documents))
            record("availableDocuments", payload["availableDocuments"], "USER_STATED_PROCEDURE_DOCUMENT", original)

        if _has_any(text, ("거래 목적", "판매 목적", "구매 목적", "거래하려")):
            payload["intendedUse"] = "TRADING"
            record("intendedUse", "TRADING", "EXPLICIT_TRADING_USE", original)
        elif _has_any(text, ("비거래 활용", "기여 목적")):
            payload["intendedUse"] = "NON_TRADING"
            record("intendedUse", "NON_TRADING", "EXPLICIT_NON_TRADING_USE", original)

        skip_assertion = _has_any(text, ("검증 없이", "인증 없이", "등록 없이", "바로 거래 가능", "공식 완료로 확정", "거래 가능하다고 확정"))
        if skip_assertion:
            payload["requestedFinalAssertion"] = True
            record("requestedFinalAssertion", True, "EXPLICIT_PRECONDITION_SKIPPING_ASSERTION", original)

    @staticmethod
    def _extract_transaction(payload: dict[str, Any], text: str, original: str, record: Any) -> None:
        if not _has_any(text, ("거래 준비", "거래준비", "결제 전", "증빙팩", "거래 게이트")):
            return
        gate_terms = {
            "G1": ("판매자·구매자 신원", "판매자와 구매자 신원", "대리권", "주체·신원"),
            "G2": ("사업·수량·빈티지", "사업과 수량과 빈티지", "단위 상태", "크레딧 상태"),
            "G3": ("토지·사업권", "토지권", "사업권"),
            "G4": ("처분권", "판매 권한"),
            "G5": ("인증 유효상태", "검증·인증", "적격성·인증"),
            "G6": ("구매목적", "구매 목적", "사용 목적"),
            "G7": ("계약 체결", "계약서", "거래 계약"),
            "G8": ("세무 검토", "세무분류", "세무 검토기록"),
            "G9": ("결제·정산", "결제와 정산", "정산 구조"),
            "G10": ("등록부 이전", "소각 절차", "사용완료"),
            "G11": ("외부 주장 승인", "증빙팩 승인", "감사 승인"),
        }
        gates = deepcopy(payload.get("gates", {}))
        for sentence in _sentences(original):
            normalized = _compact(sentence)
            for gate, subjects in gate_terms.items():
                if not _has_any(normalized, subjects):
                    continue
                if _has_any(normalized, NEGATIVE_EVIDENCE_TERMS):
                    gates[gate] = {"state": "MISSING", "reason": _snippet(sentence)}
                    record(f"gates.{gate}", gates[gate], "EXPLICIT_GATE_MISSING", sentence)
                elif _has_any(normalized, POSITIVE_EVIDENCE_TERMS):
                    gates[gate] = {"state": "PRESENT", "reason": _snippet(sentence)}
                    record(f"gates.{gate}", gates[gate], "EXPLICIT_GATE_PRESENT", sentence)
        payload["gates"] = gates

    @staticmethod
    def _extract_measurement_context(payload: dict[str, Any], text: str, original: str, record: Any) -> None:
        if payload.get("userRole") == "LEARNER":
            return
        has_boundary = bool(payload.get("organizationBoundary")) or _has_any(text, ("조직경계", "운영경계"))
        has_activity = bool(payload.get("activityData"))
        has_reduction = _has_any(text, ("직접 감축", "감축 계획", "감축 실적"))
        if has_boundary and has_activity:
            context = {
                "organizationBoundaryProvided": has_boundary,
                "activityDataProvided": has_activity,
                "directReductionContextProvided": has_reduction,
                "source": "USER_STATED",
            }
            payload["measurementContext"] = context
            record("measurementContext", context, "MINIMUM_MEASUREMENT_CONTEXT", original)

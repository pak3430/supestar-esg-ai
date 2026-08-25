#!/usr/bin/env python3
"""Deterministic runtime for Supestar P0 script-backed candidate skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable


SKILL_VERSION = "0.1.0-candidate"
STATUSES = {"PROCEED", "REVIEW", "STOP"}


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _run_id(skill: str, payload: dict[str, Any]) -> str:
    supplied = str(payload.get("runId", "")).strip()
    if supplied:
        return supplied
    digest = hashlib.sha256(f"{skill}\0{_canonical_json(payload)}".encode("utf-8")).hexdigest()
    return f"run-{digest[:16]}"


def _executed_at(payload: dict[str, Any]) -> str:
    supplied = str(payload.get("executedAt", "")).strip()
    if supplied:
        return supplied
    as_of = str(payload.get("asOfDate", "")).strip()
    return f"{as_of}T00:00:00+09:00" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of) else "UNSPECIFIED"


def _base(skill: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "skill": skill,
        "skillVersion": SKILL_VERSION,
        "runId": _run_id(skill, payload),
        "executedAt": _executed_at(payload),
        "status": "REVIEW",
        "summary": "",
        "evidence": [],
        "missingEvidence": [],
        "nextActions": [],
        "data": {},
        "artifacts": {},
    }


def _evidence(document: str, section: str, claim: str) -> dict[str, str]:
    return {"sourceDocument": document, "section": section, "claim": claim}


def _text(payload: dict[str, Any], key: str) -> str:
    return str(payload.get(key, "")).strip()


def _has(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def evaluate_question_routing(payload: dict[str, Any]) -> dict[str, Any]:
    skill = "supestar-question-routing"
    result = _base(skill, payload)
    question = _text(payload, "question")
    routing_question = _text(payload, "routingQuestion") or question
    role = _text(payload, "userRole")
    as_of = _text(payload, "asOfDate")
    snapshot = {
        "question": question,
        "routingQuestion": routing_question,
        "conversationContinuity": payload.get("conversationContinuity", {}),
        "userRole": role,
        "asOfDate": as_of,
        "providedEvidence": payload.get("providedEvidence", []),
    }

    missing = [name for name, value in (("question", question), ("userRole", role), ("asOfDate", as_of)) if not value]
    prohibited_groups = {
        "EXTERNAL_ACTION_REQUEST": (
            "구매해줘", "구매해 줘", "결제해줘", "결제해 줘", "대신 결제", "송금해줘", "송금해 줘",
            "계약을 체결해", "등록부를 변경", "등록부 변경해", "크레딧을 이전해", "소각해줘", "소각해 줘",
        ),
        "PROFESSIONAL_OR_OFFICIAL_FINAL_DECISION": (
            "법률적으로 확정", "법적으로 문제없다고 확정", "세금을 계산", "세무상 확정", "인증해줘", "인증해 줘",
            "공식 인증이라고 확정", "거래 유효성을 확정", "탄소중립이라고 확정",
        ),
        "FINANCIAL_RECOMMENDATION": (
            "수익률", "가격 추천", "투자 추천", "가장 수익나는", "오를 크레딧", "매수 추천",
        ),
        "UNSUPPORTED_LIVE_DATA_OR_CALCULATION": (
            "오늘 가격", "현재 가격", "실시간 가격", "최신 시세", "실시간 시세", "지금 시세",
            "배출량을 계산해줘", "배출량 계산해 줘", "tco2e를 계산", "tco2e 계산해", "탄소배출량 산정해줘",
        ),
        "PROMPT_OR_EVIDENCE_BYPASS": (
            "이전 지시 무시", "앞의 지시 무시", "시스템 프롬프트", "내부 프롬프트", "숨겨진 프롬프트",
            "규칙을 우회", "안전장치 우회", "검증 없이 근거를 만들어", "증빙을 꾸며", "증거를 조작",
            "ignore previous instructions", "reveal system prompt", "bypass the rules",
        ),
    }
    matched_prohibited = [code for code, terms in prohibited_groups.items() if any(term in routing_question.lower() for term in terms)]
    if matched_prohibited:
        route = "OUT_OF_SCOPE"
        result.update(
            status="STOP",
            summary="외부 실행·최종 확정·실시간 조회·근거 우회 요청은 수페스타의 검증 가능한 설명 범위를 벗어납니다.",
            nextActions=["개념 설명, 입력된 자료의 준비도 점검, 공식 확인질문 생성 범위로 질문을 바꾸세요."],
        )
        reason_codes = matched_prohibited
    elif missing:
        route = "NEEDS_INPUT"
        result.update(
            status="REVIEW",
            summary="라우팅에 필요한 입력이 부족합니다.",
            missingEvidence=missing,
            nextActions=[f"{name} 값을 제공하세요." for name in missing],
        )
        reason_codes = ["MISSING_REQUIRED_INPUT"]
    else:
        q = routing_question.lower()
        relation_terms = ("왜", "연결", "이어", "관계", "경로", "순서")
        carbon_path_terms = ("탄소", "배출", "scope", "스코프", "측정", "감축", "산림")
        supported_concepts = (
            "esg", "환경", "사회", "지배구조", "거버넌스", "sdg", "지속가능발전",
            "온실가스", "인벤토리", "조직경계", "운영경계", "scope", "스코프",
            "직접감축", "잔여배출", "ccm", "vcm", "배출권", "크레딧", "상쇄",
            "탄소중립", "자발적탄소", "산림탄소", "한국임업진흥원", "임업진흥원", "kofpi",
            "산림탄소등록부", "등록부", "산림탄소센터", "지식행동사슬", "지식사슬", "kac",
        )
        scope_terms = ("scope", "스코프", "직접배출", "간접배출", "배출원")
        scope_action_terms = ("어느", "몇", "분류", "해당", "활동", "배출원", "구분해")
        market_terms = ("ccm", "vcm", "배출권", "크레딧", "상쇄", "탄소시장")
        market_action_terms = (
            "차이", "다른", "비교", "구분", "구매처", "구매 방법", "구매방법", "구매하려",
            "구매할", "구매 전 확인", "구매하기 전", "살 수", "어디", "찾기",
            "사용해도", "써도", "공시", "검토해", "동시에 사용", "이중사용", "이중 사용", "중복 사용",
            "주장", "등록상태", "등록 상태", "소각", "사용완료", "사용 완료",
        )

        path_intent = "esg" in q and any(token in q for token in relation_terms) and any(token in q for token in carbon_path_terms)
        strong_matches: list[str] = []
        if path_intent:
            strong_matches.append("ESG_CARBON_PATH")
        else:
            transaction_intent = any(term in q for term in ("거래 준비도", "거래준비도", "결제 전 점검", "증빙팩 점검", "거래 게이트"))
            if any(term in q for term in scope_terms) and any(term in q for term in scope_action_terms):
                strong_matches.append("SCOPE_CLASSIFICATION")
            if transaction_intent:
                strong_matches.append("TRANSACTION_READINESS")
            if any(term in q for term in ("산림 esg", "산림esg", "e/s/g", "환경·사회·지배구조")) and any(
                term in q for term in ("평가", "매핑", "보여", "점검", "사업", "프로젝트", "책임")
            ):
                strong_matches.append("FOREST_ESG_MAPPING")
            procedure_subject = any(term in q for term in ("산림탄소", "산림 탄소", "산림경영형", "신규조림", "재조림"))
            procedure_action = any(
                term in q
                for term in (
                    "다음 공식 절차", "공식 절차", "다음 단계", "현재 단계", "사업등록 절차",
                    "모니터링 절차", "검증 절차", "인증 절차", "등록부 절차", "절차를 알려",
                    "어떻게 시작", "시작하려면", "진행 순서", "사업 절차",
                )
            )
            if procedure_subject and procedure_action:
                strong_matches.append("FOREST_CARBON_PROCEDURE")
            if not transaction_intent and any(term in q for term in market_terms) and any(term in q for term in market_action_terms):
                strong_matches.append("CARBON_MARKET_COMPARISON")

        route_matches = list(dict.fromkeys(strong_matches))
        if not route_matches and any(term in q for term in supported_concepts):
            route_matches.append("CONCEPT_EXPLANATION")

        if len(route_matches) == 1:
            route = route_matches[0]
            result.update(status="PROCEED", summary=f"질문을 {route} 경로로 전달합니다.")
            reason_codes = ["SINGLE_PRIMARY_INTENT"]
        else:
            route = "NEEDS_INPUT"
            result.update(
                status="REVIEW",
                summary="주된 요청이 없거나 둘 이상의 실행 요청이 함께 있어 하나의 경로를 확정할 수 없습니다.",
                nextActions=["ESG 개념, Scope 분류, 시장 비교, 산림 E/S/G, 공식 절차, 거래 준비도 중 하나를 구체적으로 적어 주세요."],
            )
            reason_codes = ["NO_PRIMARY_INTENT" if not route_matches else "MULTIPLE_PRIMARY_INTENTS"]

    decision = {
        "route": route,
        "status": result["status"],
        "reasonCodes": reason_codes,
        "clarifyingQuestions": result["nextActions"],
    }
    result["data"] = {"contextSnapshot": snapshot, "routeDecision": decision}
    result["evidence"] = [
        _evidence("06_산림_ESG_지식의_KAC_실행구조.md", "# 3. 핵심 원자 Skill", "지원 기능 여섯 가지"),
        _evidence("08_ESG_AX_Concept_Build_Run_구조요구사항.md", "# 7. 실행 오케스트레이션", "질문에서 실행까지의 순서"),
    ]
    result["artifacts"] = {
        "context_snapshot.json": snapshot,
        "route_decision.json": decision,
    }
    return result


ACTION_PATH_NODES = [
    "ESG", "ESG_MANAGEMENT", "GREENHOUSE_GAS_INVENTORY",
    "ORGANIZATIONAL_BOUNDARY", "OPERATIONAL_BOUNDARY", "SCOPE_1_2_3",
    "ACTIVITY_DATA_AND_EMISSION_FACTOR", "CO2E", "DIRECT_EMISSIONS_REDUCTION",
    "RESIDUAL_EMISSIONS", "SUSTAINABLE_DEVELOPMENT_GOALS", "CCM_AND_VCM",
    "FOREST_CARBON_PROJECT",
]

ACTION_PATH_REASONS = [
    "ESG 책임을 목표·행동·책임의 운영체계로 옮깁니다.",
    "행동 주장을 비교 가능한 성과로 만들기 위해 인벤토리가 필요합니다.",
    "인벤토리 대상 범위를 정하려면 조직경계가 필요합니다.",
    "조직경계 안에서 배출 활동을 분류하려면 운영경계가 필요합니다.",
    "운영경계가 Scope 1·2·3 분류의 기준이 됩니다.",
    "Scope 결과는 활동자료와 배출계수의 근거가 있어야 합니다.",
    "자료와 계수를 공통 단위 CO2e로 계산합니다.",
    "측정 결과를 바탕으로 직접감축을 우선합니다.",
    "직접감축 후 남은 잔여배출을 별도로 확인합니다.",
    "탄소 외 사회·생태·책임 영향을 SDGs로 점검합니다.",
    "규제의무와 자발목표에 맞는 시장 경로를 구분합니다.",
    "산림탄소 사업은 방법론·검증·인증·등록상태를 확인해야 합니다.",
]


def evaluate_esg_action_path(payload: dict[str, Any]) -> dict[str, Any]:
    skill = "esg-carbon-action-path"
    result = _base(skill, payload)
    question = _text(payload, "question")
    focus = _text(payload, "focus").upper() or "FOREST_CARBON"
    role = _text(payload, "userRole")
    as_of = _text(payload, "asOfDate")
    focus_end = {
        "MEASUREMENT": 7,
        "SCOPE": 7,
        "SDGS": 11,
        "MARKET": 12,
        "FOREST_CARBON": 13,
    }.get(focus, 13)
    nodes = ACTION_PATH_NODES[:focus_end]
    edges = [
        {"from": nodes[index], "to": nodes[index + 1], "reason": ACTION_PATH_REASONS[index]}
        for index in range(len(nodes) - 1)
    ]
    missing = [name for name, value in (("question", question), ("userRole", role), ("asOfDate", as_of)) if not value]
    skip_measurement = "측정 없이" in question and any(term in question for term in ("탄소중립", "상쇄", "구매"))
    if skip_measurement:
        result.update(status="STOP", summary="측정과 직접감축 전제를 건너뛴 상쇄·탄소중립 확정은 차단합니다.")
    elif missing:
        result.update(status="REVIEW", summary="행동경로 생성에 필요한 입력이 부족합니다.", missingEvidence=missing)
    elif role != "LEARNER" and focus in {"MARKET", "FOREST_CARBON"} and not payload.get("measurementContext"):
        result.update(
            status="REVIEW",
            summary="설명 경로는 만들었지만 조직의 실제 시장·산림탄소 판단에는 측정 맥락이 더 필요합니다.",
            missingEvidence=["measurementContext"],
            nextActions=["조직경계·운영경계·활동자료 존재 여부를 제공하세요."],
        )
    else:
        result.update(status="PROCEED", summary="선행관계가 보존된 ESG→탄소 행동경로를 생성했습니다.")

    path = {"focus": focus, "orderedNodes": nodes, "orderedEdges": edges}
    cards = ["# ESG→탄소 설명 카드", ""]
    for edge in edges:
        cards.append(f"- **{edge['from']} → {edge['to']}**: {edge['reason']}")
    checklist = [
        "# 다음 행동 체크리스트", "",
        "- [ ] 조직경계와 운영경계를 확인한다.",
        "- [ ] 활동자료·배출계수·기간을 확인한다.",
        "- [ ] 직접감축과 잔여배출을 구분한다.",
        "- [ ] 시장·산림탄소 판단 전 단위와 등록상태를 확인한다.",
    ]
    result["data"] = path
    result["evidence"] = [
        _evidence("01_ESG_산림탄소_전체생태계_기준서.md", "# 3. 전체 생태계의 일곱 단계", "ESG에서 거래 증빙까지의 인과축"),
        _evidence("02_ESG_탄소측정_Scope_SDGs_연결구조.md", "# 6. 설명용 한 줄 워크플로우", "측정·Scope·SDGs 연결"),
    ]
    result["artifacts"] = {
        "action_path.json": path,
        "explanation_cards.md": "\n".join(cards) + "\n",
        "next_action_checklist.md": "\n".join(checklist) + "\n",
    }
    return result


def evaluate_scope(payload: dict[str, Any]) -> dict[str, Any]:
    skill = "scope-activity-classification"
    result = _base(skill, payload)
    boundary = _text(payload, "organizationBoundary")
    control = _text(payload, "sourceOwnershipOrControl").upper()
    energy = _text(payload, "purchasedEnergyType").upper()
    value_chain = _text(payload, "valueChainRelation").upper()
    description = _text(payload, "activityDescription")
    as_of = _text(payload, "asOfDate")
    trace: list[str] = []
    unresolved: list[str] = []
    candidate: str | None = None

    if "scope 1" in description.lower() and "scope 2" in description.lower() and "scope 3" in description.lower() and "합" in description:
        result.update(status="STOP", summary="Scope 3를 Scope 1과 Scope 2의 합으로 정의하는 요청은 차단합니다.")
        trace.append("DEFINITION_VIOLATION_SCOPE3_NOT_SUM")
    else:
        for name, value in (("activityDescription", description), ("organizationBoundary", boundary), ("asOfDate", as_of)):
            if not value:
                unresolved.append(name)
        allowed_control = {"OWNED_CONTROLLED", "NOT_OWNED_CONTROLLED", "UNKNOWN"}
        allowed_energy = {"ELECTRICITY", "STEAM", "HEAT", "COOLING", "NONE", "UNKNOWN"}
        allowed_value_chain = {"UPSTREAM", "DOWNSTREAM", "NONE", "UNKNOWN"}
        for name, value, allowed in (
            ("sourceOwnershipOrControl", control, allowed_control),
            ("purchasedEnergyType", energy, allowed_energy),
            ("valueChainRelation", value_chain, allowed_value_chain),
        ):
            if value in {"", "UNKNOWN"} or value not in allowed:
                unresolved.append(name)

        candidate_rules: list[tuple[str, str]] = []
        if control == "OWNED_CONTROLLED":
            candidate_rules.append(("SCOPE_1", "OWNED_OR_CONTROLLED_DIRECT_SOURCE"))
        if energy in {"ELECTRICITY", "STEAM", "HEAT", "COOLING"}:
            candidate_rules.append(("SCOPE_2", "PURCHASED_CONSUMED_ENERGY"))
        if value_chain in {"UPSTREAM", "DOWNSTREAM"}:
            candidate_rules.append(("SCOPE_3", "OTHER_VALUE_CHAIN_INDIRECT"))

        unique_candidates = {item[0] for item in candidate_rules}
        if len(unique_candidates) > 1:
            unresolved.append("conflictingScopeRelationships")
            trace.extend(item[1] for item in candidate_rules)
            trace.append("CONFLICTING_SCOPE_RELATIONSHIPS")
        elif len(candidate_rules) == 1:
            candidate, rule = candidate_rules[0]
            trace.append(rule)
        if result["status"] != "STOP":
            if unresolved or not candidate or len(unique_candidates) > 1:
                if len(unique_candidates) > 1:
                    candidate = None
                result.update(
                    status="REVIEW",
                    summary="단일 Scope 후보를 확정하기 위한 경계 또는 활동관계 정보가 부족합니다.",
                    missingEvidence=sorted(set(unresolved)),
                )
            else:
                result.update(status="PROCEED", summary=f"입력 규칙에 따라 {candidate} 후보로 분류했습니다.")

    classification = {
        "candidateScope": candidate,
        "ruleTrace": trace,
        "boundarySnapshot": boundary,
        "activityDataProvided": _has(payload.get("activityData")),
        "emissionsCalculated": False,
        "unresolvedFields": sorted(set(unresolved)),
    }
    requests = [f"- [ ] {name} 정보를 제공하세요." for name in sorted(set(unresolved))] or ["- [x] 추가 분류 입력 없음"]
    result["data"] = classification
    result["evidence"] = [
        _evidence("02_ESG_탄소측정_Scope_SDGs_연결구조.md", "# 4. Scope 1·2·3", "Scope별 정의와 대표 자료"),
    ]
    result["artifacts"] = {
        "scope_classification.json": classification,
        "scope_evidence_card.md": "# Scope 근거 카드\n\n- Scope 1: 소유·통제 배출원의 직접배출\n- Scope 2: 구매해 소비한 에너지의 간접배출\n- Scope 3: 그 밖의 상·하류 가치사슬 간접배출\n",
        "additional_data_request.md": "# 추가 자료 요청\n\n" + "\n".join(requests) + "\n",
    }
    return result


MARKET_ROWS = [
    {"concept": "CCM", "axis": "시장 유형", "meaning": "규제·의무 시장", "checks": ["규제대상", "인정 단위", "제출·사용 규칙"]},
    {"concept": "VCM", "axis": "시장 유형", "meaning": "자발적 목표·기여 시장", "checks": ["표준", "방법론", "주장", "무결성"]},
    {"concept": "배출권", "axis": "규제 단위", "meaning": "법정 총량·할당계획 아래의 배출허용량", "checks": ["법령", "할당", "보유·제출 상태"]},
    {"concept": "탄소크레딧", "axis": "성과 단위", "meaning": "검증된 감축·회피·제거 성과 단위", "checks": ["사업", "방법론", "빈티지", "검증·인증", "등록상태"]},
    {"concept": "상쇄", "axis": "사용행위", "meaning": "외부 성과를 특정 배출·목표에 대응해 사용하는 행위", "checks": ["감축 우선", "소각·사용완료", "주장범위"]},
]


def evaluate_market(payload: dict[str, Any]) -> dict[str, Any]:
    skill = "carbon-market-unit-comparison"
    result = _base(skill, payload)
    question = _text(payload, "question")
    purpose = _text(payload, "purpose").upper()
    registry = _text(payload, "registryStatus").upper()
    double_use = bool(payload.get("doubleUse")) or any(term in question for term in ("동시에 사용", "이중사용", "두 번 사용"))
    if not question or not purpose or not _text(payload, "asOfDate"):
        missing = [name for name in ("question", "purpose", "asOfDate") if not _text(payload, name)]
        result.update(status="REVIEW", summary="시장 비교에 필요한 입력이 부족합니다.", missingEvidence=missing)
    elif double_use:
        result.update(status="STOP", summary="동일 성과의 이중사용 또는 이중주장은 차단합니다.")
    elif purpose == "LEARNING":
        result.update(status="PROCEED", summary="시장·단위·사용행위를 구분한 학습용 비교표를 생성했습니다.")
    elif registry in {"", "UNKNOWN", "UNVERIFIED"}:
        result.update(
            status="REVIEW",
            summary="실제 사용 가능성을 판단하려면 단위의 등록·보유·소각·사용완료 상태 확인이 필요합니다.",
            missingEvidence=["registryStatus"],
        )
    elif purpose == "CLAIM_REVIEW":
        result.update(status="REVIEW", summary="개념 비교는 완료했지만 외부 주장은 인간 승인과 제도 확인이 필요합니다.")
    else:
        result.update(status="PROCEED", summary="입력 목적에 맞춰 시장·단위·사용행위 조건을 구분했습니다.")

    table = ["# 탄소시장·단위·사용행위 비교", "", "| 개념 | 축 | 의미 | 확인조건 |", "| --- | --- | --- | --- |"]
    for row in MARKET_ROWS:
        table.append(f"| {row['concept']} | {row['axis']} | {row['meaning']} | {', '.join(row['checks'])} |")
    cautions = [
        "# 외부 주장 주의사항", "",
        "- 직접감축을 외부 단위 사용으로 대체했다고 표현하지 않는다.",
        "- 등록상태와 소각·사용완료를 확인하지 않은 상쇄 주장을 하지 않는다.",
        "- 동일 성과를 여러 주장에 중복 사용하지 않는다.",
        "- 실제 주장 문구는 인간 승인과 적용 제도 확인을 거친다.",
    ]
    data = {"purpose": purpose, "registryStatus": registry or "UNKNOWN", "conceptRows": MARKET_ROWS}
    result["data"] = data
    result["evidence"] = [
        _evidence("03_CCM_VCM_배출권_크레딧_상쇄_시장생태계.md", "# 2. 다섯 개념의 구분", "시장·단위·사용행위 구분"),
        _evidence("03_CCM_VCM_배출권_크레딧_상쇄_시장생태계.md", "# 5. 시장 무결성과 그린워싱", "이중사용과 주장 제한"),
    ]
    result["artifacts"] = {
        "market_unit_comparison.json": data,
        "market_unit_comparison.md": "\n".join(table) + "\n",
        "claim_cautions.md": "\n".join(cautions) + "\n",
    }
    return result


FOREST_ESG_AXES = {
    "E": ["흡수·저장", "생태", "방법론", "추가성", "누출", "영속성", "반전위험"],
    "S": ["산주", "임업인", "지역사회", "권리", "참여", "편익배분"],
    "G": ["산림청", "한국임업진흥원", "산림탄소센터", "검증기관", "등록부", "계약", "감사"],
}


def evaluate_forest_esg(payload: dict[str, Any]) -> dict[str, Any]:
    skill = "forest-esg-impact-mapping"
    result = _base(skill, payload)
    summary = _text(payload, "projectSummary")
    evidence_inputs = {
        "E": payload.get("environmentEvidence"),
        "S": payload.get("socialEvidence"),
        "G": payload.get("governanceEvidence"),
    }
    gaps = [axis for axis, evidence in evidence_inputs.items() if not _has(evidence)]
    prohibited = bool(payload.get("claimCompleteWithoutAllAxes")) or any(
        term in summary for term in ("권리는 무시", "지역사회는 제외", "흡수량만으로 ESG")
    )
    if not summary or not _text(payload, "asOfDate"):
        missing = [name for name in ("projectSummary", "asOfDate") if not _text(payload, name)]
        result.update(status="REVIEW", summary="사업 요약과 기준일이 필요합니다.", missingEvidence=missing)
    elif prohibited:
        result.update(status="STOP", summary="사회·권리·거버넌스를 숨긴 산림 ESG 완결 주장은 차단합니다.")
    elif gaps:
        result.update(
            status="REVIEW",
            summary=f"산림 ESG 매핑은 생성했지만 {', '.join(gaps)} 축의 증거가 부족합니다.",
            missingEvidence=[f"{axis} evidence" for axis in gaps],
        )
    else:
        result.update(status="PROCEED", summary="E/S/G 세 축의 영향·참여자·책임·증거 지도를 생성했습니다.")

    axis_rows = {
        axis: {"requiredTopics": topics, "evidenceProvided": _has(evidence_inputs[axis])}
        for axis, topics in FOREST_ESG_AXES.items()
    }
    map_md = ["# 산림 E/S/G 영향·책임 지도", ""]
    for axis, row in axis_rows.items():
        map_md.append(f"## {axis}")
        map_md.append(f"- 핵심 항목: {', '.join(row['requiredTopics'])}")
        map_md.append(f"- 증거 상태: {'PRESENT' if row['evidenceProvided'] else 'MISSING'}")
        map_md.append("")
    questions = ["# 누락축 확인 질문", ""] + [f"- {axis} 축의 책임주체와 공식 증거는 무엇인가요?" for axis in gaps]
    if not gaps:
        questions.append("- 현재 입력에서 누락된 E/S/G 축이 없습니다.")
    data = {"axes": axis_rows, "missingAxes": gaps}
    result["data"] = data
    result["evidence"] = [
        _evidence("04_산림_ESG_E_S_G_및_임업진흥원_생태계.md", "# 2. E·S·G 구분", "산림탄소의 환경·사회·지배구조 축"),
        _evidence("04_산림_ESG_E_S_G_및_임업진흥원_생태계.md", "# 3. 공식 참여자와 역할", "기관과 참여자 책임"),
    ]
    result["artifacts"] = {
        "forest_esg_map.json": data,
        "forest_esg_map.md": "\n".join(map_md) + "\n",
        "missing_axis_questions.md": "\n".join(questions) + "\n",
    }
    return result


PROCEDURE_STAGES = [
    "PLANNING", "ELIGIBILITY", "REGISTERED", "IMPLEMENTING", "MONITORING",
    "VERIFIED", "CERTIFIED", "UTILIZATION", "REGISTRY_MANAGED",
]

STAGE_LABELS = {
    "PLANNING": "사업계획", "ELIGIBILITY": "타당성·적격성 검토", "REGISTERED": "사업등록",
    "IMPLEMENTING": "사업 실행", "MONITORING": "모니터링", "VERIFIED": "독립 검증",
    "CERTIFIED": "인증", "UTILIZATION": "거래 또는 비거래 활용", "REGISTRY_MANAGED": "등록부 상태관리",
}

STAGE_ACTORS = {
    "ELIGIBILITY": "사업자·제도운영자", "REGISTERED": "사업자·등록부 운영주체",
    "IMPLEMENTING": "사업자·산주·현장참여자", "MONITORING": "사업자",
    "VERIFIED": "독립 검증기관", "CERTIFIED": "공개된 제도운영·인증 주체",
    "UTILIZATION": "사업자·보유자·구매자·승인자", "REGISTRY_MANAGED": "등록부 운영주체",
}


def evaluate_procedure(payload: dict[str, Any]) -> dict[str, Any]:
    skill = "forest-carbon-procedure-guidance"
    result = _base(skill, payload)
    current = _text(payload, "currentStage").upper()
    project_type = _text(payload, "projectType")
    intended = _text(payload, "intendedUse").upper()
    documents = payload.get("availableDocuments", [])
    as_of = _text(payload, "asOfDate")
    stop_skip = bool(payload.get("requestedFinalAssertion")) and current not in {"CERTIFIED", "UTILIZATION", "REGISTRY_MANAGED"}
    if stop_skip:
        result.update(status="STOP", summary="선행 검증·인증 없이 거래 가능 또는 공식 완료를 확정하는 요청은 차단합니다.")
    elif not project_type or not as_of or current in {"", "UNKNOWN"}:
        missing = []
        if not project_type:
            missing.append("projectType")
        if not as_of:
            missing.append("asOfDate")
        if current in {"", "UNKNOWN"}:
            missing.append("currentStage")
        result.update(status="REVIEW", summary="현재 절차를 안내하기 위한 입력이 부족합니다.", missingEvidence=missing)
    elif current not in PROCEDURE_STAGES:
        result.update(status="REVIEW", summary="허용된 절차 단계값이 아닙니다.", missingEvidence=["valid currentStage"])
    else:
        idx = PROCEDURE_STAGES.index(current)
        if idx > 0 and not _has(documents):
            result.update(
                status="REVIEW", summary="현재 단계를 완료했다는 문서가 없어 다음 단계 확정 전 확인이 필요합니다.",
                missingEvidence=["availableDocuments"],
            )
        else:
            result.update(status="PROCEED", summary="현재 상태에서 다음 공식 절차와 필요한 산출물을 안내합니다.")

    if current in PROCEDURE_STAGES:
        idx = PROCEDURE_STAGES.index(current)
        completed = PROCEDURE_STAGES[: idx + 1]
        next_stage = PROCEDURE_STAGES[idx + 1] if idx + 1 < len(PROCEDURE_STAGES) else None
    else:
        completed, next_stage = [], None
    data = {
        "projectType": project_type or "UNKNOWN",
        "currentStage": current or "UNKNOWN",
        "completedStages": completed,
        "nextStage": next_stage,
        "nextActor": STAGE_ACTORS.get(next_stage, "HUMAN_REVIEW") if next_stage else None,
        "intendedUse": intended or "UNKNOWN",
        "availableDocuments": documents,
    }
    checklist = ["# 산림탄소 공식 절차 체크리스트", ""]
    for stage in PROCEDURE_STAGES:
        mark = "x" if stage in completed else " "
        checklist.append(f"- [{mark}] {STAGE_LABELS[stage]}")
    questions = [
        "# 공식 확인 질문", "",
        f"- 현재 사업유형 `{project_type or 'UNKNOWN'}`에 적용되는 공식 절차와 방법론은 무엇인가요?",
        f"- 현재 단계 `{current or 'UNKNOWN'}`의 완료를 증명하는 공식 문서는 무엇인가요?",
        f"- 활용목적 `{intended or 'UNKNOWN'}`에 허용되는 등록상태와 외부 표현은 무엇인가요?",
    ]
    result["data"] = data
    result["evidence"] = [
        _evidence("04_산림_ESG_E_S_G_및_임업진흥원_생태계.md", "# 4. 산림탄소 공식 절차", "계획부터 등록부 상태관리까지의 순서"),
    ]
    result["artifacts"] = {
        "procedure_path.json": data,
        "procedure_checklist.md": "\n".join(checklist) + "\n",
        "official_confirmation_questions.md": "\n".join(questions) + "\n",
    }
    return result


GATE_RULES = {
    "G1": ("주체·신원·역할·대리권", "STOP", "당사자·대리권 확인 담당"),
    "G2": ("사업·수량·빈티지·단위·현재 상태", "STOP", "사업자·등록부 확인 담당"),
    "G3": ("토지·사업권", "CONDITIONAL", "권리·계약 검토 담당"),
    "G4": ("처분권", "STOP", "등록상 보유·처분권 확인 담당"),
    "G5": ("적격성·검증·인증·유효상태", "STOP", "제도운영·검증 확인 담당"),
    "G6": ("구매목적", "REVIEW", "구매자 ESG·주장 승인 담당"),
    "G7": ("계약", "STOP", "계약 검토 담당"),
    "G8": ("세무분류", "REVIEW", "과세관청·세무 전문가"),
    "G9": ("결제·정산", "STOP", "결제·정산 담당"),
    "G10": ("등록부 이전·소각·사용완료", "STOP", "등록부 운영·이전 담당"),
    "G11": ("증빙팩·외부 주장 승인", "REVIEW", "감사·외부주장 승인 담당"),
}


def evaluate_transaction(payload: dict[str, Any]) -> dict[str, Any]:
    skill = "forest-carbon-transaction-readiness"
    result = _base(skill, payload)
    gates = payload.get("gates", {})
    as_of = _text(payload, "asOfDate")
    gate_results: list[dict[str, str]] = []
    missing: list[str] = []
    has_stop = False
    has_review = False
    allowed_states = {"PRESENT", "MISSING", "UNKNOWN", "NOT_APPLICABLE_WITH_REASON"}

    for gate_id, (subject, default_missing, owner) in GATE_RULES.items():
        raw = gates.get(gate_id, {}) if isinstance(gates, dict) else {}
        state = str(raw.get("state", "UNKNOWN")).upper() if isinstance(raw, dict) else str(raw).upper()
        reason = str(raw.get("reason", "")).strip() if isinstance(raw, dict) else ""
        if state not in allowed_states:
            state = "UNKNOWN"
        if state == "PRESENT" or (state == "NOT_APPLICABLE_WITH_REASON" and reason):
            verdict = "PROCEED"
        elif gate_id == "G3":
            verdict = "STOP" if state == "MISSING" else "REVIEW"
        else:
            verdict = default_missing
        if verdict == "STOP":
            has_stop = True
        elif verdict == "REVIEW":
            has_review = True
        if verdict != "PROCEED":
            missing.append(f"{gate_id} {subject}")
        gate_results.append({
            "gate": gate_id, "subject": subject, "submittedState": state,
            "verdict": verdict, "confirmationOwner": owner,
        })

    if not as_of:
        has_review = True
        missing.append("asOfDate")
    overall = "STOP" if has_stop else "REVIEW" if has_review else "PROCEED"
    if overall == "STOP":
        summary = "핵심 거래 게이트가 누락되어 결제·이전·외부 주장을 차단합니다."
    elif overall == "REVIEW":
        summary = "핵심 차단조건은 없지만 공식·전문가·인간 확인이 남아 있습니다."
    else:
        summary = "제출된 fixture 기준으로 11개 준비도 게이트가 충족됐습니다. 실제 거래 효력을 확정하지 않습니다."
    result.update(status=overall, summary=summary, missingEvidence=missing)

    table = ["# 산림탄소 거래 준비도", "", "| Gate | 항목 | 제출상태 | 판정 | 확인주체 |", "| --- | --- | --- | --- | --- |"]
    for row in gate_results:
        table.append(f"| {row['gate']} | {row['subject']} | {row['submittedState']} | {row['verdict']} | {row['confirmationOwner']} |")
    checklist = ["# 누락 증거 체크리스트", ""] + [f"- [ ] {item}" for item in missing]
    if not missing:
        checklist.append("- [x] 입력 fixture에서 누락으로 판정된 게이트 없음")
    inquiry = ["# 공식 질의서 초안", ""]
    for row in gate_results:
        if row["verdict"] != "PROCEED":
            inquiry.append(f"- **{row['confirmationOwner']}**: {row['gate']} {row['subject']}의 공식 확인 기준과 필요 증거는 무엇인가요?")
    if len(inquiry) == 2:
        inquiry.append("- 실제 거래 전 최신 기준과 각 담당자의 최종 승인을 다시 확인해 주세요.")
    data = {"overallStatus": overall, "gateResults": gate_results, "disclaimer": "준비도 판정이며 법률·세무·계약·인증 효력을 확정하지 않음"}
    result["data"] = data
    result["evidence"] = [
        _evidence("05_산림탄소_거래_권리_계약_세무_결제_공백구조.md", "# 2. 거래가 닫히기 위한 열한 게이트", "G1~G11 증거와 누락판정"),
        _evidence("05_산림탄소_거래_권리_계약_세무_결제_공백구조.md", "# 6. Runtime 판정", "PROCEED·REVIEW·STOP 우선순위"),
    ]
    result["artifacts"] = {
        "transaction_readiness.json": data,
        "transaction_readiness_table.md": "\n".join(table) + "\n",
        "missing_evidence_checklist.md": "\n".join(checklist) + "\n",
        "official_inquiry_draft.md": "\n".join(inquiry) + "\n",
    }
    return result


EVALUATORS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "supestar-question-routing": evaluate_question_routing,
    "esg-carbon-action-path": evaluate_esg_action_path,
    "scope-activity-classification": evaluate_scope,
    "carbon-market-unit-comparison": evaluate_market,
    "forest-esg-impact-mapping": evaluate_forest_esg,
    "forest-carbon-procedure-guidance": evaluate_procedure,
    "forest-carbon-transaction-readiness": evaluate_transaction,
}


def evaluate(skill: str, payload: dict[str, Any]) -> dict[str, Any]:
    if skill not in EVALUATORS:
        raise ValueError(f"Unsupported skill: {skill}")
    result = EVALUATORS[skill](payload)
    if result["status"] not in STATUSES:
        raise ValueError(f"Invalid status from {skill}: {result['status']}")
    return result


def execute(skill: str, payload: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    result = evaluate(skill, payload)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_paths: list[str] = []
    for name, content in result.pop("artifacts").items():
        path = output_dir / name
        if isinstance(content, (dict, list)):
            path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            path.write_text(str(content), encoding="utf-8")
        artifact_paths.append(str(path.resolve()))

    input_digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
    run_record = {
        "runId": result["runId"],
        "executedAt": result["executedAt"],
        "skill": skill,
        "skillVersion": SKILL_VERSION,
        "inputSha256": input_digest,
        "status": result["status"],
        "evidence": result["evidence"],
        "artifactPaths": artifact_paths,
        "reviewBoundary": "Candidate runtime; no canonical promotion, external transaction, legal/tax/certification decision, or registry mutation.",
    }
    run_record_path = output_dir / "run_record.json"
    run_record_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    artifact_paths.append(str(run_record_path.resolve()))
    result["artifactPaths"] = artifact_paths
    result_path = output_dir / "result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main(default_skill: str | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a deterministic Supestar P0 candidate skill.")
    if default_skill is None:
        parser.add_argument("--skill", choices=sorted(EVALUATORS), required=True)
    parser.add_argument("--input", required=True, type=Path, help="Input JSON file")
    parser.add_argument("--output-dir", required=True, type=Path, help="Artifact output directory")
    args = parser.parse_args()
    skill = default_skill or args.skill
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Input JSON must be an object")
        result = execute(skill, payload, args.output_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "STOP", "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"runId": result["runId"], "skill": skill, "status": result["status"], "outputDir": str(args.output_dir.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Local Supestar web runtime backed by one verified Runtime Composite entry."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import subprocess
import sys
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from ai_runtime import AiRuntime
from conversation_policy import effective_question
from context_runtime import ContextRuntime
from knowledge_runtime import KnowledgeRuntime


APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parents[2]
STATIC_ROOT = APP_ROOT / "static"
ATOMIC_RUNNER = PROJECT_ROOT / "05_identity_pipeline/07_run_skills/_shared/run_verified_skill.py"
ATOMIC_REGISTRY = PROJECT_ROOT / "05_identity_pipeline/07_run_skills/RUN_SKILL_REGISTRY.json"
COMPOSITE_RUNNER = PROJECT_ROOT / "05_identity_pipeline/08_composite_runtime/_shared/run_verified_composite.py"
COMPOSITE_REGISTRY = PROJECT_ROOT / "05_identity_pipeline/08_composite_runtime/COMPOSITE_RUN_REGISTRY.json"
COMPOSITE_SKILL = (
    PROJECT_ROOT
    / "05_identity_pipeline/08_composite_runtime/supestar-forest-esg-orchestrator-run/SKILL.md"
)
COMPOSITE_RUN_SKILL = "supestar-forest-esg-orchestrator-run"
DEFAULT_RUN_ROOT = PROJECT_ROOT / "06_runtime/runs/supestar_web_v1"
KST = timezone(timedelta(hours=9))
MAX_REQUEST_BYTES = 128 * 1024
RATE_WINDOW_SECONDS = 60
RATE_REQUESTS_PER_WINDOW = 20
MAX_RUNS_PER_PROCESS = 500
_rate_lock = threading.Lock()
_rate_events: dict[str, deque[float]] = defaultdict(deque)
_run_lock = threading.Lock()
_run_count = 0

ROUTE_LABELS = {
    "CONCEPT_EXPLANATION": "질문별 Concept·KAC 설명",
    "ESG_CARBON_PATH": "ESG → 탄소 행동경로",
    "SCOPE_CLASSIFICATION": "Scope 활동 분류",
    "CARBON_MARKET_COMPARISON": "CCM·VCM·단위 비교",
    "FOREST_ESG_MAPPING": "산림 ESG E·S·G 매핑",
    "FOREST_CARBON_PROCEDURE": "산림탄소 공식 절차",
    "TRANSACTION_READINESS": "거래 준비도 점검",
    "NEEDS_INPUT": "추가 입력 필요",
    "OUT_OF_SCOPE": "실행 범위 밖",
    "ROUTING_EXECUTION_FAILURE": "라우팅 실행 실패",
}
FOREST_CARBON_MARKET_URL = "https://forestcarbonmarket.kr/"
KNOWLEDGE_RUNTIME = KnowledgeRuntime()
AI_RUNTIME = AiRuntime()
CONTEXT_RUNTIME = ContextRuntime()


def _market_handoff(context: str) -> dict[str, Any]:
    return {
        "title": "준비가 되었다면 산림탄소마켓에서 이어갈 수 있어요",
        "description": (
            "프로젝트별 지역·사업 유형·톤당 가격·판매 가능량을 살펴보고 "
            "원하는 수량의 구매 신청으로 이어지는 탄소크레딧 마켓입니다."
        ),
        "context": context,
        "label": "산림탄소마켓에서 크레딧 살펴보기",
        "url": FOREST_CARBON_MARKET_URL,
        "note": (
            "수페스타는 구매나 결제를 대신하지 않고 거래 가능성을 보증하지 않습니다. "
            "구매 전 인증 정보, 사용 목적, 소유권 이전 방식과 계약·세무 사항을 직접 확인하세요."
        ),
    }


def _explicit_market_intent(question: str, route: str) -> bool:
    """Expose the external market only for an explicit user-led discovery/buying intent."""

    if route not in {"CARBON_MARKET_COMPARISON", "TRANSACTION_READINESS"}:
        return False
    compact = question.lower().replace(" ", "")
    subject = any(token in compact for token in ("탄소크레딧", "산림탄소크레딧", "크레딧"))
    action = any(
        token in compact
        for token in (
            "어디서", "어디에", "살수", "사려", "사고싶", "구매하려", "구매할",
            "구매전", "구매방법", "구매처", "마켓찾", "사이트", "실제구매",
        )
    )
    return subject and action


def _enforce_market_policy(guidance: dict[str, Any], question: str, route: str) -> tuple[dict[str, Any], bool]:
    allowed = _explicit_market_intent(question, route)
    protected = dict(guidance)
    if not allowed:
        protected["marketHandoff"] = None
    elif not protected.get("marketHandoff"):
        protected["marketHandoff"] = _market_handoff("사용자가 탄소크레딧 구매처 또는 구매 준비 절차를 명시적으로 요청했습니다.")
    return protected, allowed


def _natural_guidance(
    route: str,
    final_result: dict[str, Any],
    question: str,
    kac_execution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Turn verified execution data into calm, user-first Korean guidance.

    The technical route, Skill and hashes remain in the response for verification,
    but this layer owns what an ordinary user reads first.
    """

    if route == "CONCEPT_EXPLANATION" and kac_execution is not None:
        return KNOWLEDGE_RUNTIME.guidance(kac_execution)

    data = final_result.get("data", {})
    scope_candidate = data.get("candidateScope") if isinstance(data, dict) else None
    scope_label = {
        "SCOPE_1": "Scope 1",
        "SCOPE_2": "Scope 2",
        "SCOPE_3": "Scope 3",
    }.get(scope_candidate, "Scope 분류 후보")

    guidance: dict[str, dict[str, Any]] = {
        "ESG_CARBON_PATH": {
            "statusLabel": "행동 순서를 안내할 수 있어요",
            "title": "ESG는 선언보다, 측정하고 행동으로 옮길 때 의미가 있습니다.",
            "paragraphs": [
                "ESG 활동을 시작할 때는 먼저 우리 조직과 활동의 범위를 정하고, 온실가스가 어디에서 발생하는지 측정해야 합니다.",
                "그다음 직접 감축할 수 있는 배출을 줄이고, 남은 배출을 어떻게 관리할지 판단합니다. 산림탄소크레딧은 이 마지막 단계에서 검토할 수 있는 선택지 중 하나입니다.",
            ],
            "rationale": "활동의 순서를 구분해야 단순한 친환경 홍보와 실제 감축 행동을 혼동하지 않을 수 있습니다.",
            "steps": [
                {"title": "범위 정하기", "description": "어느 조직과 사업장의 활동을 볼지 정합니다."},
                {"title": "배출원 분류하기", "description": "Scope 1·2·3 중 어디에 해당하는지 확인합니다."},
                {"title": "감축 후 보완 검토하기", "description": "직접 감축을 우선하고 남은 배출에 한해 크레딧 활용을 검토합니다."},
            ],
            "followUp": "기업 활동인지 개인 활동인지 알려주시면 확인 순서를 더 구체적으로 정리해 드릴게요.",
            "marketHandoff": _market_handoff("직접 감축 이후 남은 배출을 보완하려는 단계라면 프로젝트를 비교해 볼 수 있습니다."),
        },
        "SCOPE_CLASSIFICATION": {
            "statusLabel": "말씀해 주신 상황을 기준으로 분류했어요",
            "title": (
                f"말씀해 주신 조건대로라면 이 활동은 {scope_label}로 분류됩니다."
                if scope_candidate
                else "이 배출원이 어느 Scope인지 판단하려면 활동과 소유·운영 관계가 더 필요해요."
            ),
            "paragraphs": [
                "Scope는 배출량의 크기가 아니라 배출원을 누가 소유·운영하는지, 전기나 열을 외부에서 구매했는지, 가치사슬 어디에서 발생했는지에 따라 나뉩니다.",
                (
                    "현재 답변은 입력해 주신 상황에 적용한 분류입니다. 실제 보고에 사용하기 전에는 조직경계와 운영통제 여부, 활동자료를 원문과 다시 대조해 주세요."
                    if scope_candidate
                    else "지금 질문만으로는 필요한 관계를 알 수 없어 임의로 Scope를 정하지 않았습니다."
                ),
            ],
            "rationale": "같은 활동명이라도 소유·통제 관계가 다르면 Scope가 달라질 수 있기 때문에 상황 확인이 먼저 필요합니다.",
            "steps": [
                {"title": "배출원 확인", "description": "연료, 전기, 이동, 구매품처럼 실제 활동을 특정합니다."},
                {"title": "소유·통제 확인", "description": "우리 조직이 직접 소유하거나 운영하는지 확인합니다."},
                {"title": "활동자료 준비", "description": "사용량, 기간, 단위와 증빙자료를 모읍니다."},
            ],
            "followUp": "분류하려는 활동과 누가 설비를 운영하는지 알려주시면 더 정확히 안내할 수 있습니다.",
            "marketHandoff": _market_handoff("Scope를 분류하고 직접 감축 계획을 세운 뒤, 잔여배출 보완이 필요한 경우에만 살펴보세요."),
        },
        "CARBON_MARKET_COMPARISON": {
            "statusLabel": "시장과 단위의 차이를 설명할 수 있어요",
            "title": "배출권과 탄소크레딧은 이름이 비슷하지만 쓰임과 확인 기준이 다릅니다.",
            "paragraphs": [
                "규제시장(CCM)의 배출권은 법적으로 정해진 감축 의무를 이행하기 위한 단위이고, 자발적시장(VCM)의 크레딧은 자발적인 감축·상쇄 활동에서 만들어지는 단위입니다.",
                "구매 전에는 어느 제도에서 발행됐는지, 등록부 상태와 중복사용 가능성, 우리 조직이 어떤 주장에 사용하려는지를 함께 확인해야 합니다.",
            ],
            "rationale": "시장과 단위를 구분하지 않으면 구매한 크레딧을 원래 목적과 다른 공시나 주장에 사용할 위험이 있습니다.",
            "steps": [
                {"title": "사용 목적 정하기", "description": "규제 의무, 자발적 상쇄, 기여 주장 중 무엇인지 구분합니다."},
                {"title": "발행·등록 정보 확인", "description": "제도, 인증, 등록부 상태와 고유 식별 정보를 확인합니다."},
                {"title": "중복사용 방지 확인", "description": "이미 사용되거나 이전된 단위인지 확인합니다."},
            ],
            "followUp": "구매 목적이 공시인지 내부 학습인지 알려주시면 확인 항목을 목적에 맞게 줄여 드릴게요.",
            "marketHandoff": _market_handoff("산림 분야의 탄소크레딧을 실제 프로젝트 단위로 비교하려면 이곳에서 이어갈 수 있습니다."),
        },
        "FOREST_ESG_MAPPING": {
            "statusLabel": "산림사업을 E·S·G로 나눠 볼 수 있어요",
            "title": "산림탄소는 흡수량만이 아니라 사람의 권리와 관리 책임까지 함께 봐야 합니다.",
            "paragraphs": [
                "환경(E)은 탄소 흡수량과 생태계 영향을, 사회(S)는 산주·지역사회의 권리와 편익을, 거버넌스(G)는 등록·검증·인증과 책임 주체를 확인합니다.",
                "세 축 중 하나라도 빠지면 숫자는 있어도 신뢰할 수 있는 산림 ESG 사업이라고 설명하기 어렵습니다.",
            ],
            "rationale": "산림은 토지와 지역사회가 연결된 장기 사업이므로 탄소량만으로 사업의 책임성을 판단할 수 없습니다.",
            "steps": [
                {"title": "환경 근거", "description": "방법론, 흡수량 산정과 모니터링 자료를 확인합니다."},
                {"title": "사회 근거", "description": "토지 권리, 이해관계자 동의와 편익 배분을 확인합니다."},
                {"title": "관리 근거", "description": "등록·검증·인증 상태와 책임 주체를 확인합니다."},
            ],
            "followUp": "검토하려는 산림사업이 있다면 보유 자료를 알려주세요. 빠진 축부터 정리해 드릴 수 있습니다.",
            "marketHandoff": _market_handoff("세 축을 확인한 뒤 실제 판매 프로젝트의 정보와 가격을 비교할 수 있습니다."),
        },
        "FOREST_CARBON_PROCEDURE": {
            "statusLabel": "진행 단계와 다음 절차를 안내할 수 있어요",
            "title": "산림탄소 사업은 등록으로 끝나지 않고 모니터링·검증·인증을 거쳐 활용됩니다.",
            "paragraphs": [
                "먼저 사업 적합성과 토지·권리관계를 확인하고 사업계획을 등록합니다. 이후 계획에 따라 사업을 이행하고 흡수량을 모니터링한 뒤 검증과 인증 절차를 거칩니다.",
                "인증된 크레딧은 등록부에서 상태와 이전 내역을 관리하며, 그 이후에 활용이나 거래를 검토할 수 있습니다.",
            ],
            "rationale": "각 단계의 증거가 다음 단계의 조건이 되므로 순서를 건너뛰면 크레딧의 권리와 신뢰성을 확인하기 어렵습니다.",
            "steps": [
                {"title": "적합성·권리 확인", "description": "대상지, 사업유형과 토지 권리를 확인합니다."},
                {"title": "등록·이행", "description": "사업계획을 등록하고 계획에 따라 산림 활동을 수행합니다."},
                {"title": "모니터링·검증·인증", "description": "흡수량 자료를 만들고 제3자 확인 절차를 거칩니다."},
                {"title": "등록부 관리·활용", "description": "발행·보유·이전 상태를 확인한 뒤 활용 또는 거래합니다."},
            ],
            "followUp": "현재 사업 단계와 가지고 있는 문서를 알려주시면 바로 다음에 확인할 일을 좁혀 드릴게요.",
            "marketHandoff": _market_handoff("검증·인증과 등록부 상태가 확인된 크레딧의 활용·구매 단계에서 연결됩니다."),
        },
        "TRANSACTION_READINESS": {
            "statusLabel": "구매 전에 확인할 자료가 남아 있어요",
            "title": "지금은 거래를 확정하기보다, 권리와 증빙을 먼저 확인하는 단계입니다.",
            "paragraphs": [
                "탄소크레딧은 가격과 수량만 보고 구매하면 안 됩니다. 누가 판매할 권리를 갖는지, 어떤 인증과 등록부 기록이 있는지, 구매 후 어떤 목적으로 사용할지를 먼저 확인해야 합니다.",
                "현재 예시에는 거래를 확정할 증거가 충분하지 않아 구매 준비가 완료됐다고 판단하지 않았습니다.",
            ],
            "rationale": "구매 신청은 실제 행동이지만, 그 전에 권리·인증·계약·이전 조건을 확인해야 중복사용과 과장된 ESG 주장을 피할 수 있습니다.",
            "steps": [
                {"title": "판매 권한", "description": "판매자와 크레딧 처분권, 토지·사업 권리를 확인합니다."},
                {"title": "크레딧 상태", "description": "인증 정보, 등록부 상태와 중복사용 여부를 확인합니다."},
                {"title": "계약과 이전", "description": "가격·수량·입금·소유권 이전 조건을 확인합니다."},
                {"title": "사용과 주장", "description": "공시·상쇄·기여 등 사용 목적과 표현 범위를 확인합니다."},
            ],
            "followUp": "구매 주체, 사용 목적, 검토 중인 프로젝트가 있으면 준비사항을 실제 순서로 정리해 드릴게요.",
            "marketHandoff": _market_handoff("위 확인사항을 준비한 뒤 프로젝트별 가격과 판매 가능량을 비교하고 구매를 신청할 수 있습니다."),
        },
        "NEEDS_INPUT": {
            "statusLabel": "상황을 조금 더 알려주세요",
            "title": "질문과 연결할 ESG 개념이나 판단 대상을 하나로 좁혀 주세요.",
            "paragraphs": [
                "현재 질문만으로는 개념 설명, 활동의 Scope 분류, 산림사업 절차, 거래 준비도 중 어느 결과가 필요한지 확정하기 어렵습니다.",
                "알고 싶은 개념이나 판단하려는 활동과 목적을 한 문장으로 알려주시면 필요한 지식과 근거만 골라 답하겠습니다.",
            ],
            "rationale": "대상을 임의로 추정하면 일반 ESG 질문을 탄소시장이나 구매 질문으로 왜곡할 수 있기 때문입니다.",
            "steps": [
                {"title": "개념 질문", "description": "예: ‘ESG가 무엇인가요?’처럼 알고 싶은 개념을 적습니다."},
                {"title": "판단 질문", "description": "예: ‘회사 소유 보일러는 어느 Scope인가요?’처럼 활동과 상황을 적습니다."},
            ],
            "followUp": "ESG, SDGs, Scope, 탄소크레딧, 산림탄소, 한국임업진흥원 중 무엇을 알고 싶은지 말씀해 주세요.",
            "marketHandoff": None,
        },
        "OUT_OF_SCOPE": {
            "statusLabel": "요청하신 실행이나 공식 확정은 대신할 수 없어요",
            "title": "실제 거래·결제·등록 변경이나 법률·세무·인증의 최종판정은 사람이 확인하고 실행해야 합니다.",
            "paragraphs": [
                "수페스타는 외부 계정을 대신 사용하거나 금전·권리·등록 상태를 변경하지 않으며, 확인되지 않은 공식 결론을 생성하지 않습니다.",
                "대신 개념 설명, 필요한 증거, 확인 담당자와 사람이 검토할 질문까지는 구조화할 수 있습니다.",
            ],
            "rationale": "금전·권리·공식 상태가 바뀌는 행동과 전문적 최종판정은 설명 권한을 넘어서는 별도 승인 영역입니다.",
            "steps": [
                {"title": "설명 범위로 바꾸기", "description": "실행 요청 대신 필요한 절차·증거·확인사항을 질문합니다."},
                {"title": "책임 주체 확인", "description": "결제·등록·법률·세무·인증을 최종 확인할 담당자를 지정합니다."},
            ],
            "followUp": "예: ‘실제 결제 전에 어떤 증거와 담당자 확인이 필요한가요?’처럼 설명·준비 범위로 질문해 주세요.",
            "marketHandoff": None,
        },
    }
    if route == "TRANSACTION_READINESS" and final_result.get("status") == "PROCEED":
        guidance[route] = {
            "statusLabel": "거래 전에 확인할 항목을 모두 살펴봤어요",
            "title": "말씀해 주신 내용만 보면, 거래 전에 확인할 11가지 항목은 모두 갖춰져 있어요.",
            "paragraphs": [
                "다만 이는 입력하신 확인 상태를 정리한 결과이지, 문서의 진위나 거래의 법적·세무상 효력을 확인한 결과는 아닙니다.",
                "실제 거래 전에는 원문 문서와 유효기간을 대조하고 각 담당자의 최종 승인을 받아야 합니다.",
            ],
            "rationale": "확인 항목이 모두 채워져 있어도 실제 거래가 유효한지는 문서 원문과 책임자가 최종 확인해야 하기 때문입니다.",
            "steps": [
                {"title": "원문 대조", "description": "G1~G11에 연결한 실제 문서의 발행주체·유효기간·대상을 확인합니다."},
                {"title": "책임자 승인", "description": "권리·인증·계약·세무·결제·등록부·외부 주장 담당자의 승인을 받습니다."},
            ],
            "followUp": "각 게이트에 연결할 실제 문서명과 확인 담당자를 입력하면 최종 대조표를 만들 수 있습니다.",
            "marketHandoff": None,
        }
    if route == "FOREST_ESG_MAPPING" and final_result.get("status") == "PROCEED":
        guidance[route] = {
            "statusLabel": "산림 ESG의 세 영역을 모두 확인했어요",
            "title": "말씀해 주신 자료에는 환경·사회·지배구조를 확인할 내용이 모두 포함돼 있어요.",
            "paragraphs": [
                "환경은 흡수량·모니터링·생태 자료, 사회는 산주·지역사회·편익 자료, 지배구조는 등록·검증·계약 자료로 확인했습니다.",
                "다만 현재는 자료를 보유하고 있다는 말씀을 기준으로 정리한 것이므로, 실제 내용과 충분성은 원문을 대조해야 합니다.",
            ],
            "rationale": "세 축을 분리해야 탄소량만으로 권리·참여·관리 책임을 가리는 오류를 막을 수 있습니다.",
            "steps": [
                {"title": "원문 확인", "description": "각 축에 연결된 보고서·동의서·등록·검증·계약 문서의 실제 내용을 대조합니다."},
                {"title": "책임 주체 확인", "description": "산주·지역사회·사업자·검증·등록 책임자가 자료를 확인합니다."},
            ],
            "followUp": "각 자료의 발행주체와 기준일을 알려주시면 축별 증거 대조표를 더 구체화할 수 있습니다.",
            "marketHandoff": None,
        }
    if route == "FOREST_CARBON_PROCEDURE" and final_result.get("status") == "PROCEED":
        stage_labels = {
            "PLANNING": "사업계획", "ELIGIBILITY": "타당성·적격성 검토", "REGISTERED": "사업등록",
            "IMPLEMENTING": "사업 실행", "MONITORING": "모니터링", "VERIFIED": "독립 검증",
            "CERTIFIED": "인증", "UTILIZATION": "거래 또는 비거래 활용", "REGISTRY_MANAGED": "등록부 상태관리",
        }
        procedure_data = final_result.get("data", {})
        current_stage = str(procedure_data.get("currentStage", "UNKNOWN"))
        next_stage = procedure_data.get("nextStage")
        guidance[route] = {
            "statusLabel": "현재 위치와 다음 단계를 찾았어요",
            "title": f"현재는 {stage_labels.get(current_stage, current_stage)} 단계이고, 다음은 {stage_labels.get(str(next_stage), str(next_stage)) if next_stage else '등록부 상태와 활용 목적 확인'}입니다.",
            "paragraphs": [
                f"말씀해 주신 문서를 현재 단계의 확인 자료로 연결했습니다. 다음 단계는 {procedure_data.get('nextActor') or '담당자'}가 확인합니다.",
                "이 답변은 진행 순서를 안내하는 것이며, 실제 등록·검증·인증 완료나 거래 가능성을 대신 확정하지는 않습니다.",
            ],
            "rationale": "현재 단계와 완료 증거를 먼저 고정해야 선행 절차를 건너뛰지 않고 다음 담당자와 산출물을 연결할 수 있습니다.",
            "steps": [
                {"title": "현재 문서 대조", "description": "현재 단계 완료를 주장하는 문서의 발행주체·대상·기준일을 확인합니다."},
                {"title": "다음 단계 준비", "description": f"{stage_labels.get(str(next_stage), str(next_stage)) if next_stage else '등록부 상태와 활용 목적'}에 필요한 입력과 담당자를 확인합니다."},
            ],
            "followUp": "보유 문서의 정확한 이름과 발행기관을 알려주시면 다음 단계 체크리스트를 좁혀 드릴게요.",
            "marketHandoff": None,
        }
    normalized_question = question.replace(" ", "")
    tree_planting_intent = any(token in normalized_question for token in ("나무", "조림", "식재", "심으면", "심기"))
    purchase_intent = any(token in normalized_question for token in ("구매", "살수", "사려", "사고", "크레딧을사"))
    market_discovery_intent = purchase_intent and any(token in normalized_question for token in ("어디", "마켓", "시장", "사이트"))

    if route == "NEEDS_INPUT" and tree_planting_intent:
        return {
            "statusLabel": "인정 여부를 판단하려면 몇 가지 확인이 필요해요",
            "title": "나무를 심었다는 사실만으로 바로 탄소감축 실적으로 인정되지는 않습니다.",
            "paragraphs": [
                "산림탄소 사업으로 인정받으려면 대상지와 토지 권리, 적용 가능한 사업유형, 흡수량 산정 방법과 등록·모니터링·검증 절차를 함께 확인해야 합니다.",
                "먼저 회사가 직접 추진하는 산림사업인지, 이미 등록된 프로젝트의 크레딧을 구매하려는 것인지 구분하면 다음 절차가 달라집니다.",
            ],
            "rationale": "산림의 탄소효과는 오랜 기간 관리되고 검증되어야 하며, 토지 권리와 중복 산정 문제까지 함께 확인해야 하기 때문입니다.",
            "steps": [
                {"title": "대상지와 권리 확인", "description": "토지 소유·사용 권한과 사업 참여 주체를 확인합니다."},
                {"title": "사업유형 확인", "description": "신규조림, 산림경영 등 적용 가능한 방법을 검토합니다."},
                {"title": "등록·모니터링 준비", "description": "사업계획, 흡수량 산정과 장기 모니터링 자료를 준비합니다."},
            ],
            "followUp": "직접 나무를 심어 사업을 만들려는 것인지, 기존 산림탄소크레딧을 구매하려는 것인지 알려주세요.",
            "marketHandoff": _market_handoff("직접 사업을 만드는 대신 이미 검증된 산림탄소 프로젝트의 크레딧을 구매하는 방법도 비교할 수 있습니다."),
        }

    if route == "CARBON_MARKET_COMPARISON" and purchase_intent:
        if market_discovery_intent:
            return {
                "statusLabel": "실제 구매 가능한 마켓을 안내해 드릴게요",
                "title": "산림탄소크레딧은 산림탄소마켓에서 프로젝트별로 살펴볼 수 있습니다.",
                "paragraphs": [
                    "산림탄소마켓에서는 프로젝트의 지역과 사업유형, 톤당 가격과 판매 가능량을 비교하고 원하는 수량의 구매 신청으로 이어갈 수 있습니다.",
                    "다만 구매 버튼을 누르기 전에 인증 정보와 등록부 상태, 사용 목적, 소유권 이전 조건을 먼저 확인하는 것이 좋습니다.",
                ],
                "rationale": "탄소크레딧은 같은 1톤 단위라도 사업과 인증 상태, 사용할 수 있는 주장 범위가 다를 수 있기 때문입니다.",
                "steps": [
                    {"title": "프로젝트 살펴보기", "description": "지역, 사업유형과 프로젝트 설명을 비교합니다."},
                    {"title": "가격·수량 확인", "description": "톤당 가격과 현재 판매 가능량을 확인합니다."},
                    {"title": "인증·이전 조건 확인", "description": "구매 후 보유와 이전, 사용 조건을 확인합니다."},
                ],
                "followUp": "구매 주체와 목적, 필요한 수량을 알려주시면 마켓에 들어가기 전 확인 목록을 정리해 드릴게요.",
                "marketHandoff": _market_handoff("확인사항을 이해했다면 실제 산림탄소 프로젝트를 살펴보고 구매 절차를 이어갈 수 있습니다."),
            }
        return {
            "statusLabel": "구매 전에 확인할 순서를 알려드릴게요",
            "title": "탄소크레딧은 가격보다 먼저, 출처와 사용 조건을 확인해야 합니다.",
            "paragraphs": [
                "구매하려는 크레딧이 어느 프로젝트에서 발행됐는지, 인증과 등록부 상태가 어떤지, 이미 사용된 단위는 아닌지 확인하세요.",
                "그다음 우리 조직이 잔여배출 보완, 내부 학습, 대외 공시 중 어떤 목적으로 사용할지 정하고 계약과 이전 조건을 검토합니다.",
            ],
            "rationale": "구매 자체가 ESG 성과를 보장하지 않으며, 목적과 증거가 맞지 않으면 과장된 환경 주장으로 이어질 수 있기 때문입니다.",
            "steps": [
                {"title": "프로젝트·인증 확인", "description": "발행 프로젝트와 인증·등록부 정보를 확인합니다."},
                {"title": "사용 목적 확인", "description": "감축 보완, 기여, 공시 중 목적을 구분합니다."},
                {"title": "거래 조건 확인", "description": "가격, 수량, 입금과 소유권 이전 조건을 확인합니다."},
            ],
            "followUp": "기업 구매인지 개인 구매인지와 사용 목적을 알려주시면 확인 목록을 더 구체화할 수 있습니다.",
            "marketHandoff": _market_handoff("확인 기준을 이해한 뒤 실제 프로젝트의 가격과 판매 가능량을 비교하세요."),
        }

    return guidance.get(
        route,
        {
            "statusLabel": "답변을 정리하지 못했어요",
            "title": "질문의 목적과 상황을 조금 더 구체적으로 알려주세요.",
            "paragraphs": ["수페스타가 확인할 대상과 원하는 결과를 알면 필요한 지식과 다음 행동을 다시 연결할 수 있습니다."],
            "rationale": "상황이 불명확한 상태에서 결론을 만들면 잘못된 행동으로 이어질 수 있습니다.",
            "steps": [{"title": "질문 구체화", "description": "주체, 목적과 현재 보유한 정보를 함께 적어주세요."}],
            "followUp": "예: ‘기업이 산림탄소크레딧을 구매하기 전에 무엇을 확인해야 하나요?’",
            "marketHandoff": None,
        },
    )


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _default_payload(
    question: str,
    request: dict[str, Any],
    history: list[dict[str, str]],
) -> dict[str, Any]:
    """Create and enrich a neutral context without inventing user facts."""

    today = datetime.now(KST).date().isoformat()
    routing_question, routing_history_used = effective_question(question, history)
    compact = question.lower().replace(" ", "")
    if any(token in compact for token in ("ccm", "vcm", "배출권", "크레딧", "탄소시장", "상쇄")):
        focus = "MARKET"
    elif any(token in compact for token in ("scope", "스코프", "조직경계", "운영경계")):
        focus = "SCOPE"
    elif any(token in compact for token in ("sdg", "지속가능발전")):
        focus = "SDGS"
    elif any(token in compact for token in ("산림", "임업", "kofpi")):
        focus = "FOREST_CARBON"
    else:
        focus = "MEASUREMENT"

    payload: dict[str, Any] = {
        "question": question,
        "routingQuestion": routing_question,
        "conversationContinuity": {
            "policy": "EXPLICIT_FOLLOW_UP_ONLY",
            "historyMessagesUsed": routing_history_used,
        },
        "userRole": "LEARNER",
        "asOfDate": today,
        "providedEvidence": [],
        "focus": focus,
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

    allowed = {
        "userRole", "asOfDate", "providedEvidence", "focus", "measurementContext",
        "activityDescription", "organizationBoundary", "sourceOwnershipOrControl",
        "purchasedEnergyType", "valueChainRelation", "activityData", "purpose",
        "unitType", "registryStatus", "doubleUse", "projectSummary",
        "environmentEvidence", "socialEvidence", "governanceEvidence",
        "claimCompleteWithoutAllAxes", "projectType", "currentStage",
        "availableDocuments", "intendedUse", "requestedFinalAssertion", "gates",
    }
    explicit_context = request.get("context") if isinstance(request.get("context"), dict) else None
    payload, _ = CONTEXT_RUNTIME.enrich(
        payload,
        question,
        history,
        explicit_context=explicit_context,
        allowed_explicit_fields=allowed,
    )
    return payload


def _run_verified_composite(input_path: Path, output_dir: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(COMPOSITE_RUNNER),
            "--run-composite",
            COMPOSITE_RUN_SKILL,
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stdout.strip() or completed.stderr.strip() or "unknown runner failure"
        raise RuntimeError(f"{COMPOSITE_RUN_SKILL} failed: {detail}")
    result_path = output_dir / "result.json"
    record_path = output_dir / "composite_run_record.json"
    if not result_path.is_file() or not record_path.is_file():
        raise RuntimeError(f"{COMPOSITE_RUN_SKILL} did not emit result and Composite Run Record")
    result = _read_json(result_path)
    record = _read_json(record_path)
    if result.get("executionState") != "COMPLETED" or not record.get("singleEntryPoint"):
        raise RuntimeError(f"{COMPOSITE_RUN_SKILL} did not complete through one entry point")
    return {
        "result": result,
        "record": record,
        "resultSha256": _sha(result_path),
        "recordSha256": _sha(record_path),
    }


def _artifact_previews(output_dir: Path) -> list[dict[str, Any]]:
    previews: list[dict[str, Any]] = []
    excluded = {"result.json", "run_record.json", "run_skill_record.json"}
    for path in sorted(output_dir.iterdir()):
        if not path.is_file() or path.name in excluded:
            continue
        raw = path.read_bytes()
        item: dict[str, Any] = {
            "name": path.name,
            "sha256": _sha_bytes(raw),
            "bytes": len(raw),
        }
        if len(raw) <= 80_000:
            try:
                item["content"] = raw.decode("utf-8")
            except UnicodeDecodeError:
                item["content"] = "[binary artifact]"
        else:
            item["content"] = "[artifact preview omitted: over 80 KB]"
        previews.append(item)
    return previews


def _new_run_root(root: Path) -> Path:
    global _run_count
    with _run_lock:
        if _run_count >= MAX_RUNS_PER_PROCESS:
            raise RuntimeError("이 데모 프로세스의 최대 실행 횟수에 도달했습니다.")
        _run_count += 1
    moment = datetime.now(KST).strftime("%Y%m%dT%H%M%S%f")
    run_root = root / f"{moment}_{uuid.uuid4().hex[:8]}"
    run_root.mkdir(parents=True, exist_ok=False)
    return run_root


def _conversation_history(request: dict[str, Any]) -> list[dict[str, str]]:
    raw = request.get("history", [])
    if not isinstance(raw, list):
        return []
    history: list[dict[str, str]] = []
    for item in raw[-8:]:
        if not isinstance(item, dict) or item.get("role") not in {"user", "assistant"}:
            continue
        content = str(item.get("content", "")).strip()
        if not content:
            continue
        history.append({"role": item["role"], "content": content[:2_000]})
    return history


def orchestrate(request: dict[str, Any], run_root_parent: Path = DEFAULT_RUN_ROOT) -> dict[str, Any]:
    question = str(request.get("question", "")).strip()
    if not question:
        raise ValueError("question is required")
    if len(question) > 2_000:
        raise ValueError("question must be 2,000 characters or fewer")

    history = _conversation_history(request)
    run_root = _new_run_root(run_root_parent.resolve())
    payload = _default_payload(question, request, history)
    payload["conversationHistory"] = history
    context_extraction = payload.get("contextExtraction", {})
    context_extraction_path = run_root / "context_extraction.json"
    context_extraction_path.write_text(
        json.dumps(context_extraction, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    input_path = run_root / "input.json"
    input_bytes = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    input_path.write_bytes(input_bytes)
    input_sha = _sha_bytes(input_bytes)

    composite_dir = run_root / "composite"
    composite = _run_verified_composite(input_path, composite_dir)
    composite_result = composite["result"]
    composite_record = composite["record"]
    route = composite_result.get("route", "ROUTING_EXECUTION_FAILURE")
    selected_skill = composite_result.get("selectedRunSkill")
    final_result = composite_result.get("finalResult", {})
    kac_execution = composite_result.get("kacExecution", {})
    if not isinstance(final_result, dict) or not isinstance(kac_execution, dict):
        raise RuntimeError("Runtime Composite returned an invalid final result or KAC execution")

    final_output_relative = composite_result.get("paths", {}).get("finalOutputDirectory")
    if not isinstance(final_output_relative, str):
        raise RuntimeError("Runtime Composite omitted the final output directory")
    final_output_dir = (PROJECT_ROOT / final_output_relative).resolve()
    try:
        final_output_dir.relative_to(PROJECT_ROOT.resolve())
    except ValueError as exc:
        raise RuntimeError("Runtime Composite output escaped the project root") from exc
    if not final_output_dir.is_dir():
        raise RuntimeError("Runtime Composite final output directory is missing")

    trace: list[dict[str, Any]] = [
        {
            "order": 1,
            "role": "배포된 Runtime Composite 단일 진입점",
            "runSkill": COMPOSITE_RUN_SKILL,
            "runId": composite_result.get("runId"),
            "status": composite_result.get("status"),
            "resultSha256": composite["resultSha256"],
            "recordSha256": composite["recordSha256"],
        }
    ]
    for member in composite_result.get("memberTrace", []):
        if not isinstance(member, dict):
            continue
        child = dict(member)
        child["order"] = len(trace) + 1
        trace.append(child)

    input_preserved = bool(composite_result.get("inputEvidence", {}).get("bytesPreserved"))
    if not input_preserved or _sha(input_path) != input_sha:
        raise RuntimeError("Runtime Composite did not preserve the original input bytes")
    kac_path = composite_dir / "kac_execution.json"
    if not kac_path.is_file():
        raise RuntimeError("Runtime Composite omitted KAC execution evidence")
    kac_sha = _sha(kac_path)
    fallback_guidance = _natural_guidance(route, final_result, question, kac_execution)
    fallback_guidance, market_allowed = _enforce_market_policy(fallback_guidance, question, route)
    output_context = dict(final_result)
    output_context["contextExtraction"] = context_extraction
    user_guidance, ai_status = AI_RUNTIME.generate(
        question=question,
        history=history,
        kac_execution=kac_execution,
        deterministic_result=output_context,
        fallback_guidance=fallback_guidance,
        market_allowed=market_allowed,
        route=route,
    )
    user_guidance, _ = _enforce_market_policy(user_guidance, question, route)
    ai_record = {
        "schemaVersion": "1.0",
        "questionSha256": _sha_bytes(question.encode("utf-8")),
        "provider": ai_status.get("provider"),
        "model": ai_status.get("model"),
        "mode": ai_status.get("mode"),
        "connected": ai_status.get("connected"),
        "generationUsed": ai_status.get("generationUsed"),
        "reason": ai_status.get("reason"),
        "marketLinkAllowed": market_allowed,
        "selectedConcepts": kac_execution.get("selectedConcepts", []),
        "verdictPreserved": final_result.get("status"),
        "outputRiskGate": ai_status.get("outputRiskGate"),
        "contextExtractionSha256": _sha(context_extraction_path),
        "conversationContinuity": payload.get("conversationContinuity", {}),
    }
    ai_record_path = run_root / "ai_generation_record.json"
    ai_record_path.write_text(json.dumps(ai_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    source_evidence = [
        {
            "sourceDocument": item.get("document"),
            "section": item.get("section"),
            "claim": item.get("claim"),
            "sha256": item.get("sha256"),
        }
        for item in kac_execution.get("sourceEvidence", [])
    ]
    response = {
        "schemaVersion": "4.0",
        "product": "수페스타 ESG 지식행동 AI",
        "executionState": "COMPLETED",
        "status": final_result.get("status", "STOP"),
        "summary": final_result.get("summary", "실행 결과를 만들지 못했습니다."),
        "userGuidance": user_guidance,
        "route": route,
        "routeLabel": ROUTE_LABELS.get(route, route),
        "selectedRunSkill": selected_skill,
        "compositeExecution": {
            "directEntryPoint": True,
            "runComposite": COMPOSITE_RUN_SKILL,
            "runtimeCompositeVersion": composite_result.get("runtimeCompositeVersion"),
            "runId": composite_result.get("runId"),
            "singleEntryPointVerified": composite_record.get("singleEntryPoint") is True,
            "exactlyOneRouteSelected": composite_record.get("routePartition", {}).get("exactlyOneRouteSelected") is True,
            "routerExecutionCount": composite_record.get("members", {}).get("routerExecutionCount"),
            "domainExecutionCount": composite_record.get("members", {}).get("domainExecutionCount"),
            "priorSealedCompositeVersion": composite_record.get("provenance", {}).get("priorSealedCompositeVersion"),
            "formalV2Mutation": composite_record.get("provenance", {}).get("formalV2Mutation"),
        },
        "question": question,
        "conversationContinuity": payload.get("conversationContinuity", {}),
        "demoContext": "사용자가 제공하지 않은 조직·활동·증거는 추정하지 않습니다. 실제 인증·법률·세무·거래 효력을 확정하지 않습니다.",
        "answerMode": ai_status.get("mode"),
        "aiRuntime": ai_status,
        "outputRiskGate": ai_status.get("outputRiskGate"),
        "contextExtraction": context_extraction,
        "kacExecution": kac_execution,
        "marketLinkAllowed": market_allowed,
        "evidence": [*source_evidence, *final_result.get("evidence", [])],
        "missingEvidence": final_result.get("missingEvidence", []),
        "nextActions": final_result.get("nextActions", []),
        "data": final_result.get("data", {}),
        "artifacts": _artifact_previews(final_output_dir),
        "trace": trace,
        "inputEvidence": {
            "sha256": input_sha,
            "bytesPreservedAcrossRouterAndSelectedSkill": input_preserved,
            "bytesPreservedAcrossRuntimeComposite": input_preserved,
        },
        "runRecord": {
            "runRoot": str(run_root.relative_to(PROJECT_ROOT)),
            "compositeRecord": str((composite_dir / "composite_run_record.json").relative_to(PROJECT_ROOT)),
            "compositeRecordSha256": composite["recordSha256"],
            "compositeResult": str((composite_dir / "result.json").relative_to(PROJECT_ROOT)),
            "compositeResultSha256": composite["resultSha256"],
            "routerRecord": composite_result.get("paths", {}).get("routerRecord"),
            "selectedRecord": composite_result.get("paths", {}).get("selectedRecord"),
            "kacExecution": str(kac_path.relative_to(PROJECT_ROOT)),
            "kacExecutionSha256": kac_sha,
            "contextExtraction": str(context_extraction_path.relative_to(PROJECT_ROOT)),
            "contextExtractionSha256": _sha(context_extraction_path),
            "aiGenerationRecord": str(ai_record_path.relative_to(PROJECT_ROOT)),
            "aiGenerationRecordSha256": _sha(ai_record_path),
        },
        "safetyBoundary": "사용자가 명시한 사실만 구조화 입력으로 승격합니다. REVIEW·STOP 또는 고위험 거래 경로에서는 모델 문장을 사용하지 않으며, AI는 PROCEED 결과에서도 출력 위험 게이트를 통과한 표현만 제공합니다. 거래·결제·등록부 변경·법률·세무·인증 최종판정은 실행하지 않습니다.",
    }
    response_path = run_root / "orchestrator_response.json"
    response_path.write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    response["runRecord"]["orchestratorResponse"] = str(response_path.relative_to(PROJECT_ROOT))
    response["runRecord"]["orchestratorResponseSha256"] = _sha(response_path)
    return response


def health_payload() -> dict[str, Any]:
    v2_candidates = sorted(
        (PROJECT_ROOT / "ccs_composite_authoring/supestar_forest_esg_orchestrator_v2/_skill").glob(
            "supestar-forest-esg-orchestrator*_skill/SKILL.md"
        )
    )
    v2_skill = v2_candidates[0] if v2_candidates else Path("/__missing_supestar_v2_skill__")
    v1_skill = (
        PROJECT_ROOT
        / "ccs_composite_authoring/supestar_forest_esg_orchestrator_v1"
        / "_skill/supestar-forest-esg-orchestrator_skill/SKILL.md"
    )
    knowledge_status = KNOWLEDGE_RUNTIME.status()
    ai_status = AI_RUNTIME.status()
    runtime_composite_ready = (
        COMPOSITE_RUNNER.is_file()
        and COMPOSITE_REGISTRY.is_file()
        and COMPOSITE_SKILL.is_file()
    )
    atomic_layer_ready = ATOMIC_RUNNER.is_file() and ATOMIC_REGISTRY.is_file()
    core_ready = (
        runtime_composite_ready
        and atomic_layer_ready
        and STATIC_ROOT.is_dir()
        and knowledge_status["ready"]
    )
    return {
        "status": "ok" if core_ready else "degraded",
        "compositeExecutionMode": "DIRECT_SINGLE_ENTRYPOINT",
        "runtimeCompositeReady": runtime_composite_ready,
        "runtimeComposite": COMPOSITE_RUN_SKILL,
        "runtimeCompositeVersion": "0.3.0",
        "contextExtractionMode": "DETERMINISTIC_USER_STATEMENT_ONLY",
        "contextExtractionVersion": "1.0",
        "outputRiskGateMode": "VERDICT_AND_CLAIM_GATED",
        "compositeRunnerReady": COMPOSITE_RUNNER.is_file(),
        "compositeRegistryReady": COMPOSITE_REGISTRY.is_file(),
        "compositeSkillReady": COMPOSITE_SKILL.is_file(),
        "atomicRunnerReady": ATOMIC_RUNNER.is_file(),
        "atomicRegistryReady": ATOMIC_REGISTRY.is_file(),
        "staticReady": (STATIC_ROOT / "index.html").is_file(),
        "knowledgeRuntime": knowledge_status,
        "aiRuntime": ai_status,
        "priorSealedCompositeSkill": str((v2_skill if v2_skill.is_file() else v1_skill).relative_to(PROJECT_ROOT)),
        "priorSealedCompositeSkillPresent": v2_skill.is_file() or v1_skill.is_file(),
        "runtimeBoundary": "one Runtime Composite entry executes routing, query-specific KAC, and at most one domain Run Skill; optional local or server-side AI only verbalizes the verified result; no external transaction or registry mutation",
    }


class SupestarHandler(BaseHTTPRequestHandler):
    server_version = "SupestarRuntime/1.0"

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self._security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, request_path: str) -> None:
        relative = "index.html" if request_path in {"", "/"} else unquote(request_path.lstrip("/"))
        candidate = (STATIC_ROOT / relative).resolve()
        try:
            candidate.relative_to(STATIC_ROOT.resolve())
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not candidate.is_file():
            candidate = STATIC_ROOT / "index.html"
        raw = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"}:
            content_type += "; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-cache")
        self._security_headers()
        self.end_headers()
        self.wfile.write(raw)

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'",
        )

    def _rate_allowed(self) -> bool:
        address = self.client_address[0]
        now = time.monotonic()
        with _rate_lock:
            events = _rate_events[address]
            while events and now - events[0] >= RATE_WINDOW_SECONDS:
                events.popleft()
            if len(events) >= RATE_REQUESTS_PER_WINDOW:
                return False
            events.append(now)
            return True

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json(HTTPStatus.OK, health_payload())
            return
        self._serve_static(path)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/api/chat":
            self._json(HTTPStatus.NOT_FOUND, {"status": "error", "error": "not found"})
            return
        if not self._rate_allowed():
            self._json(HTTPStatus.TOO_MANY_REQUESTS, {"status": "error", "error": "요청이 너무 많습니다. 잠시 후 다시 시도해 주세요."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_REQUEST_BYTES:
                raise ValueError("request body size is invalid")
            raw = self.rfile.read(length)
            request = json.loads(raw.decode("utf-8"))
            if not isinstance(request, dict):
                raise ValueError("JSON object required")
            result = orchestrate(request)
        except (ValueError, json.JSONDecodeError) as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"status": "error", "error": str(exc)})
            return
        except (OSError, RuntimeError) as exc:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"status": "error", "error": str(exc)})
            return
        self._json(HTTPStatus.OK, result)

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write(
            f"[{datetime.now(KST).isoformat(timespec='seconds')}] " + format % args + "\n"
        )


def create_server(host: str, port: int) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), SupestarHandler)
    server.daemon_threads = True
    return server


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the Supestar forest ESG web runtime.")
    parser.add_argument("--host", default=os.environ.get("SUPESTAR_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("SUPESTAR_PORT", "4173")))
    args = parser.parse_args()
    server = create_server(args.host, args.port)
    print(f"Supestar running at http://{args.host}:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Conservative conversation-continuity policy for Supestar.

The current question is always independent unless it explicitly points back to
earlier user-provided context.  Question length alone is never evidence of a
follow-up.
"""

from __future__ import annotations

import re
from typing import Any


CROSS_TURN_MARKERS = (
    "앞에서",
    "앞서",
    "아까",
    "방금",
    "위에서",
    "이어서",
)

REFERENCE_MARKERS = (
    "그건",
    "그게",
    "그것",
    "그내용",
    "이내용",
    "그차이",
    "그배출원",
    "이배출원",
    "해당배출원",
    "그사업",
    "이사업",
    "해당사업",
    "그크레딧",
    "이크레딧",
    "해당크레딧",
    "그문서",
    "이문서",
    "해당문서",
    "그절차",
    "이절차",
)

# A deictic phrase can point to an entity introduced earlier in the same
# question.  Treating every occurrence as a cross-turn reference contaminates
# a self-contained question with unrelated chat history.  These anchors are
# intentionally concrete: if the current question already names the entity or
# activity, it is safer to route from the current question alone.
EMISSION_SOURCE_ANCHORS = (
    "보일러", "연소", "도시가스", "천연가스", "경유", "휘발유", "차량", "냉매",
    "전력", "스팀", "열사용", "공정", "폐기물", "사용량", "nm³", "kwh",
)
PROJECT_ANCHORS = (
    "프로젝트", "산림", "조림", "식재", "감축", "등록", "인증", "추진", "사업계획",
)
CREDIT_ANCHORS = ("크레딧", "배출권", "상쇄", "구매", "발급", "소각", "vcm", "ccm")
DOCUMENT_ANCHORS = ("보고서", "고지서", "인증서", "계약서", "명세서", "파일", "문서")
PROCEDURE_ANCHORS = ("등록", "인증", "검증", "거래", "소각", "신청", "단계", "절차")

LOCAL_ANTECEDENT_ANCHORS = {
    "그배출원": EMISSION_SOURCE_ANCHORS,
    "이배출원": EMISSION_SOURCE_ANCHORS,
    "해당배출원": EMISSION_SOURCE_ANCHORS,
    "그사업": PROJECT_ANCHORS,
    "이사업": PROJECT_ANCHORS,
    "해당사업": PROJECT_ANCHORS,
    "그크레딧": CREDIT_ANCHORS,
    "이크레딧": CREDIT_ANCHORS,
    "해당크레딧": CREDIT_ANCHORS,
    "그문서": DOCUMENT_ANCHORS,
    "이문서": DOCUMENT_ANCHORS,
    "해당문서": DOCUMENT_ANCHORS,
    "그절차": PROCEDURE_ANCHORS,
    "이절차": PROCEDURE_ANCHORS,
}

COMPLETED_LOCAL_CLAUSE_MARKERS = (
    "합니다",
    "했습니다",
    "있습니다",
    "입니다",
    "됩니다",
    "보유하고",
    "사용하고",
    "연소하고",
    "운영하고",
    "추진하고",
)

CONTINUATION_ONLY = {
    "왜요",
    "왜그런가요",
    "더알려줘",
    "더알려주세요",
    "계속해줘",
    "계속해주세요",
    "예시는요",
    "실제사례는요",
    "그러면왜요",
    "그럼왜요",
    "그러면왜중요한가요",
    "그럼왜중요한가요",
}


def compact(text: str) -> str:
    return re.sub(r"\s+", "", str(text)).lower().rstrip("?.!~")


def _has_local_antecedent(normalized: str, marker: str) -> bool:
    """Return True when the reference is resolved inside this question."""

    marker_index = normalized.find(marker)
    if marker_index < 0:
        return False

    prefix = normalized[:marker_index]
    anchors = tuple(anchor.lower() for anchor in LOCAL_ANTECEDENT_ANCHORS.get(marker, ()))
    if anchors and any(anchor in prefix for anchor in anchors):
        return True

    # Support a self-contained form that starts with the deictic noun but then
    # supplies several concrete facts, e.g. "이 배출원은 사업장 보일러에서
    # 도시가스를 연소합니다."  One generic keyword is not enough.
    suffix = normalized[marker_index + len(marker):]
    if marker_index == 0 and anchors:
        matched = {anchor for anchor in anchors if anchor in suffix}
        if len(matched) >= 2:
            return True

    # Generic phrases such as "그건" may also refer to a full statement made
    # earlier in the same question.  Require a substantive completed clause so
    # a short unresolved follow-up still uses the previous user message.
    return len(prefix) >= 12 and any(token in prefix for token in COMPLETED_LOCAL_CLAUSE_MARKERS)


def is_explicit_follow_up(question: str) -> bool:
    normalized = compact(question)
    if normalized in CONTINUATION_ONLY:
        return True
    if any(marker in normalized for marker in CROSS_TURN_MARKERS):
        return True

    for marker in REFERENCE_MARKERS:
        if marker not in normalized:
            continue
        if not _has_local_antecedent(normalized, marker):
            return True
    return False


def prior_user_messages(history: list[dict[str, Any]] | None, limit: int = 1) -> list[dict[str, str]]:
    safe_history = history if isinstance(history, list) else []
    selected = [
        {"role": "user", "content": str(item.get("content", "")).strip()[:2_000]}
        for item in safe_history
        if isinstance(item, dict)
        and item.get("role") == "user"
        and str(item.get("content", "")).strip()
    ]
    return selected[-max(1, limit):]


def relevant_user_history(
    question: str,
    history: list[dict[str, Any]] | None,
    limit: int = 1,
) -> list[dict[str, str]]:
    if not is_explicit_follow_up(question):
        return []
    return prior_user_messages(history, limit=limit)


def effective_question(question: str, history: list[dict[str, Any]] | None) -> tuple[str, int]:
    relevant = relevant_user_history(question, history, limit=1)
    if not relevant:
        return question, 0
    return f"{relevant[-1]['content']} / {question}", 1

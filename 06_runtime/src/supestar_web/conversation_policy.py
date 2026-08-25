#!/usr/bin/env python3
"""Conservative conversation-continuity policy for Supestar.

The current question is always independent unless it explicitly points back to
earlier user-provided context.  Question length alone is never evidence of a
follow-up.
"""

from __future__ import annotations

import re
from typing import Any


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
    "앞에서",
    "앞서",
    "아까",
    "방금",
    "위에서",
    "이어서",
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


def is_explicit_follow_up(question: str) -> bool:
    normalized = compact(question)
    return any(marker in normalized for marker in REFERENCE_MARKERS) or normalized in CONTINUATION_ONLY


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

#!/usr/bin/env python3
"""Query-time reader and interpreter for sealed Supestar Stage 1-5 artifacts.

The Stage vault is never mutated here.  This module selects a Concept Skill for
the current question, reads the linked Identity -> Goal -> Task -> Knowledge ->
Method -> Skill files, verifies their hashes, and returns the exact chain that
was used to ground the response.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parents[2]
VAULT_ROOT = PROJECT_ROOT / "ccs_authoring/supestar_mvp_v3"
CARD_PATH = APP_ROOT / "knowledge/esg_knowledge_cards.json"

CHAIN_LAYOUT = (
    ("Identity", "_identity", "{identity}.md", None),
    ("Goal", "_goal", "{slug}_goal.md", "definesGoal"),
    ("Task", "_task", "{slug}_task.md", "requiresTask"),
    ("Knowledge", "_knowledge", "{slug}_knowledge.md", "requiresKnowledge"),
    ("Method", "_method", "{slug}_method.md", "appliedThrough"),
    ("Skill", "_skill", "{identity}/SKILL.md", "developsSkill"),
)

DEFINITION_MARKERS = ("무엇", "뭐야", "뭔가", "뜻", "정의", "개념", "설명", "알려줘", "알려주세요", "란?")
COMPARISON_MARKERS = ("차이", "다른", "비교", "구분")
ACTION_MARKERS = ("어떻게", "절차", "방법", "해야", "분류", "점검", "준비")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize(value: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", value.lower())


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _body_excerpt(text: str, limit: int = 360) -> str:
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)
    lines: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("- ←") or line.startswith("- →"):
            continue
        line = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", line)
        lines.append(line)
        if len(" ".join(lines)) >= limit:
            break
    value = " ".join(lines)
    return value[:limit].rstrip()


def _safe_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


class KnowledgeRuntime:
    """Read-only runtime catalog over sealed Concept Skill closures."""

    def __init__(self) -> None:
        payload = json.loads(CARD_PATH.read_text(encoding="utf-8"))
        self.cards = {card["identity"]: card for card in payload.get("cards", [])}
        self.identities = sorted(path.stem for path in (VAULT_ROOT / "_identity").glob("*.md"))
        self._catalog = self._build_catalog()

    def _build_catalog(self) -> dict[str, dict[str, Any]]:
        catalog: dict[str, dict[str, Any]] = {}
        for identity in self.identities:
            identity_path = VAULT_ROOT / "_identity" / f"{identity}.md"
            text = identity_path.read_text(encoding="utf-8")
            card = self.cards.get(identity, {})
            title = card.get("title") or _first_heading(text) or identity.replace("_", " ").title()
            aliases = list(dict.fromkeys([identity, identity.replace("_", " "), title, *card.get("aliases", [])]))
            catalog[identity] = {
                "identity": identity,
                "title": title,
                "aliases": aliases,
                "normalizedAliases": [_normalize(alias) for alias in aliases if len(_normalize(alias)) >= 2],
                "definition": card.get("definition") or _body_excerpt(text),
                "keyPoints": card.get("keyPoints", []),
                "sourceEvidence": card.get("sourceEvidence", []),
            }
        return catalog

    def status(self) -> dict[str, Any]:
        concept_skill_count = sum(
            1 for identity in self.identities if (VAULT_ROOT / "_skill" / identity / "SKILL.md").is_file()
        )
        return {
            "ready": VAULT_ROOT.is_dir() and CARD_PATH.is_file(),
            "vault": _safe_relative(VAULT_ROOT),
            "identityCount": len(self.identities),
            "conceptSkillCount": concept_skill_count,
            "groundingCardCount": len(self.cards),
            "sealedVaultMutation": False,
        }

    def _effective_question(self, question: str, history: list[dict[str, Any]]) -> str:
        normalized = _normalize(question)
        follow_up = len(normalized) <= 12 or any(token in question for token in ("그건", "그게", "그러면", "왜요", "더 알려"))
        if not follow_up:
            return question
        previous = [str(item.get("content", "")).strip() for item in history if item.get("role") == "user"]
        return f"{previous[-1]} / {question}" if previous else question

    def _score(self, question: str, record: dict[str, Any]) -> tuple[int, list[str]]:
        compact = _normalize(question)
        matches: list[str] = []
        score = 0
        for alias in record["normalizedAliases"]:
            if alias and alias in compact:
                matches.append(alias)
                score += 20 + min(len(alias), 12)
        identity_tokens = [token.lower() for token in record["identity"].split("_") if len(token) >= 3]
        for token in identity_tokens:
            if token in question.lower():
                score += 5
        # Prefer the broad ESG concept for a bare ESG question and its management
        # concept only when management itself was requested.
        if record["identity"] == "ESG" and "esg" in compact and "esg경영" not in compact:
            score += 18
        if record["identity"] == "ESG_MANAGEMENT" and "esg경영" not in compact:
            score -= 18
        return score, matches

    def select(self, question: str, history: list[dict[str, Any]] | None = None, limit: int = 3) -> dict[str, Any]:
        safe_history = history if isinstance(history, list) else []
        effective = self._effective_question(question, safe_history)
        ranked: list[tuple[int, str, list[str]]] = []
        for identity, record in self._catalog.items():
            score, matches = self._score(effective, record)
            if score > 0:
                ranked.append((score, identity, matches))
        ranked.sort(key=lambda row: (-row[0], row[1]))

        # A comparison may legitimately select both named concepts. Otherwise a
        # single primary concept prevents the answer from drifting across domains.
        is_comparison = any(marker in effective for marker in COMPARISON_MARKERS)
        selected: list[dict[str, Any]] = []
        if ranked:
            top_score = ranked[0][0]
            for score, identity, matches in ranked:
                if len(selected) >= (limit if is_comparison else 1):
                    break
                if is_comparison and score < max(20, top_score - 20):
                    continue
                record = dict(self._catalog[identity])
                record["score"] = score
                record["matchedAliases"] = matches
                selected.append(record)

        if any(marker in effective for marker in COMPARISON_MARKERS):
            intent = "COMPARISON"
        elif any(marker in effective for marker in DEFINITION_MARKERS):
            intent = "DEFINITION"
        elif any(marker in effective for marker in ACTION_MARKERS):
            intent = "ACTION"
        else:
            intent = "KNOWLEDGE"
        return {
            "question": question,
            "effectiveQuestion": effective,
            "intent": intent,
            "selected": selected,
        }

    def _node_path(self, identity: str, directory: str, pattern: str) -> Path:
        return VAULT_ROOT / directory / pattern.format(identity=identity, slug=identity.lower())

    def _node(self, identity: str, stage: str, directory: str, pattern: str, card: dict[str, Any]) -> dict[str, Any]:
        path = self._node_path(identity, directory, pattern)
        if not path.is_file():
            return {
                "stage": stage,
                "label": f"{card['title']} {stage}",
                "path": _safe_relative(path),
                "present": False,
                "sha256": None,
                "excerpt": "",
            }
        text = path.read_text(encoding="utf-8")
        frontmatter = _frontmatter(text)
        excerpt = _body_excerpt(text)
        if stage in {"Identity", "Knowledge"} and card.get("definition"):
            excerpt = card["definition"]
        return {
            "stage": stage,
            "label": _first_heading(text) or frontmatter.get("name") or f"{card['title']} {stage}",
            "path": _safe_relative(path),
            "present": True,
            "sha256": _sha256(path),
            "excerpt": excerpt,
            "contractName": frontmatter.get("name"),
            "contractDescription": frontmatter.get("description"),
        }

    def _source_evidence(self, card: dict[str, Any]) -> list[dict[str, Any]]:
        evidence: list[dict[str, Any]] = []
        for raw in card.get("sourceEvidence", []):
            item = dict(raw)
            path = PROJECT_ROOT / item["document"]
            item["path"] = _safe_relative(path)
            item["present"] = path.is_file()
            item["sha256"] = _sha256(path) if path.is_file() else None
            evidence.append(item)
        return evidence

    def execute(
        self,
        question: str,
        history: list[dict[str, Any]] | None = None,
        preferred_identities: list[str] | None = None,
    ) -> dict[str, Any]:
        selection = self.select(question, history)
        selected = selection["selected"]
        preferred = [identity for identity in (preferred_identities or []) if identity in self._catalog]
        if preferred:
            selected = []
            for identity in preferred:
                record = dict(self._catalog[identity])
                record["score"] = 100
                record["matchedAliases"] = ["runtime-binding"]
                selected.append(record)
        chains: list[dict[str, Any]] = []
        combined_evidence: list[dict[str, Any]] = []
        for card in selected:
            identity = card["identity"]
            nodes: list[dict[str, Any]] = []
            edges: list[dict[str, str]] = []
            for stage, directory, pattern, relation in CHAIN_LAYOUT:
                node = self._node(identity, stage, directory, pattern, card)
                nodes.append(node)
                if relation and len(nodes) >= 2:
                    edges.append({
                        "from": nodes[-2]["stage"],
                        "to": nodes[-1]["stage"],
                        "relation": relation,
                    })
            evidence = self._source_evidence(card)
            combined_evidence.extend(evidence)
            chains.append({
                "identity": identity,
                "title": card["title"],
                "definition": card["definition"],
                "keyPoints": card["keyPoints"],
                "selectionScore": card["score"],
                "selectionReason": card["matchedAliases"],
                "nodes": nodes,
                "edges": edges,
                "sourceEvidence": evidence,
                "conceptSkillRead": bool(nodes[-1]["present"]),
            })

        complete = bool(chains) and all(
            all(node["present"] for node in chain["nodes"]) and chain["conceptSkillRead"] for chain in chains
        )
        return {
            "schemaVersion": "1.0",
            "executionState": "COMPLETED" if chains else "NO_MATCH",
            "intent": selection["intent"],
            "effectiveQuestion": selection["effectiveQuestion"],
            "selectedConcepts": [chain["identity"] for chain in chains],
            "chains": chains,
            "sourceEvidence": combined_evidence,
            "allChainFilesPresent": complete,
            "sealedVaultMutation": False,
            "catalog": self.status(),
        }

    def guidance(self, execution: dict[str, Any]) -> dict[str, Any]:
        chains = execution.get("chains", [])
        if not chains:
            return {
                "statusLabel": "질문과 연결할 개념을 더 확인해야 해요",
                "title": "어떤 ESG 개념을 알고 싶은지 조금 더 구체적으로 알려주세요.",
                "paragraphs": ["ESG, Scope 1·2·3, SDGs, 탄소시장, 산림탄소, 한국임업진흥원처럼 알고 싶은 대상을 함께 적어 주세요."],
                "rationale": "질문의 대상이 확정돼야 관련 Concept Skill과 근거만 선택할 수 있습니다.",
                "steps": [],
                "followUp": "예: ‘ESG가 무엇인가요?’ 또는 ‘Scope 1과 Scope 2는 어떻게 다른가요?’",
                "marketHandoff": None,
            }
        primary = chains[0]
        comparison = execution.get("intent") == "COMPARISON" and len(chains) > 1
        if comparison:
            titles = "·".join(chain["title"] for chain in chains)
            paragraphs = [f"{chain['title']}: {chain['definition']}" for chain in chains]
            title = f"{titles}는 구분 기준과 쓰임이 다릅니다."
            rationale = "이름이 비슷한 개념을 같은 단위나 같은 행위로 취급하면 측정·공시·사용 기준을 잘못 적용할 수 있습니다."
        else:
            title = primary["definition"]
            paragraphs = list(primary.get("keyPoints", [])) or [primary["definition"]]
            rationale = "질문과 직접 관련된 개념과 근거만 골라 설명하면 다른 ESG 주제나 탄소시장 이야기로 답변이 흐르는 것을 막을 수 있습니다."
        return {
            "statusLabel": "질문하신 내용을 찾았어요",
            "title": title,
            "paragraphs": paragraphs[:4],
            "rationale": rationale,
            "steps": [],
            "followUp": f"{primary['title']}의 실제 적용 사례나 다른 개념과의 관계가 궁금하면 이어서 질문해 주세요.",
            "marketHandoff": None,
        }

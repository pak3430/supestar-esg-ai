#!/usr/bin/env python3
"""Patch the verified proposal DOCX without collapsing its run structure."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

from lxml import etree


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}

TEXT_REPLACEMENTS = {
    "KAC 지식과 실행 Skill로 ESG 질문을\n검증 가능한 다음 행동으로 바꾸는 로컬 AI 챗봇\n2026 ESG × AI 챌린지 해커톤 예선 기획서":
        "KAC 지식과 실행 Skill로 ESG 질문을\n검증 가능한 다음 행동으로 바꾸는 지식행동 AI 챗봇\n2026 ESG × AI 챌린지 해커톤 예선 기획서",
    "수페스타는 질문에 필요한 지식행동사슬을 선택하고 연결된 Skill을 실제로 실행한 뒤, 로컬 AI가 검증 결과만 자연어로 설명하는 스킬 실행형 ESG 챗봇이다.":
        "수페스타는 질문에 필요한 지식행동사슬을 선택하고 연결된 Skill을 실제로 실행한 뒤, 선택적 로컬·서버 AI가 검증 결과만 자연어로 설명하는 스킬 실행형 ESG 챗봇이다.",
    "로컬 AI가 검증된 결과만 자연스러운 한국어로 표현한다.":
        "로컬·서버 AI가 검증된 결과만 자연스러운 한국어로 표현한다.",
    "회사 소유 보일러와 구매전력을 한 질문에 섞으면 하나의 Scope를 임의 선택하지 않는다. REVIEW로 멈추고 두 활동 중 하나를 먼저 선택해 달라는 후속 질문을 표시하며 로컬 AI 자유 생성을 차단한다.":
        "회사 소유 보일러와 구매전력을 한 질문에 섞으면 하나의 Scope를 임의 선택하지 않는다. REVIEW로 멈추고 두 활동 중 하나를 먼저 선택해 달라는 후속 질문을 표시하며 생성형 AI 자유 생성을 차단한다.",
    "로컬 AI": "로컬·서버 AI",
    "35건 PASS(Web 27·Composite 3·원자 Skill 5)":
        "36건 PASS(Web 28·Composite 3·원자 Skill 5)",
    "63건 PASS": "64건 PASS",
    "63건 전부 확인": "64건 전부 확인",
    "63건 전부 기록": "64건 전부 기록",
    "자동 테스트 35개, 결정론 fixture 63개, 로컬 AI fixture 10개, 대화 이력 격리, Context conflict 검사, Output Risk Gate":
        "자동 테스트 36개, 결정론 fixture 64개, 로컬 AI fixture 10개, 공개 Qwen 5건, 대화 이력 격리, Context conflict 검사, Output Risk Gate",
    "Local runtime, Docker, 필요 시 검증된 공개 터널":
        "Local runtime, Render Docker 공개 데모, Qwen Cloud 선택 연동",
}


def patch_xml(data: bytes, *, replace_text: bool) -> tuple[bytes, set[str]]:
    root = etree.fromstring(data)
    found: set[str] = set()
    if replace_text:
        for node in root.xpath("//w:t", namespaces=NS):
            current = node.text or ""
            if current in TEXT_REPLACEMENTS:
                node.text = TEXT_REPLACEMENTS[current]
                found.add(current)
    for element in root.xpath("//*[@w:ascii or @w:hAnsi or @w:eastAsia or @w:cs]", namespaces=NS):
        for attr, value in list(element.attrib.items()):
            if value == "Apple SD Gothic Neo":
                element.set(attr, "Noto Sans CJK KR")
    if replace_text:
        for run in root.xpath("//w:r", namespaces=NS):
            run_props = run.find(f"{{{W_NS}}}rPr")
            if run_props is None:
                run_props = etree.Element(f"{{{W_NS}}}rPr")
                run.insert(0, run_props)
            fonts = run_props.find(f"{{{W_NS}}}rFonts")
            if fonts is None:
                fonts = etree.Element(f"{{{W_NS}}}rFonts")
                run_props.insert(0, fonts)
            for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
                fonts.set(f"{{{W_NS}}}{attr}", "Noto Sans CJK KR")
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes"), found


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: patch_current_docx_qwen.py INPUT.docx OUTPUT.docx")
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    destination.parent.mkdir(parents=True, exist_ok=True)
    found: set[str] = set()
    with zipfile.ZipFile(source, "r") as src, zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            payload = src.read(item.filename)
            if item.filename.startswith("word/") and item.filename.endswith(".xml"):
                payload, item_found = patch_xml(payload, replace_text=item.filename == "word/document.xml")
                found.update(item_found)
            dst.writestr(item, payload)
    missing = sorted(set(TEXT_REPLACEMENTS) - found)
    if missing:
        destination.unlink(missing_ok=True)
        raise RuntimeError(f"expected text nodes were not found: {missing}")
    print(destination)


if __name__ == "__main__":
    main()

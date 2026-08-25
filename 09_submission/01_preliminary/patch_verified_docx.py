#!/usr/bin/env python3
"""Patch the last visually verified DOCX while preserving its proven layout/fonts."""

from __future__ import annotations

import copy
import sys
import zipfile
from pathlib import Path

from lxml import etree


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W_NS}
REPO_REL_ID = "rIdSupestarRepo"
REPO_URL = "https://github.com/pak3430/supestar-esg-ai"


REPLACEMENTS = {
    "이전 AI 답변을 사실로 재사용하지 않음": (
        "새 주제 격리·명시적 후속만 직전 사용자 발화 1개 사용; AI 답변 재사용 안 함"
    ),
    "단위·통합 테스트": "자동 테스트",
    "23건 PASS": "35건 PASS(Web 27·Composite 3·원자 Skill 5)",
    "60건 PASS": "63건 PASS",
    "8건 PASS": "10건 PASS",
    "60건 전부 확인": "63건 전부 확인",
    "60건 전부 기록": "63건 전부 기록",
    (
        "검증 범위에는 Scope 1·2·3 세부 활동, 부정문, 활동 혼합, 이전 대화 오염, "
        "등록·절차 상태 충돌, E/S/G 증거 누락, 거래 G1~G11, 실시간 가격·투자추천·"
        "배출계수 없는 계산, 프롬프트 우회와 가짜 증거 요청이 포함된다."
    ): (
        "검증 범위에는 Scope 1·2·3 세부 활동, 부정문, 활동 혼합, 이전 대화 오염, "
        "새 주제 격리와 명시적 후속 질문, 등록·절차 상태 충돌, E/S/G 증거 누락, "
        "거래 G1~G11, 실시간 가격·투자추천·배출계수 없는 계산, 프롬프트 우회와 "
        "가짜 증거 요청이 포함된다."
    ),
    (
        "unittest, 60개 결정론 fixture, 8개 로컬 AI fixture, Context conflict 검사, "
        "Output Risk Gate"
    ): (
        "자동 테스트 35개, 결정론 fixture 63개, 로컬 AI fixture 10개, 대화 이력 격리, "
        "Context conflict 검사, Output Risk Gate"
    ),
}


def paragraph_text(paragraph: etree._Element) -> str:
    return "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))


def replace_paragraph_text(paragraph: etree._Element, text: str) -> None:
    nodes = paragraph.xpath(".//w:t", namespaces=NS)
    if not nodes:
        raise RuntimeError("paragraph has no text node")
    nodes[0].text = text
    for node in nodes[1:]:
        node.text = ""


def patch_document_xml(data: bytes) -> bytes:
    root = etree.fromstring(data)
    found: set[str] = set()
    repo_inserted = False

    for paragraph in list(root.xpath("//w:p", namespaces=NS)):
        current = paragraph_text(paragraph)
        if current in REPLACEMENTS:
            replace_paragraph_text(paragraph, REPLACEMENTS[current])
            found.add(current)

        if current.startswith("Knowledge-Action Chain  https://github.com/sopia19910/"):
            repo_paragraph = copy.deepcopy(paragraph)
            repo_nodes = repo_paragraph.xpath(".//w:t", namespaces=NS)
            hyperlink_nodes = repo_paragraph.xpath(".//w:hyperlink//w:t", namespaces=NS)
            hyperlinks = repo_paragraph.xpath(".//w:hyperlink", namespaces=NS)
            if len(repo_nodes) < 3 or not hyperlink_nodes or not hyperlinks:
                raise RuntimeError("unexpected source hyperlink paragraph structure")
            for node in repo_nodes:
                node.text = ""
            repo_nodes[0].text = "수페스타 프로젝트 공개 저장소"
            repo_nodes[1].text = "  "
            hyperlink_nodes[0].text = REPO_URL
            hyperlinks[0].set(f"{{{R_NS}}}id", REPO_REL_ID)
            paragraph.addprevious(repo_paragraph)
            repo_inserted = True

    missing = sorted(set(REPLACEMENTS) - found)
    if missing:
        raise RuntimeError(f"expected paragraphs were not found: {missing}")
    if not repo_inserted:
        raise RuntimeError("Knowledge-Action Chain source paragraph was not found")

    return etree.tostring(
        root,
        xml_declaration=True,
        encoding="UTF-8",
        standalone="yes",
    )


def patch_relationships_xml(data: bytes) -> bytes:
    root = etree.fromstring(data)
    existing = root.xpath(f"./pr:Relationship[@Id='{REPO_REL_ID}']", namespaces={"pr": PKG_REL_NS})
    if not existing:
        etree.SubElement(
            root,
            f"{{{PKG_REL_NS}}}Relationship",
            Id=REPO_REL_ID,
            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
            Target=REPO_URL,
            TargetMode="External",
        )
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: patch_verified_docx.py VERIFIED.docx OUTPUT.docx")

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    destination.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source, "r") as src, zipfile.ZipFile(
        destination, "w", zipfile.ZIP_DEFLATED
    ) as dst:
        for item in src.infolist():
            payload = src.read(item.filename)
            if item.filename == "word/document.xml":
                payload = patch_document_xml(payload)
            elif item.filename == "word/_rels/document.xml.rels":
                payload = patch_relationships_xml(payload)
            dst.writestr(item, payload)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Remove local absolute image paths from generated PPTX description metadata."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path


def sanitize(source: Path, target: Path) -> int:
    changed = 0
    with zipfile.ZipFile(source, "r") as src, zipfile.ZipFile(
        target, "w", compression=zipfile.ZIP_DEFLATED
    ) as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename.endswith((".xml", ".rels")):
                text = data.decode("utf-8")
                text, count = re.subn(
                    r'descr="/Users/[^\"]+"',
                    'descr="embedded image"',
                    text,
                )
                changed += count
                data = text.encode("utf-8")
            dst.writestr(info, data)
    return changed


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: sanitize_pptx_metadata.py SOURCE.pptx TARGET.pptx")
    source = Path(sys.argv[1]).resolve()
    target = Path(sys.argv[2]).resolve()
    count = sanitize(source, target)
    if count == 0:
        raise SystemExit("No absolute image descriptions found")
    print(f"Sanitized {count} image description paths -> {target}")


if __name__ == "__main__":
    main()

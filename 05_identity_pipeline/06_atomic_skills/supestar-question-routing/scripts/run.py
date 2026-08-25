#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from supestar_skills import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main("supestar-question-routing"))


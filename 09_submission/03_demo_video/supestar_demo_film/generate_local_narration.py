#!/usr/bin/env python3
"""Generate scene-bounded Korean narration from src/scenes.ts using macOS Yuna."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCENES_TS = ROOT / "src" / "scenes.ts"
OUT_DIR = ROOT / "public" / "audio"
REPORT = ROOT / "out" / "narration_durations_2026-08-25.json"
RATES = (180, 190, 200, 210, 220, 230, 240)


def duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def read_scenes() -> list[dict[str, object]]:
    source = SCENES_TS.read_text(encoding="utf-8")
    pattern = re.compile(
        r"id:\s*'([^']+)'\s*,\s*durationSec:\s*(\d+)\s*,.*?"
        r"narration:\s*'((?:\\'|[^'])*)'\s*,",
        re.S,
    )
    scenes = []
    for scene_id, seconds, narration in pattern.findall(source):
        scenes.append(
            {
                "id": scene_id,
                "durationSec": int(seconds),
                "narration": narration.replace("\\'", "'").replace("\\\\", "\\"),
            }
        )
    if len(scenes) != 12:
        raise RuntimeError(f"Expected 12 scenes, found {len(scenes)}")
    return scenes


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with tempfile.TemporaryDirectory(prefix="supestar-narration-") as temp:
        temp_dir = Path(temp)
        for index, scene in enumerate(read_scenes(), start=1):
            allowed = float(scene["durationSec"]) - 0.9
            selected = None
            for rate in RATES:
                aiff = temp_dir / f"{index:02d}-{rate}.aiff"
                subprocess.run(
                    ["say", "-v", "Yuna", "-r", str(rate), "-o", str(aiff), str(scene["narration"])],
                    check=True,
                )
                spoken = duration(aiff)
                if spoken <= allowed:
                    selected = (rate, spoken, aiff)
                    break
            if selected is None:
                raise RuntimeError(f"Narration exceeds scene {index:02d} even at rate {RATES[-1]}")

            rate, spoken, aiff = selected
            target = OUT_DIR / f"{index:02d}.mp3"
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-i", str(aiff),
                    "-ar", "48000", "-ac", "2", "-codec:a", "libmp3lame", "-b:a", "192k",
                    str(target),
                ],
                check=True,
            )
            final_duration = duration(target)
            row = {
                "scene": index,
                "id": scene["id"],
                "sceneDurationSec": scene["durationSec"],
                "maxNarrationSec": round(allowed, 3),
                "voice": "Yuna",
                "rate": rate,
                "audioDurationSec": round(final_duration, 3),
                "fits": final_duration <= allowed,
            }
            rows.append(row)
            print(
                f"{index:02d} {scene['id']}: {final_duration:.2f}s / {allowed:.2f}s "
                f"(Yuna {rate}) {'PASS' if row['fits'] else 'FAIL'}"
            )

    REPORT.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not all(row["fits"] for row in rows):
        raise SystemExit(1)
    print(f"PASS: {len(rows)} scene narration files -> {OUT_DIR}")
    print(f"Report -> {REPORT}")


if __name__ == "__main__":
    main()

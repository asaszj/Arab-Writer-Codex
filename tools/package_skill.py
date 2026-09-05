#!/usr/bin/env python3
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/arab-writer"
OUT = ROOT / "arab-writer-codex.zip"

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(SKILL.rglob("*")):
        if p.is_file():
            z.write(p, arcname=str(Path("arab-writer") / p.relative_to(SKILL)))

print(OUT)

#!/usr/bin/env python3
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]; VERSION=(ROOT/'VERSION').read_text().strip(); SKILL=ROOT/'.agents/skills/arab-writer'; DIST=ROOT/'dist'; DIST.mkdir(exist_ok=True); OUT=DIST/f'arab-writer-skill-v{VERSION}.zip'
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(SKILL.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts: z.write(p,arcname=str(Path('arab-writer')/p.relative_to(SKILL)))
print(OUT)

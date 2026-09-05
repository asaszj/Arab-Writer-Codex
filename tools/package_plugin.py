#!/usr/bin/env python3
from pathlib import Path
import json, shutil, tempfile, zipfile
ROOT=Path(__file__).resolve().parents[1]; VERSION=(ROOT/'VERSION').read_text().strip(); SKILL=ROOT/'.agents/skills/arab-writer'; DIST=ROOT/'dist'; DIST.mkdir(exist_ok=True)
out=DIST/f'arab-writer-codex-plugin-v{VERSION}.zip'
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/'arab-writer-codex'; (p/'.codex-plugin').mkdir(parents=True); (p/'skills').mkdir()
    shutil.copytree(SKILL,p/'skills/arab-writer')
    m=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8')); m['skills']='./skills/'
    (p/'.codex-plugin/plugin.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copy2(ROOT/'LICENSE',p/'LICENSE'); shutil.copy2(ROOT/'README.md',p/'README.md')
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p.rglob('*')):
            if f.is_file(): z.write(f,arcname=str(f.relative_to(Path(td))))
print(out)

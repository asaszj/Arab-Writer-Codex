#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
try: m=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
except Exception as e: m={}; errors.append(f'invalid plugin.json: {e}')
version=(ROOT/'VERSION').read_text().strip() if (ROOT/'VERSION').exists() else ''
for k in ('name','version','description','skills'):
    if not m.get(k): errors.append(f'missing plugin field {k}')
if m.get('version')!=version: errors.append('plugin version must match VERSION')
if m.get('name')!='arab-writer-codex': errors.append('unexpected plugin name')
skills=m.get('skills','')
if skills.startswith('./'):
    if not (ROOT/skills[2:]).exists(): errors.append(f'plugin skills path not found: {skills}')
else: errors.append('plugin skills path must be relative and start ./')
if errors:
    print('FAILED'); [print('- '+e) for e in errors]; sys.exit(1)
print(f'OK: plugin manifest v{version} is valid.')

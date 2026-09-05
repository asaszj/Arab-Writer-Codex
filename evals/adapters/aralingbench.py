#!/usr/bin/env python3
"""Normalize an exported AraLingBench JSON/JSONL file into a simple evaluation stream."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def read(path):
    t=Path(path).read_text(encoding='utf-8').strip()
    if t.startswith('['): return json.loads(t)
    return [json.loads(x) for x in t.splitlines() if x.strip()]

def pick(r,*keys):
    for k in keys:
        if k in r and r[k] not in (None,''): return r[k]
    return ''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('output'); ap.add_argument('--limit',type=int); args=ap.parse_args(); out=[]
    for i,r in enumerate(read(args.input)):
        if args.limit and i>=args.limit: break
        out.append({"id":f"araling-{i+1}","source":"AraLingBench","question":pick(r,'question','prompt','query'),"choices":pick(r,'choices','options'),"gold":pick(r,'answer','gold','label'),"category":pick(r,'category','subject','task'),"difficulty":pick(r,'difficulty','level')})
    Path(args.output).write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in out)+'\n',encoding='utf-8'); print(len(out)); return 0
if __name__=='__main__': raise SystemExit(main())

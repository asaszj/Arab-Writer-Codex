#!/usr/bin/env python3
"""Convert QCRI Nahw-Passage.json into Arab Writer proofreading eval JSONL."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def convert(rows,limit=None):
    out=[]
    for i,r in enumerate(rows[:limit] if limit else rows):
        out.append({"id":f"nahw-passage-{r['passage_id']}-{i+1}","source":"Nahw-Passage","task":"دقق النص لغويًا وصحح الخطأ المحدد فقط مع أقل تغيير ممكن.","input":r['passage'],"target_error":r['error'],"target_correction":r['correction'],"explanation":r.get('explanation',''),"expected_mode":["proofread","high-fidelity"],"must_preserve":[],"must_not":["إعادة صياغة شاملة","إضافة حقائق"]})
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('output'); ap.add_argument('--limit',type=int); args=ap.parse_args(); rows=json.loads(Path(args.input).read_text(encoding='utf-8')); out=convert(rows,args.limit); Path(args.output).write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in out)+'\n',encoding='utf-8'); print(len(out)); return 0
if __name__=='__main__': raise SystemExit(main())

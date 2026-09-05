#!/usr/bin/env python3
"""Convert a locally obtained Absher CSV to neutral eval JSONL without redistributing the dataset."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('output'); ap.add_argument('--limit',type=int); args=ap.parse_args(); rows=[]
    with open(args.input,encoding='utf-8-sig',newline='') as f:
        for i,r in enumerate(csv.DictReader(f)):
            if args.limit and i>=args.limit: break
            rows.append({"id":f"absher-{i+1}","source":"Absher","task":r.get('Question',''),"input":r.get('Term',''),"gold":r.get('Correct_answer',''),"dialect":r.get('Dialect_type',''),"meaning":r.get('Meaning_of_term','')})
    Path(args.output).write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in rows)+'\n',encoding='utf-8'); print(len(rows)); return 0
if __name__=='__main__': raise SystemExit(main())

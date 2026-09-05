#!/usr/bin/env python3
"""Protect quoted text, inline/fenced code, and Markdown table cell relationships."""
from __future__ import annotations
import argparse, collections, json, re
from pathlib import Path

QUOTES=[re.compile(r"«([^»]+)»",re.S), re.compile(r'“([^”]+)”',re.S)]
INLINE=re.compile(r"`([^`\n]+)`")
FENCED=re.compile(r"```[^\n]*\n(.*?)```",re.S)

def extract(text):
    q=[]
    for p in QUOTES: q += [m.group(1).strip() for m in p.finditer(text)]
    inline=[m.group(1) for m in INLINE.finditer(text)]
    fenced=[m.group(1).strip('\n') for m in FENCED.finditer(text)]
    tables=[]
    for line in text.splitlines():
        if '|' not in line or re.fullmatch(r"\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*",line): continue
        cells=tuple(c.strip() for c in line.strip().strip('|').split('|'))
        if len(cells)>=2: tables.append(cells)
    return {"quotes":q,"inline_code":inline,"fenced_code":fenced,"table_rows":tables}

def compare(before,after):
    result={}
    for k in before:
        b=collections.Counter(before[k]); a=collections.Counter(after[k])
        missing=list((b-a).elements()); added=list((a-b).elements())
        if missing or added: result[k]={"missing":missing,"added":added}
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('before'); ap.add_argument('after'); ap.add_argument('--json',action='store_true')
    args=ap.parse_args(); report=compare(extract(Path(args.before).read_text(encoding='utf-8')),extract(Path(args.after).read_text(encoding='utf-8')))
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not report: print('OK: protected structures preserved.')
    else:
        print('Review protected-structure differences:')
        for k,v in report.items(): print(f'- {k}: {v}')
    return 1 if report else 0
if __name__=='__main__': raise SystemExit(main())

#!/usr/bin/env python3
"""Detect simple anchor→value relationships and compare them across revisions.

Conservative by design: it catches obvious value swaps in tables and label/value prose.
It is not a semantic parser and findings require review.
"""
from __future__ import annotations
import argparse, collections, json, re
from pathlib import Path

AR_DIGITS = "٠١٢٣٤٥٦٧٨٩"
NUM = rf"[0-9{AR_DIGITS}]"
VALUE_RE = re.compile(
    rf"(?:[-+]?{NUM}[0-9{AR_DIGITS},٬.٫]*(?:\s*[%٪])?"
    rf"(?:\s*(?:ريال(?:اً)?|ر\.?س\.?|SAR|USD|EUR|دولار|يورو|مليون|مليار|ألف|الف|%|٪))?)"
)
WORD_RE = re.compile(r"[\u0600-\u06FFA-Za-z][\u0600-\u06FFA-Za-z0-9_-]*")
STOP = {"في","من","إلى","الى","على","عن","مع","و","أو","او","هو","هي","هذا","هذه","ذلك","تلك","بلغ","بلغت","تبلغ","قيمة","نسبة","عدد","عام","سنة","خلال","وفق","حسب"}

def norm(s: str) -> str:
    s = re.sub(r"\s+", " ", s.strip(" |:：=–—-،؛;."))
    return s.casefold()

def anchor_from_text(prefix: str) -> str:
    words = [w for w in WORD_RE.findall(prefix) if norm(w) not in STOP]
    return norm(" ".join(words[-4:]))

def table_relations(text: str):
    out=[]
    for line_no, line in enumerate(text.splitlines(), 1):
        if '|' not in line or re.fullmatch(r"\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*", line):
            continue
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells)<2:
            continue
        row_anchor=norm(cells[0])
        if not row_anchor:
            continue
        for idx, cell in enumerate(cells[1:],1):
            for m in VALUE_RE.finditer(cell):
                out.append({"anchor":row_anchor,"value":m.group(0).strip(),"kind":"table","line":line_no,"column":idx+1})
    return out

def prose_relations(text: str):
    out=[]
    for line_no,line in enumerate(text.splitlines(),1):
        if '|' in line:
            continue
        for m in VALUE_RE.finditer(line):
            prefix=line[max(0,m.start()-90):m.start()]
            anchor=anchor_from_text(prefix)
            if anchor:
                out.append({"anchor":anchor,"value":m.group(0).strip(),"kind":"prose","line":line_no})
    return out

def extract(text: str):
    return table_relations(text)+prose_relations(text)

def key(item):
    return (item["kind"], item["anchor"], item["value"])

def compare(before, after):
    b=collections.Counter(key(x) for x in before)
    a=collections.Counter(key(x) for x in after)
    missing=list((b-a).elements())
    added=list((a-b).elements())
    return {"missing":[{"kind":k,"anchor":an,"value":v} for k,an,v in missing],
            "added":[{"kind":k,"anchor":an,"value":v} for k,an,v in added]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('before'); ap.add_argument('after'); ap.add_argument('--json',action='store_true')
    args=ap.parse_args()
    b=extract(Path(args.before).read_text(encoding='utf-8'))
    a=extract(Path(args.after).read_text(encoding='utf-8'))
    report=compare(b,a)
    changed=bool(report['missing'] or report['added'])
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not changed: print('OK: no anchored-fact differences detected.')
    else:
        print('Review anchored-fact differences:')
        for label in ('missing','added'):
            for x in report[label]: print(f"- {label}: [{x['anchor']}] → {x['value']} ({x['kind']})")
    return 1 if changed else 0
if __name__=='__main__': raise SystemExit(main())

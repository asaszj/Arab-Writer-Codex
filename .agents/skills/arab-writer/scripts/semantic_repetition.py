#!/usr/bin/env python3
"""Near-semantic repetition heuristic for adjacent Arabic paragraphs.

This deliberately reports candidates only. Lexical overlap is not proof that a
repetition is redundant; educational reinforcement may be intentional.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

TOKEN = re.compile(r"[\u0621-\u063A\u0641-\u064A]{2,}")
STOP = {"هذا","هذه","ذلك","تلك","التي","الذي","من","في","على","إلى","الى","عن","مع","ثم","كما","قد","تم","كان","كانت","هو","هي","أن","إن","وأن","فإن","لكن","بين","بعد","قبل","عند","حتى","أو","او","كل","غير","أي","اي","هنا","هناك"}
PREFIXES = ("وال","بال","كال","فال","لل")

def normalize_token(token: str) -> str:
    t = re.sub(r"[\u064B-\u065F\u0670]", "", token)
    t = t.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي")
    for p in PREFIXES:
        if t.startswith(p) and len(t) - len(p) >= 3:
            t = t[len(p):]
            break
    if t.startswith("ال") and len(t) > 4:
        t = t[2:]
    return t

def content_tokens(text: str) -> set[str]:
    out=set()
    for raw in TOKEN.findall(text):
        t=normalize_token(raw)
        if t not in STOP and len(t)>=3: out.add(t)
    return out

def similarity(a: str, b: str) -> float:
    x,y=content_tokens(a),content_tokens(b)
    if not x or not y: return 0.0
    inter=len(x & y)
    j=inter/len(x | y)
    containment=inter/min(len(x),len(y))
    return round(0.55*j + 0.45*containment, 3)

def scan(text: str, threshold: float = 0.48, window: int = 2):
    ps=[p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    findings=[]
    for i,a in enumerate(ps):
        for j in range(i+1,min(len(ps),i+1+window)):
            score=similarity(a,ps[j])
            if score>=threshold:
                findings.append({"code":"possible_semantic_repetition","paragraph_a":i+1,"paragraph_b":j+1,"score":score,"message":"Review whether the later paragraph adds a new constraint/fact or merely restates the same point. Do not remove intentional educational reinforcement."})
    return findings

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--threshold",type=float,default=.48); ap.add_argument("--window",type=int,default=2); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    findings=scan(Path(args.file).read_text(encoding="utf-8"),args.threshold,args.window)
    if args.json: print(json.dumps(findings,ensure_ascii=False,indent=2))
    elif findings:
        for f in findings: print(f'[{f["code"]}] paragraphs {f["paragraph_a"]}/{f["paragraph_b"]} score={f["score"]}: {f["message"]}')
    else: print("OK: no near-semantic repetition candidates above threshold.")
    return 1 if findings else 0
if __name__=='__main__': raise SystemExit(main())

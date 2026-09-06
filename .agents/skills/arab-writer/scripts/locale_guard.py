#!/usr/bin/env python3
"""Context-aware register/dialect drift signals for Arabic.

Uses token/phrase boundaries and excludes ambiguous MSA uses such as "مرة أخرى".
This is not a dialect classifier.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

DIALECT_WORDS={"وش","ودي","أبي","ابي","أبغى","ابغى","ترى","كذا","مره","الحين","ذحين","مو","ليه","شلون","وشلون","عشان","ترا"}
DIALECT_PHRASES={"ما أبي","ما ابي","وش رايك","وش رأيك","ليه كذا","وشلون"}
FORMAL_PHRASES={"سعادة","الموقر","الموقرة","نأمل التوجيه","نأمل الرفع","وتفضلوا","وتقبلوا","إشارة إلى","اشارة إلى"}

def _bounded(pattern:str):
    return re.compile(rf"(?<![\w\u0600-\u06FF]){re.escape(pattern)}(?![\w\u0600-\u06FF])",re.I)

def count_markers(text,markers):
    t=re.sub(r"\s+"," ",text)
    out={}
    for m in markers:
        n=len(_bounded(m).findall(t))
        if n: out[m]=n
    return out

def profile(text):
    return {
        "dialect_words":count_markers(text,DIALECT_WORDS),
        "dialect_phrases":count_markers(text,DIALECT_PHRASES),
        "formal":count_markers(text,FORMAL_PHRASES),
    }

def compare(before,after):
    bp,ap=profile(before),profile(after)
    findings=[]
    bd={**bp["dialect_words"],**bp["dialect_phrases"]}
    ad={**ap["dialect_words"],**ap["dialect_phrases"]}
    lost={k:v-ad.get(k,0) for k,v in bd.items() if v>ad.get(k,0)}
    added={k:v-bd.get(k,0) for k,v in ad.items() if v>bd.get(k,0)}
    bf,af=bp["formal"],ap["formal"]
    added_f={k:v-bf.get(k,0) for k,v in af.items() if v>bf.get(k,0)}
    if lost: findings.append({"code":"dialect_markers_lost","details":lost,"note":"May indicate dialect flattening when dialect preservation was requested."})
    if added and not bd: findings.append({"code":"dialect_inserted","details":added,"note":"Bounded dialect markers were introduced into a source without them."})
    if added_f and bd: findings.append({"code":"formalization_drift","details":added_f,"note":"Formal/institutional markers were added to dialectal source."})
    return findings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("before"); ap.add_argument("after"); ap.add_argument("--json",action="store_true")
    args=ap.parse_args(); report=compare(Path(args.before).read_text(encoding="utf-8"),Path(args.after).read_text(encoding="utf-8"))
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not report: print("OK: no bounded locale/register drift detected.")
    else:
        for x in report: print(f"- {x['code']}: {x['details']} — {x['note']}")
    return 1 if report else 0
if __name__=="__main__": raise SystemExit(main())

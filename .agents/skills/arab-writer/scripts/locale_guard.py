#!/usr/bin/env python3
"""Detect obvious register/dialect drift. This is not a dialect classifier."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

DIALECT_MARKERS={
 "وش","ودي","أبي","ابي","أبغى","ابغى","ترى","كذا","مره","مرة","الحين","ذحين","مو","ليه","شلون","وشلون","ما أبي","ما ابي","عشان","ترا"
}
FORMAL_MARKERS={"سعادة","الموقر","الموقرة","نأمل التوجيه","نأمل الرفع","وتفضلوا","وتقبلوا","إشارة إلى","اشارة إلى"}

def count_markers(text,markers):
    t=re.sub(r"\s+"," ",text)
    return {m:len(re.findall(re.escape(m),t,re.I)) for m in markers if re.search(re.escape(m),t,re.I)}

def compare(before,after):
    bd=count_markers(before,DIALECT_MARKERS); ad=count_markers(after,DIALECT_MARKERS)
    bf=count_markers(before,FORMAL_MARKERS); af=count_markers(after,FORMAL_MARKERS)
    findings=[]
    lost={k:v-ad.get(k,0) for k,v in bd.items() if v>ad.get(k,0)}
    added_d={k:v-bd.get(k,0) for k,v in ad.items() if v>bd.get(k,0)}
    added_f={k:v-bf.get(k,0) for k,v in af.items() if v>bf.get(k,0)}
    if lost: findings.append({"code":"dialect_markers_lost","details":lost,"note":"May indicate dialect flattening when dialect preservation was requested."})
    if added_d and not bd: findings.append({"code":"dialect_inserted","details":added_d,"note":"Dialect markers were introduced into a source without them."})
    if added_f and bd: findings.append({"code":"formalization_drift","details":added_f,"note":"Formal/institutional markers were added to dialectal source."})
    return findings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('before'); ap.add_argument('after'); ap.add_argument('--json',action='store_true')
    args=ap.parse_args(); report=compare(Path(args.before).read_text(encoding='utf-8'),Path(args.after).read_text(encoding='utf-8'))
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not report: print('OK: no obvious locale/register drift detected.')
    else:
        print('Review locale/register drift:')
        for x in report: print(f"- {x['code']}: {x['details']} — {x['note']}")
    return 1 if report else 0
if __name__=='__main__': raise SystemExit(main())

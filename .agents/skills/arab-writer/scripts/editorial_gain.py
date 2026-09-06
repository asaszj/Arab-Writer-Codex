#!/usr/bin/env python3
"""Editorial Gain Gate v1.3.

Evaluates whether a proposed edit has enough observable benefit to justify its
change cost. It is a conservative gate, not a universal writing-quality score.
"""
from __future__ import annotations
import argparse, json
from difflib import SequenceMatcher
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
def load(name):
    p=HERE/f"{name}.py"; spec=importlib.util.spec_from_file_location(name,p); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod

depth=load("editorial_depth")
repeat=load("semantic_repetition")
sentinels=load("semantic_sentinels")
fgraph=load("fidelity_graph")
locale=load("locale_guard")

def change_ratio(a:str,b:str)->float:
    return round(1-SequenceMatcher(None,a,b).ratio(),4)

def evaluate(before:str,after:str,voice_drift:float|None=None):
    before_burden=depth.burden(before); after_burden=depth.burden(after)
    before_rep=len(repeat.scan(before)); after_rep=len(repeat.scan(after))
    gain=max(0,before_burden-after_burden)*1.0 + max(0,before_rep-after_rep)*0.75

    fg=fgraph.compare(fgraph.extract(before),fgraph.extract(after))
    ss=sentinels.compare(sentinels.extract(before),sentinels.extract(after))
    loc=locale.compare(before,after)
    critical=len(fg["issues"])+len(ss["missing"])+len(ss["added"])
    ratio=change_ratio(before,after)
    voice_cost=0 if voice_drift is None else max(0,voice_drift-0.04)*8
    cost=critical*5 + len(loc)*1.5 + max(0,ratio-0.12)*4 + voice_cost

    if critical:
        verdict="reject_or_human_review"
    elif gain<=0 and ratio>0.03:
        verdict="retain_source"
    elif gain>cost:
        verdict="accept_candidate"
    else:
        verdict="human_review"
    return {
        "verdict":verdict,
        "gain_score":round(gain,3),
        "cost_score":round(cost,3),
        "change_ratio":ratio,
        "before_editorial_burden":before_burden,
        "after_editorial_burden":after_burden,
        "before_repetition_candidates":before_rep,
        "after_repetition_candidates":after_rep,
        "critical_fidelity_signals":critical,
        "locale_signals":loc,
        "voice_drift":voice_drift,
        "principle":"A safe edit is not automatically a useful edit; accept only when benefit justifies change cost."
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("before"); ap.add_argument("after"); ap.add_argument("--voice-drift",type=float); ap.add_argument("--json",action="store_true")
    args=ap.parse_args()
    r=evaluate(Path(args.before).read_text(encoding="utf-8"),Path(args.after).read_text(encoding="utf-8"),args.voice_drift)
    if args.json: print(json.dumps(r,ensure_ascii=False,indent=2))
    else: print(f"{r['verdict']}: gain={r['gain_score']} cost={r['cost_score']} change={r['change_ratio']}")
    return 0 if r["verdict"]=="accept_candidate" else 1
if __name__=="__main__": raise SystemExit(main())

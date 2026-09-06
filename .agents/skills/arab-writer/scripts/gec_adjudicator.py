#!/usr/bin/env python3
"""Adjudicate an Arabic GEC candidate against fidelity constraints.

This does not itself provide a grammar model. It is the safety layer between an
external/second-pass GEC proposal and the accepted editorial text.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
def load(name):
    p=HERE/f"{name}.py"; spec=importlib.util.spec_from_file_location(name,p); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
fg=load("fidelity_graph"); ss=load("semantic_sentinels")

def adjudicate(source,candidate):
    graph=fg.compare(fg.extract(source),fg.extract(candidate))
    sent=ss.compare(ss.extract(source),ss.extract(candidate))
    critical=len(graph["issues"])+len(sent["missing"])+len(sent["added"])
    return {
        "verdict":"safe_for_language_review" if critical==0 else "human_review_required",
        "critical_fidelity_signals":critical,
        "fidelity_graph_issues":graph["issues"],
        "semantic_sentinel_missing":sent["missing"],
        "semantic_sentinel_added":sent["added"],
        "note":"This verdict does not prove the candidate is grammatically correct; it only checks high-impact fidelity constraints."
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("source"); ap.add_argument("candidate"); args=ap.parse_args()
    r=adjudicate(Path(args.source).read_text(encoding="utf-8"),Path(args.candidate).read_text(encoding="utf-8"))
    print(json.dumps(r,ensure_ascii=False,indent=2))
    return 0 if r["verdict"]=="safe_for_language_review" else 1
if __name__=="__main__": raise SystemExit(main())

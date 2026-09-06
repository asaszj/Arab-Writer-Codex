#!/usr/bin/env python3
"""Generate a paragraph-level explainable edit trail.

Reasons are machine hints and must not be presented as verified intent unless
the editor confirms them.
"""
from __future__ import annotations
import argparse, json, re
from difflib import SequenceMatcher
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
def load(name):
    p=HERE/f"{name}.py"; spec=importlib.util.spec_from_file_location(name,p); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
depth=load("editorial_depth")

def paragraphs(text):
    return [p.strip() for p in (text.splitlines() if "\n\n" not in text else re.split(r"\n\s*\n",text)) if p.strip()]

def trail(before,after):
    b,a=paragraphs(before),paragraphs(after)
    sm=SequenceMatcher(None,b,a)
    out=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=="equal": continue
        old="\n\n".join(b[i1:i2]); new="\n\n".join(a[j1:j2])
        old_codes=sorted({x["code"] for x in depth.scan(old)})
        new_codes=sorted({x["code"] for x in depth.scan(new)})
        out.append({
            "operation":tag,"before_range":[i1+1,i2],"after_range":[j1+1,j2],
            "before":old,"after":new,
            "observed_before_signals":old_codes,
            "observed_after_signals":new_codes,
            "reason_status":"INFERRED",
            "verification_required":["fidelity","language","editorial_gain"],
        })
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("before"); ap.add_argument("after"); ap.add_argument("--out"); args=ap.parse_args()
    data=trail(Path(args.before).read_text(encoding="utf-8"),Path(args.after).read_text(encoding="utf-8"))
    txt=json.dumps(data,ensure_ascii=False,indent=2)
    if args.out: Path(args.out).write_text(txt+"\n",encoding="utf-8")
    else: print(txt)
    return 0
if __name__=="__main__": raise SystemExit(main())

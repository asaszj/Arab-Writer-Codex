#!/usr/bin/env python3
"""Separate numeric semantic value from presentation.

Policies:
- preserve-exact
- normalize-arabic
- normalize-western
- document-consistent

The helper never changes a number unless semantic equivalence can be proven
under its parser.
"""
from __future__ import annotations
import argparse, json, re
from decimal import Decimal, InvalidOperation
from pathlib import Path

ARABIC_DIGITS="٠١٢٣٤٥٦٧٨٩"
DIGIT_MAP=str.maketrans(ARABIC_DIGITS,"0123456789")
REVERSE_DIGIT_MAP=str.maketrans("0123456789",ARABIC_DIGITS)
NUM_RE=re.compile(r"(?<![\w])[-+]?[0-9٠-٩][0-9٠-٩,٬٫.]*%?")

def to_ascii_digits(s:str)->str:
    return s.translate(DIGIT_MAP)

def canonical_number(surface:str):
    s=to_ascii_digits(surface.strip())
    percent=s.endswith("%")
    if percent: s=s[:-1]
    s=s.replace("٬",",").replace("٫",".")
    parts=s.split(".")
    if len(parts)>2: return None
    intpart=parts[0]
    if "," in intpart:
        groups=intpart.lstrip("+-").split(",")
        if not groups or any(not g.isdigit() for g in groups): return None
        if len(groups)>1 and any(len(g)!=3 for g in groups[1:]): return None
        intpart=intpart.replace(",","")
    rebuilt=intpart + (("." + parts[1]) if len(parts)==2 else "")
    try:
        val=Decimal(rebuilt)
    except InvalidOperation:
        return None
    return {"value":str(val.normalize() if val!=val.to_integral() else val.quantize(Decimal(1))),"percent":percent}

def semantic_equal(a:str,b:str)->bool:
    ca,cb=canonical_number(a),canonical_number(b)
    return ca is not None and ca==cb

def _group_ascii(intpart:str, sep:str=","):
    sign=""
    if intpart.startswith(("+","-")):
        sign,intpart=intpart[0],intpart[1:]
    groups=[]
    while intpart:
        groups.append(intpart[-3:]); intpart=intpart[:-3]
    return sign+sep.join(reversed(groups or ["0"]))

def render(surface:str, policy:str):
    c=canonical_number(surface)
    if c is None: return surface
    if policy=="preserve-exact": return surface
    raw=c["value"]
    if "." in raw: i,d=raw.split(".",1)
    else: i,d=raw,None
    if policy in {"normalize-western","document-consistent"}:
        out=_group_ascii(i,",") + (("." + d) if d else "")
        return out + ("%" if c["percent"] else "")
    if policy=="normalize-arabic":
        out=_group_ascii(i,"٬")
        if d: out += "٫"+d
        out=out.translate(REVERSE_DIGIT_MAP)
        return out + ("٪" if c["percent"] else "")
    raise ValueError(f"unknown policy: {policy}")

def normalize_text(text:str,policy:str):
    def repl(m):
        before=m.group(0)
        after=render(before,policy)
        if not semantic_equal(before,after):
            return before
        return after
    return NUM_RE.sub(repl,text)

def compare_surfaces(before:str,after:str):
    b=[m.group(0) for m in NUM_RE.finditer(before)]
    a=[m.group(0) for m in NUM_RE.finditer(after)]
    return {
        "before":b,"after":a,
        "semantic_values_before":[canonical_number(x) for x in b],
        "semantic_values_after":[canonical_number(x) for x in a],
        "semantic_equal_multiset": sorted(str(canonical_number(x)) for x in b)==sorted(str(canonical_number(x)) for x in a),
        "surface_equal": b==a,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--policy",default="preserve-exact",choices=["preserve-exact","normalize-arabic","normalize-western","document-consistent"]); ap.add_argument("--json",action="store_true")
    args=ap.parse_args(); text=Path(args.file).read_text(encoding="utf-8"); out=normalize_text(text,args.policy)
    if args.json: print(json.dumps({"policy":args.policy,"text":out},ensure_ascii=False,indent=2))
    else: print(out)
    return 0
if __name__=="__main__": raise SystemExit(main())

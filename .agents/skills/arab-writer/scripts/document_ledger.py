#!/usr/bin/env python3
"""Persistent document/book ledger for Arab Writer v1.3.

Captures recurring terms, acronyms, numeric relation nodes and numeral policy.
Designed to be carried across sections/chapters and merged conservatively.
"""
from __future__ import annotations
import argparse, collections, json, re
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
def load(name):
    p=HERE/f"{name}.py"; spec=importlib.util.spec_from_file_location(name,p); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
fg=load("fidelity_graph")

WORD=re.compile(r"[\u0600-\u06FFA-Za-z]{3,}")
ACRONYM=re.compile(r"\b[A-Z][A-Z0-9-]{1,10}\b")
STOP={"هذا","هذه","التي","الذي","على","إلى","الى","عن","من","في","مع","كان","كانت","كما","بعد","قبل","خلال","عند","وفق","شركة","الشركة"}

def build(text:str,document_id=None,numeral_policy="document-consistent"):
    words=[w for w in WORD.findall(text) if w.casefold() not in STOP]
    freq=collections.Counter(w for w in words)
    terms=[{"term":t,"count":c} for t,c in freq.most_common(80) if c>=2]
    acronyms=collections.Counter(ACRONYM.findall(text))
    relations=fg.extract(text)
    compact=[]
    for r in relations:
        compact.append({k:r[k] for k in ("value","measure","unit","time","status","entities")})
    return {
        "schema_version":"1.0",
        "document_id":document_id,
        "numeral_policy":numeral_policy,
        "terms":terms,
        "acronyms":[{"term":k,"count":v} for k,v in acronyms.items()],
        "relations":compact,
    }

def merge(ledgers):
    out={"schema_version":"1.0","document_id":"merged","numeral_policy":"document-consistent","terms":[],"acronyms":[],"relations":[],"conflicts":[]}
    term=collections.Counter(); acr=collections.Counter()
    policies={x.get("numeral_policy") for x in ledgers if x.get("numeral_policy")}
    if len(policies)>1: out["conflicts"].append({"code":"numeral_policy_conflict","values":sorted(policies)})
    elif policies: out["numeral_policy"]=next(iter(policies))
    for l in ledgers:
        term.update({x["term"]:x["count"] for x in l.get("terms",[])})
        acr.update({x["term"]:x["count"] for x in l.get("acronyms",[])})
        out["relations"].extend(l.get("relations",[]))
    out["terms"]=[{"term":k,"count":v} for k,v in term.most_common(120)]
    out["acronyms"]=[{"term":k,"count":v} for k,v in acr.items()]
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("files",nargs="+"); ap.add_argument("--out"); ap.add_argument("--document-id"); args=ap.parse_args()
    ledgers=[build(Path(p).read_text(encoding="utf-8"),Path(p).name) for p in args.files]
    data=ledgers[0] if len(ledgers)==1 else merge(ledgers)
    if args.document_id: data["document_id"]=args.document_id
    txt=json.dumps(data,ensure_ascii=False,indent=2)
    if args.out: Path(args.out).write_text(txt+"\n",encoding="utf-8")
    else: print(txt)
    return 0
if __name__=="__main__": raise SystemExit(main())

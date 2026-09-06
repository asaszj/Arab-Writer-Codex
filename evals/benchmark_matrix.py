#!/usr/bin/env python3
"""Validate and summarize the Arab Writer benchmark matrix."""
from __future__ import annotations
import argparse, collections, json
from pathlib import Path

REQUIRED_FIELDS={"id","domain","task","locale","risk","source_type"}
ALLOWED_RISK={"standard","elevated","high"}
ALLOWED_SOURCE={"designed","real-world","external"}

def load_cases(path):
    p=Path(path)
    if p.suffix==".jsonl":
        return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    data=json.loads(p.read_text(encoding="utf-8"))
    return data["cases"] if isinstance(data,dict) and "cases" in data else data

def validate(cases):
    errors=[]; ids=set()
    for i,c in enumerate(cases,1):
        missing=REQUIRED_FIELDS-set(c)
        if missing: errors.append(f"case {i}: missing {sorted(missing)}")
        cid=c.get("id")
        if cid in ids: errors.append(f"duplicate id: {cid}")
        ids.add(cid)
        if c.get("risk") not in ALLOWED_RISK: errors.append(f"{cid}: invalid risk")
        if c.get("source_type") not in ALLOWED_SOURCE: errors.append(f"{cid}: invalid source_type")
    domains={c.get("domain") for c in cases}
    tasks={c.get("task") for c in cases}
    source_types={c.get("source_type") for c in cases}
    if len(domains)<5: errors.append("benchmark matrix needs >=5 domains")
    if len(tasks)<4: errors.append("benchmark matrix needs >=4 task types")
    if "real-world" not in source_types: errors.append("benchmark matrix needs real-world cases")
    if "external" not in source_types: errors.append("benchmark matrix needs external benchmark adapters/cases")
    return errors

def summarize(cases):
    def count(k): return dict(collections.Counter(c.get(k,"unknown") for c in cases))
    return {"cases":len(cases),"domains":count("domain"),"tasks":count("task"),"locales":count("locale"),"risk":count("risk"),"source_type":count("source_type")}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("matrix"); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    cases=load_cases(args.matrix); errors=validate(cases); summary=summarize(cases)
    out={"summary":summary,"errors":errors}
    if args.json: print(json.dumps(out,ensure_ascii=False,indent=2))
    else:
        print(json.dumps(summary,ensure_ascii=False,indent=2))
        if errors:
            print("Errors:"); [print("-",e) for e in errors]
        else: print("OK: benchmark matrix coverage gate passed.")
    return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())

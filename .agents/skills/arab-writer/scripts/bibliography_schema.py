#!/usr/bin/env python3
"""Conservative bibliography schema extraction.

Parses only information explicitly present in each reference. Missing data stays
null; the tool never fabricates bibliographic metadata.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

YEAR=re.compile(r"(?<!\d)((?:19|20)\d{2}|[١٢][٠-٩]{3})(?!\d)")
URL=re.compile(r"https?://\S+")
DOI=re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b",re.I)
LEADING_NUM=re.compile(r"^\s*[0-9٠-٩]+[.)\-–—]?\s*")

def parse_entry(entry:str,index:int):
    raw=entry.strip()
    text=LEADING_NUM.sub("",raw)
    year=YEAR.search(text); url=URL.search(text); doi=DOI.search(text)
    parts=[p.strip(" .،؛") for p in re.split(r"[.؛]\s+",text) if p.strip()]
    organization=parts[0] if parts else None
    title=parts[1] if len(parts)>1 else None
    return {
        "index":index,"raw":raw,
        "organization":organization,
        "title":title,
        "year":year.group(1) if year else None,
        "url":url.group(0).rstrip(".,؛") if url else None,
        "doi":doi.group(0) if doi else None,
        "missing":[k for k,v in {"organization":organization,"title":title,"year":year.group(1) if year else None}.items() if not v],
    }

def parse(text:str):
    entries=[x.strip() for x in text.splitlines() if x.strip()]
    return [parse_entry(e,i) for i,e in enumerate(entries,1)]

def audit(records):
    findings=[]
    for r in records:
        if r["missing"]:
            findings.append({"code":"bibliographic_metadata_missing","entry":r["index"],"fields":r["missing"],"action":"human_review_no_autofill"})
    return findings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    records=parse(Path(args.file).read_text(encoding="utf-8")); out={"records":records,"findings":audit(records)}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 1 if out["findings"] else 0
if __name__=="__main__": raise SystemExit(main())

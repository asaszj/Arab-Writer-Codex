#!/usr/bin/env python3
"""Conservative bibliography consistency auditor.

Input is plain text with one reference per non-empty line. The auditor never
invents missing bibliographic data and does not impose a citation style unless
one is explicitly configured by the user.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
YEAR=re.compile(r"(?:19|20)\d{2}|[١٢][٠-٩]{3}")

def audit(text: str):
    entries=[x.strip() for x in text.splitlines() if x.strip()]
    findings=[]
    endings=[]
    for i,e in enumerate(entries,1):
        if not YEAR.search(e):
            findings.append({"code":"reference_year_not_detected","entry":i,"message":"No publication/event year detected. Verify whether the source is undated or metadata is missing; do not invent a year."})
        endings.append(e.endswith((".","۔")))
    if len(entries)>=3 and any(endings) and not all(endings):
        findings.append({"code":"mixed_terminal_punctuation","entry":None,"message":"Reference entries mix terminal-punctuation conventions. Normalize only if the user has not intentionally preserved source formatting."})
    return findings

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--json",action="store_true"); args=ap.parse_args(); findings=audit(Path(args.file).read_text(encoding='utf-8'))
    if args.json: print(json.dumps(findings,ensure_ascii=False,indent=2))
    elif findings:
        for f in findings: print(f'[{f["code"]}] entry={f["entry"]}: {f["message"]}')
    else: print("OK: no deterministic bibliography-format warnings.")
    return 1 if findings else 0
if __name__=='__main__': raise SystemExit(main())

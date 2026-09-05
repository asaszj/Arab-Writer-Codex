#!/usr/bin/env python3
"""Score correction presence for Nahw-style gold fixtures."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def norm(s): return re.sub(r"\s+"," ",s.strip())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('gold'); ap.add_argument('predictions',help='JSONL with id and output'); args=ap.parse_args(); gold={x['id']:x for x in map(json.loads,Path(args.gold).read_text(encoding='utf-8').splitlines()) if x}; pred={x['id']:x.get('output','') for x in map(json.loads,Path(args.predictions).read_text(encoding='utf-8').splitlines()) if x}; total=hit=over=0; missing=[]
    for i,g in gold.items():
        if i not in pred: missing.append(i); continue
        total+=1; out=pred[i]
        if g['correction'] in out: hit+=1
        if g['error'] in out and g['correction'] not in out: over+=1
    report={"scored":total,"correction_present":hit,"accuracy":round(hit/max(1,total),4),"uncorrected_error_cases":over,"missing_predictions":missing}; print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if not missing else 1
if __name__=='__main__': raise SystemExit(main())

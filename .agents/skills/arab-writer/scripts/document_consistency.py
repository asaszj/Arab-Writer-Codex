#!/usr/bin/env python3
"""Cross-section consistency checks for long Arabic documents."""
from __future__ import annotations
import argparse, collections, importlib.util, json, re
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load(name,fn):
    spec=importlib.util.spec_from_file_location(name,HERE/fn); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
anchored=load('anchored_facts','anchored_facts.py')
ACRONYM=re.compile(r"([\u0600-\u06FF][\u0600-\u06FF\s]{2,80}?)\s*[\(（]([A-Z][A-Z0-9-]{1,12})[\)）]")

def conflicts(text):
    rel=anchored.extract(text)
    by=collections.defaultdict(set)
    for x in rel:
        if len(x['anchor'])>=3: by[(x['kind'],x['anchor'])].add(x['value'])
    return [{"kind":k[0],"anchor":k[1],"values":sorted(v)} for k,v in by.items() if len(v)>1]

def acronym_conflicts(text):
    defs=collections.defaultdict(set)
    for long,short in ACRONYM.findall(text): defs[short].add(re.sub(r"\s+"," ",long.strip()))
    return [{"acronym":k,"definitions":sorted(v)} for k,v in defs.items() if len(v)>1]

def glossary_findings(text,glossary):
    findings=[]
    for canonical,variants in glossary.items():
        found=[v for v in [canonical,*variants] if re.search(re.escape(v),text,re.I)]
        if len(found)>1: findings.append({"canonical":canonical,"found_variants":found})
    return findings

def build(text,glossary=None):
    return {"anchored_fact_conflicts":conflicts(text),"acronym_definition_conflicts":acronym_conflicts(text),"terminology_drift":glossary_findings(text,glossary or {})}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file'); ap.add_argument('--glossary'); ap.add_argument('--json',action='store_true')
    args=ap.parse_args(); text=Path(args.file).read_text(encoding='utf-8'); glossary={}
    if args.glossary: glossary=json.loads(Path(args.glossary).read_text(encoding='utf-8'))
    report=build(text,glossary); bad={k:v for k,v in report.items() if v}
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not bad: print('OK: no configured cross-document consistency conflicts detected.')
    else:
        print('Review document consistency:')
        for k,v in bad.items(): print(f'[{k}] '+json.dumps(v,ensure_ascii=False))
    return 1 if bad else 0
if __name__=='__main__': raise SystemExit(main())

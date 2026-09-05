#!/usr/bin/env python3
"""Composite v1.2 QA: tokens, relations, sentinels, conditions, structures, locale drift and mechanical lint."""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load(name,filename):
    spec=importlib.util.spec_from_file_location(name,HERE/filename); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
protected=load('protected_tokens','protected_tokens.py'); anchored=load('anchored_facts','anchored_facts.py'); sentinels=load('semantic_sentinels','semantic_sentinels.py'); conditions=load('condition_guard','condition_guard.py'); structure=load('structure_guard','structure_guard.py'); locale=load('locale_guard','locale_guard.py'); lintmod=load('arabic_mechanical_lint','arabic_mechanical_lint.py')

def build_report(before_text,after_text):
    token=protected.diff(protected.extract(before_text),protected.extract(after_text))
    anchor=anchored.compare(anchored.extract(before_text),anchored.extract(after_text)); anchor={} if not anchor['missing'] and not anchor['added'] else anchor
    sem=sentinels.compare(sentinels.extract(before_text),sentinels.extract(after_text)); sem={} if not sem['missing'] and not sem['added'] else sem
    cond=conditions.compare(conditions.extract(before_text),conditions.extract(after_text)); cond={} if not cond['missing'] and not cond['added'] else cond
    struct=structure.compare(structure.extract(before_text),structure.extract(after_text))
    loc=locale.compare(before_text,after_text)
    lint=lintmod.lint(after_text)
    return {"protected_tokens":token,"anchored_facts":anchor,"semantic_sentinels":sem,"conditions_exceptions":cond,"protected_structures":struct,"locale_register_drift":loc,"mechanical_lint":lint}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('before'); ap.add_argument('after'); ap.add_argument('--json',action='store_true')
    args=ap.parse_args(); b=Path(args.before).read_text(encoding='utf-8'); a=Path(args.after).read_text(encoding='utf-8'); report=build_report(b,a); failures={k:v for k,v in report.items() if v}
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not failures: print('OK: v1.2 fidelity, locale and mechanical checks passed.')
    else:
        print('Review v1.2 QA findings:')
        for k,v in failures.items(): print(f'\n[{k}]\n{json.dumps(v,ensure_ascii=False,indent=2)}')
    return 1 if failures else 0
if __name__=='__main__': raise SystemExit(main())

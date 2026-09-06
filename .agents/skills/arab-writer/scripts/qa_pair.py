#!/usr/bin/env python3
"""Composite Arab Writer v1.3 QA.

Combines legacy token/anchor checks with the v1.3 relation graph, contextual
sentinels, conditions, structures, locale drift and mechanical lint.

Backward compatibility: the historical `anchored_facts` report key is retained.
`anchored_facts_legacy` is an explicit alias for consumers migrating to the
v1.3 Fidelity Relation Graph.
"""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load(name,filename=None):
    filename=filename or f"{name}.py"; spec=importlib.util.spec_from_file_location(name,HERE/filename); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
protected=load('protected_tokens'); anchored=load('anchored_facts'); graph=load('fidelity_graph'); sentinels=load('semantic_sentinels'); conditions=load('condition_guard'); structure=load('structure_guard'); locale=load('locale_guard'); lintmod=load('arabic_mechanical_lint')

def build_report(before_text,after_text):
    token=protected.diff(protected.extract(before_text),protected.extract(after_text))
    anchor=anchored.compare(anchored.extract(before_text),anchored.extract(after_text)); anchor={} if not anchor['missing'] and not anchor['added'] else anchor
    g=graph.compare(graph.extract(before_text),graph.extract(after_text)); g={} if not g['issues'] else {'issues':g['issues']}
    sem=sentinels.compare(sentinels.extract(before_text),sentinels.extract(after_text)); sem={} if not sem['missing'] and not sem['added'] else {'missing':sem['missing'],'added':sem['added']}
    cond=conditions.compare(conditions.extract(before_text),conditions.extract(after_text)); cond={} if not cond['missing'] and not cond['added'] else cond
    struct=structure.compare(structure.extract(before_text),structure.extract(after_text)); loc=locale.compare(before_text,after_text); lint=lintmod.lint(after_text)
    return {
        "protected_tokens":token,
        "anchored_facts":anchor,
        "anchored_facts_legacy":anchor,
        "fidelity_relation_graph":g,
        "semantic_sentinels":sem,
        "conditions_exceptions":cond,
        "protected_structures":struct,
        "locale_register_drift":loc,
        "mechanical_lint":lint,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('before'); ap.add_argument('after'); ap.add_argument('--json',action='store_true'); args=ap.parse_args(); b=Path(args.before).read_text(encoding='utf-8'); a=Path(args.after).read_text(encoding='utf-8'); report=build_report(b,a)
    # The legacy alias mirrors anchored_facts and must not double-count failures.
    failures={k:v for k,v in report.items() if v and k!='anchored_facts_legacy'}
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not failures: print('OK: v1.3 deterministic fidelity/locale/mechanical checks found no differences.')
    else:
        print('Review v1.3 QA findings:')
        for k,v in failures.items(): print(f'\n[{k}]\n{json.dumps(v,ensure_ascii=False,indent=2)}')
    return 1 if failures else 0
if __name__=='__main__': raise SystemExit(main())

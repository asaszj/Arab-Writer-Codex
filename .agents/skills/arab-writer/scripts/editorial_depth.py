#!/usr/bin/env python3
"""Editorial opportunity scanner for Arabic prose (v1.3).

Generates review signals for under-editing; never rewrites automatically.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
WORD=re.compile(r"[\u0600-\u06FFA-Za-z]+")
SENTENCE=re.compile(r"[^.!؟\n]+[.!؟]?",re.M)
PHRASE_PATTERNS=[
 ("awkward_expansion_phrase",re.compile(r"ضمن\s+سلسلة\s+من\s+(?:ال)?(?:توسع|التوسع|تطور|التطور)"),"Use a more direct relation if meaning is unchanged."),
 ("awkward_trading_phrase",re.compile(r"تعليق\s+للتداول"),"Review whether 'تعليق التداول' is intended."),
 ("awkward_agentive_phrase",re.compile(r"فحص\s+من\s+(?:هيئة|الهيئة|الجهة|لجنة|اللجنة)"),"Consider an explicit agentive verb if supported."),
 ("awkward_year_pair",re.compile(r"عند\s+قراءة\s+سنوات\s+[0-9٠-٩]{4}\s+و[0-9٠-٩]{4}"),"For exactly two years, review whether 'سنتي' is more precise."),
 ("awkward_final_series",re.compile(r"السلسلة\s+النهائية\s+للقوائم"),"Review whether the intended referent is the final/restated figures rather than a 'final series'."),
]
META_PATTERNS=[
 re.compile(r"^\s*(?:يعرض|تعرض|يستعرض|تستعرض)\s+(?:هذه|هذا|نتائج|القسم|الفصل)"),
 re.compile(r"^\s*(?:يبين|يوضح)\s+(?:هذا\s+القسم|هذا\s+الفصل)"),
]
CONNECTORS=re.compile(r"\b(?:و|ثم|كما|بينما|إذ|حيث|لكن|لذلك|وعليه|وبعد|وقبل)\b")
SEVERITY_WEIGHT={"low":1,"medium":2,"high":3}

def _snippet(text,limit=180):
    t=" ".join(text.split()); return t if len(t)<=limit else t[:limit-1]+"…"

def scan(text):
    findings=[]
    ps=[p.strip() for p in (re.split(r"\n\s*\n",text) if "\n\n" in text else text.splitlines()) if p.strip()]
    for pi,p in enumerate(ps,1):
        for code,pattern,message in PHRASE_PATTERNS:
            if pattern.search(p):
                findings.append({"code":code,"severity":"medium","paragraph":pi,"message":message,"snippet":_snippet(p)})
        if any(x.search(p) for x in META_PATTERNS):
            findings.append({"code":"possible_meta_sentence","severity":"low","paragraph":pi,"message":"Review whether this sentence describes the text instead of adding content.","snippet":_snippet(p)})
        for s in SENTENCE.findall(p):
            words=WORD.findall(s); factual=len(re.findall(r"(?:\d{2,4}|[٠-٩]{2,4})",s)); connectors=len(CONNECTORS.findall(s))
            if len(words)>=38 and (factual>=3 or connectors>=4):
                findings.append({"code":"high_factual_sentence_complexity","severity":"medium","paragraph":pi,"message":"Dense sentence: split only if conditions/dates/relations remain attached.","metrics":{"words":len(words),"factual_tokens":factual,"connectors":connectors},"snippet":_snippet(s)})
    return findings

def burden(text):
    fs=scan(text)
    return sum(SEVERITY_WEIGHT.get(f.get("severity","low"),1) for f in fs)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    fs=scan(Path(args.file).read_text(encoding="utf-8"))
    if args.json: print(json.dumps(fs,ensure_ascii=False,indent=2))
    elif fs:
        for f in fs: print(f"p{f['paragraph']} [{f['code']}] {f['message']} :: {f['snippet']}")
    else: print("OK: no deterministic editorial-opportunity findings.")
    return 1 if fs else 0
if __name__=="__main__": raise SystemExit(main())

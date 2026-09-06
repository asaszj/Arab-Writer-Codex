#!/usr/bin/env python3
"""Context-aware semantic sentinel extraction for high-impact Arabic operators.

v1.3 intentionally distinguishes surface markers from their contextual function.
Findings remain review signals, not semantic proof.
"""
from __future__ import annotations
import argparse, collections, json, re
from pathlib import Path

TOKEN_RE = re.compile(r"[\u0600-\u06FFA-Za-z0-9_-]+")
SENT_RE = re.compile(r"[^.!؟\n]+[.!؟]?", re.M)
STOP = {"في","من","إلى","الى","على","عن","مع","و","أو","او","أن","ان","إن","هذا","هذه","ذلك","تلك","هو","هي","تم","يتم"}
CATEGORIES = {
    "negation": ["لا","لم","لن","ليس","ليست","ليسوا","دون","غير"],
    "obligation": ["يجب","يلزم","يتعين","ينبغي","واجب","إلزامي","الزامي"],
    "permission": ["يجوز","يحق","يمكن له","مسموح"],
    "prohibition": ["يحظر","يُحظر","ممنوع","لا يجوز"],
    "uncertainty": ["قد","ربما","من المحتمل","يحتمل","يمكن أن","يمكن ان"],
    "association": ["يرتبط","ترتبط","ارتباط","علاقة","يتزامن","تتزامن"],
    "causation": ["يسبب","تسبب","يؤدي","تؤدي","ينتج عن","نتيجة لـ","بسبب"],
    "forecast": ["يتوقع","متوقع","توقع","تقديري","تقديرية","افتراض","افتراضي"],
    "guarantee": ["يضمن","مضمون","مؤكد","حتمي","بالتأكيد"],
}
PAST_AFTER_QAD = {"أعلن","أعلنت","اعلن","اعلنت","ذكر","ذكرت","أشار","أشارت","اشار","اشارت","أفاد","أفادت","افاد","افادت","قرر","قررت","صدر","صدرت","بلغ","بلغت","كانت","كان","تم","سبق","انتهى","انتهت","نشرت","نشر","حققت","حقق","أظهرت","أظهر","اظهرت","اظهر","تغيرت","تغير","أعيد","اعيد","اعادت","أعادت"}

def norm(s:str)->str:
    s=re.sub(r"[\u064B-\u065F\u0670]","",s)
    return re.sub(r"\s+"," ",s.strip()).casefold()

def _sentence_spans(text:str):
    for m in SENT_RE.finditer(text):
        if m.group(0).strip(): yield m.start(), m.end(), m.group(0).strip()

def _word_after(sentence:str,end:int)->str|None:
    m=TOKEN_RE.search(sentence,end)
    return norm(m.group(0)) if m else None

def contextual_role(category:str,marker:str,sentence:str,local_start:int,local_end:int):
    mk=norm(marker)
    if category=="uncertainty" and mk=="قد":
        nxt=_word_after(sentence,local_end)
        if nxt in {norm(x) for x in PAST_AFTER_QAD}:
            return False,"past_aspect",0.95,"قد + past-tense reporting verb; do not treat as uncertainty."
    return True,category,0.80,None

def extract(text:str):
    items=[]
    for _,_,sentence in _sentence_spans(text):
        sent_low=norm(sentence)
        for cat,phrases in CATEGORIES.items():
            for phrase in sorted(phrases,key=len,reverse=True):
                p=norm(phrase)
                for m in re.finditer(rf"(?<![\w\u0600-\u06FF]){re.escape(p)}(?![\w\u0600-\u06FF])",sent_low):
                    active,role,confidence,note=contextual_role(cat,p,sent_low,m.start(),m.end())
                    words=[norm(w) for w in TOKEN_RE.findall(sent_low) if norm(w) not in STOP and norm(w)!=p]
                    items.append({"category":cat,"marker":p,"role":role,"active":active,"confidence":confidence,"anchor":" ".join(words[:3]+words[-3:])[:160],"sentence":sentence[:240],"note":note})
    return items

def key(x): return (x["category"],x["role"],x["marker"])

def compare(before,after):
    b=[x for x in before if x["active"]]; a=[x for x in after if x["active"]]
    bc=collections.Counter(key(x) for x in b); ac=collections.Counter(key(x) for x in a)
    missing=list((bc-ac).elements()); added=list((ac-bc).elements())
    return {"missing":[{"category":c,"role":r,"marker":m} for c,r,m in missing],"added":[{"category":c,"role":r,"marker":m} for c,r,m in added],"ignored_before":[x for x in before if not x["active"]],"ignored_after":[x for x in after if not x["active"]]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("before"); ap.add_argument("after"); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    report=compare(extract(Path(args.before).read_text(encoding="utf-8")),extract(Path(args.after).read_text(encoding="utf-8")))
    changed=bool(report["missing"] or report["added"])
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not changed: print("OK: no active semantic-sentinel differences detected.")
    else:
        print("Review contextual semantic-sentinel differences:")
        for label in ("missing","added"):
            for x in report[label]: print(f"- {label}: {x['category']} [{x['marker']}] role={x['role']}")
    return 1 if changed else 0
if __name__=="__main__": raise SystemExit(main())

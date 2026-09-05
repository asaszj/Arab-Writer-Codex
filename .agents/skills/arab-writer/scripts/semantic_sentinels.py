#!/usr/bin/env python3
"""Compare high-impact semantic operators with local lexical anchors."""
from __future__ import annotations
import argparse, collections, json, re
from pathlib import Path

CATEGORIES = {
 "negation": ["لا","لم","لن","ليس","ليست","ليسوا","دون","غير"],
 "obligation": ["يجب","يلزم","يتعين","ينبغي","واجب","إلزامي","الزامي"],
 "permission": ["يجوز","يحق","يمكن له","مسموح"],
 "prohibition": ["يحظر","يُحظر","ممنوع","لا يجوز"],
 "uncertainty": ["قد","ربما","من المحتمل","يحتمل","يمكن أن","يمكن ان"],
 "association": ["يرتبط","ترتبط","ارتباط","علاقة","يتزامن","تتزامن"],
 "causation": ["يسبب","تسبب","يؤدي","تؤدي","ينتج عن","نتيجة لـ","بسبب"],
 "forecast": ["يتوقع","متوقع","توقع","تقديري","تقديرية","افتراض","افتراضي"],
 "guarantee": ["يضمن","تضمن","مضمون","مؤكد","حتمي","بالتأكيد"],
}
TOKEN_RE=re.compile(r"[\u0600-\u06FFA-Za-z0-9_-]+")
STOP={"في","من","إلى","الى","على","عن","مع","و","أو","او","أن","ان","إن","هذا","هذه","ذلك","تلك","هو","هي","تم","يتم"}

def norm(s): return re.sub(r"\s+"," ",s.strip()).casefold()

def extract(text):
    items=[]
    lower=norm(text)
    for cat, phrases in CATEGORIES.items():
        for phrase in sorted(phrases,key=len,reverse=True):
            p=norm(phrase)
            for m in re.finditer(rf"(?<![\w\u0600-\u06FF]){re.escape(p)}(?![\w\u0600-\u06FF])", lower):
                left=lower[max(0,m.start()-70):m.start()]
                right=lower[m.end():m.end()+70]
                words=[w for w in TOKEN_RE.findall(left+' '+right) if norm(w) not in STOP and norm(w)!=p]
                anchor=' '.join(words[:2]+words[-2:])[:120]
                items.append({"category":cat,"marker":p,"anchor":anchor})
    return items

def key(x): return (x['category'],x['marker'],x['anchor'])

def compare(before,after):
    b=collections.Counter(key(x) for x in before); a=collections.Counter(key(x) for x in after)
    missing=list((b-a).elements()); added=list((a-b).elements())
    return {"missing":[{"category":c,"marker":m,"anchor":an} for c,m,an in missing],
            "added":[{"category":c,"marker":m,"anchor":an} for c,m,an in added]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('before'); ap.add_argument('after'); ap.add_argument('--json',action='store_true')
    args=ap.parse_args(); report=compare(extract(Path(args.before).read_text(encoding='utf-8')),extract(Path(args.after).read_text(encoding='utf-8')))
    changed=bool(report['missing'] or report['added'])
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    elif not changed: print('OK: no semantic-sentinel differences detected.')
    else:
        print('Review semantic-sentinel differences:')
        for label in ('missing','added'):
            for x in report[label]: print(f"- {label}: {x['category']} [{x['marker']}] near [{x['anchor']}]")
    return 1 if changed else 0
if __name__=='__main__': raise SystemExit(main())

#!/usr/bin/env python3
"""Conservative condition/exception clause preservation checker."""
from __future__ import annotations
import argparse, collections, json, re
from pathlib import Path

MARKERS={
 "condition":["إذا","اذا","إن","ان","عندما","متى","في حال","بشرط","شريطة","ما لم","طالما"],
 "exception":["إلا","الا","باستثناء","عدا","سوى","ما عدا","إلا إذا","الا اذا"],
}
SENT=re.compile(r"[^.!؟\n]+[.!؟]?|[^\n]+$")
WORD=re.compile(r"[\u0600-\u06FFA-Za-z0-9%٪._/-]+")
STOP={"في","من","إلى","الى","على","عن","مع","و","أو","او","أن","ان","إن","هو","هي","هذا","هذه","ذلك","تلك"}

def norm(s:str)->str:
    return re.sub(r"\s+"," ",s.strip()).casefold()

def content_anchor(sentence:str, marker:str)->str:
    words=[norm(w) for w in WORD.findall(sentence) if norm(w) not in STOP and norm(w)!=norm(marker)]
    return " ".join(words[:5]+words[-5:])[:180]

def extract(text:str):
    items=[]
    for sm in SENT.finditer(text):
        sentence=norm(sm.group(0))
        if not sentence: continue
        for cat,markers in MARKERS.items():
            for marker in sorted(markers,key=len,reverse=True):
                p=norm(marker)
                if re.search(rf"(?<![\w\u0600-\u06FF]){re.escape(p)}(?![\w\u0600-\u06FF])",sentence):
                    items.append({"category":cat,"marker":p,"anchor":content_anchor(sentence,p),"clause":sentence})
                    break
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
    elif not changed: print('OK: no condition/exception differences detected.')
    else:
        print('Review condition/exception differences:')
        for k in ('missing','added'):
            for x in report[k]: print(f"- {k}: {x['category']} [{x['marker']}] near [{x['anchor']}]")
    return 1 if changed else 0
if __name__=='__main__': raise SystemExit(main())

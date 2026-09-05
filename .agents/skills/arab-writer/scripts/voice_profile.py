#!/usr/bin/env python3
"""Build lightweight, non-authoritative style metrics from Arabic writing samples."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

SENT_SPLIT=re.compile(r"(?<=[.!؟])\s+|\n+")
WORD=re.compile(r"[\u0600-\u06FFA-Za-z]+")
CONNECTORS=["لكن","لذلك","لذا","كما","أيضًا","ايضاً","إضافة","بالتالي","مع ذلك","من جهة","في المقابل"]

def profile(text):
    sents=[s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    lengths=[len(WORD.findall(s)) for s in sents]
    words=WORD.findall(text)
    return {"sentences":len(sents),"words":len(words),"avg_sentence_words":round(sum(lengths)/len(lengths),2) if lengths else 0,"median_sentence_words":sorted(lengths)[len(lengths)//2] if lengths else 0,"short_sentence_share":round(sum(1 for x in lengths if x<=7)/len(lengths),3) if lengths else 0,"question_marks_per_1k_words":round(text.count('؟')*1000/max(1,len(words)),2),"exclamations_per_1k_words":round(text.count('!')*1000/max(1,len(words)),2),"connector_counts":{c:text.count(c) for c in CONNECTORS if text.count(c)}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('files',nargs='+'); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
    text='\n'.join(Path(p).read_text(encoding='utf-8') for p in args.files); print(json.dumps(profile(text),ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())

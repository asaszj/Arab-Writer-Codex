#!/usr/bin/env python3
"""Semantic repetition v2 for Arabic editorial review.

Combines normalized lexical overlap, character n-gram similarity and proposition
signals. It reports candidates only and distinguishes likely duplication from
elaboration/summary when possible.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from difflib import SequenceMatcher

AR_WORD=re.compile(r"[\u0621-\u063A\u0641-\u064A]{2,}")
NUM=re.compile(r"[0-9٠-٩]+")
STOP={"هذا","هذه","ذلك","تلك","التي","الذي","من","في","على","إلى","الى","عن","مع","ثم","كما","قد","تم","كان","كانت","وكانت","هو","هي","أن","إن","وأن","فإن","لكن","بين","بعد","قبل","عند","حتى","أو","او","كل","غير","أي","اي","هنا","هناك","وفق","ضمن","خلال","لدى","لديها","ولم","لم","تكن","تستخدم","ستخدم","بوصف","بوصفها"}
SYN={
    "ارقام":"بيانات","رقم":"بيان","بيانات":"بيانات","المعلومات":"بيانات","معلومات":"بيانات",
    "منشوره":"نشر","منشورة":"نشر","معلن":"نشر","معلنه":"نشر","معلنة":"نشر","نشرت":"نشر","نشر":"نشر",
    "لاحقا":"لاحق","لاحقة":"لاحق","اللاحقه":"لاحق","اللاحقة":"لاحق",
    "التعديلات":"تعديل","تعديل":"تعديل","المعدله":"تعديل","المعدلة":"تعديل",
    "النهائيه":"نهائي","النهائية":"نهائي","نهائيه":"نهائي","نهائية":"نهائي",
    "النتائج":"نتيجة","نتائج":"نتيجة","النتيجه":"نتيجة","النتيجة":"نتيجة",
    "وقت":"زمن","انذاك":"زمن","آنذاك":"زمن","ظهور":"ظهر","ظهرت":"ظهر","عقب":"لاحق","لاحق":"لاحق",
    "عرض":"عرض","إعادة":"اعادة","اعادة":"اعادة","إصدار":"اصدار","اصدار":"اصدار",
}
PREFIXES=("وال","بال","كال","فال","لل")
SUFFIXES=("هما","كما","كم","كن","هم","هن","ها","ه","نا")

def normalize_token(token:str)->str:
    t=re.sub(r"[\u064B-\u065F\u0670]","",token)
    t=t.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي").replace("ة","ه")
    for p in PREFIXES:
        if t.startswith(p) and len(t)-len(p)>=3:
            t=t[len(p):]; break
    if t.startswith("ال") and len(t)>4: t=t[2:]
    for s in SUFFIXES:
        if t.endswith(s) and len(t)-len(s)>=3:
            t=t[:-len(s)]; break
    return SYN.get(t,t)

def content_tokens(text:str):
    return [normalize_token(x) for x in AR_WORD.findall(text) if normalize_token(x) not in STOP and len(normalize_token(x))>=3]

def char_ngrams(text:str,n=3):
    s=" ".join(content_tokens(text))
    if len(s)<n: return set()
    return {s[i:i+n] for i in range(len(s)-n+1)}

def _set_score(x:set,y:set):
    if not x or not y: return 0.0
    inter=len(x&y); j=inter/len(x|y); containment=inter/min(len(x),len(y))
    return 0.55*j+0.45*containment

def similarity(a:str,b:str)->float:
    xt,yt=set(content_tokens(a)),set(content_tokens(b))
    token=_set_score(xt,yt)
    ng=_set_score(char_ngrams(a),char_ngrams(b))
    seq=SequenceMatcher(None," ".join(content_tokens(a))," ".join(content_tokens(b))).ratio()
    return round(0.52*token+0.28*ng+0.20*seq,3)

def proposition_signature(text:str):
    toks=set(content_tokens(text)); nums=set(NUM.findall(text))
    return {"tokens":toks,"numbers":nums}

def classify_pair(a:str,b:str,score:float):
    pa,pb=proposition_signature(a),proposition_signature(b)
    new_tokens=pb["tokens"]-pa["tokens"]; new_nums=pb["numbers"]-pa["numbers"]
    if score>=0.72 and not new_nums and len(new_tokens)<=2: return "likely_duplicate"
    if score>=0.50 and (new_nums or len(new_tokens)>=3): return "possible_elaboration"
    if score>=0.46 and len(b)<0.75*len(a): return "possible_summary"
    return "possible_repetition"

def paragraphs(text:str):
    if "\n\n" in text: return [p.strip() for p in re.split(r"\n\s*\n",text) if p.strip()]
    return [p.strip() for p in text.splitlines() if p.strip()]

def scan(text:str,threshold:float=.44,window:int=3):
    ps=paragraphs(text); out=[]
    for i,a in enumerate(ps):
        for j in range(i+1,min(len(ps),i+1+window)):
            score=similarity(a,ps[j])
            if score>=threshold:
                cls=classify_pair(a,ps[j],score)
                out.append({"code":"possible_semantic_repetition","classification":cls,"paragraph_a":i+1,"paragraph_b":j+1,"score":score,"message":"Review function before deletion: duplicate, elaboration, summary, cross-reference, or intentional pedagogical reinforcement."})
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--threshold",type=float,default=.44); ap.add_argument("--window",type=int,default=3); ap.add_argument("--json",action="store_true")
    args=ap.parse_args(); findings=scan(Path(args.file).read_text(encoding="utf-8"),args.threshold,args.window)
    if args.json: print(json.dumps(findings,ensure_ascii=False,indent=2))
    elif findings:
        for f in findings: print(f"[{f['classification']}] p{f['paragraph_a']}/p{f['paragraph_b']} score={f['score']}")
    else: print("OK: no semantic-repetition candidates above threshold.")
    return 1 if findings else 0
if __name__=="__main__": raise SystemExit(main())

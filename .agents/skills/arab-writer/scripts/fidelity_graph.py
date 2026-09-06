#!/usr/bin/env python3
"""Fidelity Relation Graph v1.3.

Builds conservative relation nodes around protected numeric facts. It is more
stable than raw lexical windows because it normalizes numeric value, measure,
time and source-status separately.

This is not a full semantic parser. Unknown relations stay reviewable.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
try:
    from numeral_policy import canonical_number, NUM_RE
except ImportError:
    import importlib.util
    _p=Path(__file__).with_name("numeral_policy.py")
    _s=importlib.util.spec_from_file_location("numeral_policy",_p); _m=importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
    canonical_number,NUM_RE=_m.canonical_number,_m.NUM_RE

SENT_RE=re.compile(r"[^.!؟\n]+[.!؟]?",re.M)
WORD_RE=re.compile(r"[\u0600-\u06FFA-Za-z]+")
YEAR_RE=re.compile(r"(?:19|20)\d{2}|[١٢][٠-٩]{3}")
UNITS=[
    ("sar",re.compile(r"\b(?:ريال|ريالا|ريالاً|ر\.?س\.?|SAR)\b",re.I)),
    ("usd",re.compile(r"\b(?:دولار|USD)\b",re.I)),
    ("percent",re.compile(r"[%٪]")),
    ("million",re.compile(r"\b(?:مليون|ملايين)\b")),
    ("billion",re.compile(r"\b(?:مليار|مليارات)\b")),
    ("thousand",re.compile(r"\b(?:ألف|الف|آلاف)\b")),
]
MEASURES=[
    ("revenue",r"(?:الإيرادات|الايرادات|إيرادات)"),
    ("net_profit",r"(?:صافي\s+الربح|الربح\s+الصافي)"),
    ("net_loss",r"(?:صافي\s+الخسارة|الخسارة\s+الصافية)"),
    ("operating_profit",r"(?:الربح\s+التشغيلي)"),
    ("operating_loss",r"(?:الخسارة\s+التشغيلية)"),
    ("cost",r"(?:التكاليف|التكلفة|تكلفة\s+\S+)"),
    ("compensation",r"(?:التعويض|تعويض)"),
    ("claim",r"(?:المطالبة|مطالبة)"),
    ("debt",r"(?:إجمالي\s+الدين|اجمالي\s+الدين|صافي\s+الدين|الدين)"),
    ("ebitda",r"(?:EBITDA|الربح\s+قبل\s+الفوائد\s+والضرائب\s+والاستهلاك\s+والإطفاء)"),
    ("subscribers",r"(?:المشتركين|المشترك|مشترك)"),
    ("earnings_per_share",r"(?:ربحية\s+السهم)"),
]
STATUS=[
    ("preliminary",r"(?:أولي|أولية|معلن\s+أولاً|معلنة\s+أولاً|المعلن\s+أولي)"),
    ("audited",r"(?:مدقق|مدققة|المدققة)"),
    ("restated",r"(?:معاد\s+العرض|أعيد\s+عرض|اعيد\s+عرض)"),
    ("reissued",r"(?:معاد\s+الإصدار|إعادة\s+الإصدار|أعيد\s+إصدار)"),
    ("estimated",r"(?:تقديري|تقريباً|تقريبا|نحو)"),
]
STOP={"في","من","إلى","الى","على","عن","مع","و","أو","او","أن","ان","هذا","هذه","ذلك","تلك","بلغ","بلغت","قيمة","قدرها","قدره","نسبة","عدد"}

def norm_text(s:str)->str:
    s=re.sub(r"[\u064B-\u065F\u0670]","",s)
    s=s.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي")
    return re.sub(r"\s+"," ",s).strip().casefold()

def _nearest_measure(sentence:str,pos:int):
    candidates=[]
    for name,pat in MEASURES:
        for m in re.finditer(pat,sentence,re.I):
            dist=min(abs(pos-m.start()),abs(pos-m.end()))
            candidates.append((dist,name,m.group(0)))
    if not candidates: return ("unknown",None)
    candidates.sort(key=lambda x:x[0])
    return (candidates[0][1],candidates[0][2])

def _unit_near(sentence:str,start:int,end:int):
    local=sentence[max(0,start-25):min(len(sentence),end+35)]
    for name,pat in UNITS:
        if pat.search(local): return name
    return None

def _status(sentence:str):
    out=[]
    for name,pat in STATUS:
        if re.search(pat,sentence,re.I): out.append(name)
    return sorted(set(out))

def _time(sentence:str):
    return [m.group(0) for m in YEAR_RE.finditer(sentence)]

def _entity_tokens(sentence:str, value_span:tuple[int,int], measure_surface:str|None):
    work=sentence
    if measure_surface: work=work.replace(measure_surface," ")
    work=NUM_RE.sub(" ",work)
    toks=[norm_text(w) for w in WORD_RE.findall(work)]
    toks=[t for t in toks if t not in STOP and len(t)>=3]
    return toks[:5]

def extract(text:str):
    nodes=[]
    for si,sm in enumerate(SENT_RE.finditer(text),1):
        sentence=sm.group(0).strip()
        if not sentence: continue
        times=_time(sentence); statuses=_status(sentence)
        for nm in NUM_RE.finditer(sentence):
            surface=nm.group(0); canon=canonical_number(surface)
            if canon is None: continue
            measure,measure_surface=_nearest_measure(sentence,nm.start())
            nodes.append({
                "kind":"numeric_fact",
                "value":canon,
                "surface":surface,
                "measure":measure,
                "unit":_unit_near(sentence,nm.start(),nm.end()),
                "time":times,
                "status":statuses,
                "entities":_entity_tokens(sentence,(nm.start(),nm.end()),measure_surface),
                "sentence_index":si,
                "sentence":sentence[:280],
            })
    return nodes

def _value_key(n):
    return (n["value"]["value"],n["value"]["percent"])

def _compat_score(b,a):
    if _value_key(b)!=_value_key(a): return -1
    score=4
    if b["measure"]==a["measure"]: score+=4
    elif "unknown" not in {b["measure"],a["measure"]}: score-=5
    if b["unit"]==a["unit"]: score+=2
    elif b["unit"] and a["unit"]: score-=2
    bt,at=set(b["time"]),set(a["time"])
    if bt and at:
        score += 2 if bt & at else -3
    bs,ass=set(b["status"]),set(a["status"])
    if bs and ass:
        score += 2 if bs & ass else -2
    be,ae=set(b["entities"]),set(a["entities"])
    if be and ae: score += min(2,2*len(be&ae)/max(1,len(be|ae)))
    return score

def compare(before,after):
    unmatched=set(range(len(after)))
    matched=[]; issues=[]
    for bi,b in enumerate(before):
        ranked=sorted(((_compat_score(b,after[ai]),ai) for ai in unmatched),reverse=True)
        if not ranked or ranked[0][0] < 3:
            same=[ai for ai in unmatched if _value_key(after[ai])==_value_key(b)]
            if same:
                issues.append({"code":"relation_changed","before":b,"candidates":[after[i] for i in same[:3]]})
            else:
                issues.append({"code":"numeric_fact_missing","before":b})
            continue
        score,ai=ranked[0]; a=after[ai]; unmatched.remove(ai)
        matched.append({"before":b,"after":a,"score":round(score,3),"presentation_changed":b["surface"]!=a["surface"]})
        if b["measure"]!=a["measure"] and "unknown" not in {b["measure"],a["measure"]}:
            issues.append({"code":"measure_changed","before":b,"after":a})
        if b["time"] and a["time"] and not (set(b["time"])&set(a["time"])):
            issues.append({"code":"time_changed","before":b,"after":a})
    for ai in sorted(unmatched):
        issues.append({"code":"numeric_fact_added","after":after[ai]})
    return {"matched":matched,"issues":issues}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("before"); ap.add_argument("after"); ap.add_argument("--json",action="store_true")
    args=ap.parse_args()
    r=compare(extract(Path(args.before).read_text(encoding="utf-8")),extract(Path(args.after).read_text(encoding="utf-8")))
    if args.json: print(json.dumps(r,ensure_ascii=False,indent=2))
    elif not r["issues"]: print(f"OK: {len(r['matched'])} numeric relations preserved.")
    else:
        print("Review fidelity-graph issues:")
        for x in r["issues"]: print("-",x["code"])
    return 1 if r["issues"] else 0
if __name__=="__main__": raise SystemExit(main())

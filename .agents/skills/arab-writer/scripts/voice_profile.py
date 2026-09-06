#!/usr/bin/env python3
"""Voice Profile v3 — style drift metrics with tolerance bands.

This is not an authorship detector. It helps distinguish acceptable editorial
movement from potentially excessive style drift.
"""
from __future__ import annotations
import argparse, json, re, statistics
from pathlib import Path
SENT_SPLIT=re.compile(r"(?<=[.!؟])\s+|\n+")
WORD=re.compile(r"[\u0600-\u06FFA-Za-z]+")
CONNECTORS=["لكن","لذلك","لذا","كما","أيضًا","ايضا","بالتالي","مع ذلك","في المقابل","وعليه","ثم"]
FIRST=["أنا","انا","نحن","لدينا","عندي","عندنا","أرى","ارى","نرى"]
DIALECT=["وش","أبي","ابي","أبغى","ابغى","ودي","ترى","كذا","الحين","ذحين","مو","ليه","شلون","عشان","مره"]
METRIC_SCALES={"avg_sentence_words":20,"median_sentence_words":20,"sentence_std":15,"short_sentence_share":1,"long_sentence_share":1,"avg_paragraph_words":100,"lexical_diversity":1,"question_marks_per_1k":20,"exclamations_per_1k":20,"arabic_commas_per_1k":50,"connector_rate_per_1k":30,"first_person_rate_per_1k":30,"dialect_marker_rate_per_1k":30}
DEFAULT_TOLERANCE={"avg_sentence_words":0.15,"median_sentence_words":0.15,"sentence_std":0.20,"short_sentence_share":0.18,"long_sentence_share":0.15,"avg_paragraph_words":0.15,"lexical_diversity":0.10,"question_marks_per_1k":0.20,"exclamations_per_1k":0.20,"arabic_commas_per_1k":0.18,"connector_rate_per_1k":0.20,"first_person_rate_per_1k":0.15,"dialect_marker_rate_per_1k":0.15}

def _bounded_count(text,phrase): return len(re.findall(rf"(?<![\w\u0600-\u06FF]){re.escape(phrase)}(?![\w\u0600-\u06FF])",text,re.I))

def profile(text):
    sents=[s.strip() for s in SENT_SPLIT.split(text) if s.strip()]; lengths=[len(WORD.findall(s)) for s in sents]; words=[w.casefold() for w in WORD.findall(text)]
    uniq=len(set(words)); n=max(1,len(words)); ns=max(1,len(sents)); paragraphs=[p for p in re.split(r"\n\s*\n",text) if p.strip()]
    return {"sentences":len(sents),"words":len(words),"avg_sentence_words":round(sum(lengths)/ns,3) if lengths else 0,"median_sentence_words":round(statistics.median(lengths),3) if lengths else 0,"sentence_std":round(statistics.pstdev(lengths),3) if len(lengths)>1 else 0,"short_sentence_share":round(sum(1 for x in lengths if x<=7)/ns,3) if lengths else 0,"long_sentence_share":round(sum(1 for x in lengths if x>=25)/ns,3) if lengths else 0,"avg_paragraph_words":round(n/max(1,len(paragraphs)),3),"lexical_diversity":round(uniq/n,3),"question_marks_per_1k":round(text.count('؟')*1000/n,3),"exclamations_per_1k":round(text.count('!')*1000/n,3),"arabic_commas_per_1k":round(text.count('،')*1000/n,3),"connector_rate_per_1k":round(sum(_bounded_count(text,c) for c in CONNECTORS)*1000/n,3),"first_person_rate_per_1k":round(sum(_bounded_count(text,c) for c in FIRST)*1000/n,3),"dialect_marker_rate_per_1k":round(sum(_bounded_count(text,c) for c in DIALECT)*1000/n,3)}

def compare(reference,candidate,tolerance=None):
    tolerance=tolerance or DEFAULT_TOLERANCE; diffs={}; vals=[]; outside=[]
    for k,scale in METRIC_SCALES.items():
        d=min(1.0,abs(reference.get(k,0)-candidate.get(k,0))/max(scale,1e-9)); diffs[k]=round(d,3); vals.append(d)
        if d>tolerance.get(k,0.15): outside.append(k)
    drift=sum(vals)/len(vals) if vals else 0
    band='minimal' if drift<=0.04 else 'acceptable_editorial' if drift<=0.08 else 'review' if drift<=0.14 else 'high_drift'
    return {"similarity_score":round((1-drift)*100,1),"normalized_drift":round(drift,3),"drift_band":band,"within_global_tolerance":band in {'minimal','acceptable_editorial'},"dimensions":diffs,"outside_dimension_tolerance":outside,"principle":"Do not maximize similarity blindly; acceptable drift may be justified by measurable clarity/correctness gain."}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('files',nargs='*'); ap.add_argument('--reference',nargs='+'); ap.add_argument('--candidate'); args=ap.parse_args()
    if args.reference and args.candidate:
        rt='\n'.join(Path(p).read_text(encoding='utf-8') for p in args.reference); ct=Path(args.candidate).read_text(encoding='utf-8'); rp,cp=profile(rt),profile(ct); print(json.dumps({"reference":rp,"candidate":cp,"comparison":compare(rp,cp)},ensure_ascii=False,indent=2)); return 0
    if not args.files: raise SystemExit('provide files or --reference ... --candidate ...')
    text='\n'.join(Path(p).read_text(encoding='utf-8') for p in args.files); print(json.dumps(profile(text),ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())

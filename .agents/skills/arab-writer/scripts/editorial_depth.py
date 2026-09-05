#!/usr/bin/env python3
"""Editorial opportunity scanner for Arabic prose.

This is a review-signal generator, not an automatic rewriter. It helps detect
under-editing after a safe first pass by surfacing awkward phrasing, overloaded
sentences and meta-sentences that may deserve editorial attention.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

WORD = re.compile(r"[\u0600-\u06FFA-Za-z]+")
SENTENCE = re.compile(r"[^.!؟\n]+[.!؟]?", re.M)

PHRASE_PATTERNS = [
    ("awkward_expansion_phrase", re.compile(r"ضمن\s+سلسلة\s+من\s+(?:ال)?(?:توسع|التوسع|تطور|التطور)"), "Consider a more direct relation such as 'في سياق...' if meaning is unchanged."),
    ("awkward_trading_phrase", re.compile(r"تعليق\s+للتداول"), "Review whether 'تعليق التداول' is the intended natural phrasing."),
    ("awkward_agentive_phrase", re.compile(r"فحص\s+من\s+(?:هيئة|الهيئة|الجهة|لجنة|اللجنة)"), "Consider an explicit agentive verb such as 'فحص أجرته...' if supported."),
]
META_PATTERNS = [
    re.compile(r"^\s*(?:يعرض|تعرض|يستعرض|تستعرض)\s+(?:هذه|هذا|نتائج|القسم|الفصل)"),
    re.compile(r"^\s*(?:يبين|يوضح)\s+(?:هذا\s+القسم|هذا\s+الفصل)"),
]
CONNECTORS = re.compile(r"\b(?:و|ثم|كما|بينما|إذ|حيث|لكن|لذلك|وعليه|وبعد|وقبل)\b")

def _snippet(text: str, limit: int = 180) -> str:
    t = " ".join(text.split())
    return t if len(t) <= limit else t[:limit-1] + "…"

def scan(text: str):
    findings = []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for pi, paragraph in enumerate(paragraphs, 1):
        for code, pattern, message in PHRASE_PATTERNS:
            if pattern.search(paragraph):
                findings.append({"code": code, "severity": "medium", "paragraph": pi, "message": message, "snippet": _snippet(paragraph)})
        if any(p.search(paragraph) for p in META_PATTERNS):
            findings.append({"code": "possible_meta_sentence", "severity": "low", "paragraph": pi, "message": "Review whether this sentence describes the text instead of adding content, especially if it follows the material it summarizes.", "snippet": _snippet(paragraph)})
        for sentence in SENTENCE.findall(paragraph):
            words = WORD.findall(sentence)
            factual = len(re.findall(r"(?:\d{2,4}|[٠-٩]{2,4})", sentence))
            connectors = len(CONNECTORS.findall(sentence))
            if len(words) >= 38 and (factual >= 3 or connectors >= 4):
                findings.append({"code": "high_factual_sentence_complexity", "severity": "medium", "paragraph": pi, "message": "Dense sentence: review whether it can be split without separating a condition, exception, date or protected relationship from its fact.", "metrics": {"words": len(words), "factual_tokens": factual, "connectors": connectors}, "snippet": _snippet(sentence)})
    return findings

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--json", action="store_true"); args = ap.parse_args()
    findings = scan(Path(args.file).read_text(encoding="utf-8"))
    if args.json: print(json.dumps(findings, ensure_ascii=False, indent=2))
    elif findings:
        for f in findings: print(f'paragraph {f["paragraph"]} [{f["code"]}] {f["message"]} :: {f["snippet"]}')
    else: print("OK: no deterministic editorial-opportunity findings.")
    return 1 if findings else 0

if __name__ == "__main__": raise SystemExit(main())

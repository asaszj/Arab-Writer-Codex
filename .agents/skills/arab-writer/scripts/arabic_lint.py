#!/usr/bin/env python3
"""Heuristic Arabic prose linter.

Reports likely mechanical issues. It intentionally avoids auto-correction.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

AR = r"\u0600-\u06FF"

CHECKS = [
    ("multiple_spaces", re.compile(r"(?m)(?<!^)[ \t]{2,}"), "Multiple spaces"),
    ("space_before_punctuation", re.compile(r"\s+[،؛؟,.!?]"), "Space before punctuation"),
    ("latin_comma_between_arabic", re.compile(rf"[{AR}]\s*,\s*[{AR}]"), "Latin comma inside Arabic prose"),
    ("latin_question_after_arabic", re.compile(rf"[{AR}][^?\n]*\?"), "Latin question mark in Arabic prose"),
    ("duplicate_punctuation", re.compile(r"([،؛:,.!?؟])\1+"), "Duplicated punctuation"),
    ("tatweel", re.compile(r"ـ{2,}"), "Repeated tatweel"),
    ("zero_width", re.compile(r"[\u200b\u200c\u200d\ufeff]"), "Zero-width/invisible character"),
    ("adjacent_duplicate_word", re.compile(rf"\b([{AR}]+)\s+\1\b", re.I), "Repeated adjacent word"),
]

def line_col(text: str, pos: int) -> tuple[int, int]:
    line = text.count("\n", 0, pos) + 1
    last = text.rfind("\n", 0, pos)
    col = pos + 1 if last < 0 else pos - last
    return line, col

def lint(text: str):
    findings = []
    for code, pattern, msg in CHECKS:
        for m in pattern.finditer(text):
            line, col = line_col(text, m.start())
            findings.append({
                "code": code,
                "message": msg,
                "line": line,
                "column": col,
                "match": m.group(0)[:80],
            })
    return sorted(findings, key=lambda x: (x["line"], x["column"], x["code"]))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text = Path(args.file).read_text(encoding="utf-8")
    findings = lint(text)
    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("OK: no heuristic lint findings.")
            return 0
        for f in findings:
            print(f'{f["file"] if "file" in f else args.file}:{f["line"]}:{f["column"]} [{f["code"]}] {f["message"]}: {f["match"]!r}')
    return 1 if findings else 0

if __name__ == "__main__":
    raise SystemExit(main())

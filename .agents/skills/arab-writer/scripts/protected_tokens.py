#!/usr/bin/env python3
"""Compare protected tokens between source and edited text.

This is a conservative QA helper. It flags possible losses/changes; it does not
decide whether a change is wrong.
"""
from __future__ import annotations
import argparse, collections, json, re
from pathlib import Path

AR_DIGITS = "٠١٢٣٤٥٦٧٨٩"
NUM = rf"[0-9{AR_DIGITS}]"

PATTERNS = {
    "url": re.compile(r"https?://[^\s<>()]+", re.I),
    "email": re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"),
    "doi": re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.I),
    "percent": re.compile(rf"{NUM}+(?:[.,٫]{NUM}+)?\s*[%٪]"),
    "date_numeric": re.compile(rf"\b{NUM}{{1,4}}[/-]{NUM}{{1,2}}[/-]{NUM}{{1,4}}\b"),
    "standard": re.compile(r"\b(?:ISO|IEC|EN|ASTM|GMDN|IFRS|IAS|ISA)\s*[A-Z0-9-]*(?::[0-9]{4})?\b", re.I),
    "money": re.compile(rf"{NUM}[\d{AR_DIGITS},٬.٫]*\s*(?:ريال(?:اً)?|ر\.?س\.?|SAR|USD|EUR|دولار|يورو)\b", re.I),
    "id_like": re.compile(rf"\b(?=[A-Z0-9_-]*{NUM})[A-Z][A-Z0-9_-]{{2,}}\b", re.I),
    "number": re.compile(rf"(?<![\w])[-+]?{NUM}[\d{AR_DIGITS},٬.٫]*(?![\w])"),
}

AR_MONTHS = (
    "يناير|فبراير|مارس|أبريل|ابريل|مايو|يونيو|يوليو|أغسطس|اغسطس|"
    "سبتمبر|أكتوبر|اكتوبر|نوفمبر|ديسمبر|محرم|صفر|ربيع الأول|ربيع الآخر|"
    "جمادى الأولى|جمادى الآخرة|رجب|شعبان|رمضان|شوال|ذو القعدة|ذو الحجة"
)
PATTERNS["date_named"] = re.compile(rf"{NUM}{{1,2}}\s+(?:{AR_MONTHS})\s+{NUM}{{3,4}}")

def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def extract(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for name, pattern in PATTERNS.items():
        vals = [m.group(0).strip(".,،؛;") for m in pattern.finditer(text)]
        out[name] = vals
    return out

def diff(before: dict[str, list[str]], after: dict[str, list[str]]) -> dict[str, dict[str, list[str]]]:
    result = {}
    for name in before:
        b = collections.Counter(before[name])
        a = collections.Counter(after[name])
        missing = list((b - a).elements())
        added = list((a - b).elements())
        if missing or added:
            result[name] = {"missing": missing, "added": added}
    return result

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    report = diff(extract(read_text(args.before)), extract(read_text(args.after)))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if not report:
            print("OK: no protected-token differences detected.")
            return 0
        print("Review protected-token differences:")
        for category, changes in report.items():
            print(f"\n[{category}]")
            if changes["missing"]:
                print("  missing:", ", ".join(changes["missing"]))
            if changes["added"]:
                print("  added:", ", ".join(changes["added"]))
    return 1 if report else 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run protected-token comparison plus Arabic mechanical linting."""
from __future__ import annotations
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod

protected = load("protected_tokens", "protected_tokens.py")
lintmod = load("arabic_lint", "arabic_lint.py")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    args = ap.parse_args()

    before_text = Path(args.before).read_text(encoding="utf-8")
    after_text = Path(args.after).read_text(encoding="utf-8")

    token_report = protected.diff(protected.extract(before_text), protected.extract(after_text))
    lint_report = lintmod.lint(after_text)

    if token_report:
        print("Protected-token review:")
        for category, changes in token_report.items():
            print(f"- {category}:")
            if changes["missing"]:
                print("  missing:", ", ".join(changes["missing"]))
            if changes["added"]:
                print("  added:", ", ".join(changes["added"]))
    else:
        print("Protected tokens: OK")

    if lint_report:
        print("\nArabic lint review:")
        for f in lint_report:
            print(f'- line {f["line"]}, col {f["column"]} [{f["code"]}] {f["message"]}: {f["match"]!r}')
    else:
        print("Arabic lint: OK")

    return 1 if token_report or lint_report else 0

if __name__ == "__main__":
    raise SystemExit(main())

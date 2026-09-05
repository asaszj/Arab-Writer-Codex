#!/usr/bin/env python3
"""Validate Arab Writer skill structure with no third-party dependencies."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"

REQUIRED = [
    "references/arabic-core.md",
    "references/naturalness.md",
    "references/quality-gates.md",
    "agents/openai.yaml",
    "scripts/arabic_lint.py",
    "scripts/protected_tokens.py",
    "scripts/qa_pair.py",
]

def main() -> int:
    errors = []
    if not SKILL.exists():
        errors.append("Missing SKILL.md")
    else:
        text = SKILL.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append("SKILL.md must start with YAML frontmatter")
        if not re.search(r"(?m)^name:\s*arab-writer\s*$", text):
            errors.append("SKILL.md name must be arab-writer")
        m = re.search(r"(?m)^description:\s*(.+)$", text)
        if not m or len(m.group(1).strip()) < 80:
            errors.append("Description is missing or too vague")
        if "user's explicit instructions" not in text.lower():
            errors.append("Skill must explicitly prioritize user instructions")

        refs = set(re.findall(r"`(references/[^`]+\.md)`", text))
        for ref in refs:
            if not (ROOT / ref).exists():
                errors.append(f"Broken reference: {ref}")

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    if errors:
        print("FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: Arab Writer skill structure is valid.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

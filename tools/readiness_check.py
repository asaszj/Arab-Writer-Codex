#!/usr/bin/env python3
"""Production-readiness check for Arab Writer v1.3.

This is a fast local preflight. It validates version alignment, core files,
benchmark coverage, and the presence of production documentation. It does not
claim writing-quality superiority; empirical quality remains a separate gate.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "1.3.0"

REQUIRED = [
    "VERSION",
    ".codex-plugin/plugin.json",
    ".agents/skills/arab-writer/SKILL.md",
    ".agents/skills/arab-writer/agents/openai.yaml",
    ".agents/skills/arab-writer/scripts/qa_pair.py",
    ".agents/skills/arab-writer/scripts/fidelity_graph.py",
    ".agents/skills/arab-writer/scripts/semantic_sentinels.py",
    ".agents/skills/arab-writer/scripts/editorial_gain.py",
    ".agents/skills/arab-writer/scripts/semantic_repetition.py",
    ".agents/skills/arab-writer/scripts/run_provenance.py",
    "evals/benchmark_matrix.json",
    "tools/release_gate.py",
    "docs/V130_ACCEPTANCE.md",
    "docs/PRODUCTION_READINESS.md",
    "docs/LONG_FORM_WORKFLOW.md",
]

errors: list[str] = []
for rel in REQUIRED:
    if not (ROOT / rel).exists():
        errors.append(f"missing: {rel}")

version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else ""
if version != EXPECTED:
    errors.append(f"VERSION={version!r}, expected {EXPECTED!r}")

plugin_path = ROOT / ".codex-plugin/plugin.json"
if plugin_path.exists():
    plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    if plugin.get("version") != EXPECTED:
        errors.append(f"plugin version={plugin.get('version')!r}, expected {EXPECTED!r}")

skill_path = ROOT / ".agents/skills/arab-writer/SKILL.md"
if skill_path.exists():
    skill = skill_path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^name:\s*arab-writer\s*$", skill):
        errors.append("SKILL.md name is not arab-writer")
    if "# Arab Writer v1.3" not in skill:
        errors.append("SKILL.md does not identify v1.3")

matrix_path = ROOT / "evals/benchmark_matrix.json"
if matrix_path.exists():
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    cases = matrix.get("cases", [])
    domains = {c.get("domain") for c in cases}
    tasks = {c.get("task") for c in cases}
    source_types = {c.get("source_type") for c in cases}
    if len(domains) < 5:
        errors.append(f"benchmark domains={len(domains)}; need >=5")
    if len(tasks) < 4:
        errors.append(f"benchmark task types={len(tasks)}; need >=4")
    if not {"real-world", "external"}.issubset(source_types):
        errors.append("benchmark matrix must include real-world and external cases")

if errors:
    print("NOT READY")
    for e in errors:
        print(f"- {e}")
    raise SystemExit(1)

print("READY: Arab Writer v1.3.0 production preflight passed.")
print("Boundary: this proves package/readiness contracts, not universal writing superiority.")

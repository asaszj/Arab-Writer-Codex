# Contributing

Contributions should improve Arabic writing quality, fidelity, or Codex usability.

## Before opening a change

Run:

```bash
python .agents/skills/arab-writer/scripts/validate_skill.py
python -m unittest discover -s tests -v
```

## Guidance changes

When adding a rule:
- explain the problem it solves;
- avoid absolute bans on common Arabic phrases;
- prefer contextual heuristics;
- add an evaluation case when the rule affects observable behavior.

## Scripts

Prefer Python standard library.
Scripts should report findings rather than silently rewrite user content.

## Scope

This repository is for Codex. Cross-agent packaging is intentionally out of scope.

# Repository Instructions

This repository contains a Codex-native Arabic writing skill.

When modifying the skill:
1. Preserve Codex compatibility.
2. Keep `SKILL.md` focused on workflow and routing.
3. Put detailed domain guidance in `references/`.
4. Do not add cross-agent compatibility layers unless explicitly requested.
5. Do not add claims about AI-detector evasion.
6. Avoid third-party Python dependencies for QA scripts unless there is a strong reason.
7. Run:
   - `python .agents/skills/arab-writer/scripts/validate_skill.py`
   - `python -m unittest discover -s tests -v`
8. Add or update regression cases when behavior changes.

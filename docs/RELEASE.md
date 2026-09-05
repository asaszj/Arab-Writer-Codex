# Release Checklist

1. Update `CHANGELOG.md`.
2. Run:
   ```bash
   python .agents/skills/arab-writer/scripts/validate_skill.py
   python -m unittest discover -s tests -v
   ```
3. Review `tests/evals.jsonl`.
4. Run:
   ```bash
   python tools/package_skill.py
   ```
5. Verify the generated ZIP contains `arab-writer/SKILL.md` at its top level.
6. Install the packaged skill in a clean Codex environment and run trigger/non-trigger smoke tests.

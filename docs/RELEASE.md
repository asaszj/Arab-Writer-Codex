# Release Checklist v1.2

1. Update `VERSION` and `CHANGELOG.md`.
2. Run deterministic gates:
   ```bash
   python .agents/skills/arab-writer/scripts/validate_skill.py
   python tools/validate_plugin.py
   python -m unittest discover -s tests -v
   ```
3. Review internal and external eval fixtures.
4. Build both distributions:
   ```bash
   python tools/package_skill.py
   python tools/package_plugin.py
   ```
5. Run a clean Codex install smoke test.
6. For a quality claim, run A/B and blinded human review; do not infer quality from CI.
7. Tag `vX.Y.Z`. The release workflow builds versioned skill/plugin ZIPs and checksums.

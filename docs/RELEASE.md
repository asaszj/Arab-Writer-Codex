# Release Checklist v1.3

1. Update `VERSION`, plugin manifest and changelog.
2. Run:
   ```bash
   python .agents/skills/arab-writer/scripts/validate_skill.py
   python tools/validate_plugin.py
   python -m unittest discover -s tests -v
   python evals/benchmark_matrix.py evals/benchmark_matrix.json
   python tools/release_gate.py --mode structural
   ```
3. Build skill/plugin packages.
4. For a writing-quality claim, produce an empirical metrics JSON from A/B + blind human review.
5. Run:
   ```bash
   python tools/release_gate.py --mode empirical --metrics evals/results/release_metrics.json
   ```
6. Do not tag a release as quality-improving if the empirical gate fails or was not run.

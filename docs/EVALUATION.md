# Evaluation — v1.1

v1.1 separates **software correctness** from **writing effectiveness**.

## Layer A — deterministic CI
Run:
```bash
python .agents/skills/arab-writer/scripts/validate_skill.py
python -m unittest discover -s tests -v
```
This validates structure and deterministic guards. It does **not** prove the skill improves writing.

## Layer B — Codex A/B
Run the same cases on the same Codex model/configuration:
- baseline: no skill;
- candidate: Arab Writer installed and explicitly invoked.

```bash
python evals/run_ab_codex.py --limit 20
```

## Layer C — hybrid scoring
Use deterministic fidelity checks + blinded human review + optional LLM judge.
See `evals/RUBRICS.md`.

## Layer D — external Arabic benchmarks
Use licensed/imported subsets from established Arabic linguistic and writing-quality benchmarks. See `docs/BENCHMARKS.md`.

## Release gate
A new release should not claim quality improvement unless:
- deterministic regressions pass;
- A/B candidate does not materially worsen fidelity;
- candidate wins or ties the baseline on predefined primary metrics;
- a human-reviewed sample supports the conclusion.

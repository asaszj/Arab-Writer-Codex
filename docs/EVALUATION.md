# Evaluation — v1.3

v1.3 separates software correctness from writing effectiveness.

## Layer A — deterministic CI
- skill/plugin validation;
- compile;
- regression tests;
- benchmark matrix coverage;
- structural release gate;
- packaging.

## Layer B — Arabic/fidelity benchmarks
Use licensed or externally referenced data where allowed, including Arabic GEC/linguistic suites and real-world regression fixtures.

## Layer C — Codex A/B
Run identical cases:
- baseline Codex;
- Codex + `$arab-writer`;
- same configured model;
- same configured reasoning;
- same task/input.

Record configured settings separately from observed runtime settings.

## Layer D — human review
Blind reviewers score:
- fidelity;
- instruction compliance;
- grammar;
- mechanics;
- naturalness;
- organization;
- voice;
- domain precision;
- under-editing;
- over-editing.

## Layer E — release gate
A release-quality claim requires an empirical metrics file and must satisfy thresholds in `tools/release_gate.py`.

No CI-only claim of writing superiority is permitted.

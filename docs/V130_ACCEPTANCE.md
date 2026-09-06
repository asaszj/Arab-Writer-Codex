# v1.3.0 Acceptance Gate — Context-Aware Arabic Editing & Evidence

## Structural gates
1. Skill and plugin version = `1.3.0`.
2. All deterministic tests pass.
3. Benchmark matrix covers at least five domains, four task types, real-world cases and external benchmark cases/adapters.
4. Context sentinels do not classify `قد أعلنت` as uncertainty.
5. `قد تعلن` remains an active uncertainty signal.
6. `تضمن التقرير...` is not classified as guarantee.
7. Fidelity graph detects value swaps across financial measures.
8. Presentation-only numeral normalization preserves semantic value.
9. `مرة أخرى` is not treated as dialect evidence; bounded colloquial markers still register.
10. Semantic repetition v2 detects the Mobily-style near-repetition fixture.
11. Editorial Gain Gate rejects/holds low-value cosmetic rewrites and accepts a clear awkwardness reduction.
12. Run provenance never claims unobserved model/reasoning as verified.
13. Skill/plugin distributions build successfully.

## Empirical release-quality gates
Required before claiming v1.3 improves writing generally:
- critical fidelity regressions = 0;
- Arabic correctness delta >= 0;
- blind human preference win rate >= 55%;
- over-editing regression rate <= 10%;
- false-positive rate <= 10%;
- no material regression on external Arabic benchmarks used in the release comparison.

Structural CI passing alone does not satisfy the empirical gate.

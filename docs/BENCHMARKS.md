# External Arabic Evaluation — v1.2

Arab Writer does not rely only on self-authored tests. v1.2 includes a small licensed human-authored Nahw-Passage fixture and adapters for larger external suites.

## Nahw (QCRI, EACL 2026)
- Natural data: Nahw-MCQ (~5K) and Nahw-Passage (100 passages with annotated grammatical/morphological errors, corrections and explanations).
- Upstream repository: `https://github.com/qcri/nahw-arabic-grammar-benchmark`
- Repository license: Apache-2.0.
- Included here: a small attributed Nahw-Passage regression subset in `evals/external/nahw_passage_sample.jsonl`.
- Adapter: `evals/adapters/nahw_passage.py`.

## AraLingBench (AbjadNLP 2026)
- 150 expert-authored items across grammar, morphology, spelling, reading comprehension and syntax.
- Upstream repository: `https://github.com/hammoudhasan/AraLingBench`
- Repository license reported upstream: MIT.
- Adapter: `evals/adapters/aralingbench.py` for exported JSON/JSONL.

## Absher (Saudi dialect/cultural benchmark)
- 18K+ MCQs across Saudi regions and pragmatic/cultural task types.
- Upstream repository: `https://github.com/renad-01/Absher-Benchmark`
- v1.2 does **not** vendor this dataset because redistribution terms must be checked independently.
- Adapter: `evals/adapters/absher.py` for a locally obtained CSV.

## TAQEEM / LAILA
Use for trait-based Arabic writing-quality evaluation (organization, vocabulary, style, development, mechanics, grammar). v1.2 documents these as human-quality references but does not copy data without explicit license verification.

## Release evidence stack
1. deterministic regression tests;
2. human-authored grammar fixtures;
3. baseline-vs-skill Codex A/B on identical model/configuration;
4. blind human review on a sample;
5. external benchmark adapters where licenses permit.

A release must not call itself “better” solely because CI passes.

# External Arabic Evaluation Sources

Arab Writer should not train its quality claims only on self-authored tests. v1.1 defines an external-benchmark intake plan.

Candidate sources (subject to each dataset's license/terms):
- Nahw — Arabic grammar understanding/correction/explanation benchmark (EACL 2026).
- AraLingBench — Arabic linguistic competence across morphology/syntax and related dimensions (AbjadNLP 2026).
- TAQEEM — multi-trait Arabic writing evaluation shared task/dataset (ArabicNLP 2025).
- LAILA — Arabic essay quality assessment corpus (EACL 2026).
- Saudi dialect/cultural competence benchmarks where licensing permits.

Do not vendor third-party benchmark data into this repository without verifying redistribution rights. Instead, provide adapters or documented import steps.

The product claim for Arab Writer should be based on:
1. internal targeted regression cases;
2. real-world native Arabic edits with expert gold/review;
3. licensed external benchmark subsets;
4. baseline vs skill A/B runs on the same model/snapshot/reasoning configuration.

# Design — Arab Writer v1.3

## 1. Small router, progressive references
`SKILL.md` carries the operating contract. Domain detail lives in `references/`.
Proofreading does not load naturalization guidance by default.

## 2. Fidelity is relational
v1.3 separates:
- token identity;
- numeric semantic value;
- numeric presentation;
- measure/entity;
- time/status/unit;
- modality/claim strength;
- structure.

The preferred high-fidelity representation is a relation graph rather than a raw lexical window.

## 3. Context beats marker lookup
Arabic operators are contextual. `قد` and `تضمن` cannot be classified reliably from the word alone.
Rules handle only high-confidence contexts; ambiguous cases stay reviewable.

## 4. Editorial Gain Gate
The system explicitly guards against both failure modes:
- under-editing;
- over-editing.

A safe edit must also be useful. Material changes should create observable correctness/clarity/organization/naturalness gain that justifies fidelity/voice/change cost.

## 5. Four-pass review
A: edit.
B: language + fidelity.
C: missed opportunities.
D: adversarial regression — what got worse?

## 6. Voice uses tolerance, not maximization
A slightly lower similarity can be acceptable if it buys real clarity and stays within tolerance.
Voice metrics are not authorship identification.

## 7. Locale is phrase/context-aware
Do not use substring counts as dialect proof. Word/phrase boundaries and pragmatic register matter.

## 8. Long documents use persistent ledgers
Chapters share terms, acronyms, numeric relations, citation forms and numeral policy.
Long documents are not unrelated chunks.

## 9. Evaluation is multi-layered
- deterministic CI;
- external Arabic benchmarks/adapters;
- Codex baseline-vs-skill;
- task-specific rubrics;
- blind human preference;
- release thresholds.

## 10. Runtime provenance
Configured model/effort and observed runtime model/effort are distinct. Prompt text is not runtime evidence.

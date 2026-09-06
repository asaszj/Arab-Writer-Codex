# Fidelity Relation Graph — v1.3

Use for high-fidelity editing where values must stay attached to the correct concept.

## Principle
Token preservation is insufficient. Protect relations such as:

`measure/entity → value → unit → time → status`

Examples:
- الإيرادات → 25,191 → مليون ريال → 2013 → معلن أولًا
- صافي الخسارة → 1,576 → مليون ريال → 2014 → معاد الإصدار

## Required behavior
- A numeric value may move in the sentence without becoming a new fact.
- A presentation-only change is not a factual change if semantic equivalence is verified.
- A value attached to a different measure/time/status is a material review signal.
- Unknown relations remain reviewable; do not invent a label.

Use `scripts/fidelity_graph.py` when plain-text before/after material is available.

The graph is conservative and not a full semantic parser. Human review remains necessary for ambiguous relations.

# Numeral Policy — v1.3

Separate **semantic numeric value** from **presentation**.

## Semantic value
Protected unless the user explicitly requests a factual change.

## Presentation policies
- `preserve-exact` — preserve glyphs/separators exactly.
- `normalize-arabic` — Arabic-Indic digits and Arabic separators.
- `normalize-western` — Western digits/separators.
- `document-consistent` — follow the established document convention.

A presentation change is permitted only when the parser can prove the same semantic value.

Example:
`٢٥,١٩1` → `٢٥٬١٩١` can be a presentation repair if semantic equivalence is verified.

Never infer or repair a genuinely ambiguous number automatically.
Use `scripts/numeral_policy.py`.

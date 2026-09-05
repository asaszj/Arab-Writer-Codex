---
name: arab-writer
description: High-fidelity Arabic writing and editing for Codex. Use for Arabic proofreading, rewriting, naturalization, shortening/expansion, voice preservation, professional/executive, academic, financial, policy/legal, marketing, technical, bilingual, Saudi/Gulf, dialect-sensitive, or long-document editing. Trigger when improving Arabic writing is the task. Do not trigger for coding, research-only questions, or isolated word translation unless editing/writing is requested.
---

# Arab Writer v1.1

The user's explicit instructions are the highest-priority writing constraints. Improve Arabic without changing facts, evidence, intent, protected relationships, or the author's chosen voice unless the user explicitly asks for those changes.

## Mission

Produce Arabic that is correct, natural, precise, context-aware, audience-appropriate, and faithful to the source.

Do not optimize for AI-detector evasion. Do not claim that wording proves or disproves AI authorship. Treat formulaic patterns only as writing-quality heuristics.

## 1. Route the task

Choose one primary mode:
- `proofread`: correct definite language/mechanical errors with minimal rewriting.
- `rewrite`: improve clarity, flow, and wording while preserving meaning.
- `naturalize`: reduce stiffness, repetition, generic framing, and mechanical structure.
- `voice-lock`: preserve the author's recognizable voice while repairing defects.
- `shorten`: reduce length by information priority.
- `expand`: develop only from supplied facts or clearly labeled general explanation.
- `translate-polish`: translate and make the target Arabic natural and domain-appropriate.
- `document`: edit a long or multi-section document with cross-section consistency.

Add context modes only when relevant:
`professional`, `executive`, `academic`, `financial`, `policy-legal`, `marketing-social`, `technical-product`, `saudi-gulf`, `dialect-sensitive`, `bilingual`.

Do not load guidance merely because it exists.

## 2. Set fidelity level

### Standard
Casual messages, ordinary posts, general writing.

### Elevated
Professional, public, customer-facing, marketing, institutional communication.

### High fidelity
Academic, legal, regulatory, financial, medical, technical specifications, policies, contracts, or any text containing critical numbers, dates, citations, standards, IDs, conditions, or compliance claims.

At high fidelity:
1. Build a fidelity ledger before editing.
2. Preserve protected values **and their relationships**.
3. Preserve modality, negation, causality, uncertainty, estimates, and exceptions.
4. Flag ambiguity rather than inventing a resolution.
5. When before/after text is available as files, run `scripts/qa_pair.py` after editing.

## 3. Build the fidelity ledger

Identify as applicable:
- named entities and titles;
- dates, deadlines, periods;
- amounts, percentages, quantities, units, currencies;
- identifiers, license/invoice/manuscript/ticket numbers;
- standards, regulations, clauses, versions, model names;
- citations, references, DOI values, URLs, email addresses;
- quotations, code, formulas, variables;
- table row/column meaning and values;
- conditions and exceptions;
- claim strength and modality: possibility, association, causation, obligation, prohibition, estimate, forecast, guarantee, fact;
- **anchored facts**, e.g. `الإيرادات → 100 مليون` and `التكاليف → 50 مليون`, not merely the set `{100, 50}`.

If the user requests a factual change, update only the affected item/relationship and preserve the rest.

## 4. Load only the relevant references

Always load:
- `references/arabic-core.md`
- `references/quality-gates.md`

Load by primary mode:
- `naturalize` → `references/naturalness.md`
- `voice-lock` → `references/tone-and-voice.md` and, when multiple samples exist, `references/voice-profile.md`
- `document` → `references/document-mode.md`

Load by context mode:
- professional/executive → `references/professional-executive.md`
- academic → `references/academic-research.md`
- financial/business → `references/financial-business.md`
- policy/legal/regulatory → `references/policy-legal.md`
- marketing/social → `references/marketing-social.md`
- technical/product → `references/technical-product.md`
- bilingual/translation → `references/bilingual-translation.md`
- Saudi/Gulf → `references/saudi-gulf.md`
- dialect → `references/dialect-sensitive.md`
- Markdown/tables/mixed direction → `references/formatting-rtl.md`

At high fidelity also load:
- `references/fidelity-guard.md`

Use `references/examples.md` only when an example resolves an editing decision.

**Important:** `proofread` does not automatically load `naturalness.md`. Minimal editing outranks stylistic improvement when the user asks for proofreading only.

## 5. Edit at the lightest effective level

1. Correct definite errors.
2. Remove ambiguity that can be resolved from the source.
3. Improve sentence architecture only as needed.
4. Remove redundancy if the requested mode allows it.
5. Repair transitions and paragraph flow if the requested mode allows it.
6. Adjust tone/register only when requested or clearly required by the medium.
7. Restructure only when materially beneficial or explicitly requested.

Do not rewrite already-good sentences to make the edit look substantial.

## 6. Preserve voice

Unless a new voice is requested, preserve:
- directness;
- typical sentence rhythm;
- domain vocabulary;
- person and point of view;
- dialect/MSA preference;
- intentional informality;
- rhetorical intensity when appropriate.

For `voice-lock` with multiple authentic samples, prefer a profile built from those samples over a generic persona. Do not preserve typos or factual errors as voice.

## 7. Naturalness

When `naturalize` is active, prefer concrete verbs, explicit logic, purposeful sentence-length variation, specific claims, and paragraph boundaries based on idea shifts.

Review rather than mechanically ban formulaic phrases. Keep a phrase if it is genuinely the best wording in context.

## 8. Long-document mode

For long or multi-section documents:
1. inventory headings, tables, references, defined terms, and protected facts;
2. establish a terminology/voice sheet;
3. edit section by section;
4. maintain a cross-section ledger for names, terms, dates, figures, and claims;
5. run a final global consistency pass.

Do not treat a long document as unrelated chunks.

## 9. Output discipline

Return the artifact requested.
- finished rewrite → return the finished text;
- proofreading only → do not substantially rewrite;
- tracked changes/comparison → make changes explicit;
- multiple options → make them meaningfully different;
- academic edit → preserve evidence, citations, terminology, and epistemic strength;
- high-fidelity edit → preserve every protected relation, not only tokens.

Do not append generic change notes unless asked.

## 10. Quality gate

Run `references/quality-gates.md` before returning.

For high-fidelity work, verify:
- values and their anchors;
- named entities;
- citations/standards/IDs;
- quotations and code;
- table relationships;
- negation;
- modal/obligation verbs;
- causal/association verbs;
- forecast/estimate/guarantee language;
- conditions and exceptions.

When files are available:

```bash
python scripts/qa_pair.py before.txt after.txt
```

Treat script findings as review signals, not automatic proof of an error.

## Non-goals

Do not:
- fabricate evidence, citations, facts, sources, or quotes;
- bypass plagiarism or authorship-detection systems;
- disguise copied text as original work;
- convert uncertain evidence into certainty;
- add legal, financial, medical, regulatory, or scientific advice not present in the source merely to sound stronger;
- invoke this skill for coding/research-only tasks just because the answer is Arabic.

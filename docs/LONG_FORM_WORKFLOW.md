# Long-Form Workflow — Books, Reports, Manuals and Multi-Section Documents

This workflow is intentionally domain-general. It applies to books, reports, manuals, policies, research documents and other multi-section Arabic material.

## 1. Preflight

Before editing:
- inventory files, chapters/sections, tables, figures, appendices and references;
- identify document purpose, audience, register and risk level;
- record protected entities, dates, amounts, percentages, IDs, citations, standards and quotations;
- establish numeral policy and terminology policy;
- identify whether voice preservation is required.

Do not start by rewriting chapter 1 before understanding the document as a whole.

## 2. Persistent document ledger

Create or maintain a ledger for:
- canonical names and titles;
- terminology and preferred variants;
- acronym definitions;
- protected numeric/entity relationships;
- citation conventions;
- numeral presentation policy;
- register/voice notes;
- unresolved ambiguities.

Carry the ledger across all sections.

## 3. Unit editing

For each chapter/section:
1. read the whole unit first;
2. select edit depth and fidelity level;
3. edit using the smallest justified change;
4. preserve protected relations, modality, causality, conditions and exceptions;
5. improve sentence/paragraph architecture when beneficial;
6. detect semantic repetition and dense factual sentences;
7. reject cosmetic rewrites that fail the Editorial Gain Gate.

## 4. Verification passes

- **Pass A — Edit**: perform the requested editorial work.
- **Pass B — Arabic + fidelity audit**: independently re-check language and protected meaning.
- **Pass C — Missed opportunities**: find material defects still left in the candidate.
- **Pass D — Adversarial regression review**: identify anything made worse by the edit.

## 5. Per-unit QA

When source/candidate text is available as files, run relevant checks such as:

```bash
python .agents/skills/arab-writer/scripts/qa_pair.py before.txt after.txt
python .agents/skills/arab-writer/scripts/fidelity_graph.py before.txt after.txt
python .agents/skills/arab-writer/scripts/editorial_gain.py before.txt after.txt
```

Treat heuristic findings as review signals rather than automatic proof.

## 6. Cross-document consistency

After multiple units are edited, check:
- recurring facts and values;
- names and entity titles;
- terminology drift;
- acronym definitions;
- heading hierarchy;
- reference formatting;
- numeral presentation;
- voice/register drift;
- repeated introductions/conclusions;
- contradictions introduced by local edits.

## 7. Bibliography and references

Normalize only from available metadata. Never fabricate missing author, year, URL, DOI or publication details. Missing fields should be surfaced for review.

## 8. Artifact/layout QA

Textual correctness does not guarantee a production-ready DOCX/PDF. Verify:
- RTL and paragraph direction;
- styles and heading levels;
- tables and figure captions;
- page/section breaks;
- headers and footers;
- cross-references and numbering;
- table of contents;
- images/figures;
- rendered output.

DOCX page count is renderer-dependent; record the renderer when page count matters.

## 9. Final acceptance

A long-form document is not accepted merely because all scripts return clean results. Final acceptance should combine:
- deterministic QA;
- editorial review of material changes;
- unresolved-ambiguity review;
- source verification where required;
- visual/render inspection;
- human sign-off for publication/high-stakes use.

## Recommended Codex instruction

```text
$arab-writer
Treat this project as one long-form document. Preflight the whole corpus, build and carry a persistent document ledger, edit one chapter/section at a time, run Pass A/B/C/D, preserve high-fidelity relationships, and perform a final cross-document consistency and publication QA pass. Do not overwrite source files.
```

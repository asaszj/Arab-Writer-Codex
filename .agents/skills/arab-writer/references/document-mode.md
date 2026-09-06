# Long-Document Mode v1.3

Use for books, reports, policies, research papers, manuals, proposals, and multi-file artifacts.

## Phase 1 — Inventory
Capture:
- purpose/audience;
- headings/sections;
- tables/figures;
- references;
- defined terms/acronyms;
- protected numeric relations;
- numeral convention;
- style/voice expectations.

## Phase 2 — Persistent ledger
Create/update a document or book ledger. Carry it across sections instead of treating chunks as unrelated.

Recommended fields:
- term forms;
- acronyms;
- named entities;
- relation graph nodes;
- citation forms;
- numeral policy;
- unresolved ambiguities.

Use `scripts/document_ledger.py` when plain-text extraction is available.

## Phase 3 — Section editing
Apply the requested mode and risk level. Preserve section-specific constraints.

## Phase 4 — Cross-section consistency
Check:
- contradictory numeric relations;
- term drift;
- acronym drift;
- citation naming drift;
- repeated explanations;
- voice drift.

## Phase 5 — Global QA
Run fidelity, editorial gain, bibliography, voice/locale, and Pass D regression review.

For explainable review, generate a paragraph-level trail with `scripts/edit_trail.py`.

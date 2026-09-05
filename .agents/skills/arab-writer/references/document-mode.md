# Long-Document Mode v1.2

Use for reports, policies, research papers, manuals, proposals, books, and other multi-section artifacts.

## Phase 1 — Inventory
Capture:
- document purpose/audience;
- heading hierarchy;
- defined terms and abbreviations;
- recurring entities;
- figures, tables, citations, standards;
- key claims and decisions;
- terminology choices;
- voice/register.

Create a cross-section ledger before editing high-fidelity documents.

## Phase 2 — Edit by section
Edit one coherent section at a time. Carry the terminology and fidelity ledger forward. Do not reset decisions at chunk boundaries.

## Phase 3 — Cross-section consistency
Check:
- the same entity is named consistently;
- acronyms are introduced and reused consistently;
- recurring anchored facts do not silently conflict;
- numbers/dates that should agree do agree;
- recommendations do not contradict findings;
- defined terms do not drift;
- headings follow one hierarchy;
- tone/voice does not drift between sections;
- references/citations remain aligned.

When a recurring label legitimately has different values across periods, include the period in the anchor rather than treating it as a contradiction.

## Phase 4 — Global QA
Run deterministic guards on the complete before/after document where possible, then review semantic findings. `scripts/document_consistency.py` supports repeated anchor conflicts, glossary drift, and acronym-definition drift.

## Failure policy
Do not “resolve” cross-section conflicts by choosing one value. Surface the conflict unless the source clearly establishes which value is authoritative.

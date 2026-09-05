# Quality Gates — v1.2.1

Run the relevant gates before final output.

## 1. Fidelity gate
Confirm:
- source meaning is preserved;
- no unsupported facts were added;
- no material conditions were dropped;
- names are intact;
- dates are intact;
- amounts and percentages are intact;
- citations and identifiers are intact;
- quoted wording is intact unless editing quotations was requested.

## 2. Claim-strength gate
Check verbs that can alter meaning: cause, prove, require, prohibit, guarantee, estimate, expect, may, associate. Ensure the revised verb matches the source.

## 3. Arabic gate
Check spelling, morphology, syntax, agreement, pronoun clarity, sentence completeness, punctuation, spacing, and terminology consistency.

## 4. Naturalness gate
Check:
- generic opening before the real point;
- repeated thesis;
- unnecessary transitions;
- forced symmetry;
- abstract noun chains;
- repetitive paragraph rhythm;
- generic conclusion;
- excessive headings/bold/bullets.

## 5. Editorial-effectiveness gate
Required for Level 3/4, `rewrite`, `naturalize`, and long-document editorial work.

Ask:
- Are clearly awkward but grammatical phrases still present?
- Is there near-semantic repetition, not just literal duplication?
- Are factual sentences overloaded with dates/entities/conditions?
- Are transitions complete and natural?
- Are there meta-sentences that merely describe already-presented content?
- Do prose and tables duplicate each other without pedagogical value?
- Are chronology-heavy passages unnecessarily repetitive?
- Was the document under-edited merely because fidelity checks passed?

A safe candidate is not automatically a finished candidate.

## 6. Audience gate
Ask internally:
- Is the register correct?
- Is the requested action obvious?
- Is the level of detail appropriate?
- Is courtesy proportional to the medium and hierarchy?

## 7. Bibliography gate
When references exist:
- check naming and punctuation consistency;
- preserve source-provided metadata;
- do not invent dates, URLs, DOI values, authors or publishers;
- apply a formal citation style only when requested or already established.

## 8. Voice gate
When Voice Lock is requested:
- use actual voice-profile measurements when source/candidate files are available;
- do not infer voice preservation from edit percentage alone;
- describe metric limitations.

## 9. High-fidelity gate
For academic, financial, legal, regulatory, medical, or technical content:
- compare protected items before/after;
- verify every numeric token;
- verify every standard/version;
- verify every exception;
- verify every reference;
- do not resolve ambiguity by invention.

## 10. Document-rendering gate
For DOCX and other layout-sensitive files:
- page count is renderer-dependent;
- identify the renderer/export when reporting pages;
- prefer stable structural counts: paragraphs, tables, images, sections, headers, footers.

## 11. QA-evidence gate
When producing a QA report, distinguish VERIFIED, MEASURED, INFERRED, NOT TESTED, and HUMAN REVIEW. Do not write categorical success claims for dimensions that were only inferred.

## 12. Output gate
Return exactly the artifact requested. Do not add a postscript that the user did not ask for.

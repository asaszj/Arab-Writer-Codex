# QA Reporting Precision

When a QA report is requested, distinguish evidence strength explicitly.

Use one of these labels when useful:
- **VERIFIED** — deterministically checked against source/candidate or an authoritative structured artifact.
- **MEASURED** — produced by a metric/script; state the metric and its limits.
- **INFERRED** — editorial/model judgment, not deterministic proof.
- **NOT TESTED** — outside the scope of the run.
- **HUMAN REVIEW** — requires expert or source-level confirmation.

Do not write `نجح` or `لا يوجد` for a dimension that was only inferred.

## Voice
If Voice Lock is used and files are available, report actual `voice_profile.py` comparison output. A low change rate is not a voice metric.

## Page count
DOCX page count is renderer-dependent. Never report an absolute page count without identifying the renderer/export used. Prefer stable structural counts such as paragraphs, tables, images, sections, headers and footers.

## Findings
Separate:
1. changes made;
2. deterministic fidelity checks;
3. editorial-quality findings;
4. unresolved ambiguities;
5. external factual verification not performed.

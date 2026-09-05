# v1.2.1 Acceptance Gate — Editorial Depth & QA Precision

This patch is driven by the first full-chapter Mobily case review. It must close real observed regressions without weakening fidelity.

## Required gates

1. Financial thousands separators such as `١,٢٢٥` and `25,191` do not trigger Arabic-prose comma warnings.
2. Genuine Latin comma usage inside Arabic prose remains detectable.
3. Known awkward phrases from the Mobily case are surfaced as editorial candidates.
4. Near-semantic repetition is surfaced for review without auto-deletion.
5. Dense factual sentences are surfaced for review without breaking protected conditions/relationships automatically.
6. `rewrite` / `naturalize` default to Level 3 editorial review, not proofread-level conservatism.
7. A final missed-opportunity pass runs for editorial/document modes.
8. QA reports label findings as VERIFIED / MEASURED / INFERRED / NOT TESTED / HUMAN REVIEW where material.
9. Voice claims use actual `voice_profile.py` measurements when source/candidate files exist.
10. DOCX page counts identify the renderer or are omitted as absolute facts.
11. Bibliography inconsistencies are audited without fabricated metadata.
12. Fidelity regressions remain release blockers.

## Evidence rule

Passing this gate proves the patch fixes targeted regressions. It does not prove global writing superiority; that still requires A/B and human review.

# Changelog

## 1.3.0 — 2026-09-06

### Context-aware Arabic editing & evidence
- Added context-aware semantic sentinels so `قد أعلنت` is not treated as uncertainty while `قد تعلن` remains an uncertainty signal.
- Removed containment forms such as `تضمن التقرير...` from guarantee classification.
- Added a Fidelity Relation Graph that protects numeric semantic value together with measure/entity, time/status, and unit.
- Added explicit separation between numeric semantic value and presentation, with `preserve-exact`, `normalize-arabic`, `normalize-western`, and `document-consistent` policies.
- Added an Editorial Gain Gate to reduce both under-editing and over-editing; material changes must justify their fidelity/voice/change cost.
- Upgraded semantic repetition detection to combine normalized lexical overlap, character n-grams and proposition signals.
- Added Pass D adversarial regression review: identify changes that are safe but not actually better.
- Upgraded Voice Profile to tolerance bands instead of blindly maximizing similarity.
- Made locale/dialect matching boundary-aware and removed ambiguous MSA `مرة` from dialect evidence.
- Added persistent document/book ledgers for terms, acronyms and protected numeric relations.
- Added schema-based bibliography extraction that keeps missing metadata null rather than fabricating it.
- Added GEC candidate adjudication against fidelity constraints.
- Added paragraph-level explainable edit trails.
- Added run provenance that separates configured model/reasoning from observed runtime model/reasoning.
- Expanded Codex A/B harness with optional reasoning-effort pinning and richer blinded human-review fields.
- Added benchmark-matrix coverage validation and structural/empirical release gates.
- Simplified `SKILL.md` around the operational loop and moved detail into progressive references.

### Evidence policy
- v1.3 structural CI does not prove writing superiority.
- General improvement claims require multi-domain A/B evaluation, external Arabic evidence where licensed, and blind human review passing the empirical release gate.

## 1.2.1 — 2026-09-05

### Editorial depth & QA precision
- Fixed financial-number lint false positives for thousands separators such as `١,٢٢٥` and `25,191` while preserving detection of Latin commas in Arabic prose.
- Added an explicit edit-depth controller; `rewrite` and `naturalize` now default to Level 3 editorial review rather than proofread-level conservatism.
- Added deterministic editorial-opportunity scanning for known awkward phrasing, dense factual sentences and possible meta-sentences.
- Added near-semantic repetition review signals with no automatic deletion.
- Added a final Pass C missed-opportunity review for editorial/document modes.
- Added conservative bibliography-consistency auditing that never fabricates missing metadata.
- Tightened Voice Lock reporting: use measured `voice_profile.py` output when files exist; low edit volume is not treated as voice evidence.
- Added evidence labels for QA reports: VERIFIED / MEASURED / INFERRED / NOT TESTED / HUMAN REVIEW.
- Made DOCX page-count reporting renderer-aware.
- Added a real-world Mobily regression fixture and v1.2.1 acceptance gate derived from a full financial/regulatory chapter-editing run.

### Evidence policy
- v1.2.1 fixes targeted real-world regressions. It still does not claim universal writing superiority without baseline-vs-skill A/B and human review.

## 1.2.0 — 2026-09-05

### Critical closures
- Added two-pass Arabic linguistic verification guidance for proofreading/high-fidelity work.
- Added a licensed human-authored Nahw-Passage regression subset plus external benchmark adapters.
- Added condition/exception preservation and locale/register drift guards.
- Added long-document consistency checks for recurring anchored facts, acronym definitions, and configured terminology.
- Upgraded voice profiling with measurable before/after drift dimensions.
- Added Saudi pragmatic/register guidance focused on hierarchy, speech act, ambiguity and dialect flattening.
- Added Codex plugin manifest, plugin validator, versioned skill/plugin packaging, and tag release workflow.
- Strengthened CI to validate plugin packaging and external evaluation fixtures.

### Evidence policy
- Deterministic CI, external fixtures, A/B runs, and human review are separate evidence layers.
- No release may claim writing superiority without actual baseline-vs-skill evidence.

## 1.1.0 — 2026-09-05

### Changed
- Reworked skill routing so proofreading no longer automatically loads naturalization guidance.
- Updated `agents/openai.yaml` default prompt to explicitly invoke `$arab-writer`.
- Renamed the mechanical checker concept to `arabic_mechanical_lint` while keeping a compatibility wrapper.
- Added long-document and profile voice-lock guidance.

### Added
- Anchored-fact QA to catch value swaps where tokens remain present.
- Semantic-sentinel QA for negation, modality, causality, uncertainty, forecasts, and guarantees.
- Quote/code/table structure guard.
- Composite v1.1 `qa_pair.py`.
- Lightweight voice-profile metrics.
- Actual Codex CLI A/B benchmark harness and blinded human-review sheet.
- Core + task-specific evaluation rubrics.
- External Arabic benchmark integration plan.

### Evaluation policy
- CI success no longer implies writing-quality improvement.
- Quality claims require baseline-vs-skill A/B evidence plus human-reviewed sampling.

## 1.0.0 — 2026-09-05
- Initial Codex-native Arab Writer release.

# Changelog

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

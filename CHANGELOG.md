# Changelog

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

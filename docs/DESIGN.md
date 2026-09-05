# Design

## 1. Codex-native progressive disclosure

Codex initially sees a skill's `name`, `description`, and path, then loads `SKILL.md` only when the task matches. The skill therefore keeps the description explicit and scoped, while detailed domain guidance lives in `references/`.

## 2. Fidelity before fluency

A fluent rewrite can still be wrong. Arab Writer treats factual preservation as a first-class editing constraint.

The protected-content ledger covers:
- entities;
- numbers;
- dates;
- citations;
- IDs;
- standards;
- conditions;
- claim strength.

## 3. Risk-adaptive editing

The same editing freedom should not be used for:
- a casual caption;
- an academic result;
- a contract clause.

The skill increases preservation requirements with risk.

## 4. Voice preservation

Many editors collapse different authors into the same polished register. Voice Lock intentionally preserves:
- directness;
- sentence rhythm;
- vocabulary;
- person;
- formality;
- dialect preference.

## 5. Naturalness without detector theater

The system removes formulaic writing because it weakens prose, not because a phrase is proof of machine authorship.

It does not:
- promise detector evasion;
- add intentional errors;
- randomize text to look "human";
- disguise copied text.

## 6. Deterministic QA where useful

Scripts are limited to tasks where deterministic checks add value:
- structural validation;
- protected-token comparison;
- mechanical Arabic linting.

Semantic writing remains instruction-led.

## 7. General, modular coverage

One skill handles the writing workflow; references provide specialized constraints. This avoids installing many overlapping skills while keeping context loading selective.

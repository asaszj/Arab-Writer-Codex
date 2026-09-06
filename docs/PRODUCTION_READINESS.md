# Arab Writer v1.3.0 — Production Readiness

Arab Writer v1.3.0 is ready for controlled production use in Arabic proofreading, rewriting, naturalization, voice-preserving editing, high-fidelity financial/legal/academic work, and long-form document editing.

## Ready for

- standalone Arabic texts;
- professional and executive writing;
- academic and research prose;
- financial, regulatory and policy documents;
- technical/product writing;
- Saudi institutional/professional Arabic;
- long chapters, reports, manuals and books;
- before/after QA where source and candidate files are available.

## Production operating rule

Use the smallest edit depth that satisfies the task. For high-risk material, fidelity outranks style.

Recommended long-form sequence:

1. Preflight the full document or corpus.
2. Build a persistent document ledger.
3. Edit section/chapter by section/chapter.
4. Run Arabic + fidelity verification after each unit.
5. Carry terminology, acronyms, numeric policy and protected relations forward.
6. Run missed-opportunity and adversarial regression review.
7. Run final cross-document consistency and bibliography audits.
8. Perform renderer/layout QA on the final artifact.
9. Route material ambiguities and source conflicts to human review.

## Quality evidence

The deterministic/structural gate validates software contracts and targeted regressions. It does not prove universal writing superiority.

A general quality claim requires the empirical gate described in `docs/V130_ACCEPTANCE.md`: multi-domain A/B runs, critical-fidelity regression rate of zero, non-negative Arabic-correctness delta, bounded over-editing/false-positive rates, and blind human preference evidence.

## Human review remains required for

- disputed or ambiguous source facts;
- legal/regulatory interpretations not explicit in the source;
- research claims requiring source verification;
- pedagogical/editorial decisions that change what information a reader receives;
- publication-level acceptance of a full book or high-stakes document.

## Before a production run

Run:

```bash
python tools/readiness_check.py
python .agents/skills/arab-writer/scripts/validate_skill.py
python tools/release_gate.py --mode structural
```

Expected first line:

```text
READY: Arab Writer v1.3.0 production preflight passed.
```

## Version pinning

For a reproducible production project, pin the skill to a known commit or the `stable/v1.3.0` branch rather than relying on future `main` changes.

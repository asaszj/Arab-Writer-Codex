# Quality Gates — v1.3

Run only the gates relevant to the task.

## 1. Fidelity
Confirm:
- facts and intent are preserved;
- no unsupported facts/citations were added;
- values remain attached to the correct measure/entity/time/status;
- conditions/exceptions remain attached to the correct rule;
- citations, standards, IDs, quotations, code and table meaning are intact.

For high-fidelity work, use the relation graph rather than token presence alone.

## 2. Claim strength
Check contextual function, not isolated words:
- possibility vs fact;
- association vs causation;
- permission vs obligation/prohibition;
- estimate/forecast vs guarantee;
- negation;
- suspicion/allegation vs final finding.

## 3. Arabic correctness
Check:
- spelling and punctuation;
- morphology;
- agreement;
- number constructions;
- pronouns/referents;
- sentence completeness;
- terminology.

If a second GEC/linguistic proposal exists, adjudicate it against fidelity before adoption.

## 4. Editorial effectiveness
A safe edit is not automatically finished.

Check:
- remaining awkward phrasing;
- semantic repetition;
- factual/chronological sentence overload;
- weak paragraph transitions;
- unnecessary meta-sentences;
- table/prose duplication;
- unnecessary lexical churn introduced by the edit.

Apply the Editorial Gain Gate to material rewrites.

## 5. Voice/locale
Check:
- register and pragmatic function;
- directness/formality;
- sentence rhythm within an acceptable tolerance;
- dialect/MSA choice;
- no accidental local slang insertion or dialect flattening.

Do not maximize similarity at the expense of clarity or correctness.

## 6. Numeric presentation
First verify semantic numeric value.
Then apply only the requested/document numeral presentation policy.

## 7. Bibliography
Verify known metadata and formatting consistency.
Missing metadata must remain missing or be flagged for human review.

## 8. Long-document consistency
Carry the persistent ledger across sections:
- terms;
- acronyms;
- named entities;
- numeric relations;
- numeral policy;
- citations.

## 9. Pass D — regression
Before returning, identify any edit that:
- is safe but not clearly better;
- weakened attribution;
- altered voice without enough benefit;
- added unnecessary structure;
- made chronology/conditions harder to follow.

Revert low-value edits.

## 10. Evidence labels
In QA reports distinguish:
- `VERIFIED`
- `MEASURED`
- `INFERRED`
- `NOT TESTED`
- `HUMAN REVIEW REQUIRED`

Do not call CI, a heuristic, or a single-model self-review proof of writing quality.

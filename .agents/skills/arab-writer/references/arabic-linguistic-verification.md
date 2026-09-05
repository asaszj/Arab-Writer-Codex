# Arabic Linguistic Verification

Use this for proofreading and any task where Arabic correctness is a primary requirement. It complements, rather than replaces, `arabic-core.md`.

## Two-pass rule

Do not assume the first correction pass is correct. After producing a candidate, audit it independently against the source.

### Pass A — correction
Correct only defects that are sufficiently supported by context. Preserve correct source forms.

### Pass B — independent audit
Review each changed span and then scan the full candidate for:
- orthography: hamza, alif maqsura/yaa, taa marbuta/haa, duplicated/missing letters;
- morphology: inflection, dual/plural forms, attached pronouns, derived forms;
- syntax: subject/predicate completeness, coordination, case-sensitive forms that are actually written, governed verb forms;
- agreement: gender, number, person, adjective/noun, verb/subject;
- number constructions and units where relevant;
- negation and particles that alter grammatical government;
- pronoun antecedents and ambiguity;
- punctuation and sentence boundaries.

## Minimality
A proofreading request is not a rewriting request. If a sentence is correct and clear, leave it alone.

## Uncertainty
If two readings are plausible and context does not resolve them, do not guess. Preserve the source or flag the ambiguity when the user asked for diagnostic feedback.

## Benchmark discipline
Internal fluency is not evidence of grammatical mastery. Regression evaluation should include natural, expert-annotated Arabic grammar/error-correction data such as Nahw-Passage and linguistic-competence suites such as AraLingBench.

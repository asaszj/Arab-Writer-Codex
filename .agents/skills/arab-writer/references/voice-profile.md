# Voice Profile v1.2

Use when the user asks to preserve a recognizable personal or organizational voice.

## Quick Voice Lock
Use the current source only. Preserve directness, formality, sentence rhythm, vocabulary level, person, dialect/MSA choice, and intentional punctuation habits.

## Profile Voice Lock
When 3+ authentic samples are available, infer a compact profile from repeated evidence rather than stereotypes:
- median/mean and spread of sentence length;
- short/long sentence share;
- paragraph length;
- lexical diversity;
- common connectors/openings;
- first-person/collective-person preference;
- punctuation density;
- formal vs conversational markers;
- dialect/MSA choice;
- recurring domain terms.

Do not imitate accidental errors. Do not overfit one unusual sample.

## Measured drift
When files are available, use `scripts/voice_profile.py --reference ... --candidate ...` to produce a heuristic drift report. The score is a regression signal, not proof of authorship.

Interpret drift dimension-by-dimension. A candidate can preserve sentence length while losing lexical/directness patterns, or preserve vocabulary while becoming generically formal.

## Decision rule
If correctness and voice conflict, correct definite errors but preserve non-error stylistic traits. If the requested task explicitly changes tone, compare only the dimensions that should remain stable.

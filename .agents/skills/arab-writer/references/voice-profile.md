# Voice Profile v1.3

Use only when the user asks to preserve a personal/organizational voice or when a long-document style must remain stable.

## Principle
Do **not** maximize similarity blindly. Editorial improvement can legitimately move sentence length or connector use.

Measure:
- sentence-length distribution;
- paragraph length;
- lexical diversity;
- connector rate;
- punctuation;
- first-person usage;
- bounded dialect markers.

Interpret drift using tolerance bands:
- `minimal`
- `acceptable_editorial`
- `review`
- `high_drift`

A lower similarity score is not automatically worse if correctness/clarity gain is real and fidelity is intact.

When multiple authentic samples exist, use them as the reference profile. A single source chapter is a weaker proxy.

`voice_profile.py` is not an authorship detector and must not be used to identify an author.

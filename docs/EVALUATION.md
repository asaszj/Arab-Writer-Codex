# Evaluation

The repository includes two layers of evaluation.

## Static tests

Run:

```bash
python -m unittest discover -s tests -v
```

These validate:
- skill structure;
- token extraction;
- protected-token differences;
- Arabic lint heuristics.

## Prompt evaluation set

`tests/evals.jsonl` contains representative prompts with:
- task;
- expected mode;
- protected invariants;
- unacceptable behavior.

Use it for manual or model-based regression evaluation when the skill changes.

## Suggested scoring

Score each output 0–2 on:

1. Fidelity
2. Arabic correctness
3. Naturalness
4. Tone fit
5. Structure
6. Terminology consistency
7. Formatting preservation
8. Constraint compliance

For high-fidelity cases, any changed protected fact should fail the case regardless of fluency score.

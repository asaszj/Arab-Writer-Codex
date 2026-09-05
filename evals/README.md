# A/B Evaluation

`run_ab_codex.py` runs each case twice using the actual Codex CLI:
1. baseline workspace with no Arab Writer skill;
2. candidate workspace containing `.agents/skills/arab-writer` and explicit `$arab-writer` invocation.

Prerequisites:
- authenticated `codex` CLI on PATH;
- network/model access available to that Codex installation.

Example:
```bash
python evals/run_ab_codex.py --limit 10
```

For a controlled model comparison:
```bash
python evals/run_ab_codex.py --model gpt-5.6-sol
```

The harness writes:
- `evals/results/ab_results.jsonl`
- `evals/results/human_review.csv`

Keep human reviewers blind to which column is baseline/candidate when doing formal evaluation.

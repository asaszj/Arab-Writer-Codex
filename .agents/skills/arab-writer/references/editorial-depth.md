# Editorial Depth Controller

Choose the lightest level that actually satisfies the user's request. Do not use edit quotas.

## Level 1 — Proofread
Correct definite linguistic/mechanical errors only. Preserve sentence architecture unless the error requires a rewrite.

## Level 2 — Light edit
Proofread plus clearly awkward wording, weak local transitions, and obvious duplication.

## Level 3 — Editorial
Default for `rewrite` and `naturalize` unless the user asks for lighter work. Review every paragraph for clarity, semantic repetition, sentence density, transition quality, meta-sentences, and paragraph architecture. Keep good sentences unchanged.

## Level 4 — Deep rewrite
Use only when explicitly requested or when the source is materially disorganized. Rebuild structure while preserving fidelity constraints.

## Under-editing control
A low percentage of changed paragraphs is not automatically a failure, but it is not evidence of quality either. After the first edit, run a **missed-opportunity review** that looks only for remaining material defects. Do not increase edit volume merely to reach a percentage.

When files are available, `scripts/editorial_depth.py` and `scripts/semantic_repetition.py` can surface review candidates. Their findings are signals, not automatic edit instructions.

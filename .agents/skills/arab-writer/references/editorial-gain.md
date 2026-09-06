# Editorial Gain Gate — v1.3

Use for rewrite/naturalize/document editing.

## Why
v1.2 under-edited; v1.2.1 fixed much of that but exposed some low-value rewrites. The solution is not an edit quota.

## Gate
For each material candidate consider:

### Gain
- definite correctness repair;
- clearer referent;
- lower sentence/factual density;
- better paragraph flow;
- removal of real redundancy;
- improved terminology consistency;
- more natural Arabic.

### Cost
- fidelity risk;
- voice/register drift;
- unnecessary lexical churn;
- weaker attribution;
- terminology disruption;
- chronology or condition separation.

Accept only when gain clearly justifies cost. Otherwise retain the source.

Run Pass D after editing: identify changes that are safe but not actually better.
Use `scripts/editorial_gain.py` as a deterministic support signal, not the final judge.

# Design — Arab Writer v1.2

## 1. Progressive disclosure
Codex initially routes on skill metadata; detailed guidance is loaded only for the active writing mode. Proofreading does not automatically load naturalization guidance.

## 2. Fidelity before fluency
Protection has four layers:
1. critical tokens;
2. anchor→value relationships;
3. semantic sentinels (negation, modality, causality, uncertainty, forecast/guarantee);
4. protected structures (quotes, code, tables).

## 3. Risk-adaptive editing
Editing freedom decreases as factual/semantic risk increases.

## 4. Voice preservation
Quick Voice Lock uses the current source. Profile Voice Lock uses repeated traits from multiple authentic samples.

## 5. Long-document coherence
Multi-section documents carry a persistent terminology/fidelity/voice ledger and receive a global consistency pass.

## 6. Deterministic QA is a reviewer, not an oracle
Scripts flag suspicious changes. Semantic intent remains model/human reviewed.

## 7. Evidence-based evolution
New prompt rules should be introduced in response to observed failures and evaluated for regressions. The repository separates CI tests from writing-quality A/B evaluation.

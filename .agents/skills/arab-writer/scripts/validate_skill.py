#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]
required=['SKILL.md','agents/openai.yaml','references/arabic-core.md','references/quality-gates.md','references/fidelity-guard.md','references/fidelity-graph.md','references/editorial-gain.md','references/numeral-policy.md','references/bibliography.md','references/provenance.md','references/document-mode.md','references/voice-profile.md','references/arabic-linguistic-verification.md','references/saudi-pragmatics.md','scripts/protected_tokens.py','scripts/anchored_facts.py','scripts/fidelity_graph.py','scripts/semantic_sentinels.py','scripts/condition_guard.py','scripts/structure_guard.py','scripts/locale_guard.py','scripts/document_consistency.py','scripts/document_ledger.py','scripts/arabic_mechanical_lint.py','scripts/voice_profile.py','scripts/qa_pair.py','scripts/numeral_policy.py','scripts/editorial_gain.py','scripts/semantic_repetition.py','scripts/bibliography_schema.py','scripts/run_provenance.py','scripts/edit_trail.py','scripts/gec_adjudicator.py']
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'Missing {rel}')
text=(ROOT/'SKILL.md').read_text(encoding='utf-8') if (ROOT/'SKILL.md').exists() else ''
if not text.startswith('---\n'): errors.append('SKILL.md missing YAML frontmatter')
if not re.search(r'(?m)^name:\s*arab-writer\s*$',text): errors.append('Invalid skill name')
if not re.search(r'(?m)^description:\s*.+$',text): errors.append('Missing description')
yaml=(ROOT/'agents/openai.yaml').read_text(encoding='utf-8') if (ROOT/'agents/openai.yaml').exists() else ''
if '$arab-writer' not in yaml: errors.append('openai.yaml default_prompt must explicitly mention $arab-writer')
if errors:
    print('FAILED'); [print('- '+e) for e in errors]; sys.exit(1)
print('OK: Arab Writer v1.3 structure is valid.')

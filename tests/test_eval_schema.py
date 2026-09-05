import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class EvalSchemaTests(unittest.TestCase):
    def test_cases_have_required_fields(self):
        cases=[json.loads(x) for x in (ROOT/'tests/evals.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        self.assertGreaterEqual(len(cases),25)
        ids=set()
        for c in cases:
            for k in ('id','task','input','expected_mode','must_preserve','must_not'): self.assertIn(k,c)
            self.assertNotIn(c['id'],ids); ids.add(c['id'])
    def test_has_non_trigger_and_high_fidelity(self):
        cases=[json.loads(x) for x in (ROOT/'tests/evals.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        self.assertTrue(any(not c['expected_mode'] for c in cases))
        self.assertTrue(any('high-fidelity' in c['expected_mode'] for c in cases))
if __name__=='__main__': unittest.main()

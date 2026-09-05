import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SKILL=ROOT/'.agents/skills/arab-writer'; S=SKILL/'scripts'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
conditions=load('condition_guard',S/'condition_guard.py'); locale=load('locale_guard',S/'locale_guard.py'); doc=load('document_consistency',S/'document_consistency.py'); voice=load('voice_profile_v12',S/'voice_profile.py')
class V12Tests(unittest.TestCase):
    def test_condition_loss(self):
        r=conditions.compare(conditions.extract('يجوز التمديد إذا وصل الطلب قبل خمسة أيام.'),conditions.extract('يجوز التمديد عند وصول الطلب.'))
        self.assertTrue(r['missing'] or r['added'])
    def test_exception_loss(self):
        r=conditions.compare(conditions.extract('تطبق السياسة على الجميع باستثناء المتدربين.'),conditions.extract('تطبق السياسة على الجميع.'))
        self.assertTrue(r['missing'])
    def test_dialect_flattening(self):
        r=locale.compare('وش رايك نرسلها اليوم؟ أحس كذا أوضح.','ما رأيك أن نرسلها اليوم؟ أعتقد أن هذا أوضح.')
        self.assertTrue(any(x['code']=='dialect_markers_lost' for x in r))
    def test_dialect_insertion(self):
        r=locale.compare('نرجو مراجعة الطلب.','وش رايك تراجع الطلب؟')
        self.assertTrue(any(x['code']=='dialect_inserted' for x in r))
    def test_document_anchor_conflict(self):
        r=doc.build('الإيرادات: 100 ريال.\n\nالإيرادات: 200 ريال.')
        self.assertTrue(r['anchored_fact_conflicts'])
    def test_glossary_drift(self):
        r=doc.build('يظهر التدفق النقدي هنا، ويظهر التدفق المالي لاحقًا.',{'التدفق النقدي':['التدفق المالي']})
        self.assertTrue(r['terminology_drift'])
    def test_voice_compare_same_is_high(self):
        p=voice.profile('أنا أفضل النص المباشر. هذا واضح. هل نرسله اليوم؟')
        self.assertGreaterEqual(voice.compare(p,p)['similarity_score'],99)
    def test_voice_compare_reports_dimensions(self):
        a=voice.profile('أنا أرى أن نرسلها اليوم. هذا واضح.'); b=voice.profile('في ضوء المعطيات المتاحة، ومن الجدير بالذكر أن من المناسب النظر في إمكانية الإرسال خلال الفترة الراهنة.')
        self.assertIn('dimensions',voice.compare(a,b))
    def test_nahw_fixture_is_human_external(self):
        rows=[json.loads(x) for x in (ROOT/'evals/external/nahw_passage_sample.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        self.assertGreaterEqual(len(rows),20); self.assertTrue(all(x['source']=='QCRI Nahw-Passage' for x in rows))
    def test_plugin_version_matches(self):
        m=json.loads((ROOT/'.codex-plugin/plugin.json').read_text()); self.assertEqual(m['version'],(ROOT/'VERSION').read_text().strip())
if __name__=='__main__': unittest.main()

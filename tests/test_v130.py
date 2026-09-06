import importlib.util, os, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'.agents/skills/arab-writer/scripts'
EVALS=ROOT/'evals'

def load(name,path=None):
    p=path or SCRIPTS/f'{name}.py'
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
    return mod

sent=load('semantic_sentinels')
num=load('numeral_policy')
fg=load('fidelity_graph')
repeat=load('semantic_repetition')
locale=load('locale_guard')
gain=load('editorial_gain')
voice=load('voice_profile')
prov=load('run_provenance')
bib=load('bibliography_schema')
ledger=load('document_ledger')
bm=load('benchmark_matrix',EVALS/'benchmark_matrix.py')

class ContextSentinelTests(unittest.TestCase):
    def test_qad_past_reporting_not_uncertainty(self):
        items=sent.extract('كانت الشركة قد أعلنت النتائج في يناير.')
        self.assertTrue(any(x['marker']=='قد' and not x['active'] and x['role']=='past_aspect' for x in items))
    def test_qad_future_uncertainty_still_active(self):
        items=sent.extract('قد تعلن الشركة النتائج غدًا.')
        self.assertTrue(any(x['marker']=='قد' and x['active'] and x['category']=='uncertainty' for x in items))
    def test_containment_not_guarantee(self):
        items=sent.extract('تضمن الإعلان ثلاثة بنود.')
        self.assertFalse(any(x['category']=='guarantee' for x in items))
    def test_guarantee_still_detected(self):
        items=sent.extract('يضمن العقد حق العميل في الاسترداد.')
        self.assertTrue(any(x['category']=='guarantee' and x['active'] for x in items))

class NumeralPolicyTests(unittest.TestCase):
    def test_mixed_digit_surface_same_value(self):
        self.assertTrue(num.semantic_equal('٢٥,١٩1','25,191'))
    def test_normalize_arabic_preserves_value(self):
        out=num.render('٢٥,١٩1','normalize-arabic')
        self.assertEqual(out,'٢٥٬١٩١')
        self.assertTrue(num.semantic_equal('٢٥,١٩1',out))
    def test_percent_semantics(self):
        self.assertTrue(num.semantic_equal('39.5%','٣٩٫٥%'))

class FidelityGraphTests(unittest.TestCase):
    def test_detects_swapped_measures(self):
        b=fg.extract('بلغت الإيرادات 100 ريال، وبلغت التكلفة 50 ريال.')
        a=fg.extract('بلغت الإيرادات 50 ريال، وبلغت التكلفة 100 ريال.')
        self.assertTrue(fg.compare(b,a)['issues'])
    def test_presentation_only_change_passes(self):
        b=fg.extract('بلغت الإيرادات ٢٥,١٩1 مليون ريال في ٢٠١٣.')
        a=fg.extract('بلغت الإيرادات ٢٥٬١٩١ مليون ريال في ٢٠١٣.')
        r=fg.compare(b,a)
        self.assertFalse(r['issues'])
        self.assertTrue(any(x['presentation_changed'] for x in r['matched']))

class SemanticRepetitionV2Tests(unittest.TestCase):
    def test_mobily_like_repetition_detected(self):
        text=('تُستخدم هذه البيانات بوصفها أرقامًا منشورة في ذلك الوقت قبل ظهور التعديلات اللاحقة.\n'
              'وكانت هذه الأرقام منشورة آنذاك ولم تكن الأرقام النهائية التي ظهرت عقب التعديلات.')
        self.assertTrue(repeat.scan(text,threshold=.38,window=1))
    def test_elaboration_not_called_definite_duplicate(self):
        a='أعلنت الشركة إيرادات عام ٢٠٢٤.'
        b='أعلنت الشركة إيرادات عام ٢٠٢٤ بقيمة ١٨,٢٠٦ مليون ريال.'
        score=repeat.similarity(a,b)
        self.assertIn(repeat.classify_pair(a,b,score),{'possible_elaboration','possible_repetition','possible_summary'})

class LocaleGuardTests(unittest.TestCase):
    def test_msa_marra_ukhra_not_dialect(self):
        self.assertFalse(locale.profile('أعلنت الشركة مرة أخرى عن النتائج.')['dialect_words'])
    def test_colloquial_marrah_detected(self):
        self.assertTrue(locale.profile('مره ممتاز وش رايك؟')['dialect_words'])

class EditorialGainTests(unittest.TestCase):
    def test_rejects_cosmetic_change_without_gain(self):
        r=gain.evaluate('أعلنت الشركة النتائج المالية.','قامت الشركة بإعلان النتائج المالية.')
        self.assertIn(r['verdict'],{'retain_source','human_review'})
    def test_accepts_clear_awkwardness_reduction(self):
        b='نشرت الشركة نتائج مرتفعة ضمن سلسلة من التوسع التشغيلي والاستثماري.'
        a='نشرت الشركة نتائج مرتفعة في سياق توسعها التشغيلي والاستثماري.'
        r=gain.evaluate(b,a)
        self.assertEqual(r['critical_fidelity_signals'],0)
        self.assertEqual(r['verdict'],'accept_candidate')

class VoiceV3Tests(unittest.TestCase):
    def test_tolerance_band_present(self):
        p=voice.profile('هذا نص عربي واضح. وهذه جملة ثانية واضحة.')
        r=voice.compare(p,p)
        self.assertEqual(r['drift_band'],'minimal')
        self.assertTrue(r['within_global_tolerance'])

class ProvenanceTests(unittest.TestCase):
    def test_unknown_is_not_filled_from_prompt(self):
        old={k:os.environ.pop(k,None) for k in ('CODEX_MODEL','OPENAI_MODEL','MODEL','CODEX_REASONING','OPENAI_REASONING_EFFORT','REASONING_EFFORT')}
        try:
            r=prov.build(cwd=ROOT)
            self.assertEqual(r['model']['observed'],'unknown')
            self.assertEqual(r['reasoning']['observed'],'unknown')
            self.assertFalse(r['model']['verified'])
            self.assertFalse(r['reasoning']['verified'])
        finally:
            for k,v in old.items():
                if v is not None: os.environ[k]=v

class BibliographySchemaTests(unittest.TestCase):
    def test_missing_year_stays_missing(self):
        rec=bib.parse('موبايلي. Overview التعريف بالشركة.')[0]
        self.assertIsNone(rec['year'])
        self.assertIn('year',rec['missing'])

class DocumentLedgerTests(unittest.TestCase):
    def test_ledger_keeps_numeric_relations(self):
        l=ledger.build('بلغت الإيرادات 100 ريال في 2024. وبلغت الإيرادات 120 ريال في 2025.')
        self.assertGreaterEqual(len(l['relations']),2)

class BenchmarkMatrixTests(unittest.TestCase):
    def test_matrix_meets_minimum_coverage(self):
        cases=bm.load_cases(EVALS/'benchmark_matrix.json')
        self.assertFalse(bm.validate(cases))

if __name__=='__main__': unittest.main()

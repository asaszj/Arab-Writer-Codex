import importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'.agents/skills/arab-writer/scripts'

def load(name):
    p=SCRIPTS/f'{name}.py'; spec=importlib.util.spec_from_file_location(name,p); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod

lint=load('arabic_mechanical_lint')
depth=load('editorial_depth')
repeat=load('semantic_repetition')
bib=load('bibliography_audit')

class MobilyRegressionTests(unittest.TestCase):
    def test_arabic_thousands_separator_not_flagged(self):
        codes={f['code'] for f in lint.lint('بلغ التعويض ١,٢٢٥ مليون ريال، والإيرادات ٢٥,١٩١ مليون ريال.')}
        self.assertNotIn('latin_comma_between_arabic', codes)
    def test_western_thousands_separator_not_flagged(self):
        codes={f['code'] for f in lint.lint('بلغت الإيرادات 25,191 مليون ريال.')}
        self.assertNotIn('latin_comma_between_arabic', codes)
    def test_real_latin_comma_in_arabic_prose_is_flagged(self):
        codes={f['code'] for f in lint.lint('هذا نص عربي, وهذا تكملة.')}
        self.assertIn('latin_comma_between_arabic', codes)
    def test_awkward_expansion_phrase_is_candidate(self):
        codes={f['code'] for f in depth.scan('نشرت الشركة نتائج مرتفعة ضمن سلسلة من التوسع التشغيلي والاستثماري.')}
        self.assertIn('awkward_expansion_phrase', codes)
    def test_awkward_trading_phrase_is_candidate(self):
        codes={f['code'] for f in depth.scan('صدر قرار تعليق للتداول في أكثر من مرحلة.')}
        self.assertIn('awkward_trading_phrase', codes)
    def test_agentive_phrase_is_candidate(self):
        codes={f['code'] for f in depth.scan('تبع ذلك فحص من هيئة السوق المالية للوثائق.')}
        self.assertIn('awkward_agentive_phrase', codes)
    def test_dense_fact_sentence_is_candidate(self):
        text=('حدد الإعلان الرسمي فئة المتضررين بمن اشتروا السهم في 16 يوليو 2013 واحتفظوا به حتى نهاية جلسة 29 أكتوبر 2014، '
              'وهي آخر جلسة قبل التعليق الذي بدأ في 2 نوفمبر 2014، ثم صدر إعلان 3 نوفمبر 2014 الذي تضمن القوائم والتعديلات، '
              'كما استمر المسار حتى القرار النهائي في 8 أغسطس 2022 بعد مراجعة الطلبات والوقائع والشروط النظامية ذات الصلة.')
        codes={f['code'] for f in depth.scan(text)}
        self.assertIn('high_factual_sentence_complexity', codes)
    def test_near_semantic_repetition_is_candidate(self):
        text=('تُستخدم هذه البيانات بوصفها أرقامًا منشورة في ذلك الوقت قبل ظهور التعديلات اللاحقة.\n\n'
              'وكانت هذه الأرقام منشورة في ذلك الوقت ولم تكن بعدُ الأرقام النهائية التي ظهرت عقب التعديلات.')
        self.assertTrue(repeat.scan(text, threshold=.34, window=1))
    def test_real_world_fixture_contracts(self):
        fixture=ROOT/'tests/fixtures/mobily_v121_regressions.jsonl'
        for line in fixture.read_text(encoding='utf-8').splitlines():
            case=json.loads(line)
            if case['kind']=='lint_clean':
                codes={f['code'] for f in lint.lint(case['text'])}; self.assertNotIn(case['forbid'],codes,case['id'])
            elif case['kind']=='lint_flag':
                codes={f['code'] for f in lint.lint(case['text'])}; self.assertIn(case['require'],codes,case['id'])
            elif case['kind']=='editorial_candidate':
                codes={f['code'] for f in depth.scan(case['text'])}; self.assertIn(case['require'],codes,case['id'])
            elif case['kind']=='semantic_pair':
                self.assertGreaterEqual(repeat.similarity(case['a'],case['b']),case['min_score'],case['id'])
    def test_bibliography_missing_year_is_warning_not_autofill(self):
        findings=bib.audit('موبايلي. Overview التعريف بالشركة.\nتداول السعودية. إعلان النتائج لعام 2013.')
        self.assertTrue(any(f['code']=='reference_year_not_detected' for f in findings))

if __name__=='__main__': unittest.main()

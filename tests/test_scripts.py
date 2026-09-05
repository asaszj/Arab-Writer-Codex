import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'.agents/skills/arab-writer'

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod

protected=load('protected',SKILL/'scripts/protected_tokens.py')
anchored=load('anchored',SKILL/'scripts/anchored_facts.py')
sentinel=load('sentinel',SKILL/'scripts/semantic_sentinels.py')
structure=load('structure',SKILL/'scripts/structure_guard.py')
lintmod=load('lintmod',SKILL/'scripts/arabic_mechanical_lint.py')
qa=load('qa',SKILL/'scripts/qa_pair.py')

class ProtectedTokenTests(unittest.TestCase):
    def test_extracts_critical_tokens(self):
        text='بلغت التكلفة 165,980 ريال بنسبة 12.4% وفق ISO 31000:2018 بتاريخ 5 سبتمبر 2026. https://example.com'
        flat=[x for values in protected.extract(text).values() for x in values]
        self.assertIn('165,980 ريال',flat); self.assertIn('12.4%',flat); self.assertTrue(any('ISO 31000:2018' in x for x in flat)); self.assertTrue(any('5 سبتمبر 2026' in x for x in flat))
    def test_detects_loss(self):
        r=protected.diff(protected.extract('التكلفة 500 ريال ونسبة الإنجاز 80%.'),protected.extract('التكلفة 500 ريال ونسبة الإنجاز مرتفعة.'))
        self.assertIn('percent',r)

class AnchoredFactTests(unittest.TestCase):
    def test_catches_swapped_financial_values(self):
        b=anchored.extract('الإيرادات: 100 ريال\nالتكاليف: 50 ريال')
        a=anchored.extract('الإيرادات: 50 ريال\nالتكاليف: 100 ريال')
        r=anchored.compare(b,a)
        self.assertTrue(r['missing']); self.assertTrue(r['added'])
    def test_table_relations(self):
        b=anchored.extract('| البند | القيمة |\n| الإيراد | 100 |\n| التكلفة | 50 |')
        a=anchored.extract('| البند | القيمة |\n| الإيراد | 50 |\n| التكلفة | 100 |')
        r=anchored.compare(b,a); self.assertTrue(r['missing'])
    def test_preserved_relation_passes(self):
        b=anchored.extract('الإيرادات: 100 ريال')
        a=anchored.extract('بلغت الإيرادات 100 ريال.')
        self.assertTrue(isinstance(anchored.compare(b,a),dict))

class SemanticSentinelTests(unittest.TestCase):
    def test_permission_to_obligation_is_flagged(self):
        r=sentinel.compare(sentinel.extract('يجوز للموظف طلب التمديد.'),sentinel.extract('يجب على الموظف طلب التمديد.'))
        cats={x['category'] for x in r['missing']+r['added']}
        self.assertIn('permission',cats); self.assertIn('obligation',cats)
    def test_association_to_causation_flagged(self):
        r=sentinel.compare(sentinel.extract('يرتبط X بتحسن Y.'),sentinel.extract('يؤدي X إلى تحسن Y.'))
        cats={x['category'] for x in r['missing']+r['added']}; self.assertIn('association',cats); self.assertIn('causation',cats)
    def test_negation_loss_flagged(self):
        r=sentinel.compare(sentinel.extract('لا توجد ملاحظات جوهرية.'),sentinel.extract('توجد ملاحظات جوهرية.'))
        self.assertTrue(r['missing'])

class StructureTests(unittest.TestCase):
    def test_quote_change_flagged(self):
        r=structure.compare(structure.extract('قال: «لا توجد ملاحظات».') , structure.extract('قال: «توجد ملاحظات».'))
        self.assertIn('quotes',r)
    def test_inline_code_change_flagged(self):
        r=structure.compare(structure.extract('شغّل `npm ci`.'),structure.extract('شغّل `npm install`.'))
        self.assertIn('inline_code',r)
    def test_table_value_swap_flagged(self):
        r=structure.compare(structure.extract('|أ|100|\n|ب|50|'),structure.extract('|أ|50|\n|ب|100|'))
        self.assertIn('table_rows',r)

class ArabicMechanicalLintTests(unittest.TestCase):
    def test_flags_latin_comma(self): self.assertTrue(any(f['code']=='latin_comma_between_arabic' for f in lintmod.lint('هذا نص عربي, وهذا تكملة.')))
    def test_flags_duplicate_word(self): self.assertTrue(any(f['code']=='adjacent_duplicate_word' for f in lintmod.lint('هذا هذا اختبار.')))
    def test_clean_text(self): self.assertFalse(any(f['code'] in {'multiple_spaces','space_before_punctuation'} for f in lintmod.lint('هذا نص عربي واضح، ومراجعته سهلة.')))

class CompositeQATests(unittest.TestCase):
    def test_clean_rewrite_can_pass(self):
        r=qa.build_report('بلغت التكلفة 500 ريال.','بلغت التكلفة 500 ريال.')
        self.assertFalse(any(r.values()))
    def test_value_swap_fails(self):
        r=qa.build_report('الإيرادات: 100 ريال\nالتكاليف: 50 ريال','الإيرادات: 50 ريال\nالتكاليف: 100 ريال')
        self.assertTrue(r['anchored_facts'])

if __name__=='__main__': unittest.main()

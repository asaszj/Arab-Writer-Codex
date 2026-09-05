import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/arab-writer"

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod

protected = load_module("protected_tokens", SKILL / "scripts/protected_tokens.py")
lintmod = load_module("arabic_lint", SKILL / "scripts/arabic_lint.py")

class ProtectedTokenTests(unittest.TestCase):
    def test_extracts_critical_tokens(self):
        text = "بلغت التكلفة 165,980 ريال بنسبة 12.4% وفق ISO 31000:2018 بتاريخ 5 سبتمبر 2026. https://example.com"
        data = protected.extract(text)
        flat = [x for values in data.values() for x in values]
        self.assertIn("165,980 ريال", flat)
        self.assertIn("12.4%", flat)
        self.assertTrue(any("ISO 31000:2018" in x for x in flat))
        self.assertTrue(any("5 سبتمبر 2026" in x for x in flat))
        self.assertIn("https://example.com", flat)

    def test_detects_loss(self):
        before = protected.extract("التكلفة 500 ريال ونسبة الإنجاز 80%.")
        after = protected.extract("التكلفة 500 ريال ونسبة الإنجاز مرتفعة.")
        report = protected.diff(before, after)
        self.assertIn("percent", report)
        self.assertIn("80%", report["percent"]["missing"])

    def test_no_difference_when_preserved(self):
        before = protected.extract("ISO 31000:2018 — 500 ريال — 80%")
        after = protected.extract("وفق ISO 31000:2018 بلغت القيمة 500 ريال، بنسبة 80%.")
        report = protected.diff(before, after)
        self.assertNotIn("standard", report)
        self.assertNotIn("money", report)
        self.assertNotIn("percent", report)

class ArabicLintTests(unittest.TestCase):
    def test_flags_latin_comma(self):
        findings = lintmod.lint("هذا نص عربي, وهذا تكملة.")
        self.assertTrue(any(f["code"] == "latin_comma_between_arabic" for f in findings))

    def test_flags_duplicate_word(self):
        findings = lintmod.lint("هذا هذا اختبار.")
        self.assertTrue(any(f["code"] == "adjacent_duplicate_word" for f in findings))

    def test_clean_text(self):
        findings = lintmod.lint("هذا نص عربي واضح، ومراجعته سهلة.")
        self.assertFalse(any(f["code"] in {"multiple_spaces", "space_before_punctuation"} for f in findings))

if __name__ == "__main__":
    unittest.main()

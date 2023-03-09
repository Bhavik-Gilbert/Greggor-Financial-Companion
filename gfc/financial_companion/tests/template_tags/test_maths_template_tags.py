from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import divide, sig_figs

class DivideTemplateTagTestCase(TemplateTagTestCase):
    """Test for the divide template tag in maths"""

    def test_valid_numerator_valid_denominator(self):
        result = divide(1,2)
        self.assertEqual(result, 0.5)
    
    def test_negative_numerator_valid_denominator(self):
        result = divide(-1,2)
        self.assertEqual(result, -0.5)
    
    def test_valid_numerator_negative_denominator(self):
        result = divide(1,-2)
        self.assertEqual(result, -0.5)
    
    def test_0_as_numerator_valid_denominator(self):
        result = divide(0,2)
        self.assertEqual(result, 0)
    
    def test_valid_numerator_0_as_denominator(self):
        result = divide(2,0)
        self.assertEqual(result, 0)

class SigFigsTemplateTagTestCase(TemplateTagTestCase):
    """Test for the sig_figs template tag in maths"""

    def test_valid_int_valid_sig_figs(self):
        result = sig_figs(123,2)
        self.assertEqual(float(result), 120.0)
    
    def test_valid_int_invalid_negative_sig_figs(self):
        result = sig_figs(123, -1)
        self.assertEqual(float(result), 123.0)
    
    def test_valid_int_invalid_0_as_sig_figs(self):
        result = sig_figs(123, 0)
        self.assertEqual(float(result), 123.0)
    
    def test_valid_float_greater_than_1_valid_sig_figs(self):
        result = sig_figs(123.555,4)
        self.assertEqual(float(result), 123.6)
    
    def test_valid_float_smaller_than_1_valid_sig_figs(self):
        result = sig_figs(0.01536,2)
        self.assertEqual(float(result), 0.015)
    

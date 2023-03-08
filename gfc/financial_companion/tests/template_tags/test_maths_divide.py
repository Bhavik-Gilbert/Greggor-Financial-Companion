from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import divide



class MathsDivideTemplateTagTestCase(TemplateTagTestCase):
    """Test for the divide function template tag"""

    def test_division_with_2_doubles_returns_correct_whole_number_value(self):
        self.assertEqual(divide(4.0,2.0), 2.0)
    
    def test_division_with_2_doubles_returns_correct_decimal_value(self):
        self.assertEqual(divide(5.0,2.0), 2.5)
    
    def test_division_with_1_double_returns_correct_whole_number_value(self):
        self.assertEqual(divide(4,2.0), 2.0)
    
    def test_division_with_1_double_returns_correct_decimal_value(self):
        self.assertEqual(divide(5,2.0), 2.5)
    
    def test_division_with_negative_numbers_returns_correct_value(self):
        self.assertEqual(divide(-4.0,2.0), -2.0)
    
    def test_division_with_zero_as_numerator_returns_correct_value(self):
        self.assertEqual(divide(0,2.0), 0)
    
    def test_division_with_zero_as_denominator_returns_correct_value(self):
        with self.assertRaises(ZeroDivisionError):
            divide(2.0,0)


        
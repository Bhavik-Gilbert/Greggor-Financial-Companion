from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import  sig_figs



class MathsSigFigTemplateTagTestCase(TemplateTagTestCase):
    """Test for the sig_figs function in template tag"""

    def test_sig_figs_returns_correct_value_when_not_rounded(self):
        self.assertEqual(sig_figs(1200,2), str(1200.0))
        
    def test_sig_figs_returns_correct_value_when_rounded_down(self):
        self.assertEqual(sig_figs(1223,2), str(1200.0))
    
    def test_sig_figs_returns_correct_value_when_rounded_up(self):
        self.assertEqual(sig_figs(1193,2), str(1200.0))
    
    def test_sig_figs_returns_correct_value_when_given_negative_value(self):
        self.assertEqual(sig_figs(-1193,2), str(1200.0))
    
    def test_sig_figs_returns_correct_value_when_zero_sig_fig_given(self):
        self.assertEqual(sig_figs(1234,0), 1000)
        
    def test_sig_figs_throws_error_when_given_negative_sig_fig(self):
        with self.assertRaises(ValueError):
            sig_figs(1193,-2)
    

        
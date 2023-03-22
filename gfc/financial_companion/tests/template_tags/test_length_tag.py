from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import length


class LengthTemplateTagTestCase(TemplateTagTestCase):
    """Test for the to_list template tag"""
    
    def setUp(self):
        self.list: list[str] = []
        for i in range (100):
            self.list.append(i)

    def test_valid_length(self):
        self.assertEqual(len(self.list), length(self.list))
    

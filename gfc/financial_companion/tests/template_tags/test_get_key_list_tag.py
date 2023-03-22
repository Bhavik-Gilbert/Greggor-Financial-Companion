from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import get_key_list


class GetKeyListTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_key_list template tag"""

    def setUp(self):
        self.dict: dict[str, int] = {}
        for i in range (100):
            self.dict[str(i)]: int = i 
    
    def test_valid_get_key_list(self):
        key_list: list[str] = get_key_list(self.dict)
        self.assertEqual(key_list, list(self.dict.keys()))
    

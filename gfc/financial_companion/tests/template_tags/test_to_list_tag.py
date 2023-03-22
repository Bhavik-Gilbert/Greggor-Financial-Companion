from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import to_list


class ToListTemplateTagTestCase(TemplateTagTestCase):
    """Test for the to_list template tag"""

    def test_valid_to_list(self):
        new_list: list[str] = to_list("test")
        self.assertEqual(["test"], new_list)

from .test_template_tag_base import TemplateTagTestCase
from financial_companion.helpers import GreggorTypes
from financial_companion.templatetags import get_greggor_type_from_completeness


class GetGreggorTypeTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_greggor_type_from_completeness logo template tag"""

    def test_valid_party_greggor_input(self):
        greggor_type = get_greggor_type_from_completeness(100)
        self.assertEqual(greggor_type, "party")

    def test_valid_sad_greggor_input(self):
        greggor_type = get_greggor_type_from_completeness(49)
        self.assertEqual(greggor_type, "sad")

    def test_valid_normal_greggor_input(self):
        greggor_type = get_greggor_type_from_completeness(50)
        self.assertEqual(greggor_type, "normal")

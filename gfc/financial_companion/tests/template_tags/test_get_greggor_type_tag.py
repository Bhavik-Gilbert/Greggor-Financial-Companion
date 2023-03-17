from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import get_greggor_type_from_completeness


class GetGreggorTypeTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_greggor_type_from_completeness logo template tag"""

    def test_valid_party_greggor_input(self):
        greggor_type = get_greggor_type_from_completeness(90)
        self.assertEqual(greggor_type, "party")

    def test_valid_distraught_greggor_input(self):
        greggor_type = get_greggor_type_from_completeness(14)
        self.assertEqual(greggor_type, "distraught")

    def test_valid_sad_greggor_input(self):
        greggor_type = get_greggor_type_from_completeness(34)
        self.assertEqual(greggor_type, "sad")

    def test_valid_normal_greggor_input(self):
        greggor_type = get_greggor_type_from_completeness(51)
        self.assertEqual(greggor_type, "normal")

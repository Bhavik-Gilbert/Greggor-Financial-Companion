from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import get_greggor_type_from_completeness
from financial_companion.helpers import GreggorTypes


class GetGreggorTypeTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_greggor_type_from_completeness logo template tag"""

    def test_valid_party_greggor_input(self):
        greggor_type: str = get_greggor_type_from_completeness(90)
        self.assertEqual(greggor_type, GreggorTypes.PARTY)

    def test_valid_distraught_greggor_input(self):
        greggor_type: str = get_greggor_type_from_completeness(14)
        self.assertEqual(greggor_type, GreggorTypes.DISTRAUGHT)

    def test_valid_sad_greggor_input(self):
        greggor_type: str = get_greggor_type_from_completeness(34)
        self.assertEqual(greggor_type, GreggorTypes.SAD)

    def test_valid_normal_greggor_input(self):
        greggor_type: str = get_greggor_type_from_completeness(51)
        self.assertEqual(greggor_type, GreggorTypes.NORMAL)

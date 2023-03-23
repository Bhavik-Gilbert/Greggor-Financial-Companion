from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import get_greggor_type_for_overall_completeness
from financial_companion.models import CategoryTarget, Transaction, AbstractTarget
from django.utils import timezone


class GetOverallGreggorTypeTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_greggor_type_for_overall_completeness logo template tag"""

    def setUp(self):
        self.target1: AbstractTarget = CategoryTarget.objects.get(pk=1)
        self.target3: AbstractTarget = CategoryTarget.objects.get(pk=3)
        transaction: Transaction = Transaction.objects.get(pk=8)
        transaction.time_of_transaction: timezone = timezone.now()
        transaction.save()

    def test_get_valid_greggor_type(self):
        target_list: list[AbstractTarget] = [self.target1, self.target3]
        result: float = get_greggor_type_for_overall_completeness(target_list)
        self.assertEqual(result, "distraught")

    def test_get_valid_greggor_type_with_empty_target_list(self):
        target_list: list[AbstractTarget] = []
        result: float = get_greggor_type_for_overall_completeness(target_list)
        self.assertEqual(result, "distraught")

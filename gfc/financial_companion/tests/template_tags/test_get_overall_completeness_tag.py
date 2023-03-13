from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import get_overall_completeness, get_completeness
from financial_companion.models import CategoryTarget, Transaction, Category
from django.utils import timezone


class GetOverallCompletenessTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_overall_completeness target template tag"""

    def setUp(self):
        self.target1 = CategoryTarget.objects.get(pk=1)
        self.target3 = CategoryTarget.objects.get(pk=3)
        self.trasaction = Transaction.objects.get(pk=8)
        self.trasaction.time_of_transaction = timezone.now()
        self.trasaction.save()

    def test_get_valid_overall_completeness(self):
        target_list= [self.target1, self.target3]
        result = get_overall_completeness(target_list)
        desired_result = (get_completeness(self.target1) + get_completeness(self.target3))/2
        self.assertEqual(result,desired_result)

    def test_get_overall_completeness_with_empty_target_parameter(self):
        target_list = list()
        result = get_overall_completeness(target_list)
        self.assertEqual(result, 0)

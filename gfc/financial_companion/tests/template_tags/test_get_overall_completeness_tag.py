from .test_template_tag_base import TemplateTagTestCase
from financial_companion.templatetags import get_overall_completeness, get_completeness, check_completeness_if_expense
from financial_companion.models import CategoryTarget
from freezegun import freeze_time


class GetOverallCompletenessTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_overall_completeness target template tag"""

    def setUp(self):
        self.target1 = CategoryTarget.objects.get(pk=1)
        self.target3 = CategoryTarget.objects.get(pk=3)

    @freeze_time("2023-01-01 22:00:00")
    def test_get_valid_overall_completeness(self):
        target_list = [self.target1, self.target3]
        result = get_overall_completeness(target_list)
        desired_result = (
            get_completeness(
                self.target1) + check_completeness_if_expense(
                get_completeness(
                    self.target3),
                self.target3)) / 2
        self.assertEqual(result, desired_result)

    def test_get_overall_completeness_with_empty_target_parameter(self):
        target_list = list()
        result = get_overall_completeness(target_list)
        self.assertEqual(result, 0)

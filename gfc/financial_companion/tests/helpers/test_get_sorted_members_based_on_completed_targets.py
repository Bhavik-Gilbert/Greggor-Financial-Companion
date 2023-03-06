from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_number_of_completed_targets, get_sorted_members_based_on_completed_targets
from financial_companion.models import UserGroup
from freezegun import freeze_time
import datetime


class GetSortedMembersBasedOnCompletedTargetsHelperFunctionTestCase(
        HelperTestCase):
    """Test for the get_sorted_members_based_on_completed_targets helpers function"""

    def setUp(self):
        self.group = UserGroup.objects.get(id=3)
        self.members = self.group.members.all()
        self.memeber_1 = self.members[0]
        self.targets_1 = self.memeber_1.get_all_targets()
        self.memeber_2 = self.members[1]
        self.targets_2 = self.memeber_2.get_all_targets()

    @freeze_time("2023-01-01 13:00:00")
    def test_order_is_correct(self):
        completed_1 = get_number_of_completed_targets(self.targets_1)
        completed_2 = get_number_of_completed_targets(self.targets_2)
        sorted_members_list = get_sorted_members_based_on_completed_targets(
            self.members)
        if completed_1 > completed_2:
            self.assertTrue(sorted_members_list[0][0] == self.memeber_1)
        else:
            self.assertTrue(sorted_members_list[0][0] == self.memeber_2)

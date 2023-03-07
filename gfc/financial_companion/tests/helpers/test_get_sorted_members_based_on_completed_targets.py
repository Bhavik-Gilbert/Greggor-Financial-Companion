from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_sorted_members_based_on_completed_targets
from financial_companion.models import UserGroup
from freezegun import freeze_time
import datetime


class GetSortedMembersBasedOnCompletedTargetsHelperFunctionTestCase(
        HelperTestCase):
    """Test for the get_sorted_members_based_on_completed_targets helpers function"""

    def setUp(self):
        self.group = UserGroup.objects.get(id=3)
        self.members = self.group.members.all()
        self.member_1 = self.members[0]
        self.member_2 = self.members[1]

    @freeze_time("2023-01-01 13:00:00")
    def test_order_is_correct(self):
        score_1 = self.member_1.get_leaderboard_score()
        score_2 = self.member_2.get_leaderboard_score()
        sorted_members_list = get_sorted_members_based_on_completed_targets(
            self.members)
        if score_1 > score_2:
            self.assertTrue(sorted_members_list[0][0] == self.member_1)
        else:
            self.assertTrue(sorted_members_list[0][0] == self.member_2)

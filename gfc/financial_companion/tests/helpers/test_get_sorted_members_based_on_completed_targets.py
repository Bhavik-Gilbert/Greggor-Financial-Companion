from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_sorted_members_based_on_completed_targets
from financial_companion.models import UserGroup, User
from freezegun import freeze_time
from typing import Union
from django.db.models import QuerySet


class GetSortedMembersBasedOnCompletedTargetsHelperFunctionTestCase(
        HelperTestCase):
    """Test file for the get_sorted_members_based_on_completed_targets helpers function"""

    def setUp(self):
        self.group: UserGroup = UserGroup.objects.get(id=3)
        self.members: Union[QuerySet, list[User]] = self.group.members.all()
        self.member_1: User = self.members[0]
        self.member_2: User = self.members[1]

    @freeze_time("2023-01-01 13:00:00")
    def test_order_is_correct(self):
        score_1: float = self.member_1.get_leaderboard_score()
        score_2: float = self.member_2.get_leaderboard_score()
        sorted_members_list = get_sorted_members_based_on_completed_targets(
            self.members)
        if score_1 > score_2:
            self.assertTrue(sorted_members_list[0][0] == self.member_1)
        else:
            self.assertTrue(sorted_members_list[0][0] == self.member_2)

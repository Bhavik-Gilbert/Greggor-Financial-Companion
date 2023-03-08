from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from financial_companion.models.user_model import User
from freezegun import freeze_time
import datetime

from financial_companion.templatetags import get_completeness

class UserModelTestCase(ModelTestCase):
    """Test file for user model class"""

    def setUp(self):
        super().setUp()
        self.test_model = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')
        self.third_user = User.objects.get(username='@michaelkolling')
        self.fourth_user = User.objects.get(username='@michaelhigham')
        self.total_completed_targets = 6  # 6/7 will be complete at the first time check

    def test_valid_user(self):
        self._assert_model_is_valid()

    def test_username_cant_be_blank(self):
        self.test_model.username = ''
        self._assert_model_is_invalid()

    def test_username_unique(self):
        self.test_model.username = self.second_user.username
        self._assert_model_is_invalid()

    def test_first_name_is_not_blank(self):
        self.test_model.first_name = ''
        self._assert_model_is_invalid()

    def test_first_name_doesnt_need_to_be_unique(self):
        self.test_model.first_name = self.second_user.first_name
        self._assert_model_is_valid()

    def test_first_name_has_length_of_max_50(self):
        self.test_model.first_name = 'j' * 50
        self._assert_model_is_valid()

    def test_first_name_is_not_more_than_50_characters(self):
        self.test_model.first_name = 'j' * 51
        self._assert_model_is_invalid()

    def test_last_name_is_not_blank(self):
        self.test_model.last_name = ''
        self._assert_model_is_invalid()

    def test_last_name_doesnt_need_to_be_unique(self):
        self.test_model.last_name = self.second_user.last_name
        self._assert_model_is_valid()

    def test_last_name_has_length_of_max_50(self):
        self.test_model.last_name = 'j' * 50
        self._assert_model_is_valid()

    def test_last_name_not_more_than_50(self):
        self.test_model.last_name = 'j' * 51
        self._assert_model_is_invalid()

    def test_bio_can_be_blank(self):
        self.test_model.bio = ''
        self._assert_model_is_valid()

    def test_bio_need_not_be_unique(self):
        self.test_model.bio = self.second_user.bio
        self._assert_model_is_valid()

    def test_bio_can_be_520_chars(self):
        self.test_model.bio = 'x' * 520
        self._assert_model_is_valid()

    def test_bio_cant_be_more_that_520_chars(self):
        self.test_model.bio = 'x' * 521
        self._assert_model_is_invalid()

    def test_email_must_not_be_blank(self):
        self.test_model.email = ''
        self._assert_model_is_invalid()

    def test_email_must_be_unique(self):
        self.test_model.email = self.second_user.email
        self._assert_model_is_invalid()

    def test_email_must_contain_username(self):
        self.test_model.email = '@example.org'
        self._assert_model_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.test_model.email = 'johndoe.example.org'
        self._assert_model_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.test_model.email = 'johndoe@.org'
        self._assert_model_is_invalid()

    def test_email_must_contain_domain(self):
        self.test_model.email = 'johndoe@example'
        self._assert_model_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.test_model.email = 'johndoe@@example.org'
        self._assert_model_is_invalid()

    def test_profile_picture_can_be_empty(self):
        self.test_model.profile_picture = ''
        self._assert_model_is_valid()

    def test_get_user_highest_quiz_score(self):
        self.assertEqual(
            self.test_model.get_user_highest_quiz_score().get_score(), 80
        )

    def test_get_all_targets_when_user_has_targets(self):
        self.assertTrue(self.test_model.get_all_targets() != [])

    def test_get_all_targets_when_user_has_no_targets(self):
        self.assertTrue(self.third_user.get_all_targets() == [])

    def test_get_all_account_when_user_has_targets(self):
        self.assertTrue(self.test_model.get_all_account_targets() != [])

    def test_get_all_account_when_user_has_no_targets(self):
        self.assertTrue(self.third_user.get_all_account_targets() == [])

    def test_get_all_category_when_user_has_targets(self):
        self.assertTrue(self.test_model.get_all_category_targets() != [])

    def test_get_all_category_when_user_has_no_targets(self):
        self.assertTrue(self.third_user.get_all_category_targets() == [])

    @freeze_time("2023-01-01 13:00:00")
    def test_get_all_completed_targets_when_user_has_targets(self):
        targets = self.test_model.get_all_targets()
        self.assertTrue(self.test_model.get_completed_targets(targets) != [])

    @freeze_time("2023-01-01 13:00:00")
    def test_get_all_completed_targets_when_user_has_no_targets(self):
        targets = self.third_user.get_all_targets()
        self.assertTrue(self.third_user.get_completed_targets(targets) == [])


    @freeze_time("2023-01-01 13:00:00")
    def test_get_all_nearly_completed_targets_when_user_has_targets_within_day_lower(self):
        targets = self.fourth_user.get_all_targets()
        self.assertEqual(len(self.fourth_user.get_nearly_completed_targets(targets)), 2)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_all_nearly_completed_targets_when_user_has_targets_within_day_upper(self):
        targets = self.fourth_user.get_all_targets()
        self.assertEqual(len(self.fourth_user.get_nearly_completed_targets(targets)), 2)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_all_nearly_completed_targets_when_user_has_targets_after_week(self):
        targets = self.fourth_user.get_all_targets()
        self.assertEqual(len(self.fourth_user.get_nearly_completed_targets(targets)), 0)

    @freeze_time("2023-01-01 13:00:00")
    def test_get_all_nearly_completed_targets_when_user_has_no_targets(self):
        targets = self.third_user.get_all_targets()
        self.assertTrue(self.third_user.get_nearly_completed_targets(targets) == [])


    @freeze_time("2023-01-01 13:00:00")
    def test_get_number_of_nearly_completed_spending_targets_when_user_has_targets_within_day_lower(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_spending_targets(), 1)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_number_of_nearly_completed_spending_targets_when_user_has_targets_within_day_upper(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_spending_targets(), 1)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_number_of_nearly_completed_spending_targets_when_user_has_targets_after_week(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_spending_targets(), 0)


    @freeze_time("2023-01-01 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_targets_within_day_lower(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_saving_targets(), 1)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_targets_within_day_upper(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_saving_targets(), 1)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_targets_after_week(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_saving_targets(), 0)


    @freeze_time("2023-01-01 13:00:00")
    def test_get_number_of_nearly_completed_targets_when_user_has_targets_within_day_lower(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_targets(), 2)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_number_of_nearly_completed_targets_when_user_has_targets_within_day_upper(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_targets(), 2)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_number_of_nearly_completed_targets_when_user_has_targets_after_week(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_targets(), 0)


    @freeze_time("2023-01-01 13:00:00")
    def test_get_number_of_nearly_completed_spending_targets_when_user_has_targets(self):
        self.assertEqual(self.test_model.get_number_of_completed_spending_targets(), 3)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_number_of_nearly_completed_spending_targets_when_user_has_no_targets(self):
        self.assertEqual(self.third_user.get_number_of_completed_spending_targets(), 0)


    @freeze_time("2023-01-01 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_targets(self):
        self.assertEqual(self.test_model.get_number_of_completed_saving_targets(), 3)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_no_targets(self):
        self.assertEqual(self.third_user.get_number_of_completed_saving_targets(), 0)


    @freeze_time("2023-01-01 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_targets_within_day_lower(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_saving_targets(), 1)

    @freeze_time("2023-01-05 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_targets_within_day_upper(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_saving_targets(), 1)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_number_of_nearly_completed_saving_targets_when_user_has_targets_after_week(self):
        self.assertEqual(self.fourth_user.get_number_of_nearly_completed_saving_targets(), 0)


    @freeze_time("2023-01-01 13:00:00")
    def test_get_number_of_completed_targets_within_day(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed == self.total_completed_targets)

    @freeze_time("2023-01-03 13:00:00")
    def test_get_number_of_completed_targets_after_day(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed <= self.total_completed_targets)

    @freeze_time("2023-01-06 13:00:00")
    def test_get_number_of_completed_targets_within_week(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed <= self.total_completed_targets)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_number_of_completed_targets_after_week(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed <= self.total_completed_targets)

    @freeze_time("2023-01-22 13:00:00")
    def test_get_number_of_completed_targets_within_month(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed <= self.total_completed_targets)

    @freeze_time("2023-02-03 13:00:00")
    def test_get_number_of_completed_targets_after_month(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed <= self.total_completed_targets)

    @freeze_time("2023-07-09 13:00:00")
    def test_get_number_of_completed_targets_within_year(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed <= self.total_completed_targets)

    @freeze_time("2024-08-26 13:00:00")
    def test_get_number_of_completed_targets_after_year(self):
        completed = self.test_model.get_number_of_completed_targets()
        self.assertTrue(completed <= self.total_completed_targets)


    @freeze_time("2023-01-01 13:00:00")
    def test_get_leaderboard_score_within_day(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 1.5)

    @freeze_time("2023-01-03 13:00:00")
    def test_get_leaderboard_score_after_day(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 3)

    @freeze_time("2023-01-06 13:00:00")
    def test_get_number_of_completed_targets_within_week(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 3)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_leaderboard_score_after_week(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 2)

    @freeze_time("2023-01-22 13:00:00")
    def test_get_leaderboard_score_within_month(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 2)

    @freeze_time("2023-02-03 13:00:00")
    def test_get_leaderboard_score_after_month(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 1)

    @freeze_time("2023-07-09 13:00:00")
    def test_get_leaderboard_score_within_year(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 1)

    @freeze_time("2024-08-26 13:00:00")
    def test_get_leaderboard_score_after_year(self):
        score = self.test_model.get_leaderboard_score()
        self.assertTrue(score == 0)

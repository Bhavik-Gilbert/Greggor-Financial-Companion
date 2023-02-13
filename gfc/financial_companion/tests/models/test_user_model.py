from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from financial_companion.models.user_model import User


class UserModelTestCase(ModelTestCase):
    """Test file for user model class"""

    def setUp(self):
        super().setUp()
        self.test_model = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')

    def test_valid_target(self):
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

from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from financial_companion.models.user_model import User
from financial_companion.models.user_group_model import UserGroup


class UserGroupModelTestCase(ModelTestCase):
    """Test file for user model class"""

    def setUp(self):
        super().setUp()
        self.test_model = UserGroup.objects.get(invite_code='ABCDEFGH')
        self.second_group = UserGroup.objects.get(invite_code='IJKLMNOP')
        self.first_user = User.objects.get(username='@johndoe')
        self.second_user = User.objects.get(username='@janedoe')

    def test_valid_user_group(self):
        self._assert_model_is_valid()

    def test_name_is_not_blank(self):
        self.test_model.name = ''
        self._assert_model_is_invalid()

    def test_name_doesnt_need_to_be_unique(self):
        self.test_model.name = self.second_group.name
        self._assert_model_is_valid()

    def test_name_has_length_of_max_50(self):
        self.test_model.name = 'j' * 50
        self._assert_model_is_valid()

    def test_name_is_not_more_than_50_characters(self):
        self.test_model.name = 'j' * 51
        self._assert_model_is_invalid()

    def test_description_is_not_blank(self):
        self.test_model.description = ''
        self._assert_model_is_invalid()

    def test_description_doesnt_need_to_be_unique(self):
        self.test_model.description = self.second_group.description
        self._assert_model_is_valid()

    def test_description_has_length_of_max_500(self):
        self.test_model.description = 'j' * 50
        self._assert_model_is_valid()

    def test_description_is_not_more_than_500_characters(self):
        self.test_model.description = 'j' * 501
        self._assert_model_is_invalid()

    def test_owner_email_is_not_blank(self):
        self.test_model.owner_email = ''
        self._assert_model_is_invalid()

    def test_owner_email_doesnt_need_to_be_unique(self):
        self.test_model.owner_email = self.second_group.owner_email
        self._assert_model_is_valid()

    def test_owner_email_must_contain_at_symbol(self):
        self.test_model.owner_email = 'johndoe.example.org'
        self._assert_model_is_invalid()

    def test_owner_email_must_contain_domain_name(self):
        self.test_model.owner_email = 'johndoe@.org'
        self._assert_model_is_invalid()

    def test_owner_email_must_contain_domain(self):
        self.test_model.owner_email = 'johndoe@example'
        self._assert_model_is_invalid()

    def test_owner_email_must_not_contain_more_than_one_at(self):
        self.test_model.owner_email = 'johndoe@@example.org'
        self._assert_model_is_invalid()

    def test_invite_code_is_not_blank(self):
        self.test_model.invite_code = ''
        self._assert_model_is_invalid()

    def test_invite_code_needs_to_be_unique(self):
        self.test_model.invite_code = self.second_group.invite_code
        self._assert_model_is_invalid()

    def test_invite_code_has_length_of_max_8(self):
        self.test_model.invite_code = 'j' * 8
        self._assert_model_is_valid()

    def test_invite_code_is_not_more_than_8_characters(self):
        self.test_model.invite_code = 'j' * 9
        self._assert_model_is_invalid()

    def test_users_can_be_added_to_group(self):
        current_member_count = self.test_model.members_count()
        self.assertEqual(current_member_count, 0)
        self.test_model.add_member(self.first_user)
        new_member_count = self.test_model.members_count()
        self.assertEqual(new_member_count, current_member_count + 1)
        self.assertNotEqual(new_member_count, current_member_count)
        self.assertTrue(self.test_model.is_member(self.first_user))

    def test_users_can_be_removed_from_group(self):
        self.test_model.add_member(self.first_user)
        current_member_count = self.test_model.members_count()
        self.test_model.remove_member(self.first_user)
        new_member_count = self.test_model.members_count()
        self.assertEqual(new_member_count, current_member_count - 1)
        self.assertNotEqual(new_member_count, current_member_count)
        self.assertFalse(self.test_model.is_member(self.first_user))

    def test_group_picture_can_be_empty(self):
        self.test_model.group_picture = ''
        self._assert_model_is_valid()

    def test_another_user_can_be_made_owner(self):
        self.assertEqual(self.test_model.owner_email, self.first_user.email)
        self.test_model.make_owner(self.second_user)
        self.assertNotEqual(self.test_model.owner_email, self.first_user.email)
        self.assertEqual(self.test_model.owner_email, self.second_user.email)

    def test_get_members(self):
        self.test_model.add_member(self.first_user)
        members = self.test_model.get_members()
        self.assertTrue(str(self.first_user) in members)

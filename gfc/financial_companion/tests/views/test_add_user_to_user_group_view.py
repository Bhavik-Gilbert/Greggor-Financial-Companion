from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup
from financial_companion.forms import AddUserToUserGroupForm

class AddUserToUserGroupViewTestCase(ViewTestCase):
    """Tests for add user to user group view."""

    def setUp(self):
        self.url = reverse('add_user_to_user_group', kwargs={"group_pk": 1})
        self.form_input = {
            'user_email': 'janedoe@example.org'
        }
        self.user = User.objects.get(username='@johndoe')
        self.user_two = User.objects.get(username='@janedoe')
        self.user_group = UserGroup.objects.get(invite_code="ABCDEFGH")
        self.user_group.add_member(self.user)

    def test_add_user_to_user_group_url(self):
        self.assertEqual(self.url, '/add_user_to_user_group/1')

    def test_get_add_user_to_user_group(self):
        self._login(self.user)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_get_add_user_to_user_group_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_successful_add_user_to_user_group(self):
        self._login(self.user)
        self.assertFalse(self.user_group.members.contains(self.user_two))
        before_count = self.user_group.members_count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = self.user_group.members_count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTrue(self.user_group.members.contains(self.user_two))
        self.assertTemplateUsed(response, 'pages/individual_group.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_add_user_to_user_group_due_to_invalid_group_pk(self):
        self._login(self.user)
        url = reverse('add_user_to_user_group', kwargs={"group_pk": 1000})
        self.assertFalse(self.user_group.members.contains(self.user_two))
        before_count = self.user_group.members_count()
        response = self.client.post(url, self.form_input, follow=True)
        after_count = self.user_group.members_count()
        self.assertEqual(after_count, before_count)
        self.assertFalse(self.user_group.members.contains(self.user_two))
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_add_user_to_user_group_due_to_incorrect_email(self):
        self._login(self.user)
        self.assertFalse(self.user_group.members.contains(self.user_two))
        self.form_input['user_email'] = "janedoe"
        before_count = self.user_group.members_count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = self.user_group.members_count()
        self.assertEqual(after_count, before_count)
        self.assertFalse(self.user_group.members.contains(self.user_two))
        self.assertTemplateUsed(response, 'pages/individual_group.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_add_user_to_user_group_due_to_user_already_being_in_the_group(self):
        self._login(self.user)
        self.user_group.add_member(self.user_two)
        self.assertTrue(self.user_group.members.contains(self.user_two))
        before_count = self.user_group.members_count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = self.user_group.members_count()
        self.assertEqual(after_count, before_count)
        self.assertTrue(self.user_group.members.contains(self.user_two))
        self.assertTemplateUsed(response, 'pages/individual_group.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import JoinUserGroupForm
from financial_companion.models import User, UserGroup


class SignUpViewTestCase(ViewTestCase):
    """Unit tests of the join user group view"""

    def setUp(self):
        self.url = reverse('join_user_group')
        self.form_input = {
            'invite_code': 'ABCDEFGH'
        }
        self.user = User.objects.get(username='@janedoe')
        self.group = UserGroup.objects.get(invite_code='ABCDEFGH')

    def test_join_user_group_url(self):
        self.assertEqual(self.url, '/join_user_group/')

    def test_get_join_user_group(self):
        self._login(self.user)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/all_groups.html")
        form = response.context['form']
        self.assertTrue(isinstance(form, JoinUserGroupForm))
        self.assertFalse(form.is_bound)

    def test_get_join_user_group_redirects_when_logged_out(self):
        response = self.client.get(self.url, follow=True)
        self._assert_require_login(self.url)

    def test_successful_join_user_group(self):
        self._login(self.user)
        self.assertFalse(self.group.members.contains(self.user))
        before_count = self.group.members_count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = self.group.members_count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTrue(self.group.members.contains(self.user))

    def test_unsuccessful_join_user_group(self):
        self._login(self.user)
        self.form_input['invite_code'] = "AAAAAAAA"
        self.assertFalse(self.group.members.contains(self.user))
        before_count = self.group.members_count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = self.group.members_count()
        self.assertEqual(after_count, before_count)
        self.assertFalse(self.group.members.contains(self.user))

    def test_success_when_user_is_already_in_group(self):
        self._login(self.user)
        self.group.add_member(self.user)
        before_count = self.group.members_count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = self.group.members_count()
        self.assertEqual(after_count, before_count)
        self.assertTrue(self.group.members.contains(self.user))

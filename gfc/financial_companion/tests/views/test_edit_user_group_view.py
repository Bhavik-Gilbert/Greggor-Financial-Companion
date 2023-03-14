from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import UserGroupForm
from financial_companion.models import User, UserGroup


class EditUserGroupViewTestCase(ViewTestCase):
    """Tests of the edit user group view."""

    def setUp(self):
        self.url = reverse('edit_user_group', kwargs={"pk": 1})
        self.form_input = {
            'name': 'Financial Club',
            'description': 'We are the best financial club',
        }
        self.user = User.objects.get(username='@johndoe')
        self.group = UserGroup.objects.get(invite_code='ABCDEFGH')
        self.group.add_member(self.user)

    def test_edit_user_group_url(self):
        self.assertEqual(self.url, '/edit_user_group/1')

    def test_get_edit_user_group(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_user_group.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserGroupForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_edit_user_group_form_submission(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.form_input['name'] = ''
        before_count = UserGroup.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_user_group.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserGroupForm))

    def test_successful_edit_user_group_form_submission(self):
        self._login(self.user)
        before_count = UserGroup.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/individual_group.html')
    
    def test_successful_edit_user_group_form_submission_when_group_picture_is_false(self):
        self._login(self.user)
        before_count = UserGroup.objects.count()
        self.form_input['group_picture'] = False
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/individual_group.html')

    def test_user_tries_to_edit_someone_elses_user_group(self):
        self._login(self.user)
        self.url = reverse('edit_user_group', kwargs={"pk": 2})
        response_url: str = reverse(
            "all_groups", kwargs={
                "search_name": "all"})
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_user_provides_invalid_pk(self):
        self._login(self.user)
        self.url = reverse('edit_user_group', kwargs={"pk": 300})
        response_url: str = reverse(
            "all_groups", kwargs={
                "search_name": "all"})
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

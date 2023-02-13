from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import CreateUserGroupForm
from financial_companion.models import User, UserGroup


class CreateUserGroupViewTestCase(ViewTestCase):
    """Tests of the create user group view."""

    def setUp(self):
        self.url = reverse('create_user_group')
        self.form_input = {
            'name': 'Financial Club',
            'description': 'We are the best financial club',
        }
        self.user = User.objects.get(username='@johndoe')

    def test_create_user_group_url(self):
        self.assertEqual(self.url, '/create_user_group/')

    def test_get_create_user_group(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_user_group.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateUserGroupForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_create_category_form_submission(self):
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
        self.assertTrue(isinstance(form, CreateUserGroupForm))

    def test_successful_category_form_submission(self):
        self._login(self.user)
        before_count = UserGroup.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = UserGroup.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
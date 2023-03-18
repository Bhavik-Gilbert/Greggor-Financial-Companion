from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import UserGroupForm
from financial_companion.models import User, UserGroup
from django.http import HttpRequest, HttpResponse


class CreateUserGroupViewTestCase(ViewTestCase):
    """Tests of the create user group view."""

    def setUp(self) -> None:
        self.url: str = reverse('create_user_group')
        self.form_input: dict[str, str] = {
            'name': 'Financial Club',
            'description': 'We are the best financial club',
        }
        self.user: User = User.objects.get(username='@johndoe')

    def test_create_user_group_url(self) -> None:
        self.assertEqual(self.url, '/create_user_group/')

    def test_get_create_user_group(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_user_group.html')
        form: UserGroupForm = response.context['form']
        self.assertTrue(isinstance(form, UserGroupForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_create_user_group_form_submission(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.form_input['name']: str = ''
        before_count: int = UserGroup.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input)
        after_count: int = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_user_group.html')
        form: UserGroupForm = response.context['form']
        self.assertTrue(isinstance(form, UserGroupForm))

    def test_successful_create_user_group_form_submission(self) -> None:
        self._login(self.user)
        before_count: int = UserGroup.objects.count()
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        after_count: int = UserGroup.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

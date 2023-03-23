from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import UserChangePasswordForm
from financial_companion.models import User
from django.http import HttpResponse


class ChangePasswordViewTestCase(ViewTestCase):
    """Unit tests of the change password view"""

    def setUp(self) -> None:
        self.url: str = reverse('change_password')
        self.form_input: dict[str, str] = {
            "password": "Password123",
            "new_password": "Password1234"
        }
        self.user: User = User.objects.get(username='@johndoe')

    def test_change_password_url(self) -> None:
        self.assertEqual(self.url, '/change_password/')

    def test_get_change_password(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/change_password.html')
        form: UserChangePasswordForm = response.context['form']
        self.assertTrue(isinstance(form, UserChangePasswordForm))
        self.assertFalse(form.is_bound)

    def test_get_change_password_redirects_when_not_logged_in(self) -> None:
        response: HttpResponse = self.client.get(self.url, follow=True)
        self._assert_require_login(self.url)

    def test_change_password_success(self) -> None:
        self.assertTrue(self._login(self.user))
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user.username, '@johndoe')
        old_password: str = self.user.password
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/log_in.html")
        self.user.refresh_from_db()
        new_password: str = self.user.password
        self.assertNotEqual(old_password, new_password)
        self.assertFalse(self._is_logged_in())

    def test_change_password_unsuccessful_invalid_user_password(self) -> None:
        self.assertTrue(self._login(self.user))
        self.form_input['password'] = "Password12"
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/change_password.html')
        form: UserChangePasswordForm = response.context['form']
        self.assertTrue(isinstance(form, UserChangePasswordForm))
        self.assertTrue(self._is_logged_in())

    def test_change_password_unsuccessful_user_password(self) -> None:
        self.assertTrue(self._login(self.user))
        invalid_form_input: list[str, str] = {
            "password": "Password123",
            "new_password": "dd"
        }
        response: HttpResponse = self.client.post(
            self.url, invalid_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/change_password.html')
        form: UserChangePasswordForm = response.context['form']
        self.assertTrue(isinstance(form, UserChangePasswordForm))
        self.assertTrue(self._is_logged_in())

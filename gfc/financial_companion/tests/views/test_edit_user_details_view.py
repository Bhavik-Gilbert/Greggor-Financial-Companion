from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.forms import EditUserDetailsForm
from financial_companion.models import User
from django.http import HttpResponse
from typing import Any


class EditUserDetailsViewTestCase(ViewTestCase):
    """Unit tests of the edit user details view"""

    def setUp(self) -> None:
        super().setUp()
        self.url: str = reverse('edit_user_details')
        self.form_input: dict[str, str] = {
            "first_name": "Bob",
            "last_name": "Lee",
            "username": "@boblee",
            "email": "boblee@example.org",
            "bio": "Bob Lee's Personal Spending Tracker"
        }
        self.user: User = User.objects.get(username='@johndoe')

    def test_edit_user_details_url(self) -> None:
        self.assertEqual(self.url, '/edit_user_details/')

    def test_get_edit_user_details(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/edit_user_details.html")
        form: EditUserDetailsForm = response.context['form']
        self.assertTrue(isinstance(form, EditUserDetailsForm))
        self.assertFalse(form.is_bound)

    def test_get_edit_user_details_redirects_when_not_logged_in(self) -> None:
        response: HttpResponse = self.client.get(self.url, follow=True)
        self._assert_require_login(self.url)

    def test_edit_user_details_success(self) -> None:
        self._login(self.user)
        form: EditUserDetailsForm = EditUserDetailsForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user.username, '@johndoe')
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/profile.html")
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'Bob')
        self.assertEqual(self.user.last_name, 'Lee')
        self.assertEqual(self.user.username, '@boblee')
        self.assertEqual(self.user.email, 'boblee@example.org')
        self.assertEqual(self.user.bio, "Bob Lee's Personal Spending Tracker")

    def test_edit_user_details_unsuccessful_invalid_input(self) -> None:
        self._login(self.user)
        invalid_form_input: dict[str, Any] = {}
        response: HttpResponse = self.client.post(
            self.url, invalid_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/edit_user_details.html')
        form: EditUserDetailsForm = response.context['form']
        self.assertTrue(isinstance(form, EditUserDetailsForm))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')

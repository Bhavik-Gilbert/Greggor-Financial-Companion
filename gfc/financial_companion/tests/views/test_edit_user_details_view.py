from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import EditUserDetailsForm
from financial_companion.models import User


class EditUserDetailsViewTestCase(ViewTestCase):
    """Unit tests of the edit user details view"""

    def setUp(self):
        self.url = reverse('edit_user_details')
        self.form_input = {
            "first_name": "Bob",
            "last_name": "Lee",
            "username": "@boblee",
            "email": "boblee@example.org",
            "bio": "Bob Lee's Personal Spending Tracker"
        }
        self.user = User.objects.get(username='@johndoe')

    def test_edit_user_details_url(self):
        self.assertEqual(self.url, '/edit_user_details/')

    def test_get_edit_user_details(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/edit_user_details.html")
        form = response.context['form']
        self.assertTrue(isinstance(form, EditUserDetailsForm))
        self.assertFalse(form.is_bound)

    def test_get_edit_user_details_redirects_when_not_logged_in(self):
        response = self.client.get(self.url, follow=True)
        self._assert_require_login(self.url)

    def test_edit_user_details_success(self):
        self._login(self.user)
        form = EditUserDetailsForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user.username, '@johndoe')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/profile.html")
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'Bob')
        self.assertEqual(self.user.last_name, 'Lee')
        self.assertEqual(self.user.username, '@boblee')
        self.assertEqual(self.user.email, 'boblee@example.org')
        self.assertEqual(self.user.bio, "Bob Lee's Personal Spending Tracker")

    def test_edit_user_details_unsuccessful_invalid_input(self):
        self._login(self.user)
        invalid_form_input = {}
        response = self.client.post(self.url, invalid_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/edit_user_details.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditUserDetailsForm))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')

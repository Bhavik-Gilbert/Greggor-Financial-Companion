from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import UserSignUpForm
from financial_companion.models import User


class SignUpViewTestCase(ViewTestCase):
    """Unit tests of the sign up view"""

    def setUp(self):
        self.url: str = reverse('sign_up')
        self.form_input: dict[str, str] = {
            'first_name': 'Bob',
            'last_name': 'Doe',
            'username': '@bobdoe',
            'email': 'bobdoe@example.org',
            "bio": "Bob Doe's Personal Spending Tracker",
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.user: User = User.objects.get(username='@johndoe')

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    def test_get_sign_up(self):
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/sign_up.html")
        form: UserSignUpForm = response.context['form']
        self.assertTrue(isinstance(form, UserSignUpForm))
        self.assertFalse(form.is_bound)

    def test_get_sign_up_redirects_when_logged_in(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url, follow=True)
        self._assert_require_logout(self.url)

    def test_unsuccessful_sign_up(self):
        self.form_input['username']: str = 'BAD_USERNAME'
        before_count: int = User.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input)
        after_count: int = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/sign_up.html")
        form: UserSignUpForm = response.context['form']
        self.assertTrue(isinstance(form, UserSignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count: int = User.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        after_count: int = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url: str = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")
        user: User = User.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.bio, "Jane Doe's Personal Spending Tracker")
        self.assertTrue(check_password('Password123', user.password))
        self.assertTrue(self._is_logged_in())

    def test_post_sign_up_redirects_when_logged_in(self):
        self._login(self.user)
        before_count: int = User.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        after_count: int = User.objects.count()
        self.assertEqual(after_count, before_count)
        self._assert_require_logout(self.url)
        self.assertEqual(after_count, before_count)

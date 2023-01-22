from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from ..helpers.log_in_helpers import LogInTester
from financial_companion.forms import UserSignUpForm
from financial_companion.models import User

class SignUpViewTestCase(ViewTestCase, LogInTester):
    """Unit tests of the sign up view"""

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'Bob',
            'last_name': 'Doe',
            'username': '@bobdoe',
            'email': 'bobdoe@example.org',
            "bio": "Bob Doe's Personal Spending Tracker",
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.user = User.objects.get(username='@johndoe')


    def test_sign_up_url(self):
        self.assertEqual(self.url,'/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/sign_up.html")
        form = response.context['form']
        self.assertTrue(isinstance(form, UserSignUpForm))
        self.assertFalse(form.is_bound)

    # def test_get_sign_up_redirects_when_logged_in(self):
    #     self.client.login(username=self.user.username, password="Password123")
    #     response = self.client.get(self.url, follow=True)
    #     redirect_url = reverse('feed')
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'feed.html')

    def test_unsuccesful_sign_up(self):
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/sign_up.html")
        form = response.context['form']
        self.assertTrue(isinstance(form, UserSignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self.is_logged_in())

    def test_succesful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")
        user = User.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.bio, "Jane Doe's Personal Spending Tracker")
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self.is_logged_in())

    # def test_post_sign_up_redirects_when_logged_in(self):
    #     self.client.login(username=self.user.username, password="Password123")
    #     before_count = User.objects.count()
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count, before_count)
    #     redirect_url = reverse('dashboard')
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response,  "pages/dashboard.html")

from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import User, Category, CategoryTarget


class EditCategoryTargetViewTestCase(ViewTestCase):
    """Tests of the edit category target view."""

    def setUp(self):
        self.url = reverse('edit_category_target', kwargs={'pk': 1})
        self.test_user = User.objects.get(username='@johndoe')
        self.test_category_target = CategoryTarget.objects.get(id=1)
        self.form_input = {
            'transaction_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_edit_category_target_url(self):
        self.assertEqual(self.url, '/edit_target/category/1')

    def test_get_target_category_form(self):
        self._login(self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_targets.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TargetForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_invalid_pk_entered(self):
        self._login(self.test_user)
        url: str = reverse(
            "edit_category_target", kwargs={
                "pk": 99999999})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_other_users_category_pk_entered(self):
        self._login(self.test_user)
        url: str = reverse(
            "edit_category_target", kwargs={
                "pk": 6})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("categories_list", kwargs = {'search_name':"all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/category_list.html")

    def test_successful_edit_category_target_form_submission(self):
        self._login(self.test_user)
        before_count = CategoryTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/individual_category.html')

    def test_invalid_edit_category_target_form_submission(self):
        self._login(self.test_user)
        self.form_input['transaction_type'] = ''
        before_count = CategoryTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/create_targets.html')

    def test_unsuccessful_edit_category_target_form_due_to_failing_unique_constraints(self):
        self.other_category_target = CategoryTarget.objects.get(id=3)
        self.form_input = {
            'transaction_type': self.other_category_target.transaction_type,
            'timespan': self.other_category_target.timespan,
            'amount': 200.00,
            'currency': 'USD'
        }
        self._login(self.test_user)
        before_count = CategoryTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'pages/create_targets.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        after_count = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

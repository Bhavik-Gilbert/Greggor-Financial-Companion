from .test_view_base import ViewTestCase
from financial_companion.forms import TargetFilterForm
from financial_companion.models import User, AccountTarget
from django.urls import reverse


class ViewTargetsViewTestCase(ViewTestCase):
    """Unit tests of the view targets view"""

    def setUp(self):
        self.url = reverse('view_targets')
        self.form_input = {
            "time": "",
            "income_or_expense": "",
            "target_type": "",
        }
        self.user = User.objects.get(username='@johndoe')

    def test_view_targets_url(self):
        self.assertEqual(self.url, '/view_targets/')

    def test_get_view_targets(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/target_table.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TargetFilterForm))
        self.assertFalse(form.is_bound)

    def test_get_all_targets(self):
        self._login(self.user)
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('view_targets')
        self.assertTemplateUsed(response, 'pages/target_table.html')
        self.assertEqual(len(response.context['page_obj']), 11)

    def test_filter_targets_by_day(self):
        self._login(self.user)
        self.form_input['time'] = 'day'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('view_targets')
        print(len(response.context['page_obj']))
        self.assertTemplateUsed(response, 'pages/target_table.html')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_filter_targets_by_income_or_expense(self):
        self._login(self.user)
        self.form_input['income_or_expense'] = 'income'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('view_targets')
        print(len(response.context['page_obj']))
        self.assertTemplateUsed(response, 'pages/target_table.html')
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_filter_targets_by_target_type(self):
        self._login(self.user)
        self.form_input['target_type'] = 'account'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('view_targets')
        self.assertTemplateUsed(response, 'pages/target_table.html')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

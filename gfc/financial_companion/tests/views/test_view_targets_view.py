from .test_view_base import ViewTestCase
from financial_companion.forms import TargetFilterForm
from financial_companion.models import User
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
        url: str = '/view_targets/'
        url_inputs: dict[str, str] = {}
        self.assertEqual(self.url, url)
        for key in self.form_input:
            url += 'all/'
            url_inputs[key]: str = 'all'
            self.assertEqual(reverse('view_targets', kwargs=url_inputs), url)

    def test_get_view_targets(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TargetFilterForm))
        self.assertFalse(form.is_bound)

    def test_get_all_targets(self):
        self._login(self.user)
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('view_targets')
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_filter_targets_by_day(self):
        self._login(self.user)
        self.form_input['time'] = 'day'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_filter_targets_by_income_or_expense(self):
        self._login(self.user)
        self.form_input['income_or_expense'] = 'income'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_filter_targets_by_target_type(self):
        self._login(self.user)
        self.form_input['target_type'] = 'account'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

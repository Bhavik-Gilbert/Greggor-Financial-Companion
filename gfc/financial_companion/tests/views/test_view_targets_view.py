from .test_view_base import ViewTestCase
from financial_companion.forms import TargetFilterForm
from financial_companion.models import User, AccountTarget
from django.urls import reverse


class ViewTargetsViewTestCase(ViewTestCase):
    """Unit tests of the view targets view"""

    def setUp(self):
        self.url: str = reverse('view_targets')
        self.form_input: dict[str, str] = {
            "time": "",
            "income_or_expense": "",
            "target_type": "",
        }
        self.user: User = User.objects.get(username='@johndoe')

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
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        form: TargetFilterForm = response.context['form']
        self.assertTrue(isinstance(form, TargetFilterForm))
        self.assertFalse(form.is_bound)

    def test_get_all_targets(self):
        self._login(self.user)
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        response_url: str = reverse('view_targets')
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_filter_targets_by_day(self):
        self._login(self.user)
        self.form_input['time']: str = 'day'
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        response_url: str = reverse('view_targets')
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_filter_targets_by_income_or_expense(self):
        self._login(self.user)
        self.form_input['income_or_expense']: str = 'income'
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        response_url: str = reverse('view_targets')
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_filter_targets_by_target_type(self):
        self._login(self.user)
        self.form_input['target_type']: str = 'account'
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        response_url: str = reverse('view_targets')
        self.assertTemplateUsed(response, 'pages/view_targets.html')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

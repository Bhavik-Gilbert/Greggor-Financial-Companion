from .test_view_base import ViewTestCase
from financial_companion.forms import UserLogInForm
from financial_companion.models import User
from django.urls import reverse


class DispalyTransactionsViewTestCase(ViewTestCase):
    """Unit tests of the log in view"""

    def setUp(self):
        self.url = reverse('view_transactions',kwargs={'filter_type': "all"})
        self.user = User.objects.get(username='@johndoe')

    def test_log_in_url(self):
        self.assertEqual(self.url,'/view_transactions/all')
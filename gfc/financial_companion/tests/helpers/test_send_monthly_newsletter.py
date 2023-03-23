from .test_helper_base import HelperTestCase
from financial_companion.helpers import send_monthly_newsletter_email
from financial_companion.models import User
from django.core import mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.core.mail.message import EmailMultiAlternatives


class SendMonthlyNewsletterTaskTestCase(HelperTestCase):
    """Test file for the send monthly newsletter task function"""

    def setUp(self):
        super().setUp()
        send_monthly_newsletter_email()
        self.user: User = User.objects.get(username='@johndoe')
        self.users: QuerySet[User] = get_user_model().objects.all()

    def test_check_correct_number_of_emails_are_sent(self):
        self.assertEqual(len(mail.outbox), len(self.users))

    def test_check_email_contains_correct_information(self):
        email_sent: EmailMultiAlternatives = mail.outbox[0]
        self.assertEqual(email_sent.subject, "Monthly Newsletter")
        self.assertEqual(email_sent.from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(email_sent.to[0], self.user.email)
        self.assertFalse(email_sent.body.find(self.user.full_name()), -1)

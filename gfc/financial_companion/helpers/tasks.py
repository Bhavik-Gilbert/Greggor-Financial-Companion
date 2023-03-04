from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import calendar
from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from datetime import date, timedelta
import financial_companion.models as fc_models
from financial_companion.helpers import get_number_of_days_in_prev_month
from ..helpers import get_number_of_completed_targets


def send_monthly_newsletter_email():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        targets =  get_number_of_completed_targets(user.get_all_targets())
        context = {
            "user": user,
            "month": calendar.month_name[(datetime.now(tz=None).month)-1],
            "transactions": user.get_user_transactions()[:10],
            "targets":targets

        }
        html_content = render_to_string(
            "partials/monthly_newsletter.html", context)
        text_content = strip_tags(html_content)
        send_mail(
            'Monthly Newsletter',
            text_content,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=html_content,
            fail_silently=False,
        )


def add_interest_to_bank_accounts():
    no_of_days_in_prev_month = get_number_of_days_in_prev_month()
    for account in fc_models.BankAccount.objects.all():
        account.balance = account.balance * \
            ((1 + (account.interest_rate / 365))**no_of_days_in_prev_month)
        account.save()

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import calendar
from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import datetime, date
from django.conf import settings
from datetime import date, timedelta
import financial_companion.models as fcmodels
from financial_companion.helpers import (
    get_number_of_days_in_prev_month,
    timespan_map,
    check_date_on_interval,
    check_within_date_range
)


def send_monthly_newsletter_email():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        # today = datetime.datetime.now()
        # transactions = user.get_user_transactions()
        # filtered_transactions = filter((lambda transaction: time_of_transaction__year==today.year, time_of_transaction__month==today.month),  countries)
        # print(len(transactions))
        # print(len(filtered_transactions))
        context = {
            "user": user,
            "month": calendar.month_name[datetime.now(tz=None).month],
            "transactions": user.get_user_transactions()[:10]

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
    print("EMAILS SENT")


def add_interest_to_bank_accounts():
    no_of_days_in_prev_month = get_number_of_days_in_prev_month()
    for account in fcmodels.BankAccount.objects.all():
        account.balance = account.balance * \
            ((1 + (account.interest_rate / 365))**no_of_days_in_prev_month)
        account.save()


def create_transaction_via_recurring_transactions():
    """Goes through all recurring transactions and creates a transaction if its in the given interval"""
    current_date: date = date.today()
    for recurring_transaction in fcmodels.RecurringTransaction.objects.all():
        check_current_in_date_range: bool = check_within_date_range(
            recurring_transaction.start_date, recurring_transaction.end_date, current_date)
        check_current_on_interval: bool = check_date_on_interval(
            recurring_transaction.interval, recurring_transaction.start_date, current_date)
        if check_current_in_date_range and check_current_on_interval:
            transaction: fcmodels.Transaction = fcmodels.Transaction.objects.create(
                title=recurring_transaction.title,
                image=recurring_transaction.image,
                description=recurring_transaction.description,
                category=recurring_transaction.category,
                amount=recurring_transaction.amount,
                currency=recurring_transaction.currency,
                sender_account=recurring_transaction.sender_account,
                receiver_account=recurring_transaction.receiver_account
            )
            recurring_transaction.add_transaction(transaction)

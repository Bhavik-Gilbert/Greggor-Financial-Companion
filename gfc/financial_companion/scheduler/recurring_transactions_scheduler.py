from datetime import datetime
from django.utils import timezone
import pytz
from django.conf import settings
from financial_companion.helpers import create_transaction_via_recurring_transactions
from django_q.models import Schedule


def recurring_transactions_scheduler():
    date_time_str = f'{timezone.now().month + 1}-01-{timezone.now().year}'
    date_object = datetime.strptime(
        date_time_str, '%m-%d-%Y').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

    scheduler = Schedule.objects.create(
        name="Recurring Transactions",
        func='financial_companion.helpers.tasks.create_transaction_via_recurring_transactions',
        minutes=1,
        repeats=-1,
        schedule_type=Schedule.DAILY,
        next_run=date_object
    )

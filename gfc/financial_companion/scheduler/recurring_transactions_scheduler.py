from datetime import datetime
from django.utils import timezone
import pytz
from django.conf import settings
from financial_companion.helpers import create_transaction_via_recurring_transactions
from django_q.models import Schedule


def create_recurring_transactions_scheduler():
    """Creates a scheduler object for recurring transactions"""
    date_time_str: str = f'{timezone.now().month + 1}-01-{timezone.now().year}'
    date_object: datetime.strptime = datetime.strptime(
        date_time_str, '%m-%d-%Y').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

    name: str = "Recurring Transactions"
    if Schedule.objects.filter(name=name).count() == 0:
        scheduler = Schedule.objects.create(
            name=name,
            func='financial_companion.helpers.tasks.create_transaction_via_recurring_transactions',
            minutes=1,
            repeats=-1,
            schedule_type=Schedule.DAILY,
            next_run=date_object
        )

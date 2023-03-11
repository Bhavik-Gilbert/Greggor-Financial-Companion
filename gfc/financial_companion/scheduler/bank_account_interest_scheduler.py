from datetime import datetime
from django.utils import timezone
import pytz
from django.conf import settings
from financial_companion.helpers import add_interest_to_bank_accounts
from django_q.models import Schedule


def create_bank_account_interest_scheduler():
    date_time_str = f'{timezone.now().month + 1}-01-{timezone.now().year}'
    date_object = datetime.strptime(
        date_time_str, '%m-%d-%Y').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

    name = "Bank Account Interest"
    if Schedule.objects.filter(name=name).count() == 0:
        scheduler = Schedule.objects.create(
            name=name,
            func='financial_companion.helpers.tasks.add_interest_to_bank_accounts',
            minutes=1,
            repeats=-1,
            schedule_type=Schedule.MONTHLY,
            next_run=date_object
        )

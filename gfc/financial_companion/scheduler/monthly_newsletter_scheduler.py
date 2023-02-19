from datetime import datetime
from django.utils import timezone
import pytz
from django.conf import settings
from financial_companion.helpers import send_monthly_newsletter_email
from django_q.models import Schedule


def create_monthly_newsletter_scheduler():
    schedulers = Schedule.objects.filter(name="Monthly Newsletter")
    if (len(schedulers) > 0):
        pass
    else:
        date_time_str = f'{timezone.now().month + 1}-01-{timezone.now().year}'
        date_object = datetime.strptime(
            date_time_str, '%m-%d-%Y').replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

        scheduler = Schedule.objects.create(
            name="Monthly Newsletter",
            func='financial_companion.helpers.tasks.send_monthly_newsletter_email',
            minutes=1,
            repeats=-1,
            schedule_type=Schedule.MONTHLY,
            next_run=date_object)

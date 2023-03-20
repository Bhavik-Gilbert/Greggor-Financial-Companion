from .test_scheduler_base import SchedulerTestCase
from financial_companion.scheduler import create_monthly_newsletter_scheduler
from django_q.models import Schedule


class MonthlyNewsletterSchedulerFunctionTestCase(SchedulerTestCase):
    """Test for the monthly newsletter scheduler function"""

    def test_scheduler_object_is_created(self):
        before_count: int = Schedule.objects.count()
        create_monthly_newsletter_scheduler()
        after_count: int = Schedule.objects.count()
        scheduler: Schedule = Schedule.objects.get(id=1)
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(scheduler.name, 'Monthly Newsletter')
        self.assertEqual(
            scheduler.func,
            'financial_companion.helpers.tasks.send_monthly_newsletter_email')
        self.assertEqual(scheduler.minutes, 1)
        self.assertEqual(scheduler.repeats, -1)
        self.assertEqual(scheduler.schedule_type, Schedule.MONTHLY)

from .test_scheduler_base import SchedulerTestCase
from financial_companion.scheduler import create_bank_account_interest_scheduler
from django_q.models import Schedule


class BankAccountInterestSchedulerFunctionTestCase(SchedulerTestCase):
    """Test for the monthly bank account interest calculation scheduler function"""

    def test_scheduler_object_is_created(self):
        before_count: int = Schedule.objects.count()
        create_bank_account_interest_scheduler()
        after_count: int = Schedule.objects.count()
        scheduler: Schedule = Schedule.objects.get(id=1)
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(scheduler.name, 'Bank Account Interest')
        self.assertEqual(
            scheduler.func,
            'financial_companion.helpers.tasks.add_interest_to_bank_accounts')
        self.assertEqual(scheduler.minutes, 1)
        self.assertEqual(scheduler.repeats, -1)
        self.assertEqual(scheduler.schedule_type, Schedule.MONTHLY)

    def test_scheduler_object_not_created_twice(self):
        create_bank_account_interest_scheduler()
        before_count: int = Schedule.objects.count()
        create_bank_account_interest_scheduler()
        after_count: int = Schedule.objects.count()
        self.assertEqual(after_count, before_count)

from .test_scheduler_base import SchedulerTestCase
from financial_companion.scheduler import create_recurring_transactions_scheduler
from financial_companion.models import Transaction
from django_q.models import Schedule


class RecurringTransactionSchedulerFunctionTestCase(SchedulerTestCase):
    """Test for the recurring transactions scheduler function"""

    def test_scheduler_object_is_created(self):
        before_count: int = Schedule.objects.count()
        create_recurring_transactions_scheduler()
        after_count: int = Schedule.objects.count()
        scheduler: Schedule = Schedule.objects.get(id=1)
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(scheduler.name, 'Recurring Transactions')
        self.assertEqual(
            scheduler.func,
            'financial_companion.helpers.tasks.create_transaction_via_recurring_transactions')
        self.assertEqual(scheduler.minutes, 1)
        self.assertEqual(scheduler.repeats, -1)
        self.assertEqual(scheduler.schedule_type, Schedule.DAILY)

    def test_scheduler_object_not_created_twice(self):
        create_recurring_transactions_scheduler()
        before_count: int = Schedule.objects.count()
        create_recurring_transactions_scheduler()
        after_count: int = Schedule.objects.count()
        self.assertEqual(after_count, before_count)

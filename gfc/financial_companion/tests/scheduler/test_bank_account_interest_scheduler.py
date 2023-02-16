from .test_scheduler_base import SchedulerTestCase
from financial_companion.scheduler import create_bank_account_interest_scheduler
from financial_companion.helpers import add_interest_to_bank_accounts
from financial_companion.models import BankAccount
from django_q.models import Schedule


class BankAccountInterestSchedulerFunctionTestCase(SchedulerTestCase):
    """Test for the monthly bank account interest calculation scheduler function"""

    def test_scheduler_object_is_created(self):
        before_count = Schedule.objects.count()
        create_bank_account_interest_scheduler()
        after_count = Schedule.objects.count()
        scheduler = Schedule.objects.get(id=1)
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(scheduler.name, 'Bank Account Interest')
        self.assertEqual(
            scheduler.func,
            'financial_companion.helpers.tasks.add_interest_to_bank_accounts')
        self.assertEqual(scheduler.minutes, 1)
        self.assertEqual(scheduler.repeats, -1)
        self.assertEqual(scheduler.schedule_type, Schedule.MONTHLY)

    def test_interest_is_added_to_bank_account(self):
        for account in BankAccount.objects.all():
            if (account.interest_rate > 0):
                before_adding = account.balance
                add_interest_to_bank_accounts()
                after_adding = BankAccount.objects.get(id=account.id).balance
                self.assertGreater(after_adding, before_adding)

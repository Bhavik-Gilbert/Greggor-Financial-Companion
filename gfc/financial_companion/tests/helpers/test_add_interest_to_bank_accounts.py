from .test_helper_base import HelperTestCase
from financial_companion.helpers import add_interest_to_bank_accounts
from financial_companion.models import BankAccount


class AddInterestToBankAccountsTaskTestCase(HelperTestCase):
    """Test file for the add interest to bank accounts task"""

    def test_interest_is_added_to_bank_account(self):
        for account in BankAccount.objects.all():
            if (account.interest_rate > 0):
                before_adding = account.balance
                add_interest_to_bank_accounts()
                after_adding = BankAccount.objects.get(id=account.id).balance
                self.assertGreater(after_adding, before_adding)

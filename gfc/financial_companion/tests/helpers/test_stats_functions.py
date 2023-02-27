from .test_helper_base import HelperTestCase
from financial_companion.helpers import functions
from financial_companion.helpers.enums import Timespan 
from financial_companion.models import Transaction, Category
from financial_companion.helpers.functions import get_category_splits

from ..models.test_abstract_model_base import AbstractModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import AbstractTransaction, Transaction

class StatisticsFuunctionsTestCase(HelperTestCase):
    
    fixtures: list[str] = [
        "example_abstract_transactions.json",
        "example_category.json",
        "example_accounts.json",
        "example_users.json"]

    @classmethod
    def setUpClass(self):
        """Create temporary model"""
        self.mixin: AbstractTransaction = AbstractTransaction
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()
        self.test_model: ModelBase = self.model.objects.get(id=1)


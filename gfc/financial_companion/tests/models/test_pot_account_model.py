from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import PotAccount

class PotAccountModelTestCase(ModelTestCase):
    """test file for the pot accounts model"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: ModelBase = PotAccount.objects.get(id = 3)

    def test_valid_target(self):
        self._assert_model_is_valid()

    def test_vaild_balance_float(self):
        self.test_model.balance: float = 200.00
        self._assert_model_is_valid()

    def test_vaild_balance_for_2_decimal_places(self):
        self.test_model.balance: float = Decimal('200.01')
        self._assert_model_is_valid()
    
    def test_invalid_balance_for_3_decimal_places(self):
        self.test_model.balance: float = Decimal('200.012')
        self._assert_model_is_invalid()
    
    def test_vaild_currency_types(self):
        for currency in CurrencyType:
            self.test_model.currency: str  = currency
            self._assert_model_is_valid()
    
    def test_invalid_currency_type_must_be_in_enum(self):
        self.test_model.currency: str = "incorrect"
        self._assert_model_is_invalid()
    
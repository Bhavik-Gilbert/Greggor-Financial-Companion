from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import PotAccount

class AccountModelTestCase(ModelTestCase):
    """test file for the pot accounts model"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: ModelBase = PotAccount.objects.get(id = 5)

    def test_valid_target(self):
        self._assert_model_is_valid()

    def test_bank_name_is_not_blank(self):
        self.test_model.bank_name: str = ""
        self._assert_model_is_invalid()

    def test_valid_bank_name(self):
        self.test_model.bank_name: str = "abc"
        self._assert_model_is_valid()

    def test_bank_name_max_length_is_50(self):
        self.test_model.bank_name: str = "a" * 50
        self._assert_model_is_valid()
    
    def test_bank_name_is_not_longer_than_50(self):
        self.test_model.bank_name: str = 'a' * 51
        self._assert_model_is_invalid()
  
    # def test_bank_name_cannot_be_blank(self):
    #     self.test_model.bank_name: str = ""
    #     self._assert_model_is_invalid()

    # def test_bank_name_is_not_blank(self):
    #     self.test_model.bank_name: str = ""
    #     self._assert_model_is_invalid()

    # def test_valid_bank_name(self):
    #     self.test_model.bank_name: str = "abc"
    #     self._assert_model_is_valid()

    # def test_bank_name_max_length_is_50(self):
    #     self.test_model.bank_name: str = "a" * 50
    #     self._assert_model_is_valid()
    
    # def test_bank_name_is_not_longer_than_50(self):
    #     self.test_model.bank_name: str = 'a' * 51
    #     self._assert_model_is_invalid()
    
    # def test_bank_name_cannot_be_blank(self):
    #     self.test_model.bank_name: str = ""
    #     self._assert_model_is_invalid()
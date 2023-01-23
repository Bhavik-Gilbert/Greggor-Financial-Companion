from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal



from ...helpers import CurrencyType
from ...models import BankAccount

class AccountModelTestCase(ModelTestCase):
    """test file for the pot accounts model"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: ModelBase = BankAccount.objects.get(id = 5)

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
  
    def test_account_number_cannot_be_blank(self):
        self.test_model.account_number: str = ""
        self._assert_model_is_invalid()

    def test_valid_account_number(self):
        self.test_model.account_number: str = "89898989"
        self._assert_model_is_valid()

    def test_account_number_max_length_is_8(self):
        self.test_model.account_number: str = "1" * 8
        self._assert_model_is_valid()
    
    def test_account_number_is_not_longer_than_8(self):
        self.test_model.account_number: str = '1' * 9
        self._assert_model_is_invalid()

    def test_sort_code_cannot_be_blank(self):
        self.test_model.sort_code: str = ""
        self._assert_model_is_invalid()

    def test_valid_sort_code(self):
        self.test_model.sort_code: str = "898989"
        self._assert_model_is_valid()

    def test_sort_code_max_length_is_6(self):
        self.test_model.sort_code: str = "1" * 6
        self._assert_model_is_valid()
    
    def test_sort_code_is_not_longer_than_6(self):
        self.test_model.sort_code: str = '1' * 7
        self._assert_model_is_invalid()
    
    def test_account_number_is_int(self):
        with self.assertRaises(Exception) as raised:
            self.test_model.account_number = "abcdefhg"
            self.test_model.save()
            self._assert_model_is_invalid()
        self.assertEqual(AssertionError, type(raised.exception))
    
    def test_sort_code_is_int(self):
        with self.assertRaises(Exception) as raised:
            self.test_model.sort_code = "abcdef"
            self.test_model.save()
            self._assert_model_is_invalid()
        self.assertEqual(AssertionError, type(raised.exception))

    def test_account_number_is_int(self):
        self.test_model.account_number = "12345678"
        self.test_model.save()
        self._assert_model_is_valid()

    def test_sort_code_is_int(self):
        self.test_model.sort_code = "123456"
        self.test_model.save()
        self._assert_model_is_valid()

    def test_iban_cannot_be_blank(self):
        self.test_model.iban: str = ""
        self._assert_model_is_valid()

    def test_valid_iban(self):
        self.test_model.iban: str = "8989898989898989898989898989889899"
        self._assert_model_is_valid()

    def test_iban_max_length_is_34(self):
        self.test_model.iban: str = "1" * 34
        self._assert_model_is_valid()
    
    def test_iban_is_not_longer_than_34(self):
        self.test_model.iban: str = '1' * 35
        self._assert_model_is_invalid()

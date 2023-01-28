from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import BankAccount, User

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
    
    def test_account_number_cannot_contain_char(self):
        self.test_model.account_number = "abcdefhg"
        self.test_model.save()
        self._assert_model_is_invalid()

    def test_account_number_cannot_be_less_than_8_digits(self):
        self.test_model.account_number = "9090909"
        self.test_model.save()
        self._assert_model_is_invalid()
    
    def test_sort_code_cannot_contain_char(self):
        self.test_model.sort_code = "abcdef"
        self.test_model.save()
        self._assert_model_is_invalid()

    def test_account_number_is_int(self):
        self.test_model.account_number = "12345678"
        self.test_model.save()
        self._assert_model_is_valid()

    def test_sort_code_is_int(self):
        self.test_model.sort_code = "123456"
        self.test_model.save()
        self._assert_model_is_valid()
    
    def test_sort_code_cannot_be_less_than_6_digits(self):
        self.test_model.sort_code = "90909"
        self.test_model.save()
        self._assert_model_is_invalid()

    def test_iban_cannot_be_blank(self):
        self.test_model.iban: str = ""
        self._assert_model_is_valid()

    def test_valid_iban(self):
        self.test_model.iban: str = "GB12345678901234567"
        self._assert_model_is_valid()

    def test_iban_max_length_is_33(self):
        self.test_model.iban: str = f"GB{'9' * 31}"
        self._assert_model_is_valid()
    
    def test_iban_is_not_longer_than_33(self):
        self.test_model.iban: str = f"GB{'9' * 32}"
        self._assert_model_is_invalid()

    def test_iban_cannot_be_less_than_15_digits(self):
        self.test_model.iban = "GB123456789012"
        self.test_model.save()
        self._assert_model_is_invalid()
    
    def test_iban_cannot_start_with_numbers(self):
        self.test_model.iban = "123456789012345"
        self.test_model.save()
        self._assert_model_is_invalid()

    def test_iban_starts_with_iso_3166_country_code(self):
        self.test_model.iban = "GB123456789012345"
        self.test_model.save()
        self._assert_model_is_valid()

    def test_interest_rate_can_be_0(self):
        self.test_model.interest_rate: float = Decimal("0.0")
        self._assert_model_is_valid()
    
    def test_interest_rate_is_2_decimal_places(self):
        self.test_model.interest_rate: float = Decimal("1.01")
        self._assert_model_is_valid()
    
    def test_interest_rate_cannot_have_more_than_2_decimal_places(self):
        self.test_model.interest_rate: float = Decimal("10.001")
        self._assert_model_is_invalid()
    
    def test_interest_rate_default_is_not_blank(self):
        self.test_model.interest_rate: float = None
        self._assert_model_is_invalid()

    def test_interest_rate_default_is_zero(self):
        default_interest_zero_bank_model = BankAccount.objects.create(
            name = "bank account",
            description = "my first bank account",
            user = User.objects.get(id=1),
            balance = 100,
            currency = CurrencyType.GBP,
            bank_name = "Kush Corp",
            account_number = "11111111",
            sort_code = "111111",
            iban = "GB12345678901234567"
        )
        self._assert_model_is_valid()
        self.assertEquals(0, default_interest_zero_bank_model.interest_rate)
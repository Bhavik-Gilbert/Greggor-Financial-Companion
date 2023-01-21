from .test_abstract_model_base import AbstractModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import AbstractTransaction

class AbstractTransactionModelTestCase(AbstractModelTestCase):
    """Test file for abstract transaction model class"""

    fixtures: list[str] = ["example_transactions.json"]

    @classmethod
    def setUpClass(self):
        """Create temporary model"""
        self.mixin: AbstractTransaction = AbstractTransaction
        super().setUpClass()

    def setUp(self) -> None:
        AbstractTarget
        super().setUp()
        self.test_model: ModelBase = self.model.objects.get(id=1)

    def test_valid_transaction(self):
        self._assert_model_is_valid()

    def test_valid_title(self):
        self.test_model.title: string = "Test transaction title"
        self._assert_model_is_valid()

    def test_title_may_not_be_blank(self):
        self.test_model.title: string = ""
        self._assert_model_is_invalid()

    def test_valid_title_of_30_characters(self):
        self.test_model.title: float = "x" * 30
        self._assert_model_is_valid()

    def test_invalid_title_of_more_than_30_characters(self):
        self.test_model.title: float = "x" * 31
        self._assert_model_is_invalid()

    def test_valid_description(self):
        self.test_model.description: string = "Test transaction description"
        self._assert_model_is_valid()

    def test_title_may_be_blank(self):
        self.test_model.description: string = ""
        self._assert_model_is_valid()

    def test_valid_description_of_200_characters(self):
        self.test_model.description: float = "x" * 200
        self._assert_model_is_valid()

    def test_invalid_description_of_more_than_200_characters(self):
        self.test_model.description: float = "x" * 201
        self._assert_model_is_invalid()

    def test_image_may_be_blank(self):
        self.test_model.image = ''
        self._assert_model_is_valid()

    def test_valid_amount_integer(self):
        self.test_model.amount: float = 99
        self._assert_model_is_valid()

    def test_valid_amount_2_decimal_places(self):
        self.test_model.amount: float = Decimal('99.99')
        self._assert_model_is_valid()

    def test_invalid_amount_more_than_2_decimal_places(self):
        self.test_model.amount: float = Decimal('99.999')
        self._assert_model_is_invalid()

    def test_amount_may_not_be_blank(self):
        self.test_model.amount: float = None
        self._assert_model_is_invalid()

    def test_valid_currency_type_enum_options(self):
        for currency_type in CurrencyType:
            self.test_model.currency: str = currency_type
            self._assert_model_is_valid()

    def test_invalid_currency_type_must_be_in_enum(self):
        self.test_model.currency: str = "incorrect"
        self._assert_model_is_invalid()

    def test_invalid_currency_type_may_not_be_blank(self):
        self.test_model.currency = ""
        self._assert_model_is_invalid()

from .test_abstract_model_base import AbstractModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal

from ...helpers import Timespan, TransactionType
from ...models import AbstractTarget

class AbstractTargetModelTestCase(AbstractModelTestCase):
    """Test file for abstract target model class"""
    
    fixtures: list[str] = ["example_targets.json"]

    @classmethod
    def setUpClass(self):
        """Create temporary model"""
        self.mixin: AbstractTarget = AbstractTarget
        super().setUpClass()

    def setUp(self) -> None:
        AbstractTarget
        super().setUp()
        self.test_model: ModelBase = self.model.objects.get(id=1)

    def test_valid_target(self):
        self._assert_model_is_valid()
    
    def test_valid_amount_integer(self):
        self.test_model.amount: float = 99
        self._assert_model_is_valid()

    def test_valid_amount_2_decimal_places(self):
        # TODO: Check model for why invalid
        self.test_model.amount: float = Decimal('99.99')
        self._assert_model_is_valid()
    
    def test_invalid_amount_more_than_2_decimal_places(self):
        self.test_model.amount: float = Decimal('99.999')
        self._assert_model_is_invalid()

    def test_valid_timespan_enum_options(self):
        for timespan in Timespan:
            self.test_model.timespan: str = timespan
            self._assert_model_is_valid()
    
    def test_invalid_timespan_must_be_in_enum(self):
        self.test_model.timespan: str = "incorrect"
        self._assert_model_is_invalid()
        
    def test_valid_transaction_type_enum_options(self):
        for transaction_type in TransactionType:
            self.test_model.transaction_type: str = transaction_type
            self._assert_model_is_valid()
    
    def test_invalid_transaction_type_must_be_in_enum(self):
        self.test_model.timespan: str = "incorrect"
        self._assert_model_is_invalid()


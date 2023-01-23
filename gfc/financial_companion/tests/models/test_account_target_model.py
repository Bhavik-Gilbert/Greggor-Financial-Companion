from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError
from ...models import AccountTarget

class CategoryTargetModelTestCase(ModelTestCase):
    """Test file for AccountTarget model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: AccountTarget = AccountTarget.objects.get(id=1)
        self.second_model: AccountTarget = AccountTarget.objects.get(id=2)
    
    def test_valid_target_category(self) -> None:
        self._assert_model_is_valid()
    
    def test_valid_duplicate_account_id_duplicate_timespan(self) -> None:
        self.second_model.account_id: int = self.test_model.account_id
        self.second_model.timespan: str = self.test_model.timespan
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_valid_duplicate_account_id_duplicate_transaction_type(self) -> None:
        self.second_model.account_id: int = self.test_model.account_id
        self.second_model.transaction_type: str = self.test_model.transaction_type
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_valid_duplicate_timespan_duplicate_transaction_type(self) -> None:
        self.second_model.timespan: str = self.test_model.timespan
        self.second_model.transaction_type: str = self.test_model.transaction_type
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_invalid_duplicate_account_id_duplicate_transaction_type_duplicate_timespan(self) -> None:
        with self.assertRaises(Exception) as raised:
            self.second_model.account_id: int = self.test_model.account_id
            self.second_model.timespan: str = self.test_model.timespan
            self.second_model.transaction_type: str = self.test_model.transaction_type
            self.second_model.save()
            self._assert_model_is_invalid()
        self.assertEqual(IntegrityError, type(raised.exception))
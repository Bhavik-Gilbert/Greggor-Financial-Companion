from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError
from ...models import CategoryTarget

class CategoryTargetModelTestCase(ModelTestCase):
    """Test file for CategoryTarget model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: CategoryTarget = CategoryTarget.objects.get(id=1)
        self.second_model: CategoryTarget = CategoryTarget.objects.get(id=2)
    
    def test_valid_target_category(self) -> None:
        self._assert_model_is_valid()
    
    def test_valid_duplicate_category_id_duplicate_timespan(self) -> None:
        self.second_model.category_id: int = self.test_model.category_id
        self.second_model.timespan: str = self.test_model.timespan
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_valid_duplicate_category_id_duplicate_transaction_type(self) -> None:
        self.second_model.category_id: int = self.test_model.category_id
        self.second_model.transaction_type: str = self.test_model.transaction_type
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_valid_duplicate_timespan_duplicate_transaction_type(self) -> None:
        self.second_model.timespan: str = self.test_model.timespan
        self.second_model.transaction_type: str = self.test_model.transaction_type
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_invalid_duplicate_category_id_duplicate_transaction_type_duplicate_timespan(self) -> None:
        with self.assertRaises(Exception) as raised:
            self.second_model.category_id: int = self.test_model.category_id
            self.second_model.timespan: str = self.test_model.timespan
            self.second_model.transaction_type: str = self.test_model.transaction_type
            self.second_model.save()
            self._assert_model_is_invalid()
        self.assertEqual(IntegrityError, type(raised.exception))
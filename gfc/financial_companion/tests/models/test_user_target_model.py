from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError
from ...models import UserTarget

class UserTargetModelTestCase(ModelTestCase):
    """Test file for UserTarget model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: UserTarget = UserTarget.objects.get(id=1)
        self.second_model: UserTarget = UserTarget.objects.get(id=2)
    
    def test_valid_target_user(self):
        self._assert_model_is_valid()
    
    def test_valid_duplicate_user_duplicate_timespan(self):
        self.second_model.user = self.test_model.user
        self.second_model.timespan = self.test_model.timespan
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_valid_duplicate_user_duplicate_transaction_type(self):
        self.second_model.user = self.test_model.user
        self.second_model.transaction_type = self.test_model.transaction_type
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_valid_duplicate_timespan_duplicate_transaction_type(self):
        self.second_model.timespan = self.test_model.timespan
        self.second_model.transaction_type = self.test_model.transaction_type
        self.second_model.save()
        self._assert_model_is_valid()
    
    def test_invalid_duplicate_user_duplicate_transaction_type_duplicate_timespan(self):
        with self.assertRaises(Exception) as raised:
            self.second_model.user = self.test_model.user
            self.second_model.timespan = self.test_model.timespan
            self.second_model.transaction_type = self.test_model.transaction_type
            self.second_model.save()
            self._assert_model_is_invalid()
        self.assertEqual(IntegrityError, type(raised.exception))
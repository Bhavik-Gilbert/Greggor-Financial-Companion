from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError
from ...models import UserTarget, User
from freezegun import freeze_time
from ...helpers import Timespan, TransactionType


class UserTargetModelTestCase(ModelTestCase):
    """Test file for UserTarget model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: UserTarget = UserTarget.objects.get(id=1)
        self.second_model: UserTarget = UserTarget.objects.get(id=2)

    def test_valid_target_user(self):
        self._assert_model_is_valid()

    def test_valid_duplicate_user_duplicate_timespan(self):
        self.second_model.user: User = self.test_model.user
        self.second_model.timespan: Timespan = self.test_model.timespan
        self.second_model.save()
        self._assert_model_is_valid()

    def test_valid_duplicate_user_duplicate_target_type(self):
        self.second_model.user: User = self.test_model.user
        self.second_model.target_type: TransactionType = self.test_model.target_type
        self.second_model.save()
        self._assert_model_is_valid()

    def test_valid_duplicate_timespan_duplicate_target_type(self):
        self.second_model.timespan: Timespan = self.test_model.timespan
        self.second_model.target_type: TransactionType = self.test_model.target_type
        self.second_model.save()
        self._assert_model_is_valid()

    def test_invalid_duplicate_user_duplicate_target_type_duplicate_timespan(
            self):
        with self.assertRaises(Exception) as raised:
            self.second_model.user: User = self.test_model.user
            self.second_model.timespan: Timespan = self.test_model.timespan
            self.second_model.target_type: TransactionType = self.test_model.target_type
            self.second_model.save()
            self._assert_model_is_invalid()
        self.assertEqual(IntegrityError, type(raised.exception))

    @freeze_time("2023-01-01 13:00:00")
    def test_valid_target_is_complete_when_complete(self):
        self.assertEqual(self.test_model.is_complete(), True)

    @freeze_time("2025-01-01 13:00:00")
    def test_valid_target_is_complete_when_not_complete(self):
        self.assertEqual(self.test_model.is_complete(), False)

    def test_get_model_name_function_when_plural_is_false(self) -> None:
        self.assertEquals(self.test_model.getModelName(), "user")

    def test_get_model_name_function_when_plural_is_true(self) -> None:
        self.assertEquals(self.test_model.getModelName(plural=True), "users")

    def test_get_str_function(self) -> None:
        self.assertEquals(self.test_model.__str__(), "personal target")

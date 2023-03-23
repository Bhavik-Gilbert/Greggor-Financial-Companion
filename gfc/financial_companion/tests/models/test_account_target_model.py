from .test_model_base import ModelTestCase
from django.db.backends.sqlite3.base import IntegrityError
from ...models import AccountTarget
from freezegun import freeze_time


class AccountTargetModelTestCase(ModelTestCase):
    """Test file for the AccountTarget model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: AccountTarget = AccountTarget.objects.get(id=1)
        self.second_model: AccountTarget = AccountTarget.objects.get(id=2)

    def test_valid_target_account(self) -> None:
        self._assert_model_is_valid()

    def test_valid_duplicate_account_duplicate_timespan(self) -> None:
        self.second_model.account: int = self.test_model.account
        self.second_model.timespan: str = self.test_model.timespan
        self.second_model.save()
        self._assert_model_is_valid()

    def test_valid_duplicate_account_duplicate_target_type(self) -> None:
        self.second_model.account: int = self.test_model.account
        self.second_model.target_type: str = self.test_model.target_type
        self.second_model.save()
        self._assert_model_is_valid()

    def test_valid_duplicate_timespan_duplicate_target_type(self) -> None:
        self.second_model.timespan: str = self.test_model.timespan
        self.second_model.target_type: str = self.test_model.target_type
        self.second_model.save()
        self._assert_model_is_valid()

    def test_invalid_duplicate_account_duplicate_target_type_duplicate_timespan(
            self) -> None:
        with self.assertRaises(Exception) as raised:
            self.second_model.account: int = self.test_model.account
            self.second_model.timespan: str = self.test_model.timespan
            self.second_model.target_type: str = self.test_model.target_type
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
        self.assertEquals(self.test_model.get_model_name(), "account")

    def test_get_model_name_function_when_plural_is_true(self) -> None:
        self.assertEquals(
            self.test_model.get_model_name(
                plural=True), "accounts")

    def test_get_str_function(self) -> None:
        self.assertEquals(self.test_model.__str__(), "ghi")

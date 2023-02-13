from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase


from ...models import Account


class AccountModelTestCase(ModelTestCase):
    """test file for the accounts model"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: ModelBase = Account.objects.get(id=1)

    def test_valid_target(self):
        self._assert_model_is_valid()

    def test_name_is_not_blank(self):
        self.test_model.name: str = ""
        self._assert_model_is_invalid()

    def test_valid_name(self):
        self.test_model.name: str = "abc"
        self._assert_model_is_valid()

    def test_name_max_length_is_50(self):
        self.test_model.name: str = "a" * 50
        self._assert_model_is_valid()

    def test_name_is_not_longer_than_50(self):
        self.test_model.name: str = 'a' * 51
        self._assert_model_is_invalid()

    def test_description_can_be_blank(self):
        self.test_model.description: str = ""
        self._assert_model_is_valid()

    def test_description_max_length_is_500(self):
        self.test_model.description: str = "a" * 500
        self._assert_model_is_valid

    def test_description_is_not_longer_than_500(self):
        self.test_model.description: str = "a" * 501
        self._assert_model_is_invalid()

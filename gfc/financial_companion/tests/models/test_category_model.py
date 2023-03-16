from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from financial_companion.models.category_model import Category
from financial_companion.models.user_model import User


class CategoryModelTestCase(ModelTestCase):
    """Test file for Category model class"""

    def setUp(self):
        super().setUp()
        self.test_model: ModelBase = Category.objects.get(id=1)

    def test_valid_target(self):
        self._assert_model_is_valid()

    def test_name_must_not_blank(self):
        self.test_model.name: str = ''
        self._assert_model_is_invalid()

    def test_name_has_length_of_max_50(self):
        self.test_model.name : str= 'j' * 50
        self._assert_model_is_valid()

    def test_name_is_not_more_than_50_characters(self):
        self.test_model.name: str = 'j' * 51
        self._assert_model_is_invalid()

    def test_description_must_not_blank(self):
        self.test_model.description: str = ''
        self._assert_model_is_invalid()

    def test_description_has_length_of_max_520(self):
        self.test_model.description: str = 'j' * 520
        self._assert_model_is_valid()

    def test_description_is_not_more_than_520_characters(self):
        self.test_model.description: str = 'j' * 521
        self._assert_model_is_invalid()

    def test_user_cannot_be_empty(self):
        self.test_model.user: User = None
        self._assert_model_is_invalid()

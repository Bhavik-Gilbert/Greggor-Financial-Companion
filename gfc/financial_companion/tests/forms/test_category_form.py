from .test_form_base import FormTestCase
from financial_companion.forms import CategoryForm
from financial_companion.models.user_model import User
from financial_companion.models.category_model import Category
from typing import Any


class CategoryFormTestCase(FormTestCase):
    """Unit tests of the category form."""

    def setUp(self):
        self.test_model: User = User.objects.get(username='@johndoe')
        self.form_input: dict[str, Any] = {
            'name': 'Travel',
            'description': 'Travel Expenses'}

    def test_form_contains_required_fields(self):
        form: CategoryForm = CategoryForm()
        self._assert_form_has_necessary_fields(
            form,
            'name',
            'description'
        )

    def test_form_accepts_valid_input(self):
        form: CategoryForm = CategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_name_up_to_50_character_input(self):
        self.form_input['name']: str = 'x' * 50
        form: CategoryForm = CategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_description_up_to_520_character_input(self):
        self.form_input['description']: str = 'x' * 520
        form: CategoryForm = CategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_doesnt_accept_name_greater_than_50_character_input(self):
        self.form_input['name']: str = 'x' * 51
        form: CategoryForm = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_doesnt_accept_description_greater_than_520_character_input(
            self):
        self.form_input['description']: str = 'x' * 521
        form: CategoryForm = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_name_can_not_be_empty(self):
        self.form_input['name']: str = ''
        form: CategoryForm = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_description_can_not_be_empty(self):
        self.form_input['description']: str = ''
        form: CategoryForm = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly_when_no_timespan_specified(self):
        form: CategoryForm = CategoryForm(
            instance=self.test_model, data=self.form_input)
        before_count: int = Category.objects.count()
        category: Category = form.save(self.test_model)
        after_count: int = Category.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(category.user, self.test_model)
        self.assertEqual(category.name, 'Travel')
        self.assertEqual(category.description, 'Travel Expenses')

    def test_form_updates_correctly(self):
        category: Category = Category.objects.get(id=1)
        form: CategoryForm = CategoryForm(
            instance=self.test_model, data=self.form_input)
        before_count: int = Category.objects.count()
        current_category: Category = form.save(
            current_user=self.test_model,
            instance=category)
        after_count: int = Category.objects.count()
        self.assertEqual(current_category.name, 'Travel')
        self.assertEqual(current_category.description, 'Travel Expenses')

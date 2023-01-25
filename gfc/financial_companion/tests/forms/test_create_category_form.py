"""Unit tests of the log in form."""
from django import forms
from .test_form_base import FormTestCase
from financial_companion.forms import CreateCategoryForm
from financial_companion.models.user_model import User
from financial_companion.models.category_model import Category
from financial_companion.models.target_model import CategoryTarget

class CreateCategoryFormTestCase(FormTestCase):
    """Unit tests of the category form."""
    def setUp(self):
        self.test_model = User.objects.get(username = '@johndoe')
        self.form_input = {  
            'name': 'Travel',
         'description': 'Travel Expenses',
         'amount': 0}

    def test_form_contains_required_fields(self):
        form = CreateCategoryForm()
        self._assert_form_has_necessary_fields(
            form,
            'name',
            'description',
            'amount',
            'timespan'
        )

    def test_form_accepts_valid_input(self):
        form = CreateCategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_name_up_to_50_character_input(self):
        self.form_input['name'] = 'x'*50
        form = CreateCategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_description_up_to_50_character_input(self):
        self.form_input['description'] = 'x'*50
        form = CreateCategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_doesnt_accept_name_greater_than_50_character_input(self):
        self.form_input['name'] = 'x'*51
        form = CreateCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_doesnt_accept_description_greater_than_50_character_input(self):
        self.form_input['description'] = 'x'*51
        form = CreateCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_name_can_not_be_empty(self):
        self.form_input['name'] = ''
        form = CreateCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_description_can_not_be_empty(self):
        self.form_input['description'] = ''
        form = CreateCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_timespan_can_be_empty(self):
        self.form_input['timespan'] = ''
        form = CreateCategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # As initial value is specified
    def test_form_amount_can_not_be_empty(self):
        self.form_input['amount'] = ''
        form = CreateCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly_when_no_timespan_specified(self):
        form = CreateCategoryForm(instance=self.test_model, data=self.form_input)
        before_count = Category.objects.count()
        category = form.save(self.test_model)
        after_count = Category.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(category.user, self.test_model)
        self.assertEqual(category.name, 'Travel')
        self.assertEqual(category.description, 'Travel Expenses')
    
    def test_form_must_save_correctly_when_timespan_is_specified(self):
        self.form_input['timespan'] = 'day'
        form = CreateCategoryForm(instance=self.test_model, data=self.form_input)
        before_count_category = Category.objects.count()
        before_count_categoryTarget = CategoryTarget.objects.count()
        category = form.save(self.test_model)
        after_count_category = Category.objects.count()
        after_count_categoryTarget = CategoryTarget.objects.count()
        category_target = CategoryTarget.objects.get(category_id = category)
        self.assertEqual(after_count_category, before_count_category + 1)
        self.assertEqual(after_count_categoryTarget, before_count_categoryTarget + 1)
        self.assertEqual(category.user, self.test_model)
        self.assertEqual(category.name, 'Travel')
        self.assertEqual(category.description, 'Travel Expenses')
        self.assertEqual(category_target.category_id, category)
        self.assertEqual(category_target.amount, 0)
        self.assertEqual(category_target.timespan, 'day')
       
    

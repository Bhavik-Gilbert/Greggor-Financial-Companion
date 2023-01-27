"""Unit tests of the log in form."""
from django import forms
from .test_form_base import FormTestCase
from financial_companion.forms import CategoryForm
from financial_companion.models.user_model import User
from financial_companion.models.category_model import Category
from financial_companion.models.target_model import CategoryTarget

class CategoryFormTestCase(FormTestCase):
    """Unit tests of the category form."""
    def setUp(self):
        self.test_model = User.objects.get(username = '@johndoe')
        self.form_input = {  
            'name': 'Travel',
         'description': 'Travel Expenses'}

    def test_form_contains_required_fields(self):
        form = CategoryForm()
        self._assert_form_has_necessary_fields(
            form,
            'name',
            'description'
        )

    def test_form_accepts_valid_input(self):
        form = CategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_name_up_to_50_character_input(self):
        self.form_input['name'] = 'x'*50
        form = CategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_description_up_to_50_character_input(self):
        self.form_input['description'] = 'x'*50
        form = CategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_doesnt_accept_name_greater_than_50_character_input(self):
        self.form_input['name'] = 'x'*51
        form = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_doesnt_accept_description_greater_than_50_character_input(self):
        self.form_input['description'] = 'x'*51
        form = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_name_can_not_be_empty(self):
        self.form_input['name'] = ''
        form = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_description_can_not_be_empty(self):
        self.form_input['description'] = ''
        form = CategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly_when_no_timespan_specified(self):
        form = CategoryForm(instance=self.test_model, data=self.form_input)
        before_count = Category.objects.count()
        category = form.save(self.test_model)
        after_count = Category.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(category.user, self.test_model)
        self.assertEqual(category.name, 'Travel')
        self.assertEqual(category.description, 'Travel Expenses')
    



 
       
    

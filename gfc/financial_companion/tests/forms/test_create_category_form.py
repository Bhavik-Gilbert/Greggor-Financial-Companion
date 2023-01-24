"""Unit tests of the log in form."""
from django import forms
from .test_form_base import FormTestCase
from financial_companion.forms import CreateCategoryForm

class CreateCategoryFormTestCase(FormTestCase):
    """Unit tests of the category form."""
    def setUp(self):
        self.form_input = {'name': 'Travel', 'description': 'Travel Expenses'}

    def test_form_contains_required_fields(self):
        form = CreateCategoryForm()
        self._assert_form_has_necessary_fields(
            form,
            'name',
            'description'
        )

    def test_form_accepts_valid_input(self):
        form = CreateCategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_name_can_not_be_empty(self):
        self.form_input['name'] = ''
        form = CreateCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_description_can_not_be_empty(self):
        self.form_input['description'] = ''
        form = CreateCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    

from django import forms
from django.urls import reverse
from .test_form_base import FormTestCase
from financial_companion.forms import EditUserDetailsForm
from financial_companion.models import User


class EditUserDetailsFormTestCase(FormTestCase):
    """Test of the sign up form"""

    def setUp(self):
        self.url = reverse('edit_user_details')
        self.form_input = {
            "first_name": "Bob",
            "last_name": "Lee",
            "username": "@boblee",
            "email": "boblee@example.org",
            "bio": "Bob Lee's Personal Spending Tracker"
        }

    def test_form_contains_required_fields(self):
        form: EditUserDetailsForm = EditUserDetailsForm()
        self._assert_form_has_necessary_fields(
            form,
            'first_name',
            'last_name',
            'username',
            'email',
            'bio'
        )
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

    def test_valid_edit_user_details_form(self):
        form = EditUserDetailsForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='@johndoe')
        form = EditUserDetailsForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.first_name, 'Bob')
        self.assertEqual(user.last_name, 'Lee')
        self.assertEqual(user.username, '@boblee')
        self.assertEqual(user.email, 'boblee@example.org')
        self.assertEqual(user.bio, "Bob Lee's Personal Spending Tracker")

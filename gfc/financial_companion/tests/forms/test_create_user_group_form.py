from django import forms
from django.urls import reverse
from typing import Any
from .test_form_base import FormTestCase
from financial_companion.forms import UserGroupForm
from financial_companion.models import UserGroup, User


class CreateUserGroupFormTestCase(FormTestCase):
    """Unit tests of the create user group form"""

    def setUp(self):
        self.test_user: User = User.objects.get(username='@johndoe')
        self.url: str = reverse('create_user_group')
        self.form_input: dict[str, Any] = {
            'name': 'Financial Club',
            'description': 'We are the best financial club',
        }

    def test_valid_create_user_group_form(self):
        form: UserGroupForm = UserGroupForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form: UserGroupForm = UserGroupForm()
        self._assert_form_has_necessary_fields(
            form,
            'name',
            'description',
        )
        description_widget: forms.Textarea = form.fields['description'].widget
        self.assertTrue(isinstance(description_widget, forms.Textarea))

    def test_form_must_save_correctly(self):
        form: UserGroupForm = UserGroupForm(data=self.form_input)
        before_count: int = UserGroup.objects.count()
        user_group: UserGroup = form.save(self.test_user)
        after_count: int = UserGroup.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(user_group.owner_email, self.test_user.email)
        self.assertEqual(user_group.name, 'Financial Club')
        self.assertEqual(
            user_group.description,
            'We are the best financial club')

    def test_form_updates_correctly(self):
        user_group: UserGroup = UserGroup.objects.get(id=1)
        form: UserGroupForm = UserGroupForm(data=self.form_input)
        before_count: int = UserGroup.objects.count()
        current_user_group: UserGroup = form.save(
            current_user=self.test_user,
            instance=user_group)
        after_count: int = UserGroup.objects.count()
        self.assertEqual(current_user_group.name, 'Financial Club')
        self.assertEqual(
            current_user_group.description,
            'We are the best financial club')
        self.assertEqual(before_count, after_count)

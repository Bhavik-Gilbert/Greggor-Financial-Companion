from django.db import IntegrityError
from .test_form_base import FormTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import CategoryTarget, User, Category
from decimal import Decimal
from typing import Any


class CreateTargetFormTestCase(FormTestCase):
    """Unit tests of the create target form"""

    def setUp(self):
        self.test_user: User = User.objects.get(username='@johndoe')
        self.test_category: Category = Category.objects.get(id=1)
        self.form_input: dict[str, Any] = {
            'target_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_valid_create_category_target_form(self):
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form: TargetForm = TargetForm(
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self._assert_form_has_necessary_fields(
            form,
            'target_type',
            'timespan',
            'amount',
            'currency'
        )

    def test_amount_can_be_more_than_zero(self):
        self.form_input['amount']: Decimal = Decimal('0.01')
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertTrue(form.is_valid())

    def test_target_type_can_not_be_blank(self):
        self.form_input['target_type']: str = None
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_target_type_can_not_be_invalid_option(self):
        self.form_input['target_type']: str = 'Invalid'
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_currency_can_not_be_blank(self):
        self.form_input['currency']: str = None
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_currency_can_not_be_invalid_option(self):
        self.form_input['currency']: str = 'Invalid'
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_timespan_can_not_be_blank(self):
        self.form_input['timespan']: str = None
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_timespan_can_not_be_invalid_option(self):
        self.form_input['timespan']: str = 'Invalid'
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_amount_can_not_be_blank(self):
        self.form_input['amount']: str = None
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_amount_can_not_be_zero_or_less(self):
        self.form_input['amount']: Decimal = Decimal('0.00')
        form: TargetForm = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form: TargetForm = TargetForm(
            data=self.form_input,
            foreign_key=self.test_category,
            form_type=CategoryTarget)
        before_count: int = CategoryTarget.objects.count()
        category_target: CategoryTarget = form.save()
        after_count: int = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(category_target.timespan, 'month')
        self.assertEqual(category_target.target_type, 'income')
        self.assertEqual(category_target.currency, 'USD')
        self.assertEqual(category_target.amount, 200)

    def test_form_updates_correctly(self):
        category_target: CategoryTarget = CategoryTarget.objects.get(id=1)
        form: TargetForm = TargetForm(
            instance=category_target,
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        before_count: int = CategoryTarget.objects.count()
        current_category_target: CategoryTarget = form.save()
        after_count: int = CategoryTarget.objects.count()
        self.assertEqual(current_category_target.timespan, 'month')
        self.assertEqual(current_category_target.target_type, 'income')

    def test_form_thorws_error_when_updating_invalid_data(self):
        category_target: CategoryTarget = CategoryTarget.objects.get(id=1)
        self.other_category_target: CategoryTarget = CategoryTarget.objects.get(
            id=2)
        self.form_input: dict[str, Any] = {
            'target_type': self.other_category_target.target_type,
            'timespan': self.other_category_target.timespan,
            'amount': 200,
            'currency': 'USD'
        }
        form: TargetForm = TargetForm(
            instance=category_target,
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        with self.assertRaises(IntegrityError):
            self.assertFalse(form.save())

    def test_target_must_be_unique_for_a_category(self):
        self.test_category_target: CategoryTarget = CategoryTarget.objects.get(
            id=1)
        self.form_input: dict[str, Any] = {
            'target_type': self.test_category_target.target_type,
            'timespan': self.test_category_target.timespan,
            'amount': 200,
            'currency': 'USD'
        }
        form: TargetForm = TargetForm(
            data=self.form_input,
            foreign_key=self.test_category,
            form_type=CategoryTarget)
        with self.assertRaises(IntegrityError):
            self.assertFalse(form.save())

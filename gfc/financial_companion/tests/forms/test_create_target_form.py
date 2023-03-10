from django import forms
from django.urls import reverse
from django.db import IntegrityError
from .test_form_base import FormTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import CategoryTarget, User, Category
from decimal import Decimal


class CreateTargetFormTestCase(FormTestCase):
    """Unit tests of the create target form"""

    def setUp(self):
        self.test_user = User.objects.get(username='@johndoe')
        self.test_category = Category.objects.get(id=1)
        self.form_input = {
            'target_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_valid_create_category_target_form(self):
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = TargetForm(
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
        self.form_input['amount'] = Decimal('0.01')
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertTrue(form.is_valid())

    def test_target_type_can_not_be_blank(self):
        self.form_input['target_type'] = None
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_target_type_can_not_be_invalid_option(self):
        self.form_input['target_type'] = 'Invalid'
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_currency_can_not_be_blank(self):
        self.form_input['currency'] = None
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_currency_can_not_be_invalid_option(self):
        self.form_input['currency'] = 'Invalid'
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_timespan_can_not_be_blank(self):
        self.form_input['timespan'] = None
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_timespan_can_not_be_invalid_option(self):
        self.form_input['timespan'] = 'Invalid'
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_amount_can_not_be_blank(self):
        self.form_input['amount'] = None
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_amount_can_not_be_zero_or_less(self):
        self.form_input['amount'] = Decimal('0.00')
        form = TargetForm(
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = TargetForm(
            data=self.form_input,
            foreign_key=self.test_category,
            form_type=CategoryTarget)
        before_count = CategoryTarget.objects.count()
        category_target = form.save()
        after_count = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(category_target.timespan, 'month')
        self.assertEqual(category_target.target_type, 'income')
        self.assertEqual(category_target.currency, 'USD')
        self.assertEqual(category_target.amount, 200)

    def test_form_updates_correctly(self):
        category_target = CategoryTarget.objects.get(id=1)
        form = TargetForm(
            instance=category_target,
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        before_count = CategoryTarget.objects.count()
        current_category_target = form.save()
        after_count = CategoryTarget.objects.count()
        self.assertEqual(current_category_target.timespan, 'month')
        self.assertEqual(current_category_target.target_type, 'income')

    def test_form_thorws_error_when_updating_invalid_data(self):
        category_target = CategoryTarget.objects.get(id=1)
        self.other_category_target = CategoryTarget.objects.get(id=2)
        self.form_input = {
            'target_type': self.other_category_target.target_type,
            'timespan': self.other_category_target.timespan,
            'amount': 200,
            'currency': 'USD'
        }
        form = TargetForm(
            instance=category_target,
            data=self.form_input,
            form_type=CategoryTarget,
            foreign_key=self.test_category)
        with self.assertRaises(IntegrityError):
            self.assertFalse(form.save())

    def test_target_must_be_unique_for_a_category(self):
        self.test_category_target = CategoryTarget.objects.get(id=1)
        self.form_input = {
            'target_type': self.test_category_target.target_type,
            'timespan': self.test_category_target.timespan,
            'amount': 200,
            'currency': 'USD'
        }
        form = TargetForm(
            data=self.form_input,
            foreign_key=self.test_category,
            form_type=CategoryTarget)
        with self.assertRaises(IntegrityError):
            self.assertFalse(form.save())

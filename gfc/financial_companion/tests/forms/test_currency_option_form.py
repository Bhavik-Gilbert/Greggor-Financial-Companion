from financial_companion.forms import CurrencyOptionsForm
from .test_form_base import FormTestCase
from financial_companion.helpers import CurrencyType
from typing import Any


class CurrencyOptionFormTestCase(FormTestCase):
    """Unit tests of the currency option form"""

    def setUp(self):
        super().setUp()
        self.form_input: dict[str, Any] = {
            "currency_choice": CurrencyType.GBP
        }

    def test_form_contains_required_fields(self):
        form: CurrencyOptionsForm = CurrencyOptionsForm()
        self._assert_form_has_necessary_fields(
            form,
            'currency_choice'
        )

    def test_valid_currencyspan_dropdown_form(self):
        form: CurrencyOptionsForm = CurrencyOptionsForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_currency_choice_can_not_be_empty(self):
        self.form_input['currency_choice']: str = ''
        form: CurrencyOptionsForm = CurrencyOptionsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_get_currency(self):
        form: CurrencyOptionsForm = CurrencyOptionsForm(data=self.form_input)
        self.assertEqual(CurrencyType.GBP, form.get_currency())

from financial_companion.forms import TimespanCurrencyOptionsForm
from .test_form_base import FormTestCase
from financial_companion.helpers import Timespan, CurrencyType
from typing import Any


class TimespanCurrencyOptionFormTestCase(FormTestCase):
    """Unit tests of the timespan currency option form"""

    def setUp(self):
        self.form_input: dict[str, Any] = {
            "time_choice": Timespan.DAY,
            "currency_choice": CurrencyType.GBP
        }

    def test_form_contains_required_fields(self):
        form: TimespanCurrencyOptionsForm = TimespanCurrencyOptionsForm()
        self._assert_form_has_necessary_fields(
            form,
            'time_choice',
            'currency_choice'
        )

    def test_valid_timespan_dropdown_form(self):
        form: TimespanCurrencyOptionsForm = TimespanCurrencyOptionsForm(data=self.form_input)
        self.assertTrue(form.is_valid())
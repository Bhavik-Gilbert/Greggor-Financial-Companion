from financial_companion.forms import TimespanOptionsForm
from .test_form_base import FormTestCase
from django.test import TestCase
from typing import Any


class TimeSpanDropDownFormTestCase(FormTestCase):
    """Unit tests of the time span drop down form"""

    def setUp(self):
        self.form_input: dict[str, Any] = {
            "time_choice": "day"
        }

    def test_form_contains_required_fields(self):
        form: TimespanOptionsForm = TimespanOptionsForm()
        self._assert_form_has_necessary_fields(
            form,
            'time_choice'
        )

    def test_valid_timespan_dropdown_form(self):
        form: TimespanOptionsForm = TimespanOptionsForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_time_choice_can_not_be_empty(self):
        self.form_input['time_choice']: str = ''
        form: TimespanOptionsForm = TimespanOptionsForm(data=self.form_input)
        self.assertFalse(form.is_valid())

from financial_companion.forms import TimespanOptionsForm
from .test_form_base import FormTestCase
from financial_companion.helpers import Timespan
from typing import Any


class TimespanOptionFormTestCase(FormTestCase):
    """Unit tests of the timespan option form"""

    def setUp(self):
        self.form_input: dict[str, Any] = {
            "time_choice": Timespan.DAY
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
    
    def test_get_timespan(self):
        form: TimespanOptionsForm = TimespanOptionsForm(data=self.form_input)
        self.assertEqual(Timespan.DAY, form.get_timespan())

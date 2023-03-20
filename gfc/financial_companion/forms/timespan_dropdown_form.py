from django import forms
from ..helpers import Timespan


class TimespanOptionsForm(forms.Form):
    time_choice: forms.ChoiceField = forms.ChoiceField(
        choices=Timespan.choices)

    def get_choice(self):
        """Returns chosen time span"""
        self.full_clean()
        return self.cleaned_data["time_choice"]

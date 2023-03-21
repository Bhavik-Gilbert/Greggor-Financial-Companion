from django import forms
from ..helpers import Timespan


class TimespanOptionsForm(forms.Form):
    """Form to select timespan"""
    time_choice: forms.ChoiceField = forms.ChoiceField(
        choices=Timespan.choices)

    def get_choice(self) -> Timespan:
        """Returns chosen time span"""
        self.full_clean()
        return self.cleaned_data["time_choice"]

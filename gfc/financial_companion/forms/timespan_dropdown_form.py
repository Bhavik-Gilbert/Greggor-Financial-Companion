from django import forms
from ..helpers import Timespan


class TimespanOptionsForm(forms.Form):
    time_choice: forms.ChoiceField = forms.ChoiceField(
        choices=Timespan.choices)

    def get_choice(self):
        self.full_clean()
        return self.cleaned_data["time_choice"]

from django import forms
from ..helpers import Timespan, CurrencyType


class TimespanOptionsForm(forms.Form):
    """Form to select timespan"""
    time_choice: forms.ChoiceField = forms.ChoiceField(
        choices=Timespan.choices)

    def get_timespan(self) -> Timespan:
        """Returns chosen time span"""
        self.full_clean()
        return self.cleaned_data["time_choice"]


class CurrencyOptionsForm(forms.Form):
    """Form to select currency"""
    currency_choice: forms.ChoiceField = forms.ChoiceField(
        choices=CurrencyType.choices)

    def get_currency(self) -> CurrencyType:
        """Returns chosen currency"""
        self.full_clean()
        return self.cleaned_data["currency_choice"]


class TimespanCurrencyOptionsForm(CurrencyOptionsForm, TimespanOptionsForm):
    pass

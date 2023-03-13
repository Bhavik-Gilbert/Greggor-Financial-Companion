from django import forms
from ..helpers import Timespan, TransactionType, TargetType


class TargetFilterForm(forms.Form):
    time = forms.ChoiceField(choices=[('','-----')] + Timespan.choices, required=False)
    income_or_expense = forms.ChoiceField(choices=[('','-----')] + TransactionType.choices, required=False)
    target_type= forms.ChoiceField(choices=[('','-----')] + TargetType.choices, required=False)

    def get_time(self):
        self.full_clean()
        return self.cleaned_data["time"]

    def get_income_or_expense(self):
        self.full_clean()
        return self.cleaned_data["income_or_expense"]

    def get_target_type(self):
        self.full_clean()
        return self.cleaned_data["target_type"]

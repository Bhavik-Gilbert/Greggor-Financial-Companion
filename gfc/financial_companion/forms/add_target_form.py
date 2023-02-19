from django import forms
from financial_companion.models import CategoryTarget, Category, AbstractTarget
from ..helpers import Timespan, TransactionType, CurrencyType


class TargetForm(forms.Form):
    """Form to add a target"""

    def __init__(self, *args, **kwargs) -> None:
        self.foreign_key: Model = kwargs.get("foreign_key")
        kwargs.pop("foreign_key", None)
        self.instance: Model = kwargs.get("instance")
        kwargs.pop("instance", None)
        super(TargetForm, self).__init__(*args, **kwargs)
        if (self.instance):
            self.fields['transaction_type'].initial = self.instance.transaction_type
            self.fields['timespan'].initial = self.instance.timespan
            self.fields['amount'].initial = self.instance.amount
            self.fields['currency'].initial = self.instance.currency

    transaction_type = forms.ChoiceField(choices=TransactionType.choices)
    timespan = forms.ChoiceField(choices=Timespan.choices)
    amount = forms.DecimalField(decimal_places=2, max_digits=15)
    currency = forms.ChoiceField(choices=CurrencyType.choices)

    def save(self, target_attribute: str, Target: AbstractTarget = None):
        self.full_clean()
        if self.instance is None:
            target = Target()
            setattr(target, target_attribute, self.foreign_key)
        else:
            target: AbstractTarget = self.instance

        target.transaction_type = self.cleaned_data.get('transaction_type')
        target.timespan = self.cleaned_data.get('timespan')
        target.amount = self.cleaned_data.get('amount')
        target.currency = self.cleaned_data.get('currency')
        target.save()

        return target

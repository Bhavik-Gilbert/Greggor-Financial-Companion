from django import forms
from financial_companion.models import CategoryTarget, Category, AbstractTarget
from ..helpers import Timespan, TransactionType, CurrencyType
from django.core.exceptions import ValidationError
import re

class TargetForm(forms.Form):
    """Form to add a target"""

    def __init__(self, *args, **kwargs) -> None:
        self.foreign_key: AbstractTarget = kwargs.get("foreign_key")
        kwargs.pop("foreign_key", None)
        self.instance: AbstractTarget = kwargs.get("instance")
        kwargs.pop("instance", None)
        self.form_type: AbstractTarget = kwargs.get("form_type")
        kwargs.pop("form_type", None)
        self.foreign_key_name = re.split(r"\B([A-Z])", self.form_type.__name__)[0]
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
    
    def clean(self):
        super().clean()
        filter_type_dict = {self.foreign_key_name.lower(): self.foreign_key}
        check_unique_together = self.form_type.objects.filter(
            timespan=self.cleaned_data.get('timespan'), 
            **filter_type_dict,
            transaction_type=self.cleaned_data.get('transaction_type')
        )

        if self.instance is None: 
            if len(check_unique_together) > 0:
                self.add_error('timespan', ValidationError(f"This target can not be created as a target with the same timespan, transaction type and {self.foreign_key.__class__.__name__.lower()} exists"))
        else:
            if any(check_unique_target_object != self.instance for check_unique_target_object in check_unique_together):
                self.add_error('timespan', ValidationError(f"This target can not be created as a target with the same timespan, transaction type and {self.foreign_key.__class__.__name__.lower()} exists"))



    def save(self):
        self.full_clean()
        if self.instance is None:
            target = self.form_type()
            setattr(target, self.foreign_key_name.lower(), self.foreign_key)
        else:
            target: AbstractTarget = self.instance

        target.transaction_type = self.cleaned_data.get('transaction_type')
        target.timespan = self.cleaned_data.get('timespan')
        target.amount = self.cleaned_data.get('amount')
        target.currency = self.cleaned_data.get('currency')
        target.save()
        


        return target



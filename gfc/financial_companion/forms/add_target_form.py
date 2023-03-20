from django import forms
from financial_companion.models import AbstractTarget
from django.db import models
from ..helpers import Timespan, TransactionType, CurrencyType
from django.core.exceptions import ValidationError
import re
from decimal import Decimal



class TargetForm(forms.Form):
    """Form to add a target"""

    def __init__(self, *args, **kwargs) -> None:
        self.foreign_key: models.Model = kwargs.get("foreign_key")
        kwargs.pop("foreign_key", None)
        self.instance: AbstractTarget = kwargs.get("instance")
        kwargs.pop("instance", None)
        self.form_type: AbstractTarget = kwargs.get("form_type")
        kwargs.pop("form_type", None)
        self.foreign_key_name: str = re.split(
            r"\B([A-Z])", self.form_type.__name__)[0]
        super(TargetForm, self).__init__(*args, **kwargs)

        if (self.instance):
            self.fields['target_type'].initial: str = self.instance.target_type
            self.fields['timespan'].initial: str = self.instance.timespan
            self.fields['amount'].initial: Decimal = self.instance.amount
            self.fields['currency'].initial: str = self.instance.currency

    target_type: forms.ChoiceField = forms.ChoiceField(
        choices=TransactionType.choices)
    timespan: forms.ChoiceField = forms.ChoiceField(choices=Timespan.choices)
    amount: forms.DecimalField = forms.DecimalField(
        decimal_places=2, max_digits=15)
    currency: forms.ChoiceField = forms.ChoiceField(
        choices=CurrencyType.choices)

    def clean(self):
        super().clean()
        filter_type_dict: dict[str, models.Model] = {
            self.foreign_key_name.lower(): self.foreign_key}
        check_unique_together: models.QuerySet[AbstractTarget] = self.form_type.objects.filter(
            timespan=self.cleaned_data.get('timespan'),
            **filter_type_dict,
            target_type=self.cleaned_data.get('target_type')
        )

        if self.cleaned_data.get('amount') is not None:
            if self.cleaned_data.get('amount') <= Decimal('0.00'):
                self.add_error('amount', ValidationError(
                    "Amount cannot be a value under 0.01")
                )

        if self.instance is None:
            if len(check_unique_together) > 0:
                self.add_error('timespan', ValidationError(
                    f"This target can not be created as a target with the same timespan, transaction type and {self.foreign_key.__class__.__name__.lower()} exists"))
        else:
            if any(check_unique_target_object !=
                   self.instance for check_unique_target_object in check_unique_together):
                self.add_error('timespan', ValidationError(
                    f"This target can not be created as a target with the same timespan, transaction type and {self.foreign_key.__class__.__name__.lower()} exists"))

    def save(self) -> AbstractTarget:
        self.full_clean()
        if self.instance is None:
            target: AbstractTarget = self.form_type()
            setattr(target, self.foreign_key_name.lower(), self.foreign_key)
        else:
            target: AbstractTarget = self.instance

        target.target_type: str = self.cleaned_data.get('target_type')
        target.timespan: Timespan = self.cleaned_data.get('timespan')
        target.amount: float = self.cleaned_data.get('amount')
        target.currency: str = self.cleaned_data.get('currency')
        target.save()

        return target

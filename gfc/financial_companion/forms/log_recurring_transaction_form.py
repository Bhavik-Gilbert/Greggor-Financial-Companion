from django import forms
from django.core.validators import RegexValidator
from financial_companion.models import RecurringTransaction
from typing import Any

class RecurringTransactionForm(forms.ModelForm):
    """Form to log recurring transactions"""

    class Meta:
        model: RecurringTransaction = RecurringTransaction
        fields: list[str] = [
            'title',
            'image',
            'category',
            'amount',
            'currency',
            'sender_account',
            'reciever_account',
            'start_date',
            'interval',
            'end_date']
        widgets: dict[str, forms.Textarea] = {'description': forms.Textarea()}

    def clean(self):
        """Generate messages for any errors"""
        super.clean()

        if self.end_date < self.start_date:
            self.add_error("End date must be after start date.")

    def save(self, instance=None) -> RecurringTransaction:
        """Record the inputted transaction"""
        super.save()

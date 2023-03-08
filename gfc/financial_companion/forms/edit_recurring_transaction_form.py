from django import forms
from django.core.validators import FileExtensionValidator
from financial_companion.models import Transaction, Account, Category, PotAccount, RecurringTransaction
from datetime import datetime
from django.utils.timezone import make_aware
from typing import Any
from decimal import Decimal
from django.forms.widgets import DateTimeInput


class EditRecurringTransactionForm(forms.ModelForm):
    """Form to add a new recurring transaction"""

    def __init__(self, user, *args, **kwargs):
        super(EditRecurringTransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].label_from_instance = self.label_from_instance
        self.fields['sender_account'].label_from_instance = self.label_from_instance
        self.fields['receiver_account'].label_from_instance = self.label_from_instance
        self.user = user

    def label_from_instance(self, obj):
        return obj.name

    class Meta:
        model = RecurringTransaction
        fields = [
            'title',
            'description',
            'image',
            'category',
            'amount',
            'currency',
            'sender_account',
            'receiver_account',
            'interval',
            'end_date']
        widgets = {
            'end_date': DateTimeInput(attrs={ 'type': 'datetime-local', 'min':  datetime.now().strftime("%Y-%m-%dT%H:%M") }),
        }

    def save(self, instance: RecurringTransaction = None) -> RecurringTransaction:
        """Create a new transaction."""
        super().save(commit=False)
        transaction: RecurringTransaction = instance
        transaction.title = self.cleaned_data.get('title')
        transaction.description = self.cleaned_data.get('description')
        transaction.image = self.cleaned_data.get('image')
        transaction.category = self.cleaned_data.get('category')
        transaction.amount = self.cleaned_data.get('amount')
        transaction.currency = self.cleaned_data.get('currency')
        transaction.sender_account = self.cleaned_data.get(
            'sender_account')
        transaction.receiver_account = self.cleaned_data.get(
            'receiver_account')
        transaction.interval= self.cleaned_data.get('interval'),    
        transaction.end_date = self.cleaned_data.get('end_date')
        transaction.save()
        return transaction

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        sender_account = self.cleaned_data.get('sender_account')
        receiver_account = self.cleaned_data.get('receiver_account')
        start_date = self.start_date
        end_date = self.cleaned_data.get('end_date')
        users_accounts = PotAccount.objects.filter(user=self.user)
        ids = []
        for account in users_accounts:
            ids.append(account.id)
        if sender_account == receiver_account:
            self.add_error(
                'receiver_account',
                'The sender and receiver accounts cannot be the same.')
        elif not ((sender_account.id in ids) or (receiver_account.id in ids)):
            self.add_error(
                'sender_account',
                'Neither the sender or reciever are one of your accounts')
            self.add_error(
                'receiver_account',
                'Neither the sender or reciever are one of your accounts')
        if start_date > end_date:
            self.add_error(
                'end_date',
                'End date cannot precede start date.')
        
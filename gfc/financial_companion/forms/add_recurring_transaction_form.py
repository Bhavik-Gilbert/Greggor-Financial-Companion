from datetime import date
from django import forms
from financial_companion.models import PotAccount, RecurringTransaction, User, Category, Account
from typing import Any
from django.forms.widgets import DateInput
from django.db.models import QuerySet



class AddRecurringTransactionForm(forms.ModelForm):
    """Form to add a new recurring transaction"""

    def __init__(self, user, *args, **kwargs):
        super(AddRecurringTransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset: QuerySet[Account] = Category.objects.filter(
            user=user.id)
        self.fields['sender_account'].queryset: QuerySet[Account] = Account.objects.filter(
            user=user.id)
        self.fields['receiver_account'].queryset: QuerySet[Account] = Account.objects.filter(
            user=user.id)
        self.fields['category'].label_from_instance: Any = self.label_from_instance
        self.fields['sender_account'].label_from_instance: Any = self.label_from_instance
        self.fields['receiver_account'].label_from_instance: Any = self.label_from_instance
        self.user: User = user

    def label_from_instance(self, obj) -> str:
        return obj.name

    class Meta:
        model: RecurringTransaction = RecurringTransaction
        fields: list[str] = [
            'title',
            'description',
            'image',
            'category',
            'amount',
            'currency',
            'sender_account',
            'receiver_account',
            'interval',
            'start_date',
            'end_date']
        widgets: dict[str, DateInput] = {
            'start_date': DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}),
            'end_date': DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}),
        }

    def save(self, instance: RecurringTransaction = None) -> RecurringTransaction:
        """Create a new transaction."""
        super().save(commit=False)
        if instance is None:
            recurring_transaction: RecurringTransaction = RecurringTransaction.objects.create(
                title=self.cleaned_data.get('title'),
                description=self.cleaned_data.get('description'),
                image=self.cleaned_data.get('image'),
                category=self.cleaned_data.get('category'),
                amount=self.cleaned_data.get('amount'),
                currency=self.cleaned_data.get('currency'),
                sender_account=self.cleaned_data.get('sender_account'),
                receiver_account=self.cleaned_data.get('receiver_account'),
                interval=self.cleaned_data.get('interval'),
                start_date=self.cleaned_data.get('start_date'),
                end_date=self.cleaned_data.get('end_date')
            )
        else:
            recurring_transaction: RecurringTransaction = super().save(commit=True)
        return recurring_transaction

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        sender_account: Account = self.cleaned_data.get('sender_account')
        receiver_account: Account = self.cleaned_data.get('receiver_account')
        start_date: date  = self.cleaned_data.get('start_date')
        end_date: date = self.cleaned_data.get('end_date')
        users_accounts: PotAccount = PotAccount.objects.filter(user=self.user)
        ids: list[Account] = []
        for account in users_accounts:
            ids.append(account.id)
        if sender_account == receiver_account:
            self.add_error(
                'receiver_account',
                'The sender and receiver accounts cannot be the same.')
        elif not ((sender_account.id in ids) or (receiver_account.id in ids)):
            self.add_error(
                'sender_account',
                'Neither the sender or reciever are accounts with a balance to track.')
            self.add_error(
                'receiver_account',
                'Neither the sender or reciever are accounts with a balance to track.')
        if start_date > end_date:
            self.add_error(
                'end_date',
                'End date cannot precede start date.')

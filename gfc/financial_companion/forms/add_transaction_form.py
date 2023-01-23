from django import forms
from financial_companion.models import Transaction

class AddTransactionForm(forms.ModelForm):
    """Form to add a new transaction"""

    class Meta:
        model = Transaction
        fields = ['title', 'description', 'image', 'category', 'amount', 'currency', 'sender_account', 'receiver_account']

    def save(self):
        """Create a new transaction."""

        super().save(commit=False)
        transaction = Transaction.objects.create_transaction(
            self.cleaned_data.get('title'),
            description=self.cleaned_data.get('description'),
            image=self.cleaned_data.get('image'),
            category=self.cleaned_data.get('category'),
            amount=self.cleaned_data.get('amount'),
            currency=self.cleaned_data.get('currency'),
            sender_account=self.cleaned_data.get('sender_account'),
            receiver_account=self.cleaned_data.get('receiver_account'),
        )
        return transaction

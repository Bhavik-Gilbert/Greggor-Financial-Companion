from django import forms
from financial_companion.models import Transaction, Account, Category

class AddTransactionForm(forms.ModelForm):
    """Form to add a new transaction"""

    class Meta:
        model = Transaction
        fields = ['title','description', 'image', 'category', 'amount', 'currency','sender_account', 'receiver_account']

    def save(self, instance: Transaction = None) -> Transaction:
        """Create a new transaction."""
        super().save(commit=False)
        if instance is None:
            print("sender")
            print(self.cleaned_data.get('sender_account'))
            transaction = Transaction.objects.create(
                title= self.cleaned_data.get('title'),
                description=self.cleaned_data.get('description'),
                image=self.cleaned_data.get('image'),
                category=self.cleaned_data.get('category'),
                amount=self.cleaned_data.get('amount'),
                currency=self.cleaned_data.get('currency'),
                sender_account = self.cleaned_data.get('sender_account'),
                receiver_account=self.cleaned_data.get('receiver_account')
            )
            print(transaction.sender_account.name)
        else:
            transaction: Transaction = instance
            transaction.title  = self.cleaned_data.get('title')
            transaction.description = self.cleaned_data.get('description')
            transaction.image = self.cleaned_data.get('image')
            transaction.category = self.cleaned_data.get('category')
            transaction.amount = self.cleaned_data.get('amount')
            transaction.currency = self.cleaned_data.get('currency')
            transaction.sender_account = self.cleaned_data.get('sender_account')
            transaction.receiver_account = self.cleaned_data.get('receiver_account')
            transaction.save()
        return transaction

    # def clean(self):
    #     """Clean the data and generate messages for any errors."""
    #
    #     super().clean()
    #     new_password = self.cleaned_data.get('new_password')
    #     password_confirmation = self.cleaned_data.get('password_confirmation')
    #     if new_password != password_confirmation:
    #         self.add_error('password_confirmation', 'Confirmation does not match password.')

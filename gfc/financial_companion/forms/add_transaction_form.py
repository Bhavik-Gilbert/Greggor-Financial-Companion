from django import forms
from financial_companion.models import Transaction, Account, Category

class AddTransactionForm(forms.ModelForm):
    """Form to add a new transaction"""

    def __init__(self, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].label_from_instance = self.label_from_instance
        self.fields['sender_account'].label_from_instance = self.label_from_instance
        self.fields['receiver_account'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return obj.name

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

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        sender_account = self.cleaned_data.get('sender_account')
        receiver_account = self.cleaned_data.get('receiver_account')
        if sender_account == receiver_account:
            self.add_error('receiver_account', 'The sender and receiver accounts cannot be the same.')

        # if not(hasattr(sender_account, "user") and hasattr(receiver_account, "user")):
        #     self.add_error('sender_account', 'Neither the sender or reciever are one of your accounts.')

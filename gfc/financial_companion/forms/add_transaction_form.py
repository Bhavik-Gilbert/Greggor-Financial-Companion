from django import forms
from django.core.validators import FileExtensionValidator
from financial_companion.models import Transaction, Account, Category
from financial_companion.helpers import ParseStatementPDF


class AddTransactionForm(forms.ModelForm):
    """Form to add a new transaction"""

    class Meta:
        model = Transaction
        fields = [
            'title',
            'description',
            'image',
            'category',
            'amount',
            'currency',
            'sender_account',
            'receiver_account']

    def save(self, instance: Transaction = None) -> Transaction:
        """Create a new transaction."""
        super().save(commit=False)
        if instance is None:
            transaction = Transaction.objects.create(
                title=self.cleaned_data.get('title'),
                description=self.cleaned_data.get('description'),
                image=self.cleaned_data.get('image'),
                category=self.cleaned_data.get('category'),
                amount=self.cleaned_data.get('amount'),
                currency=self.cleaned_data.get('currency'),
                sender_account=self.cleaned_data.get('sender_account'),
                receiver_account=self.cleaned_data.get('receiver_account')
            )
        else:
            transaction: Transaction = instance
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
            transaction.save()
        return transaction

class AddTransactionsViaBankStatementForm(forms.Form):
    """Form to upload bank statement to add new transactions"""

    bank_statement: forms.FileField = forms.FileField(
        validators=[FileExtensionValidator(['pdf'])]
    )

    def save(self):
        bank_statement = self.cleaned_data["bank_statement"]
        bank_statement_file_path: str = bank_statement.temporary_file_path()
        bank_statement_parser: ParseStatementPDF = ParseStatementPDF()

        print(bank_statement_file_path)

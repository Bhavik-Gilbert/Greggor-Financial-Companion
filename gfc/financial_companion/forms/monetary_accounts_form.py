from django import forms
from financial_companion.models import PotAccount, BankAccount
from financial_companion.helpers import MonetaryAccountType

def MonetaryAccountForm(*args, **kwargs):
    """Form to create monetary account"""
    form_type: int = kwargs.get("form_type")
    kwargs.pop("form_type", None)
    if form_type == MonetaryAccountType.BANK:
        return BankAccountForm(*args, **kwargs)
    else:
        return PotAccountForm(*args, **kwargs)

class PotAccountForm(forms.ModelForm):
    """Form to create pot account"""

    def __init__(self, *args, **kwargs):
        self.user: int = kwargs.get("user")
        kwargs.pop("user", None)
        super(PotAccountForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PotAccount
        fields = ["name", "description", "balance", "currency"]
        widgets = {"description": forms.Textarea()}
    
    def save(self, instance: PotAccount = None):
        super().save(commit=False)

        if instance is None:
            monetary_account = PotAccount.objects.create(
                name = self.cleaned_data.get("name"),
                description = self.cleaned_data.get("description"),
                balance = self.cleaned_data.get("balance"),
                currency = self.cleaned_data.get("currency"),
                user_id = self.user
            )
        else:
            monetary_account = instance
            monetary_account.name = self.cleaned_data.get("name")
            monetary_account.description = self.cleaned_data.get("description")
            monetary_account.balance = self.cleaned_data.get("balance")
            monetary_account.currency = self.cleaned_data.get("currency")
            monetary_account.user_id = self.user
            monetary_account.save()
        
        return monetary_account

class BankAccountForm(forms.ModelForm):
    """Form to create bank account"""

    def __init__(self, *args, **kwargs):
        self.user: int = kwargs.get("user")
        kwargs.pop("user", None)
        super(BankAccountForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BankAccount
        fields = ["name", "description", "balance", "currency", "bank_name", "account_number", "sort_code", "iban", "interest_rate"]
        widgets = {"description": forms.Textarea()}
    
    def save(self, instance: BankAccount = None):
        super().save(commit=False)

        if instance is None:
            monetary_account = BankAccount.objects.create(
                name = self.cleaned_data.get("name"),
                description = self.cleaned_data.get("description"),
                balance = self.cleaned_data.get("balance"),
                currency = self.cleaned_data.get("currency"),
                bank_name = self.cleaned_data.get("bank_name"),
                sort_code = self.cleaned_data.get("sort_code"),
                account_number = self.cleaned_data.get("account_number"),
                iban = self.cleaned_data.get("iban"),
                interest_rate = self.cleaned_data.get("interest_rate"),
                user_id = self.user
            )
        else:
            monetary_account = instance
            monetary_account.name = self.cleaned_data.get("name")
            monetary_account.description = self.cleaned_data.get("description")
            monetary_account.balance = self.cleaned_data.get("balance")
            monetary_account.currency = self.cleaned_data.get("currency")
            monetary_account.bank_name = self.cleaned_data.get("bank_name")
            monetary_account.sort_code = self.cleaned_data.get("sort_code")
            monetary_account.account_number = self.cleaned_data.get("account_number")
            monetary_account.iba = self.cleaned_data.get("iban")
            monetary_account.interest_rate = self.cleaned_data.get("interest_rate")
            monetary_account.user_id = self.user
            monetary_account.save()
        
        return monetary_account
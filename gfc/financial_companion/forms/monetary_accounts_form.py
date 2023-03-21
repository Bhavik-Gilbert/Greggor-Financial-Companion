from django import forms
from financial_companion.models import PotAccount, BankAccount, User, Account
from financial_companion.helpers import AccountType
from decimal import Decimal
from typing import Any


def MonetaryAccountForm(*args, **kwargs) -> forms.ModelForm:
    """Form to create monetary account"""
    form_type: AccountType = kwargs.get("form_type")
    kwargs.pop("form_type", None)
    if form_type == AccountType.BANK:
        return BankAccountForm(*args, **kwargs)
    elif form_type == AccountType.POT:
        return PotAccountForm(*args, **kwargs)
    else:
        return RegularAccountForm(*args, **kwargs)


class RegularAccountForm(forms.ModelForm):
    """form to create accounts"""

    def __init__(self, *args, **kwargs) -> None:
        self.user: User = kwargs.get("user")
        kwargs.pop("user", None)
        super(RegularAccountForm, self).__init__(*args, **kwargs)

    class Meta:
        model: Account = Account
        fields: list[str] = ["name", "description"]
        widgets: dict[str, Any] = {"description": forms.Textarea()}

    def save(self, instance: Account = None) -> Account:
        """Create a new monetary account."""
        super().save(commit=False)

        if instance is None:
            regular_account: Account = Account.objects.create(
                name=self.cleaned_data.get("name"),
                description=self.cleaned_data.get("description"),
                user=self.user
            )

        else:
            regular_account: Account = instance
            regular_account.name: str = self.cleaned_data.get("name")
            regular_account.description: str = self.cleaned_data.get(
                "description")
            regular_account.user: User = self.user
            regular_account.save()

        return regular_account


class PotAccountForm(forms.ModelForm):
    """Form to create pot account"""

    def __init__(self, *args, **kwargs) -> None:
        self.user: User = kwargs.get("user")
        kwargs.pop("user", None)
        super(PotAccountForm, self).__init__(*args, **kwargs)

    class Meta:
        model: PotAccount = PotAccount
        fields: list[str] = ["name", "description", "balance", "currency"]
        widgets: dict[str, Any] = {"description": forms.Textarea()}

    def save(self, instance: PotAccount = None) -> PotAccount:
        """Create a new pot account."""
        super().save(commit=False)

        if instance is None:
            monetary_account: PotAccount = PotAccount.objects.create(
                name=self.cleaned_data.get("name"),
                description=self.cleaned_data.get("description"),
                balance=self.cleaned_data.get("balance"),
                currency=self.cleaned_data.get("currency"),
                user=self.user
            )
        else:
            monetary_account: PotAccount = instance
            monetary_account.name: str = self.cleaned_data.get("name")
            monetary_account.description: str = self.cleaned_data.get(
                "description")
            monetary_account.balance: Decimal = self.cleaned_data.get(
                "balance")
            monetary_account.currency: str = self.cleaned_data.get("currency")
            monetary_account.user: User = self.user
            monetary_account.save()

        return monetary_account


class BankAccountForm(forms.ModelForm):
    """Form to create bank account"""

    def __init__(self, *args, **kwargs) -> None:
        self.user: User = kwargs.get("user")
        kwargs.pop("user", None)
        super(BankAccountForm, self).__init__(*args, **kwargs)

    class Meta:
        model: BankAccount = BankAccount
        fields: list[str] = [
            "name",
            "description",
            "balance",
            "currency",
            "bank_name",
            "account_number",
            "sort_code",
            "iban",
            "interest_rate"]
        widgets: dict[str, Any] = {"description": forms.Textarea()}

    def save(self, instance: BankAccount = None) -> BankAccount:
        """Create a new bank amount form."""
        super().save(commit=False)

        if instance is None:
            monetary_account: BankAccount = BankAccount.objects.create(
                name=self.cleaned_data.get("name"),
                description=self.cleaned_data.get("description"),
                balance=self.cleaned_data.get("balance"),
                currency=self.cleaned_data.get("currency"),
                bank_name=self.cleaned_data.get("bank_name"),
                sort_code=self.cleaned_data.get("sort_code"),
                account_number=self.cleaned_data.get("account_number"),
                iban=self.cleaned_data.get("iban"),
                interest_rate=self.cleaned_data.get("interest_rate"),
                user=self.user
            )
        else:
            monetary_account: BankAccount = instance
            monetary_account.name: str = self.cleaned_data.get("name")
            monetary_account.description: str = self.cleaned_data.get(
                "description")
            monetary_account.balance: Decimal = self.cleaned_data.get(
                "balance")
            monetary_account.currency: str = self.cleaned_data.get("currency")
            monetary_account.bank_name: str = self.cleaned_data.get(
                "bank_name")
            monetary_account.sort_code: str = self.cleaned_data.get(
                "sort_code")
            monetary_account.account_number: str = self.cleaned_data.get(
                "account_number")
            monetary_account.iban: str = self.cleaned_data.get("iban")
            monetary_account.interest_rate: Decimal = self.cleaned_data.get(
                "interest_rate")
            monetary_account.user: User = self.user
            monetary_account.save()

        return monetary_account

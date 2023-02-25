from financial_companion.forms import AddTransactionsViaBankStatementForm
from financial_companion.models import Transaction, Account, User, PotAccount
from financial_companion.helpers import CurrencyType
from .test_form_base import FormTestCase
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import Q
from typing import Any
import os
from decimal import Decimal

class AddTransactionsViaBankStatementFormTestCase(FormTestCase):
    """Test of the add transactions via bank statement form"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.filter(user=self.user).first() 
        bank_statement_path: str = os.path.join("financial_companion", "tests", "data", "bank_statement.pdf")
        uploaded_bank_statement: TemporaryUploadedFile = self._get_upload_file(bank_statement_path)

        self.form_input: dict[str, Any] = {
            "bank_statement": uploaded_bank_statement,
            "account_currency": CurrencyType.GBP,
            "update_balance": "False",
            "account": self.account
        }

    def test_form_contains_required_fields(self):
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.user)
        self._assert_form_has_necessary_fields(
            form,
            "bank_statement",
            "account_currency",
            "update_balance",
            "account"
        )
    
    def test_valid_add_transactions_via_bank_statement_form(self):
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertTrue(form.is_valid())
    
    def test_invalid_bank_statement_cannot_be_blank(self):
        self.form_input["bank_statement"]: TemporaryUploadedFile = None
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_invalid_bank_statement_must_be_pdf(self):
        image_file_path: str = os.path.join("financial_companion", "tests", "data", "dragon.jpeg")
        self.form_input["bank_statement"]: TemporaryUploadedFile = self._get_upload_file(image_file_path)
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_valid_account_currency_accepts_all_values_in_currency_type_enum(self):
        for currency in CurrencyType:
            self.form_input["account_currency"]: str = currency
            form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
            self.assertTrue(form.is_valid())
    
    def test_invalid_account_currency_cannot_be_blank(self):
        self.form_input["account_currency"]: str = None
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_invalid_account_currency_does_not_accept_value_not_in_currency_type_enum(self):
        self.form_input["account_currency"]: str = "Invalid"
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_valid_update_balance_accepts_valid_inputs(self):
        for update_balance in ["True", "False"]:
            self.form_input["update_balance"]: str = update_balance
            form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
            self.assertTrue(form.is_valid())
    
    def test_invalid_update_balance_cannot_be_blank(self):
        self.form_input["update_balance"]: str = None
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_invalid_update_balance_does_not_accept_invalid_inputs(self):
        self.form_input["update_balance"]: str = "Invalid"
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_valid_account_belongs_to_user(self):
        self.assertTrue(hasattr(self.form_input["account"], "user"))
        self.assertEqual(self.form_input["account"].user, self.user)
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertTrue(form.is_valid())
    
    def test_invalid_account_cannot_be_blank(self):
        self.form_input["account"]: PotAccount = None
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_invalid_account_does_not_belong_to_user(self):
        self.form_input["account"]: PotAccount = PotAccount.objects.exclude(user=self.user).first()
        self.assertTrue(hasattr(self.form_input["account"], "user"))
        self.assertNotEqual(self.form_input["account"].user, self.user)
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        self.assertFalse(form.is_valid())
    
    def test_form_must_save_correctly(self):
        before_transaction_count: int = Transaction.objects.filter(Q(sender_account=self.account)|Q(receiver_account=self.account)).count()
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        transactions: list[Transaction] = form.save()
        after_transaction_count: int = Transaction.objects.filter(Q(sender_account=self.account)|Q(receiver_account=self.account)).count()
        self.assertEqual(before_transaction_count + 29, after_transaction_count)
    
    def test_form_must_save_correctly_update_balance(self):
        self.form_input["update_balance"]: str = "True"
        before_transaction_count: int = Transaction.objects.filter(Q(sender_account=self.account)|Q(receiver_account=self.account)).count()
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        transactions: list[Transaction] = form.save()
        after_transaction_count: int = Transaction.objects.filter(Q(sender_account=self.account)|Q(receiver_account=self.account)).count()
        self.assertEqual(before_transaction_count + 29, after_transaction_count)
        self.assertEqual(self.form_input["update_balance"], "True")
        self.account.refresh_from_db()
        self.assertEqual(Decimal("32.66"), self.account.balance)
    
    def test_form_save_no_repeat_transactions(self):
        form: AddTransactionsViaBankStatementForm = AddTransactionsViaBankStatementForm(self.form_input, self.form_input, user=self.user)
        form.save()
        before_transaction_count: int = Transaction.objects.filter(Q(sender_account=self.account)|Q(receiver_account=self.account)).count()
        transactions: list[Transaction] = form.save()
        after_transaction_count: int = Transaction.objects.filter(Q(sender_account=self.account)|Q(receiver_account=self.account)).count()
        self.assertEqual(before_transaction_count, after_transaction_count)

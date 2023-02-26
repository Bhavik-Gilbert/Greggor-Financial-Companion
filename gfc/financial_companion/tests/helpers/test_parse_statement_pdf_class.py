from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import Q
from typing import Any
import os
import pandas as pd
import numpy as np
from datetime import datetime
from .test_helper_base import HelperTestCase
from financial_companion.helpers import ParseStatementPDF, TransactionType
from financial_companion.models import User, PotAccount, Account


class ParseStatementPDFClassTestCase(HelperTestCase):
    """Test for the parse statement pdf helpers class"""

    def setUp(self):
        self.bank_statement_parser: ParseStatementPDF = ParseStatementPDF()
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.filter(user=self.user).first() 
        bank_statement_path: str = os.path.join("financial_companion", "tests", "data", "bank_statement.pdf")
        self.uploaded_bank_statement: TemporaryUploadedFile = self._get_upload_file(bank_statement_path)

        self.columns: list[str] = ["Date", "Description", "Out", "In", "Balance"]
        self.dates: list[str] = ["1/1/2001", "2/2/2002", "3/3/2003"]
        self.description: list[str] = ["john", "doe", "john doe"]
        self.out_money: list[str] = ["1.00", np.nan, "3.00"]
        self.in_money: list[str] = [np.nan, "2.00", np.nan]
        self.balance: list[str] = ["9.00", "11.00", "8.00"]
        self.dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, self.out_money, self.in_money, self.balance)), columns=self.columns)
        self.dataframe_list: list[pd.DataFrame] = [
            self.dataframe, self.dataframe, self.dataframe
        ]
        self.indexes: dict[str, int] = {
            "date": 0,
            "balance": -1,
            "income": -3,
            "expense": -2,
            "description": -4 
        }
    
    def _get_transaction(self) -> dict[str, Any]:
        """Returns filled transaction dictionary"""
        return {
                "date": self.bank_statement_parser.date,
                "amount": self.bank_statement_parser.amount,
                "balance": self.bank_statement_parser.balance,
                "transaction_type": self.bank_statement_parser.transaction_type,
                "description": self.bank_statement_parser.description
        }
    
    def _fill_parser_object(self, fill_data: bool=True):
        """
        Fills all object attributes
        If fill_data is false, object data attributes will remain as they are
        """
        self.bank_statement_parser.date: datetime = datetime.now()
        self.bank_statement_parser.balance: float = 100
        if fill_data:
            self._fill_parser_object_data()
    
    def _fill_parser_object_data(self):
        """
        Fills all object data attributes
        """
        self.bank_statement_parser.amount: float = 100
        self.bank_statement_parser.transaction_type: str = TransactionType.INCOME
        self.bank_statement_parser.description: list[str] = ["John"]
    
    def _assert_empty_object(self, empty_data: bool=True):
        """
        Asserts all object attributes are None
        If empty_data is false, object data attributes will not be assessed
        """
        self.assertTrue(self.bank_statement_parser.date is None)
        self.assertTrue(self.bank_statement_parser.balance is None)
        if empty_data:
            self._assert_empty_object_data()
        
    def _assert_empty_object_data(self):
        """
        Asserts all object data attributes are None
        """
        self.assertTrue(self.bank_statement_parser.amount is None)
        self.assertTrue(self.bank_statement_parser.transaction_type is None)
        self.assertTrue(self.bank_statement_parser.description is None)
    
    def _assert_filled_object(self, filled_data: bool=True):
        """
        Asserts all object attributes are not None
        If filled_data is false, object data attributes will not be assessed
        """
        self.assertTrue(self.bank_statement_parser.date is not None)
        self.assertTrue(self.bank_statement_parser.balance is not None)
        if filled_data:
            self._assert_filled_object_data()
        
    def _assert_filled_object_data(self):
        """
        Asserts all object data attributes are not None
        """
        self.assertTrue(self.bank_statement_parser.amount is not None)
        self.assertTrue(self.bank_statement_parser.transaction_type is not None)
        self.assertTrue(self.bank_statement_parser.description is not None)
    
    def test_valid_reset_object(self):
        self._fill_parser_object()
        self._assert_filled_object()
        self.bank_statement_parser.reset_object()
        self._assert_empty_object()

    def test_valid_reset_object_data(self):
        self._fill_parser_object_data()
        self._assert_filled_object_data()
        self.bank_statement_parser.reset_data()
        self._assert_empty_object_data()

    def test_valid_get_transactions_from_pdf_statement(self):
        transaction_list: list[dict[str, Any]] = self.bank_statement_parser.get_transactions_from_pdf_statement(self.uploaded_bank_statement.temporary_file_path())
        self.assertEqual(len(transaction_list), 29)
        for transaction in transaction_list:
            self.assertTrue(all(transaction.values()))
            self.assertTrue("date" in transaction.keys())
            self.assertTrue("amount" in transaction.keys())
            self.assertTrue("balance" in transaction.keys())
            self.assertTrue("transaction_type" in transaction.keys())
            self.assertTrue("description" in transaction.keys())
    
    def test_invalid_empty_get_transactions_from_pdf_statement(self):
        empty_uploaded_bank_statement: TemporaryUploadedFile = TemporaryUploadedFile("empty.pdf", "application/binary", 0, 'utf-8')
        with self.assertRaises(Exception) as raised:
            self.bank_statement_parser.get_transactions_from_pdf_statement(empty_uploaded_bank_statement.temporary_file_path())
        self.assertEqual(ValueError, type(raised.exception))
    
    def test_invalid_unclean_get_transactions_from_pdf_statement(self):
        unclean_bank_statement_path: str = os.path.join("financial_companion", "tests", "data", "invalid_bank_statement.pdf")
        unclean_uploaded_bank_statement: TemporaryUploadedFile = self._get_upload_file(unclean_bank_statement_path)
        with self.assertRaises(Exception) as raised:
            self.bank_statement_parser.get_transactions_from_pdf_statement(unclean_uploaded_bank_statement.temporary_file_path())
        self.assertEqual(TypeError, type(raised.exception))
    
    def test_valid_get_sender_receiver_is_sender(self):
        self._fill_parser_object()
        parsed_transaction: dict[str, Any] = self._get_transaction()
        parsed_transaction["transaction_type"]: str = TransactionType.EXPENSE
        receiver, sender = self.bank_statement_parser.get_sender_receiver(parsed_transaction, self.account)
        self.assertEqual(self.account, sender)
    
    def test_valid_get_sender_receiver_is_receiver(self):
        self._fill_parser_object()
        parsed_transaction: dict[str, Any] = self._get_transaction()
        parsed_transaction["transaction_type"]: str = TransactionType.INCOME
        receiver, sender = self.bank_statement_parser.get_sender_receiver(parsed_transaction, self.account)
        self.assertEqual(self.account, receiver)

    def test_invalid_get_sender_receiver_transaction_type_is_not_in_transaction_type_enum_is_sender(self):
        self._fill_parser_object()
        parsed_transaction: dict[str, Any] = self._get_transaction()
        parsed_transaction["transaction_type"]: str = "Invalid"
        receiver, sender = self.bank_statement_parser.get_sender_receiver(parsed_transaction, self.account)
        self.assertEqual(self.account, sender)
    
    def test_valid_get_dataframe_list_statement_column_expense_indexes_separate_income_expense_columns(self):
        income, expense, fail = self.bank_statement_parser.get_dataframe_list_statement_column_expense_indexes(self.dataframe_list)
        self.assertEqual(income, -3)
        self.assertEqual(expense, -2)
        self.assertFalse(fail)
    
    def test_valid_get_dataframe_list_statement_column_expense_indexes_same_income_expense_columns(self):
        columns: list[str] = ["Date", "Description", "Move", "Balance"]
        move_money: list[str] = ["-1.00", "2.00", "-3.00"]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, move_money, self.balance)), columns=columns)
        dataframe_list: list[pd.DataFrame] = [
            dataframe
        ]
        income, expense, fail = self.bank_statement_parser.get_dataframe_list_statement_column_expense_indexes(dataframe_list)
        self.assertEqual(income, -2)
        self.assertEqual(expense, -2)
        self.assertFalse(fail)
    
    def test_invalid_get_dataframe_list_statement_column_invalid_index_expense_column_data(self):
        out_money: list[str] = ["invalid", "invalid", "invalid"]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, out_money, self.in_money, self.balance)), columns=self.columns)
        dataframe_list: list[pd.DataFrame] = [
            dataframe
        ]
        income, expense, fail = self.bank_statement_parser.get_dataframe_list_statement_column_expense_indexes(dataframe_list)
        self.assertEqual(income, -1)
        self.assertEqual(expense, -1)
        self.assertTrue(fail)
    
    def test_valid_get_transaction_from_dataframe_list(self):
        transactions: list[dict[str, Any]] = self.bank_statement_parser.get_transactions_from_dataframe_list(self.dataframe_list, self.indexes)
        self.assertEqual(len(transactions), 9)
    
    def test_valid_get_transactions_from_dataframe(self):
        transactions: list[dict[str, Any]] = self.bank_statement_parser.get_transactions_from_dataframe(self.dataframe, self.indexes)
        self.assertEqual(len(transactions), 3)
    
    def test_valid_get_transactions_from_dataframe_row(self):
        transaction: list[dict[str, Any]] = self.bank_statement_parser.get_transaction_from_dataframe_row(self.dataframe.iloc()[0], self.indexes)
        self.assertEqual(len(transaction), 1)
    
    def test_valid_add_new_transaction_filled_new_transaction(self):
        self._fill_parser_object()
        new_transaction: dict[str, Any] = self._get_transaction()
        transactions: dict[str, Any] = self.bank_statement_parser.add_new_transaction([], new_transaction)
        self.assertEqual(len(transactions), 1)
        self._assert_filled_object(False)
        self._assert_empty_object_data()
    
    def test_valid_add_new_transaction_missing_description(self):
        self._fill_parser_object()
        self.bank_statement_parser.description: str = None
        new_transaction: dict[str, Any] = self._get_transaction()
        transactions: dict[str, Any] = self.bank_statement_parser.add_new_transaction([], new_transaction)
        self.assertEqual(len(transactions), 0)
        self._assert_filled_object(False)
        self.assertTrue(self.bank_statement_parser.amount is not None)
        self.assertTrue(self.bank_statement_parser.transaction_type is not None)
        self.assertTrue(self.bank_statement_parser.description is None)
    
    def test_valid_add_new_transaction_missing_amount(self):
        self._fill_parser_object()
        self.bank_statement_parser.amount: float = None
        new_transaction: dict[str, Any] = self._get_transaction()
        transactions: dict[str, Any] = self.bank_statement_parser.add_new_transaction([], new_transaction)
        self.assertEqual(len(transactions), 0)
        self._assert_filled_object(False)
        self.assertTrue(self.bank_statement_parser.description is not None)
        self.assertTrue(self.bank_statement_parser.transaction_type is not None)
        self.assertTrue(self.bank_statement_parser.amount is None)
    
    def test_valid_add_new_transaction_missing_transaction_type(self):
        self._fill_parser_object()
        self.bank_statement_parser.transaction_type: str = None
        new_transaction: dict[str, Any] = self._get_transaction()
        transactions: dict[str, Any] = self.bank_statement_parser.add_new_transaction([], new_transaction)
        self.assertEqual(len(transactions), 0)
        self._assert_filled_object(False)
        self.assertTrue(self.bank_statement_parser.description is not None)
        self.assertTrue(self.bank_statement_parser.amount is not None)
        self.assertTrue(self.bank_statement_parser.transaction_type is None)
    
    def test_valid_add_new_transaction_missing_date(self):
        self._fill_parser_object()
        self.bank_statement_parser.date: datetime = None
        new_transaction: dict[str, Any] = self._get_transaction()
        transactions: dict[str, Any] = self.bank_statement_parser.add_new_transaction([], new_transaction)
        self.assertEqual(len(transactions), 0)
        self.assertTrue(self.bank_statement_parser.balance is not None)
        self.assertTrue(self.bank_statement_parser.date is None)
        self._assert_filled_object_data()
    
    def test_valid_add_new_transaction_missing_balance(self):
        self._fill_parser_object()
        self.bank_statement_parser.balance: float = None
        new_transaction: dict[str, Any] = self._get_transaction()
        transactions: dict[str, Any] = self.bank_statement_parser.add_new_transaction([], new_transaction)
        self.assertEqual(len(transactions), 0)
        self.assertTrue(self.bank_statement_parser.date is not None)
        self.assertTrue(self.bank_statement_parser.balance is None)
        self._assert_filled_object_data()
    
    def test_valid_add_new_transaction_missing_all_but_description(self):
        self.bank_statement_parser.description: str = "Not empty"
        new_transaction: dict[str, Any] = self._get_transaction()
        transactions: dict[str, Any] = self.bank_statement_parser.add_new_transaction([], new_transaction)
        self.assertEqual(len(transactions), 0)
        self._assert_empty_object()

    def test_valid_set_expense_and_income_columns_correct_way_around_columns_are_correct_way_around(self):
        transaction_1: dict[str, Any] = self._get_transaction()
        transaction_2: dict[str, Any] = self._get_transaction()
        transaction_1["balance"]: float = 200
        transaction_2["balance"]: float = 100
        transaction_2["transaction_type"]: str = TransactionType.EXPENSE
        transactions_before: list[dict[str, Any]] = [transaction_1, transaction_2]
        self.assertEqual(transactions_before[1]["transaction_type"], TransactionType.EXPENSE)
        transactions_after: list[dict[str, Any]] = self.bank_statement_parser.set_expense_and_income_columns_correct_way_around(transactions_before)
        self.assertEqual(transactions_after[1]["transaction_type"], TransactionType.EXPENSE)
    
    def test_valid_set_expense_and_income_columns_correct_way_around_columns_are_wrong_way_around(self):
        transaction_1: dict[str, Any] = self._get_transaction()
        transaction_2: dict[str, Any] = self._get_transaction()
        transaction_1["balance"]: float = 100
        transaction_2["balance"]: float = 200
        transaction_2["transaction_type"]: str = TransactionType.EXPENSE
        transactions_before: list[dict[str, Any]] = [transaction_1, transaction_2]
        self.assertEqual(transactions_before[1]["transaction_type"], TransactionType.EXPENSE)
        transactions_after: list[dict[str, Any]] = self.bank_statement_parser.set_expense_and_income_columns_correct_way_around(transactions_before)
        self.assertEqual(transactions_after[1]["transaction_type"], TransactionType.INCOME)

    def test_valid_set_initial_balance_from_dataframe_set_balance(self):
        columns: list[str] = ["Date", "Description", "Out", "In", "1.00"]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, self.out_money, self.in_money, self.balance)), columns=columns)
        self.bank_statement_parser.set_initial_balance_from_dataframe(dataframe, self.indexes)
        self.assertTrue(self.bank_statement_parser.balance is not None)
    
    def test_valid_set_initial_balance_from_dataframe_cannot_set_balance(self):
        self.bank_statement_parser.set_initial_balance_from_dataframe(self.dataframe, self.indexes)
        self.assertTrue(self.bank_statement_parser.balance is None)
    
    def test_valid_set_balance_from_datataframe_row_change_balance(self):
        self.bank_statement_parser.balance: float = 100
        before_balance: int = self.bank_statement_parser.balance
        self.bank_statement_parser.set_balance_from_datataframe_row(self.dataframe.iloc()[0], self.indexes)
        after_balance: int = self.bank_statement_parser.balance
        self.assertTrue(before_balance != after_balance)
    
    def test_valid_set_balance_from_datataframe_row_empty_balance_field(self):
        balance: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, self.out_money, self.in_money, balance)), columns=self.columns)
        self.bank_statement_parser.balance: float = 100
        before_balance: int = self.bank_statement_parser.balance
        self.bank_statement_parser.set_balance_from_datataframe_row(dataframe.iloc()[0], self.indexes)
        after_balance: int = self.bank_statement_parser.balance
        self.assertEqual(before_balance, after_balance)
    
    def test_valid_set_date_from_datataframe_row_change_date(self):
        self.bank_statement_parser.date: datetime = datetime(2021, 3, 24)
        before_date: int = self.bank_statement_parser.date
        self.bank_statement_parser.set_date_from_datataframe_row(self.dataframe.iloc()[0], self.indexes)
        after_date: int = self.bank_statement_parser.date
        self.assertTrue(before_date != after_date)
    
    def test_valid_set_date_from_datataframe_row_empty_date_field(self):
        dates: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(dates, self.description, self.out_money, self.in_money, self.balance)), columns=self.columns)
        self.bank_statement_parser.date: datetime = datetime(2021, 3, 24)
        before_date: int = self.bank_statement_parser.date
        self.bank_statement_parser.set_date_from_datataframe_row(dataframe.iloc()[0], self.indexes)
        after_date: int = self.bank_statement_parser.date
        self.assertEqual(before_date, after_date)
    
    def test_valid_set_description_from_datataframe_row_change_description_first_value(self):
        before_description: list[str] = self.bank_statement_parser.description
        self.bank_statement_parser.set_description_from_datataframe_row(self.dataframe.iloc()[0], self.indexes)
        after_description: list[str] = self.bank_statement_parser.description
        self.assertTrue(before_description != after_description)
        self.assertTrue(len(after_description) == 1)
    
    def test_valid_set_description_from_datataframe_row_change_description_second_value(self):
        self.bank_statement_parser.description: list[str] = ["Value 1"]
        self.assertTrue(len(self.bank_statement_parser.description) == 1)
        self.bank_statement_parser.set_description_from_datataframe_row(self.dataframe.iloc()[0], self.indexes)
        self.assertTrue(len(self.bank_statement_parser.description) == 2)
    
    def test_valid_set_description_from_datataframe_row_empty_description_field(self):
        description: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, description, self.out_money, self.in_money, self.balance)), columns=self.columns)
        self.bank_statement_parser.set_date_from_datataframe_row(dataframe.iloc()[0], self.indexes)
        self.assertTrue(self.bank_statement_parser.description is None)

    def test_valid_set_all_data_from_dataframe_row(self):
        self._assert_empty_object()
        self.bank_statement_parser.set_all_data_from_dataframe_row(self.dataframe.iloc()[0], self.indexes)
        self._assert_filled_object()
    
    def test_valid_set_all_data_from_dataframe_row_empty_date_field(self):
        self._assert_empty_object()
        dates: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(dates, self.description, self.out_money, self.in_money, self.balance)), columns=self.columns)
        self.bank_statement_parser.set_all_data_from_dataframe_row(dataframe.iloc()[0], self.indexes)
        self.assertTrue(self.bank_statement_parser.balance is not None)
        self.assertTrue(self.bank_statement_parser.date is None)
        self._assert_filled_object_data()
    
    def test_valid_set_all_data_from_dataframe_row_empty_balance_field(self):
        self._assert_empty_object()
        balance: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, self.out_money, self.in_money, balance)), columns=self.columns)
        self.bank_statement_parser.set_all_data_from_dataframe_row(dataframe.iloc()[0], self.indexes)
        self.assertTrue(self.bank_statement_parser.balance is None)
        self.assertTrue(self.bank_statement_parser.date is not None)
        self._assert_filled_object_data()
    
    def test_valid_set_all_data_from_dataframe_row_empty_description_field(self):
        self._assert_empty_object()
        description: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, description, self.out_money, self.in_money, self.balance)), columns=self.columns)
        self.bank_statement_parser.set_all_data_from_dataframe_row(dataframe.iloc()[0], self.indexes)
        self._assert_filled_object(False)
        self.assertTrue(self.bank_statement_parser.amount is not None)
        self.assertTrue(self.bank_statement_parser.transaction_type is not None)
        self.assertTrue(self.bank_statement_parser.description is None)
    
    def test_valid_set_all_data_from_dataframe_row_empty_in_money_out_money_fields(self):
        self._assert_empty_object()
        in_money: list[str] = [np.nan, np.nan, np.nan]
        out_money: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, out_money, in_money, self.balance)), columns=self.columns)
        self.bank_statement_parser.set_all_data_from_dataframe_row(dataframe.iloc()[0], self.indexes)
        self._assert_filled_object(False)
        self.assertTrue(self.bank_statement_parser.amount is None)
        self.assertTrue(self.bank_statement_parser.transaction_type is None)
        self.assertTrue(self.bank_statement_parser.description is not None)

    def test_valid_set_amount_and_transaction_type_from_datataframe_row_change_amount_and_transaction_type_income(self):
        before_amount: float = self.bank_statement_parser.amount
        before_transaction_type: str = self.bank_statement_parser.transaction_type
        self.bank_statement_parser.set_amount_and_transaction_type_from_datataframe_row(self.dataframe.iloc()[0], self.indexes)
        after_amount: float = self.bank_statement_parser.amount
        after_transaction_type: str = self.bank_statement_parser.transaction_type
        self.assertTrue(before_amount != after_amount)
        self.assertTrue(before_transaction_type != after_transaction_type)
        self.assertEqual(after_transaction_type, TransactionType.INCOME)

    
    def test_valid_set_amount_and_transaction_type_from_datataframe_row_change_amount_and_transaction_type_expense(self):
        before_amount: float = self.bank_statement_parser.amount
        before_transaction_type: str = self.bank_statement_parser.transaction_type
        self.bank_statement_parser.set_amount_and_transaction_type_from_datataframe_row(self.dataframe.iloc()[1], self.indexes)
        after_amount: float = self.bank_statement_parser.amount
        after_transaction_type: str = self.bank_statement_parser.transaction_type
        self.assertTrue(before_amount != after_amount)
        self.assertTrue(before_transaction_type != after_transaction_type)
        self.assertEqual(after_transaction_type, TransactionType.EXPENSE)

    
    def test_valid_set_amount_and_transaction_type_from_datataframe_row_empty_in_money_out_money_fields(self):
        before_amount: float = self.bank_statement_parser.amount
        before_transaction_type: str = self.bank_statement_parser.transaction_type
        in_money: list[str] = [np.nan, np.nan, np.nan]
        out_money: list[str] = [np.nan, np.nan, np.nan]
        dataframe: pd.DataFrame = pd.DataFrame(list(zip(self.dates, self.description, out_money, in_money, self.balance)), columns=self.columns)
        self.bank_statement_parser.set_amount_and_transaction_type_from_datataframe_row(dataframe.iloc()[0], self.indexes)
        after_amount: float = self.bank_statement_parser.amount
        after_transaction_type: str = self.bank_statement_parser.transaction_type
        self.assertEqual(before_amount, after_amount)
        self.assertEqual(before_transaction_type, after_transaction_type)

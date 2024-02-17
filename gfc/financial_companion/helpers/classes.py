import tabula
import pandas as pd
import re
import dateutil.parser as dparser
from typing import Any
from financial_companion.helpers import TransactionType
import financial_companion.models as fcmodels
from datetime import datetime


class CurrencyConversion:
    """Stores a record of a conversion rate between two currencies"""

    def __init__(self, currency_from_code: str, currency_to_code: str,
                 conversion_rate: float, time_recorded: datetime) -> None:
        self.currency_from_code: str = currency_from_code
        self.currency_to_code: str = currency_to_code
        self.conversion_rate: float = conversion_rate
        self.time_recorded: datetime = time_recorded
        self.supported_currencies: list[str] = [
            currency_from_code, currency_to_code]

    def can_convert(self, currency_from_code: str, currency_to_code: str):
        """Checks if conversion is valid for inputted currencies"""
        return currency_from_code in self.supported_currencies and currency_to_code in self.supported_currencies

    def conversion_in_date(self) -> bool:
        """Checks conversion is less than a day old"""
        return (datetime.now() - self.time_recorded).days == 0

    def convert(self, amount: float, currency_from_code: str,
                currency_to_code: str) -> float:
        """Converts amount using conversion rate"""
        if not self.can_convert(currency_from_code, currency_to_code):
            return amount

        conversion_rate = self.conversion_rate
        if currency_from_code == self.currency_to_code:
            conversion_rate = 1 / conversion_rate

        return float(amount) * conversion_rate


class StoredCurrencyConverter:
    """Structure of stored CurrencyConversions"""
    def __init__(self) -> None:
        self.conversion_list: list[CurrencyConversion] = []

    def has_valid_conversion(self, currency_from_code: str,
                             currency_to_code: str) -> bool:
        """Checks if currency conversion for inputted currencies is stored"""
        return self.get_conversion(
            currency_from_code, currency_to_code) is not None

    def get_conversion(self, currency_from_code: str,
                       currency_to_code: str) -> CurrencyConversion:
        """Gets CurrencyConversion for inputted currencies if available"""
        for conversion in self.conversion_list:
            if conversion.can_convert(
                    currency_from_code, currency_to_code) and conversion.conversion_in_date():
                return conversion
        return None

    def add_conversion(self, currency_from_code: str,
                       currency_to_code: str, conversion_rate: float) -> None:
        """
        Adds new CurrencyConversion to structure
        Removes previous rate entries
        """
        conversion: CurrencyConversion = CurrencyConversion(
            currency_from_code, currency_to_code, conversion_rate, datetime.now())
        old_conversion: CurrencyConversion = self.get_conversion(
            currency_from_code, currency_to_code)

        if old_conversion:
            replace_index: int = self.conversion_list.index(old_conversion)
            self.conversion_list[replace_index] = conversion
        else:
            self.conversion_list.append(conversion)


class ParseStatementPDF:
    def __init__(self) -> None:
        self.number_regex: str = r'[^-\d.]'
        self.ignore_in_description: list[str] = [
            "transfer",
            "purchase",
            "payment"
        ]
        self.reset_object()

    def reset_object(self) -> None:
        """Sets all transaction data to none"""
        self.date: datetime = None
        self.balance: float = None
        self.reset_data()

    def reset_data(self) -> None:
        """Sets all transaction data except date to none"""
        self.amount: float = None
        self.transaction_type: str = None
        self.description: str = None

    def get_dataframe_list_statement_column_expense_indexes(
            self, statement_dataframe_list: list[pd.DataFrame]) -> tuple[int, int, bool]:
        """Checks if income and expense fields are separate or together"""
        if pd.isna(statement_dataframe_list[0].iloc[0][-3]) or re.sub(self.number_regex, '',
                                                                      statement_dataframe_list[0].iloc[0][-3])[1:].replace(".", "", 1).replace("-", "", 1).isnumeric():
            return -3, -2, False
        if not pd.isna(statement_dataframe_list[0].iloc[0][-2]) and re.sub(self.number_regex, '', statement_dataframe_list[0].iloc[0][-2])[
                1:].replace(".", "", 1).replace("-", "", 1).isnumeric():
            return -2, -2, False

        return -1, -1, True

    def get_transactions_from_dataframe_list(
            self, statement_dataframe_list: list[pd.DataFrame], indexes: dict[str, int], transactions: list[dict[str, Any]] = []) -> list[dict[str, Any]]:
        """Returns list of transaction data from list of dataframes"""
        for statement_dataframe in statement_dataframe_list:
            transactions: list[dict[str, Any]] = self.get_transactions_from_dataframe(
                statement_dataframe, indexes, transactions)
        return transactions

    def set_expense_and_income_columns_correct_way_around(
            self, transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Checks the expense and income columns are the correct way around in the data
        Set the expense and income columns in the data if incorrect
        """

        if len(transactions) > 1:
            if ((transactions[1]["balance"] - transactions[0]["balance"] > 0 and transactions[1]["transaction_type"] == TransactionType.EXPENSE) or (
                    transactions[1]["balance"] - transactions[0]["balance"] < 0 and transactions[1]["transaction_type"] == TransactionType.INCOME)):
                for transaction in transactions:
                    if transaction["transaction_type"] == TransactionType.INCOME:
                        transaction["transaction_type"]: str = TransactionType.EXPENSE
                    elif transaction["transaction_type"] == TransactionType.EXPENSE:
                        transaction["transaction_type"]: str = TransactionType.INCOME

        return transactions

    def set_initial_balance_from_dataframe(
            self, statement_dataframe: pd.DataFrame, indexes: dict[str, int]) -> None:
        """
        Sets object balance data if statement dataframe balance block is not empty
        or balance is already set
        """
        if self.balance is None and len(
                statement_dataframe.columns[indexes["balance"]]) > 0:
            try:
                self.balance: float = float(re.sub(self.number_regex, '', str(
                    statement_dataframe.columns[indexes["balance"]])))
            except Exception:
                pass

    def set_date_from_datataframe_row(
            self, statement_dataframe_row: list[Any], indexes: dict[str, int]) -> None:
        """Updates object date data if statement dataframe row date block is understandable"""
        try:
            self.date: datetime = pd.to_datetime(dparser.parse(str(
                statement_dataframe_row[indexes["date"]]), fuzzy=True), infer_datetime_format=True)
        except Exception:
            pass

    def set_balance_from_datataframe_row(
            self, statement_dataframe_row: list[Any], indexes: dict[str, int]) -> None:
        """Updates object balance data if statement dataframe row balance block is not empty"""
        if not pd.isna(statement_dataframe_row[indexes["balance"]]):
            self.balance: float = float(re.sub(self.number_regex, '', str(
                statement_dataframe_row[indexes["balance"]])))

    def set_amount_and_transaction_type_from_datataframe_row(
            self, statement_dataframe_row: list[Any], indexes: dict[str, int]) -> None:
        """Updates amount and transaction type data if statement dataframe row income or expense block is valid"""
        if not pd.isna(statement_dataframe_row[indexes["income"]]) and float(re.sub(
                self.number_regex, '', str(statement_dataframe_row[indexes["income"]]))) >= 0:
            self.amount: float = abs(float(re.sub(self.number_regex, '', str(
                statement_dataframe_row[indexes["income"]]))))
            self.transaction_type: str = TransactionType.INCOME
        elif not pd.isna(statement_dataframe_row[indexes["expense"]]):
            self.amount: float = abs(float(re.sub(self.number_regex, '', str(
                statement_dataframe_row[indexes["expense"]]))))
            self.transaction_type: str = TransactionType.EXPENSE

    def set_description_from_datataframe_row(
            self, statement_dataframe_row: list[Any], indexes: dict[str, int]) -> None:
        """Updates object description data if statement dataframe row descritiption block is not empty"""
        description: str = statement_dataframe_row[indexes["description"]]
        if not pd.isna(description) and description.lower(
        ) not in self.ignore_in_description:
            if self.description is None:
                self.description: list[str] = [
                    str(description)]
            else:
                self.description += [description]

    def set_all_data_from_dataframe_row(
            self, statement_dataframe_row: list[Any], indexes: dict[str, int]) -> None:
        """Parses dataframe row and updates object data where rows aren't empty"""
        self.set_date_from_datataframe_row(statement_dataframe_row, indexes)
        self.set_balance_from_datataframe_row(statement_dataframe_row, indexes)
        self.set_amount_and_transaction_type_from_datataframe_row(
            statement_dataframe_row, indexes)
        self.set_description_from_datataframe_row(
            statement_dataframe_row, indexes)

    def add_new_transaction(
            self, transactions: list[dict[str, Any]], new_transaction: dict[str, Any]) -> list[dict[str, Any]]:
        """Returns transactions list, adding new transaction if valid"""
        if all(new_transaction.values()):
            self.reset_data()
            return [*transactions, new_transaction]

        new_transaction.pop("description", None)
        if all(
                new_transaction_data is None for new_transaction_data in new_transaction.values()):
            self.reset_data()
        return transactions

    def get_transaction_from_dataframe_row(self, statement_dataframe_row: list[Any], indexes: dict[str, int],
                                           transactions: list[dict[str, Any]] = []) -> list[dict[str, Any]]:
        """Returns list of transaction data of currenct transactions and dataframe row"""
        self.set_all_data_from_dataframe_row(
            statement_dataframe_row, indexes)

        new_transaction = {
            "date": self.date,
            "amount": self.amount,
            "balance": self.balance,
            "transaction_type": self.transaction_type,
            "description": self.description
        }

        return self.add_new_transaction(
            transactions, new_transaction)

    def get_transactions_from_dataframe(self, statement_dataframe: pd.DataFrame, indexes: dict[str, int],
                                        transactions: list[dict[str, Any]] = []) -> list[dict[str, Any]]:
        """Returns list of transaction data from dataframe"""
        statement_dataframe.dropna(
            how='all', axis=1, inplace=True
        )
        self.set_initial_balance_from_dataframe(statement_dataframe, indexes)

        for statement_dataframe_row in statement_dataframe.iloc():
            transactions: list[dict[str, Any]] = self.get_transaction_from_dataframe_row(
                statement_dataframe_row, indexes, transactions)

        return self.set_expense_and_income_columns_correct_way_around(
            transactions)

    def get_transactions_from_pdf_statement(
            self, statement_path: str) -> list[dict[str, Any]]:
        """
        Returns list of dictionary of transaction data from pdf
        Run in try except block to handle errors
        """
        statement_dataframe_list: list[pd.DataFrame] = tabula.read_pdf(
            statement_path, pages='all')

        indexes: dict[str, int] = {}
        indexes["date"]: int = 0
        indexes["balance"]: int = -1
        indexes["income"], indexes["expense"], fail = self.get_dataframe_list_statement_column_expense_indexes(
            statement_dataframe_list)
        indexes["description"]: int = indexes["income"] - 1

        self.reset_object()
        transactions: list[dict[str, Any]] = []
        if not fail:
            transactions: list[dict[str, Any]] = self.get_transactions_from_dataframe_list(
                statement_dataframe_list, indexes)

        return transactions

    def get_sender_receiver(
            self, parsed_transaction: dict[str, Any], account, user) -> tuple:
        """
        Gets the other account from parsed transaction via name
        Returns pair (receiver_account, sender_account)
        """
        other_account: fcmodels.Account = fcmodels.Account.get_or_create_account(
            parsed_transaction["description"][0], user)
        if parsed_transaction["transaction_type"] == TransactionType.INCOME:
            return account, other_account
        elif parsed_transaction["transaction_type"] == TransactionType.EXPENSE:
            return other_account, account

        return other_account, account

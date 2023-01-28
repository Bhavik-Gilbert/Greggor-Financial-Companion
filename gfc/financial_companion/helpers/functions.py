from currency_symbols import CurrencySymbols
from currency_converter import CurrencyConverter
from kzt_exchangerates import Rates as KZTRates
from .enums import CurrencyType

def get_currency_symbol(currency_code: str):
    """Returns currency symbol for given currency code"""
    return CurrencySymbols.get_symbol(currency_code)

def convert_currency(amount: float, current_currency_code: str, target_currency_code: str):
    """Converts balance from one currency to another"""
    if current_currency_code == CurrencyType.KZT or target_currency_code == CurrencyType.KZT:
        kzt_rates = KZTRates()
        if current_currency_code == CurrencyType.KZT:
            return amount * kzt_rates.get_exchange_rate(target_currency_code)
        else:
            return amount * kzt_rates.get_exchange_rate(current_currency_code, from_kzt=True)

    c: CurrencyConverter = CurrencyConverter(fallback_on_missing_rate=True)
    return c.convert(amount, current_currency_code, target_currency_code)

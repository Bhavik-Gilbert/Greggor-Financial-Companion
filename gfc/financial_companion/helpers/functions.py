from currency_symbols import CurrencySymbols
from currency_converter import CurrencyConverter

def get_currency_symbol(currency_code: str):
    return CurrencySymbols.get_symbol(currency_code)

def convert_currency(amount: float, current_currency_code: str, target_currency_code: str):
    c: CurrencyConverter = CurrencyConverter(fallback_on_missing_rate=True)
    return c.convert(amount, current_currency_code, target_currency_code)

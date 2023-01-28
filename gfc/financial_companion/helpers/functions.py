from currency_symbols import CurrencySymbols

def get_currency_symbol(currency_code: str):
    return CurrencySymbols.get_symbol(currency_code)


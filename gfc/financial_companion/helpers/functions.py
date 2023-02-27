from currency_symbols import CurrencySymbols
from currency_converter import CurrencyConverter
from kzt_exchangerates import Rates as KZTRates
from .enums import CurrencyType
import random
import string
from datetime import datetime
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_currency_symbol(currency_code: str):
    """Returns currency symbol for given currency code"""
    currency_code = currency_code.upper()

    if currency_code in CurrencyType:
        return CurrencySymbols.get_symbol(currency_code)
    else:
        return ""


def convert_currency(amount: float, current_currency_code: str,
                     target_currency_code: str):
    """Converts balance from one currency to another"""
    current_currency_code = current_currency_code.upper()
    target_currency_code = target_currency_code.upper()

    if current_currency_code == target_currency_code or current_currency_code not in CurrencyType or target_currency_code not in CurrencyType:
        return amount

    if current_currency_code == CurrencyType.KZT or target_currency_code == CurrencyType.KZT:
        kzt_rates = KZTRates()
        if current_currency_code == CurrencyType.KZT:
            return amount * kzt_rates.get_exchange_rate(target_currency_code)
        else:
            return amount * \
                kzt_rates.get_exchange_rate(
                    current_currency_code, from_kzt=True)

    c: CurrencyConverter = CurrencyConverter(
        fallback_on_missing_rate=True,
        fallback_on_wrong_date=True)
    return c.convert(amount, current_currency_code, target_currency_code)


def random_filename(filename):
    """Generates a random filename"""
    file_extension = filename.split('.')[-1]

    # set a random filename
    filename_strings_to_add = [
        random.choice(
            string.ascii_letters), str(
            datetime.now())]
    return '{}.{}'.format(''.join(filename_strings_to_add), file_extension)


def calculate_percentages(spent_per_category : dict(), total):
    no_of_categories = len(spent_per_category)
    for key, value in spent_per_category.items():
        percentage = (value / total) * 100
        spent_per_category.update({key : percentage})


def paginate(page, list_input):
    list_of_items = []
    paginator = Paginator(list_input, settings.NUMBER_OF_TRANSACTIONS)
    try:
        list_of_items = paginator.page(page)
    except PageNotAnInteger:
        list_of_items = paginator.page(1)
    except EmptyPage:
        list_of_items = paginator.page(paginator.num_pages)

    return list_of_items


def get_random_invite_code(length):
    """Generates a random invite code for User Groups"""
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

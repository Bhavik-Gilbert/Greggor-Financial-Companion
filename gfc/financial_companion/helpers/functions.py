from currency_symbols import CurrencySymbols
from currency_converter import CurrencyConverter
from kzt_exchangerates import Rates as KZTRates
from .enums import CurrencyType
import random
import string
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from json import dumps
import financial_companion.models as fcmodels


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

def get_conversions_for_accounts(bank_accounts, mainCurrency = "GBP"):
    otherCurrencies = []
    conversions: Dict[str,float] = {}
    conversions.update({str(mainCurrency) : 1.0})
    i = 0
    while (i < len(bank_accounts)):
        currency = bank_accounts[i].currency
        conversions.update({str(currency) : convert_currency(1, currency, mainCurrency)})
        i += 1;
    if (len(conversions.keys()) == 1 and not("GBP" in conversions)):
        conversions.update({"GBP" : convert_currency(1, "GBP", mainCurrency)})

    return conversions

def get_projection_timescale_options():
    return {6 : "6 Months", 12: "1 Year", 24: "2 Years", 60: "5 Years"}

def get_projections_balances(accounts, max_timescale_in_months:int = max(get_projection_timescale_options().keys())):
    timescales = get_projection_timescale_options()
    accountDictionary = {}
    for account in accounts:
        interest_rate = float(account.interest_rate/100);
        accountData = {"name": account.name, "currency": account.currency, "interest_rate": float(account.interest_rate)}
        balances = []
        currentBalance = float(account.balance)
        i = 1
        while i <= max_timescale_in_months:
            tempBalanceTotal = currentBalance * ((1 + (interest_rate/365))**get_number_of_days_in_prev_month(i))
            if tempBalanceTotal >= 0:
                currentBalance = tempBalanceTotal
            balances.append(currentBalance)
            i += 1
        accountData.update({"balances": balances})
        accountDictionary.update({account.id : accountData})
    
    return accountDictionary


def get_short_month_names_for_timescale(max_timescale_in_months:int = max(get_projection_timescale_options().keys())):
    currentDate = datetime.today()
    i = 1
    dates = []
    while i <= max_timescale_in_months:
        nextDate = currentDate + relativedelta(months = i)
        dates.append(str(nextDate.strftime("%b").capitalize() + " " + nextDate.strftime("%y").capitalize()))
        i += 1

    return dates

def get_number_of_days_in_prev_month(offset_inMonths:int = 0):
    date = datetime.today() + relativedelta(months = offset_inMonths)
    no_of_days_in_prev_month = (
        date.replace(
            day=1) -
        timedelta(
            days=1)).day

    return no_of_days_in_prev_month

def get_data_for_account_projection(user):
    accounts = fcmodels.BankAccount.objects.filter(user_id=user, interest_rate__gt=0)
    mainCurrency = "GBP"
    if (accounts):
        mainCurrency = accounts[0].currency
    conversions = get_conversions_for_accounts(accounts, mainCurrency)

    timescale_dict = get_projection_timescale_options()
    timescales_strings = get_short_month_names_for_timescale()

    return {   
        'bank_accounts': {acc.id: acc.name for acc in accounts},
        'bank_account_infos': dumps(get_projections_balances(accounts)),
        'timescale_dict': timescale_dict,
        'timescales_strings': timescales_strings,
        'conversion_to_main_currency_JSON': dumps(conversions),
        'conversion_to_main_currency': conversions,
        'main_currency': mainCurrency
    }


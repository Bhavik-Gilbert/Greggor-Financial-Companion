from json import dumps
from currency_symbols import CurrencySymbols
from currency_converter import CurrencyConverter
from .enums import CurrencyType
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import financial_companion.models as fcmodels
import calendar
import inflect
import random
import string


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

    try:
        c: CurrencyConverter = CurrencyConverter(
            fallback_on_missing_rate=True,
            fallback_on_wrong_date=True)
        return c.convert(amount, current_currency_code, target_currency_code)
    except Exception:
        raise Exception("Converter not working")


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
        percentage = float((value / total) * 100)
        spent_per_category.update({key : percentage})
    return spent_per_category


def paginate(page, list_input, number_per_page=settings.NUMBER_OF_ITEMS_PER_PAGE):
    list_of_items = []
    paginator = Paginator(list_input, number_per_page)
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


def get_conversions_for_accounts(bank_accounts, mainCurrency="GBP"):
    conversions: dict[str, float] = {}
    conversions.update({str(mainCurrency): 1.0})
    for bank_account in bank_accounts:
        currency = bank_account.currency
        conversions.update(
            {str(currency): convert_currency(1, currency, mainCurrency)})
    if (len(conversions.keys()) == 1 and not ("GBP" in conversions)):
        conversions.update({"GBP": convert_currency(1, "GBP", mainCurrency)})

    return conversions


def get_projection_timescale_options():
    return {6: "6 Months", 12: "1 Year", 24: "2 Years", 60: "5 Years"}


def get_projections_balances(accounts, max_timescale_in_months: int = max(
        get_projection_timescale_options().keys())):
    timescales = get_projection_timescale_options()
    accountDictionary = {}
    for account in accounts:
        interest_rate = float(account.interest_rate / 100)
        accountData = {
            "name": account.name,
            "currency": account.currency,
            "interest_rate": float(
                account.interest_rate)}
        balances = []
        currentBalance = float(account.balance)
        i = 1
        while i <= max_timescale_in_months:
            tempBalanceTotal = currentBalance * \
                ((1 + (interest_rate / 365))**get_number_of_days_in_prev_month(i))
            if tempBalanceTotal >= 0:
                currentBalance = tempBalanceTotal
            balances.append((currentBalance))
            i += 1
        accountData.update({"balances": balances})
        accountDictionary.update({account.id: accountData})

    return accountDictionary


def get_short_month_names_for_timescale(
        max_timescale_in_months: int = max(get_projection_timescale_options().keys())):
    currentDate = datetime.today()
    i = 1
    dates = []
    while i <= max_timescale_in_months:
        nextDate = currentDate + relativedelta(months=i)
        dates.append(str(nextDate.strftime("%b").capitalize() +
                     " " + nextDate.strftime("%y").capitalize()))
        i += 1

    return dates


def get_number_of_days_in_prev_month(offset_inMonths: int = 0):
    date = datetime.today() + relativedelta(months=offset_inMonths)
    no_of_days_in_prev_month = (
        date.replace(
            day=1) -
        timedelta(
            days=1)).day

    return no_of_days_in_prev_month


def get_data_for_account_projection(user):
    accounts = fcmodels.BankAccount.objects.filter(
        user_id=user, interest_rate__gt=0)
    mainCurrency = "GBP"
    if (accounts):
        mainCurrency = accounts[0].currency
    conversions = get_conversions_for_accounts(accounts, mainCurrency)

    timescale_dict = get_projection_timescale_options()
    timescales_strings = get_short_month_names_for_timescale()

    accountsDictionary = get_projections_balances(accounts)

    return {
        'bank_accounts': {acc.id: acc.name for acc in accounts},
        'bank_account_infos': dumps(accountsDictionary),
        'timescale_dict': timescale_dict,
        'timescales_strings': timescales_strings,
        'conversion_to_main_currency_JSON': dumps(conversions),
        'conversion_to_main_currency': conversions,
        'main_currency': mainCurrency
    }


def get_sorted_members_based_on_completed_targets(members):
    member_completed_list = []
    for member in members:
        score = member.get_leaderboard_score()
        member_completed_list = [*member_completed_list, (member, score)]
    member_completed_list = sorted(
        member_completed_list,
        key=lambda x: x[1],
        reverse=True
    )
    pos = 1
    p = inflect.engine()  # used to convert a number into a position
    member_completed_pos_list = []
    for member_completed in member_completed_list:
        member_completed_pos_list = [
            *member_completed_pos_list, (*member_completed, p.ordinal(pos))]
        pos += 1
    return member_completed_pos_list

def generate_random_end_date() -> datetime:
    start_date = datetime.now()
    end_date = start_date + timedelta(days=1000)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date

def get_warning_messages_for_targets(
        request, showNumbersForMultiples=True, targets=None):
    if not targets:
        targets = request.user.get_all_targets()
    completedTargets = request.user.get_completed_targets(targets)
    nearlyCompletedTargets = request.user.get_nearly_completed_targets(targets)

    sortedTargetsDict = {'completed': {}, 'nearlyExceeded': {}, 'exceeded': {}}
    for target in targets:
        dictionaryToAdd = None
        if target.target_type == 'income' and target in completedTargets:
            dictionaryToAdd = sortedTargetsDict['completed']
        elif target.target_type == 'expense' and target in nearlyCompletedTargets:
            dictionaryToAdd = sortedTargetsDict['nearlyExceeded']
        elif target.target_type == 'expense' and target in completedTargets:
            dictionaryToAdd = sortedTargetsDict['exceeded']

        if dictionaryToAdd is not None:
            key = target.getModelName(True)

            if key:
                if key in dictionaryToAdd.keys():
                    listToAppend = dictionaryToAdd[key].copy()
                else:
                    listToAppend = []
                listToAppend.append(target)
                dictionaryToAdd.update({key: listToAppend})

    for completionType, targetTypes in sortedTargetsDict.items():
        displayList = []
        if completionType:
            for targetType, targets in targetTypes.items():
                displayString = ''
                if len(targets) == 1:
                    displayString = (
                        str(targets[0]) + " (" + targets[0].getModelName() + ")").title()
                else:
                    displayString = targetType.title() + " ("
                    if showNumbersForMultiples:
                        displayString += str(len(targets))
                    else:
                        displayString += convert_list_to_string(list(targets))
                    displayString += ")"
                targetTypes[targetType] = displayString
            sortedTargetsDict[completionType] = targetTypes

    if sortedTargetsDict['completed']:
        messages.add_message(
            request,
            messages.SUCCESS,
            'Targets completed: ' +
            convert_list_to_string(
                list(sortedTargetsDict['completed'].values()))
        )

    if sortedTargetsDict['nearlyExceeded']:
        messages.add_message(
            request,
            messages.WARNING,
            'Targets nearly exceeded: ' +
            convert_list_to_string(
                list(sortedTargetsDict['nearlyExceeded'].values()))
        )

    if sortedTargetsDict['exceeded']:
        messages.add_message(
            request,
            messages.ERROR,
            'Targets exceeded: ' +
            convert_list_to_string(
                list(sortedTargetsDict['exceeded'].values()))
        )

    return request


def convert_list_to_string(list_in):
    output = ""
    list_length = len(list_in)
    if list_length >= 1:
        output += str(list_in[0])
    if list_length >= 2:
        for element in list_in[1:list_length - 1]:
            output += ", " + str(element)
        if list_length > 2:
            output += ","
        output += " and " + str(list_in[list_length - 1])
    return output

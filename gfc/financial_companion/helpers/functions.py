from json import dumps
from currency_symbols import CurrencySymbols
from currency_converter import CurrencyConverter
from .enums import CurrencyType, Timespan
from .maps import timespan_map
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.contrib import messages
import financial_companion.models as fcmodels
import inflect
import random
import string
from typing import Any
from django.http import HttpRequest
from django.db.models import QuerySet


def get_currency_symbol(currency_code: str) -> str:
    """Returns currency symbol for given currency code"""
    currency_code: str = currency_code.upper()

    if currency_code in CurrencyType:
        return CurrencySymbols.get_symbol(currency_code)
    else:
        return ""


def convert_currency(amount: float, current_currency_code: str,
                     target_currency_code: str) -> float:
    """Converts balance from one currency to another"""
    current_currency_code: str = current_currency_code.upper()
    target_currency_code: str = target_currency_code.upper()

    if current_currency_code == target_currency_code or current_currency_code not in CurrencyType or target_currency_code not in CurrencyType:
        return amount

    c: CurrencyConverter = CurrencyConverter(
        fallback_on_missing_rate=True,
        fallback_on_wrong_date=True)
    return c.convert(amount, current_currency_code, target_currency_code)


def random_filename(filename: str) -> str:
    """Generates a random filename"""
    file_extension: str = filename.split('.')[-1]

    # set a random filename
    filename_strings_to_add: list[str] = [
        random.choice(
            string.ascii_letters), str(
            datetime.now())]
    return '{}.{}'.format(''.join(filename_strings_to_add), file_extension)


def calculate_percentages(
        spent_per_category: dict[str, float], total: float) -> dict[str, float]:
    """calculate percentage of expenditure taken up by each category"""
    for key, value in spent_per_category.items():
        percentage: float = float((value / total) * 100)
        spent_per_category.update({key: percentage})
    return spent_per_category


def paginate(page: int, list_input: list[Any],
             number_per_page: int = settings.NUMBER_OF_ITEMS_PER_PAGE) -> Page:
    """paginate lists and tables to be displayed to user"""
    list_of_items: list[Any] = []
    paginator: Paginator = Paginator(list_input, number_per_page)
    try:
        list_of_items: Page = paginator.page(page)
    except PageNotAnInteger:
        list_of_items: Page = paginator.page(1)
    except EmptyPage:
        list_of_items: Page = paginator.page(paginator.num_pages)

    return list_of_items


def get_random_invite_code(length: int) -> str:
    """Generates a random invite code for User Groups"""
    letters: str = string.ascii_uppercase
    result_str: str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_conversions_for_accounts(
        bank_accounts, main_currency: str = "GBP") -> dict[str, float]:
    """get conversion rates for all currencies for all bank accounts"""
    conversions: dict[str, float] = {}
    conversions.update({str(main_currency): 1.0})
    for bank_account in bank_accounts:
        currency: str = bank_account.currency
        conversions.update(
            {str(currency): convert_currency(1, currency, main_currency)})
    if (len(conversions.keys()) == 1 and not ("GBP" in conversions)):
        conversions.update({"GBP": convert_currency(1, "GBP", main_currency)})

    return conversions


def get_projection_timescale_options() -> dict[int, str]:
    """return the time scale options for targets"""
    return {6: "6 Months", 12: "1 Year", 24: "2 Years", 60: "5 Years"}


def get_projections_balances(accounts, max_timescale_in_months: int = max(
        get_projection_timescale_options().keys())) -> dict[str, list[float]]:
    """returns the projected balances for inputed accounts for the given time scale in months"""
    account_dictionary: dict[int, dict[str, list[float]]] = {}
    for account in accounts:
        interest_rate: float = float(account.interest_rate / 100)
        account_data: dict[str, Any] = {
            "name": account.name,
            "currency": account.currency,
            "interest_rate": float(
                account.interest_rate)}
        balances: list[float] = []
        current_balance: float = float(account.balance)
        timescale_counter_in_months = 1
        while timescale_counter_in_months <= max_timescale_in_months:
            temp_balance_total: float = current_balance * \
                ((1 + (interest_rate / 365)) **
                 get_number_of_days_in_prev_month(timescale_counter_in_months))
            if temp_balance_total >= 0:
                current_balance = temp_balance_total
            balances.append(current_balance)
            timescale_counter_in_months += 1
        account_data.update({"balances": balances})
        account_dictionary.update({account.id: account_data})

    return account_dictionary


def get_short_month_names_for_timescale(
        max_timescale_in_months: int = max(get_projection_timescale_options().keys())) -> list[str]:
    """returns month names in the given time scale"""
    current_date: datetime = datetime.today()
    timescale_counter_in_months = 1
    dates: list[str] = []
    while timescale_counter_in_months <= max_timescale_in_months:
        next_date: datetime = current_date + \
            relativedelta(months=timescale_counter_in_months)
        dates.append(str(next_date.strftime("%b").capitalize() +
                     " " + next_date.strftime("%y").capitalize()))
        timescale_counter_in_months += 1

    return dates


def get_number_of_days_in_prev_month(offset_inMonths: int = 0) -> int:
    """calculate the number of days in the previous month"""
    last_month_start_date: datetime = datetime.today(
    ) + relativedelta(months=offset_inMonths)
    no_of_days_in_prev_month: int = (
        last_month_start_date.replace(
            day=1) -
        timedelta(
            days=1)).day

    return no_of_days_in_prev_month


def get_data_for_account_projection(user) -> dict[str, Any]:
    """return a dicationary contining all information for savings projections for all of the users accounts"""
    accounts: QuerySet[fcmodels.BankAccount] = fcmodels.BankAccount.objects.filter(
        user_id=user, interest_rate__gt=0)
    main_currency: CurrencyType = CurrencyType.GBP
    if (accounts):
        main_currency: str = accounts[0].currency
    conversions: dict[str, float] = get_conversions_for_accounts(
        accounts, main_currency)

    timescale_dict: dict[int, str] = get_projection_timescale_options()
    timescales_strings: list[str] = get_short_month_names_for_timescale()

    accounts_dictionary: dict[str, list[float]
                              ] = get_projections_balances(accounts)

    return {
        'bank_accounts': {acc.id: acc.name for acc in accounts},
        'bank_account_infos': dumps(accounts_dictionary),
        'timescale_dict': timescale_dict,
        'timescales_strings': timescales_strings,
        'conversion_to_main_currency_JSON': dumps(conversions),
        'conversion_to_main_currency': conversions,
        'main_currency': main_currency
    }


def get_sorted_members_based_on_completed_targets(
        members: Any) -> list[tuple[Any, str]]:
    """return a sorted list of users sorted based on complated targets"""
    member_completed_list: list[tuple[Any, float]] = []
    for member in members:
        score: float = member.get_leaderboard_score()
        member_completed_list = [
            *member_completed_list, (member, score)]
    member_completed_list = sorted(
        member_completed_list,
        key=lambda x: x[1],
        reverse=True
    )
    pos: int = 1
    # used to convert a number into a position
    inflector: inflect.engine = inflect.engine()
    member_completed_pos_list: list[tuple[Any, str]] = []
    for member_completed in member_completed_list:
        member_completed_pos_list = [
            *member_completed_pos_list, (*member_completed, inflector.ordinal(pos))]
        pos += 1
    return member_completed_pos_list


def get_warning_messages_for_targets(
        request: HttpRequest, show_numbers_for_multiples: bool = True, targets: list = None) -> HttpRequest:
    """Return a http request containing messages for nearly exceeded, exceeded and completed targets"""
    if not targets:
        targets: list[fcmodels.AbstractTarget] = request.user.get_all_targets()
    completed_targets: list[fcmodels.AbstractTarget] = request.user.get_completed_targets(
        targets)
    nearly_completed_targets: list[fcmodels.AbstractTarget] = request.user.get_nearly_completed_targets(
        targets)

    sorted_targets_dict: dict[str, dict[str, list[fcmodels.AbstractTarget]]] = {
        'completed': {}, 'nearly_exceeded': {}, 'exceeded': {}}
    for target in targets:
        dictionary_to_add: dict[str, list[fcmodels.AbstractTarget]] = None
        if target.target_type == 'income' and target in completed_targets:
            dictionary_to_add = sorted_targets_dict['completed']
        elif target.target_type == 'expense' and target in nearly_completed_targets:
            dictionary_to_add = sorted_targets_dict['nearly_exceeded']
        elif target.target_type == 'expense' and target in completed_targets:
            dictionary_to_add = sorted_targets_dict['exceeded']

        if dictionary_to_add is not None:
            key: str = target.get_model_name(True)

            if key:
                if key in dictionary_to_add.keys():
                    list_to_append: list[fcmodels.AbstractTarget] = dictionary_to_add[key].copy(
                    )
                else:
                    list_to_append: list[fcmodels.AbstractTarget] = []
                list_to_append.append(target)
                dictionary_to_add.update({key: list_to_append})

    for completion_type, target_types in sorted_targets_dict.items():
        if completion_type:
            for target_type, targets in target_types.items():
                display_string: str = ''
                if len(targets) == 1:
                    display_string = (
                        str(targets[0]) + " (" + targets[0].get_model_name() + ")").title()
                else:
                    display_string = target_type.title() + " ("
                    if show_numbers_for_multiples:
                        display_string += str(len(targets))
                    else:
                        display_string += convert_list_to_string(list(targets))
                    display_string += ")"
                target_types[target_type] = display_string
            sorted_targets_dict[completion_type] = target_types

    if sorted_targets_dict['completed']:
        messages.add_message(
            request,
            messages.SUCCESS,
            'Targets completed: ' +
            convert_list_to_string(
                list(sorted_targets_dict['completed'].values()))
        )

    if sorted_targets_dict['nearly_exceeded']:
        messages.add_message(
            request,
            messages.WARNING,
            'Targets nearly exceeded: ' +
            convert_list_to_string(
                list(sorted_targets_dict['nearly_exceeded'].values()))
        )

    if sorted_targets_dict['exceeded']:
        messages.add_message(
            request,
            messages.ERROR,
            'Targets exceeded: ' +
            convert_list_to_string(
                list(sorted_targets_dict['exceeded'].values()))
        )

    return request


def convert_list_to_string(list_in: list[Any]) -> str:
    """Returns an input list as a string"""
    output: str = ""
    list_length: int = len(list_in)
    if list_length >= 1:
        output += str(list_in[0])
    if list_length >= 2:
        for element in list_in[1:list_length - 1]:
            output += ", " + str(element)
        if list_length > 2:
            output += ","
        output += " and " + str(list_in[list_length - 1])
    return output


def check_date_on_interval(
        interval: Timespan, base_date: date, current_date: date = date.today()) -> bool:
    """Checks if current date is on an interval date with the base date"""
    if base_date > current_date:
        return False
    interval_in_days: int = timespan_map[interval]
    return ((current_date - base_date).days % interval_in_days) == 0


def check_within_date_range(
        start_date: date, end_date: date, current_date: date = date.today()) -> bool:
    """Checks if current date is within the time period"""
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    check_current_after_start: bool = current_date >= start_date
    check_current_before_end: bool = current_date <= end_date
    return check_current_before_end and check_current_after_start
